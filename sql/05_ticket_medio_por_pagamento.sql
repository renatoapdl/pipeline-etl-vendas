-- Pergunta: Qual o ticket médio e o volume por meio de pagamento?
-- Fonte: gold.fato_pagamentos

SELECT
  payment_type AS meio_pagamento,
  COUNT(*) AS pagamentos,
  COUNT(DISTINCT order_id) AS pedidos,
  ROUND(SUM(payment_value), 2) AS valor_total,
  ROUND(AVG(payment_value), 2) AS ticket_medio_pagamento,
  ROUND(AVG(payment_installments), 2) AS parcelas_medias
FROM gold.fato_pagamentos
GROUP BY payment_type
ORDER BY valor_total DESC;
