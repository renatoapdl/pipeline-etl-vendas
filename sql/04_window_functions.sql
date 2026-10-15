-- Pergunta de negócio: Como ranquear vendas por receita dentro de cada categoria?
-- Resultado esperado: Para cada categoria, exibir produtos com ranking por receita bruta decrescente.

SELECT
  categoria,
  produto,
  ROUND(SUM(valor_unitario * quantidade), 2) AS receita_bruta,
  SUM(quantidade) AS qtd_total,
  ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY SUM(valor_unitario * quantidade) DESC) AS rn,
  RANK() OVER (PARTITION BY categoria ORDER BY SUM(valor_unitario * quantidade) DESC) AS rk
FROM silver.vendas
WHERE categoria IS NOT NULL
GROUP BY categoria, produto
HAVING SUM(valor_unitario * quantidade) > 0
ORDER BY categoria, rk, produto;

-- Pergunta adicional (não coberta no SQLBolt): Qual a diferença prática entre ROW_NUMBER e RANK ao ranquear produtos por receita dentro da mesma categoria?
