-- Pergunta de negócio: Quais clientes geram mais receita bruta?
-- Resultado esperado: Top de clientes com receita, quantidade total e média por item, ordenados por receita decrescente.

SELECT
  id_cliente,
  COUNT(DISTINCT produto) AS produtos_distintos,
  SUM(quantidade) AS qtd_total,
  ROUND(SUM(valor_unitario * quantidade), 2) AS receita_bruta,
  ROUND(SUM(valor_unitario * quantidade) / NULLIF(SUM(quantidade), 0), 2) AS ticket_medio_item
FROM silver.vendas
WHERE id_cliente IS NOT NULL
GROUP BY id_cliente
HAVING SUM(valor_unitario * quantidade) > 100
ORDER BY receita_bruta DESC
LIMIT 20;

-- Pergunta adicional (não coberta no SQLBolt): Quais clientes ultrapassam R$ 1.000 em receita bruta, com pelo menos 5 itens vendidos?
