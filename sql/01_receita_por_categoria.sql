-- Pergunta: Quais categorias geram mais receita (produtos + frete)? => TOP 10
-- Fonte: gold.fato_itens + gold.dim_produto

SELECT
  p.categoria_pt AS categoria,
  COUNT(DISTINCT f.order_id) AS pedidos,
  COUNT(*) AS itens,
  ROUND(SUM(f.price), 2) AS receita_produtos,
  ROUND(SUM(f.freight_value), 2) AS frete,
  ROUND(SUM(f.price + f.freight_value), 2) AS receita_total
FROM gold.fato_itens f
JOIN gold.dim_produto p ON f.cod_produto = p.cod_produto
WHERE p.categoria_pt IS NOT NULL
  AND p.categoria_pt <> ''
GROUP BY p.categoria_pt
ORDER BY receita_total DESC
LIMIT 10;