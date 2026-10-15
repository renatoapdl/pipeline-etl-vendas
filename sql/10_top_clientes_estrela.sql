-- Pergunta de negócio: Quais clientes geram mais receita, consultando o modelo estrela?
-- Resultado esperado: top de clientes por receita, via JOIN entre o fato e a dimensão (mesmo resultado da query 03).

SELECT
  c.id_cliente,
  COUNT(*) AS pedidos,
  ROUND(SUM(f.valor_total), 2) AS receita_bruta
FROM gold.fato_vendas f
JOIN gold.dim_cliente c ON f.cod_cliente = c.cod_cliente
GROUP BY c.id_cliente
ORDER BY receita_bruta DESC
LIMIT 10;
