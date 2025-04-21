WITH vendas_mensais AS (
 	SELECT 
    	TO_CHAR(data_pedido, 'YYYY-MM') AS mes_ano,
    	SUM(valor_total) AS total_vendas
  	FROM pedidos
  	GROUP BY TO_CHAR(data_pedido, 'YYYY-MM')
),

vendas_com_lag AS (
	SELECT 
    	mes_ano,
    	total_vendas,
    	LAG(total_vendas) OVER (ORDER BY mes_ano) AS vendas_mes_anterior
  	FROM vendas_mensais
)

SELECT 
 	mes_ano,
  	total_vendas,
  	ROUND(
    CASE 
     	WHEN vendas_mes_anterior IS NULL THEN NULL
      	WHEN vendas_mes_anterior = 0 THEN NULL
      	ELSE ((total_vendas - vendas_mes_anterior) / vendas_mes_anterior) * 100
    	END, 2
  ) AS crescimento_percentual
FROM vendas_com_lag
ORDER BY mes_ano;