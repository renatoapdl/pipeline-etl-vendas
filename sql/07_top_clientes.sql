-- Pergunta: Quais clientes (customer_unique_id) geram mais receita? => TOP 10
-- Fonte: gold.fato_itens + gold.dim_cliente

SELECT
  c.customer_unique_id,
  c.estado,
  COUNT(DISTINCT f.order_id) AS pedidos,
  COUNT(*) AS itens,
  ROUND(SUM(f.price + f.freight_value), 2) AS receita_total
FROM gold.fato_itens f
JOIN gold.dim_cliente c ON f.cod_cliente = c.cod_cliente
GROUP BY c.customer_unique_id, c.estado
ORDER BY receita_total DESC
LIMIT 10;
