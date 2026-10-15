-- Pergunta de negócio: Quais são as dimensões mínimas para um esquema estrela com base nas vendas?
-- Resultado esperado: Definição lógica de dim_cliente, dim_produto e fato_vendas (modelo estrela com 2 dimensões + 1 fato).

-- DIMENSÃO CLIENTE (2 dimensões)
SELECT DISTINCT
  id_cliente
FROM silver.vendas
WHERE id_cliente IS NOT NULL
ORDER BY id_cliente;

-- DIMENSÃO PRODUTO (2 dimensões)
SELECT DISTINCT
  produto,
  categoria
FROM silver.vendas
WHERE produto IS NOT NULL
ORDER BY categoria, produto;

-- FATO VENDAS (1 fato)
SELECT
  id_venda,
  id_cliente,
  produto,
  categoria,
  data_venda,
  canal AS canal_venda,
  quantidade,
  valor_unitario,
  ROUND(valor_unitario * quantidade, 2) AS valor_total
FROM silver.vendas
ORDER BY id_venda;
