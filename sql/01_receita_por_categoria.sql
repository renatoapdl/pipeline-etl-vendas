-- Pergunta de negócio: Qual categoria gera mais receita bruta com base nos dados de vendas?
-- Resultado esperado: Lista de categorias ordenada por receita bruta decrescente.

SELECT
  categoria,
  ROUND(SUM(valor_unitario * quantidade), 2) AS receita_bruta,
  COUNT(DISTINCT id_cliente) AS clientes_distintos,
  SUM(quantidade) AS qtd_total
FROM silver.vendas
WHERE categoria IS NOT NULL
GROUP BY categoria
HAVING SUM(valor_unitario * quantidade) > 0
ORDER BY receita_bruta DESC;
