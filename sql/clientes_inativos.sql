WITH ultimo_pedido AS(
	SELECT
		c.id_cliente,
		c.nome,
		MAX(p.data_pedido) AS data_ultimo_pedido
	FROM clientes c
	LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente
	GROUP BY c.id_cliente, c.nome
)
SELECT * from ultimo_pedido
WHERE data_ultimo_pedido < CURRENT_DATE - INTERVAL '6 months'or data_ultimo_pedido is null
ORDER BY data_ultimo_pedido ASC;