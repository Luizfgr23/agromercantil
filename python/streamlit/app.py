import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import run_query

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.sidebar.title("Menu")
page = st.sidebar.radio("Escolha a página:", ["Visão Geral", "Outras Análises"])

st.markdown("""
    <style>
    body {
        background-color: #CFDDC5;
        color: white;
    }
    .stApp {
        background-color: #CFDDC5;
        color: black;
    }
    .css-1aumxhk {
        background-color: #CFDDC5;
    }
    .css-1d391kg, .css-1cpxqw2 {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Filtros
st.sidebar.markdown("### Filtros")

clientes_df = run_query("SELECT id_cliente, nome FROM clientes ORDER BY nome;")
clientes_opcoes = clientes_df['nome'].tolist()
cliente_selecionado = st.sidebar.multiselect("Selecionar Cliente(s):", clientes_opcoes, default=clientes_opcoes)

data_min = run_query("SELECT MIN(data_pedido) AS data_min FROM pedidos;")['data_min'][0]
data_max = run_query("SELECT MAX(data_pedido) AS data_max FROM pedidos;")['data_max'][0]
data_inicio = st.sidebar.date_input("Data inicial:", pd.to_datetime(data_min))
data_fim = st.sidebar.date_input("Data final:", pd.to_datetime(data_max))

cliente_nomes = "','".join(cliente_selecionado)

# Primeira página
if page == "Visão Geral":
    st.title("Visão Geral das Vendas")

    df_total = run_query(f"""
        SELECT SUM(valor_total) AS total_vendas
        FROM pedidos p
        JOIN clientes c ON p.id_cliente = c.id_cliente
        WHERE p.data_pedido BETWEEN '{data_inicio}' AND '{data_fim}'
          AND c.nome IN ('{cliente_nomes}')
    """)

    df_ticket = run_query(f"""
        SELECT AVG(valor_total) AS ticket_medio
        FROM pedidos p
        JOIN clientes c ON p.id_cliente = c.id_cliente
        WHERE p.data_pedido BETWEEN '{data_inicio}' AND '{data_fim}'
          AND c.nome IN ('{cliente_nomes}')
    """)

    df_fat_mes = run_query(f"""
        SELECT AVG(v.total_vendas) AS faturamento_medio
        FROM (
            SELECT DATE_TRUNC('month', data_pedido) AS mes, SUM(valor_total) AS total_vendas
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.data_pedido BETWEEN '{data_inicio}' AND '{data_fim}'
              AND c.nome IN ('{cliente_nomes}')
            GROUP BY mes
        ) v;
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Vendas", f"R$ {df_total['total_vendas'][0]:,.2f}")
    col2.metric("Ticket Médio", f"R$ {df_ticket['ticket_medio'][0]:,.2f}")
    col3.metric("Faturamento Médio Mensal", f"R$ {df_fat_mes['faturamento_medio'][0]:,.2f}")

    st.markdown("---")

    # Gráfico de Vendas mensal
    st.subheader("Evolução Mensal das Vendas")
    historico_query = f"""
        WITH vendas_mensais AS (
            SELECT TO_CHAR(p.data_pedido, 'YYYY-MM') AS mes_ano, SUM(p.valor_total) AS total_vendas
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.data_pedido BETWEEN '{data_inicio}' AND '{data_fim}'
              AND c.nome IN ('{cliente_nomes}')
            GROUP BY TO_CHAR(p.data_pedido, 'YYYY-MM')
        ),
        vendas_com_lag AS (
            SELECT mes_ano, total_vendas,
                   LAG(total_vendas) OVER (ORDER BY mes_ano) AS vendas_mes_anterior
            FROM vendas_mensais
        )
        SELECT mes_ano, total_vendas,
               ROUND(
                   CASE
                       WHEN vendas_mes_anterior IS NULL THEN NULL
                       WHEN vendas_mes_anterior = 0 THEN NULL
                       ELSE ((total_vendas - vendas_mes_anterior) / vendas_mes_anterior) * 100
                   END, 2
               ) AS crescimento_percentual
        FROM vendas_com_lag
        ORDER BY mes_ano;
    """
    df_vendas = run_query(historico_query)
    fig = px.bar(df_vendas, x="mes_ano", y="total_vendas", title="Vendas por Mês")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_vendas)

    # Top 5 produtos mais vendidos
    st.subheader("Top 5 Produtos Mais Vendidos")
    top5_query = f"""
        WITH vendas_ultimo_ano AS (
            SELECT ip.id_produto, pr.nome,
                   SUM(ip.quantidade * ip.preco_unitario) AS total_vendas
            FROM itens_pedido ip
            JOIN pedidos pd ON pd.id_pedido = ip.id_pedido
            JOIN produtos pr ON pr.id_produto = ip.id_produto
            JOIN clientes c ON pd.id_cliente = c.id_cliente
            WHERE pd.data_pedido BETWEEN '{data_inicio}' AND '{data_fim}'
              AND c.nome IN ('{cliente_nomes}')
            GROUP BY ip.id_produto, pr.nome
        )
        SELECT * FROM vendas_ultimo_ano
        ORDER BY total_vendas DESC
        LIMIT 5;
    """
    df_top5 = run_query(top5_query)
    st.dataframe(df_top5)

