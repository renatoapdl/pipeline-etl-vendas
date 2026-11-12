-- Pergunta: Como se distribuem as parcelas (quantidade e valor)?
-- Fonte: gold.fato_pagamentos

WITH base AS (
  SELECT
    payment_installments AS parcelas,
    COUNT(*) AS pagamentos,
    SUM(payment_value) AS valor
  FROM gold.fato_pagamentos
  GROUP BY payment_installments
)
SELECT
  parcelas,
  pagamentos,
  ROUND(100.0 * pagamentos / SUM(pagamentos) OVER (), 2) AS pct_pagamentos,
  ROUND(valor, 2) AS valor_total,
  ROUND(100.0 * valor / SUM(valor) OVER (), 2) AS pct_valor
FROM base
ORDER BY parcelas;
