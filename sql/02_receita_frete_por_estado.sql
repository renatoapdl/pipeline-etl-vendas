-- Pergunta: Como a receita, o frete e o ticket médio se distribuem por estado do cliente?
-- Fonte: gold.fato_itens + gold.dim_cliente

SELECT
  c.estado,
  COUNT(DISTINCT f.order_id) AS pedidos,
  ROUND(SUM(f.price), 2) AS receita_produtos,
  ROUND(SUM(f.freight_value), 2) AS frete,
  ROUND(SUM(f.price + f.freight_value), 2) AS receita_total,
  ROUND(SUM(f.price + f.freight_value) / COUNT(DISTINCT f.order_id), 2) AS ticket_medio_pedido
FROM gold.fato_itens f
JOIN gold.dim_cliente c ON f.cod_cliente = c.cod_cliente
GROUP BY c.estado
ORDER BY receita_total DESC;
