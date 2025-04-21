WITH vendas_ultimo_ano AS(
	SELECT 
		ip.id_produto,
		p.nome,
		sum(ip.quantidade * ip.preco_unitario) as total_vendas
	FROM itens_pedido ip
	JOIN pedidos pd ON pd.id_pedido = ip.id_pedido
	JOIN produtos p ON p.id_produto = ip.id_produto
	WHERE EXTRACT(YEAR FROM pd.data_pedido) = 2024
	GROUP BY ip.id_produto,p.nome
)

SELECT id_produto,nome,total_vendas FROM vendas_ultimo_ano ORDER BY total_vendas DESC LIMIT 5;