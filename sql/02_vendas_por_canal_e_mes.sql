-- Pergunta de negócio: Qual canal de venda performa melhor por mês?
-- Resultado esperado: Total de vendas, quantidade e receita bruta agrupados por canal e mês, ordenados por mês e receita.

SELECT
  canal AS canal_venda,
  YEAR(data_venda) AS ano,
  MONTH(data_venda) AS mes,
  COUNT(DISTINCT CONCAT(id_cliente, data_venda, produto)) AS pedidos_estimados,
  SUM(quantidade) AS qtd_total,
  ROUND(SUM(valor_unitario * quantidade), 2) AS receita_bruta
FROM silver.vendas
WHERE data_venda IS NOT NULL
  AND canal IS NOT NULL
GROUP BY canal, YEAR(data_venda), MONTH(data_venda)
ORDER BY ano, mes, receita_bruta DESC;

-- Pergunta adicional (não coberta no SQLBolt): Em quais meses o canal 'web' superou 'loja' em receita bruta?
