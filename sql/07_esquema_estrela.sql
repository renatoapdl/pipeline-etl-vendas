-- Pergunta de negócio: Quais são as dimensões mínimas para um esquema estrela com base nas vendas?
-- Resultado esperado: Definição lógica de dim_cliente, dim_produto e fato_vendas (modelo estrela com 2 dimensões + 1 fato).

-- DIMENSÃO CLIENTE (2 dimensões)
SELECT DISTINCT
  id_cliente
FROM vendas_bruto
WHERE id_cliente IS NOT NULL
ORDER BY id_cliente;

-- DIMENSÃO PRODUTO (2 dimensões)
SELECT DISTINCT
  produto,
  categoria
FROM vendas_bruto
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
FROM vendas_bruto
ORDER BY id_venda;

-- Pergunta adicional (não coberta no SQLBolt): Por que este modelo (2 dims + 1 fato) atende ao conceito de esquema estrela para responder agregações por cliente/categoria/produto?
