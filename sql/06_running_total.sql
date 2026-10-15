-- Pergunta de negócio: Qual a receita total acumulada por categoria ao longo do tempo (running total)?
-- Resultado esperado: Receita acumulada por categoria ordenada por data, com janela de soma móvel.

SELECT
  categoria,
  data_venda,
  ROUND(SUM(SUM(valor_unitario * quantidade)) OVER (
    PARTITION BY categoria
    ORDER BY data_venda
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ), 2) AS receita_acumulada_categoria
FROM silver.vendas
WHERE categoria IS NOT NULL
  AND data_venda IS NOT NULL
GROUP BY categoria, data_venda
ORDER BY categoria, data_venda;
