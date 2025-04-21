WITH pedidos_cliente AS (
  SELECT * FROM pedidos
),

ultimo_pedido AS (
  SELECT
    id_cliente,
    data_pedido,
    valor_total,
    LAG(data_pedido) OVER (PARTITION BY id_cliente ORDER BY data_pedido DESC) AS data_pedido_anterior,
    COUNT(id_pedido) OVER (PARTITION BY id_cliente) AS total_pedidos,
    SUM(valor_total) OVER (PARTITION BY id_cliente) AS valor_total_pedidos,
    ROW_NUMBER() OVER (PARTITION BY id_cliente ORDER BY data_pedido DESC) AS rn -- Pega o pedido mais recente
  FROM pedidos_cliente
),

resumo_rfm AS (
  SELECT 
    id_cliente,
    CURRENT_DATE - data_pedido AS dias_desde_ultimo_pedido,
    total_pedidos,
    CASE
      WHEN total_pedidos > 0 THEN valor_total_pedidos / total_pedidos
      ELSE 0
    END AS ticket_medio
  FROM ultimo_pedido
  WHERE rn = 1 -- apenas o último pedido de cada cliente
)

SELECT * FROM resumo_rfm;