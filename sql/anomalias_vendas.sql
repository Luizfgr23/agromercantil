WITH valor_itens_pedido AS(
	SELECT
		id_pedido,
		SUM(quantidade * preco_unitario ) as valor_calculado
	FROM itens_pedido
	group by id_pedido
)
SELECT 
	p.id_pedido,
	p.valor_total as valor_registrado,
	v.valor_calculado
FROM pedidos p
JOIN valor_itens_pedido v on p.id_pedido = v.id_pedido
Where Round(p.valor_total, 2) != Round(v.valor_calculado,2);