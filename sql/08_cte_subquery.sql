-- Pergunta de negócio: Quais categorias têm receita bruta total maior que a média geral de receita bruta por categoria?
-- Resultado esperado: Lista de categorias com receita_bruta, ordenadas decrescentemente.

WITH receita_por_categoria AS (
    SELECT 
        categoria,
        ROUND(SUM(valor_unitario * quantidade), 2) AS receita_bruta
    FROM silver.vendas 
    WHERE categoria IS NOT NULL
    GROUP BY categoria
    HAVING SUM(valor_unitario * quantidade) > 0
),
media_geral AS (
    SELECT 
        ROUND(AVG(receita_bruta), 2) AS media_bruta_categoria
    FROM receita_por_categoria
)
SELECT 
    rpc.categoria,
    rpc.receita_bruta
FROM receita_por_categoria rpc
CROSS JOIN media_geral mg
WHERE rpc.receita_bruta > mg.media_bruta_categoria
ORDER BY rpc.receita_bruta DESC;
