-- Pergunta: Qual a receita acumulada por categoria ao longo dos meses (running total)?
-- Fonte: gold.fato_itens + gold.dim_produto + gold.dim_data

WITH mensal AS (
  SELECT
    p.categoria_pt AS categoria,
    d.ano_mes,
    SUM(f.price + f.freight_value) AS receita_mes
  FROM gold.fato_itens f
  JOIN gold.dim_produto p ON f.cod_produto = p.cod_produto
  JOIN gold.dim_data d ON f.cod_data = d.cod_data
  WHERE p.categoria_pt IS NOT NULL
    AND p.categoria_pt <> ''
  GROUP BY p.categoria_pt, d.ano_mes
)
SELECT
  categoria,
  ano_mes,
  ROUND(receita_mes, 2) AS receita_mes,
  ROUND(SUM(receita_mes) OVER (
    PARTITION BY categoria
    ORDER BY ano_mes
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ), 2) AS receita_acumulada
FROM mensal
ORDER BY categoria, ano_mes;
