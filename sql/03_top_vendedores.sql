-- Pergunta: Quais vendedores geram mais receita e qual o preço médio por item? => TOP 10
-- Fonte: gold.fato_itens + gold.dim_vendedor

SELECT
  v.seller_id,
  v.estado,
  COUNT(DISTINCT f.order_id) AS pedidos,
  COUNT(*) AS itens,
  ROUND(SUM(f.price), 2) AS receita_produtos,
  ROUND(SUM(f.price + f.freight_value), 2) AS receita_total,
  ROUND(AVG(f.price), 2) AS preco_medio_item
FROM gold.fato_itens f
JOIN gold.dim_vendedor v ON f.cod_vendedor = v.cod_vendedor
GROUP BY v.seller_id, v.estado
ORDER BY receita_total DESC
LIMIT 10;
