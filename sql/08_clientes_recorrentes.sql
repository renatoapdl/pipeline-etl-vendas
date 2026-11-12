-- Pergunta: Qual a taxa de clientes recorrentes (2+ pedidos)?
-- Fonte: gold.fato_itens + gold.dim_cliente

WITH por_cliente AS (
  SELECT
    c.customer_unique_id,
    COUNT(DISTINCT f.order_id) AS pedidos
  FROM gold.fato_itens f
  JOIN gold.dim_cliente c ON f.cod_cliente = c.cod_cliente
  GROUP BY c.customer_unique_id
)
SELECT
  COUNT(*) AS clientes,
  SUM(CASE WHEN pedidos >= 2 THEN 1 ELSE 0 END) AS recorrentes,
  ROUND(100.0 * SUM(CASE WHEN pedidos >= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_recorrentes
FROM por_cliente;
