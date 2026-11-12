-- Pergunta: Como a receita evolui mês a mês?
-- Fonte: gold.fato_itens + gold.dim_data

SELECT
  d.ano,
  d.mes,
  d.ano_mes,
  COUNT(DISTINCT f.order_id) AS pedidos,
  ROUND(SUM(f.price), 2) AS receita_produtos,
  ROUND(SUM(f.freight_value), 2) AS frete,
  ROUND(SUM(f.price + f.freight_value), 2) AS receita_total
FROM gold.fato_itens f
JOIN gold.dim_data d ON f.cod_data = d.cod_data
GROUP BY d.ano, d.mes, d.ano_mes
ORDER BY d.ano, d.mes;