# Segunda página
elif page == "Outras Análises":
    st.title("Outras Análises")

    # RFM
    st.subheader("Análise RFM")
    rfm_query = f"""
        WITH pedidos_cliente AS (
            SELECT p.* FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.data_pedido BETWEEN '{data_inicio}' AND '{data_fim}'
              AND c.nome IN ('{cliente_nomes}')
        ),
        ultimo_pedido AS (
            SELECT id_cliente, data_pedido, valor_total,
                   COUNT(id_pedido) OVER (PARTITION BY id_cliente) AS total_pedidos,
                   SUM(valor_total) OVER (PARTITION BY id_cliente) AS valor_total_pedidos,
                   ROW_NUMBER() OVER (PARTITION BY id_cliente ORDER BY data_pedido DESC) AS rn
            FROM pedidos_cliente
        ),
        resumo_rfm AS (
            SELECT id_cliente,
                   CURRENT_DATE - data_pedido AS dias_desde_ultimo_pedido,
                   total_pedidos,
                   CASE WHEN total_pedidos > 0 THEN valor_total_pedidos / total_pedidos ELSE 0 END AS ticket_medio
            FROM ultimo_pedido
            WHERE rn = 1
        )
        SELECT * FROM resumo_rfm;
    """
    df_rfm = run_query(rfm_query)
    st.dataframe(df_rfm)

    # Inativos
    st.subheader("Clientes Inativos (6+ meses)")
    inativos_query = f"""
        WITH ultimo_pedido AS (
            SELECT c.id_cliente, c.nome, MAX(p.data_pedido) AS data_ultimo_pedido
            FROM clientes c
            LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente
            GROUP BY c.id_cliente, c.nome
        )
        SELECT * FROM ultimo_pedido
        WHERE data_ultimo_pedido < CURRENT_DATE - INTERVAL '6 months'
           OR data_ultimo_pedido IS NULL
           AND nome IN ('{cliente_nomes}')
        ORDER BY data_ultimo_pedido;
    """
    df_inativos = run_query(inativos_query)
    st.dataframe(df_inativos)

    # Anomalias
    st.subheader("Anomalias de Vendas (valores divergentes)")
    anomalias_query = """
        WITH valor_itens_pedido AS (
            SELECT id_pedido,
                   SUM(quantidade * preco_unitario) AS valor_calculado
            FROM itens_pedido
            GROUP BY id_pedido
        )
        SELECT p.id_pedido, p.valor_total AS valor_registrado, v.valor_calculado
        FROM pedidos p
        JOIN valor_itens_pedido v ON p.id_pedido = v.id_pedido
        WHERE ROUND(p.valor_total, 2) != ROUND(v.valor_calculado, 2);
    """
    df_anomalias = run_query(anomalias_query)
    st.dataframe(df_anomalias)