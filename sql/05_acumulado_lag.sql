-- Pergunta de negócio: Como evolui a receita acumulada de um cliente ao longo do tempo?
-- Resultado esperado: Para cada cliente, exibir vendas ordenadas por data com receita acumulada e variação em relação ao registro anterior.

SELECT
  id_cliente,
  data_venda,
  produto,
  valor_unitario * quantidade AS receita_item,
  ROUND(SUM(valor_unitario * quantidade) OVER (
    PARTITION BY id_cliente
    ORDER BY data_venda, id_venda
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ), 2) AS receita_acumulada,
  LAG(valor_unitario * quantidade, 1, 0) OVER (
    PARTITION BY id_cliente
    ORDER BY data_venda, id_venda
  ) AS receita_item_anterior
FROM vendas_bruto
WHERE id_cliente IS NOT NULL
  AND data_venda IS NOT NULL
ORDER BY id_cliente, data_venda, id_venda;

-- Pergunta adicional (não coberta no SQLBolt): Em que situação usar LAG() ajuda a identificar picos de compra por cliente?
