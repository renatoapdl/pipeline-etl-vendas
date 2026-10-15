-- Pergunta de negócio: Qual categoria gera mais receita, agora consultando o modelo estrela?
-- Resultado esperado: o mesmo da query 01, via JOIN entre o fato e a dimensão (reconcilia Gold e Silver).

SELECT
  p.categoria,
  ROUND(SUM(f.valor_total), 2) AS receita_bruta,
  SUM(f.quantidade) AS qtd_total
FROM gold.fato_vendas f
JOIN gold.dim_produto p ON f.cod_produto = p.cod_produto
GROUP BY p.categoria
ORDER BY receita_bruta DESC;
