-- Pergunta: O Gold preserva as somas do Silver? (diferença deve ser 0)
-- Fonte: gold.fato_itens + silver.items, gold.fato_pagamentos + silver.payments

SELECT
  'fato_itens.price' AS metrica,
  ROUND((SELECT SUM(price) FROM gold.fato_itens), 2) AS gold,
  ROUND((SELECT SUM(price) FROM silver.items), 2) AS silver,
  ROUND(
    (SELECT SUM(price) FROM gold.fato_itens) - (SELECT SUM(price) FROM silver.items), 2
  ) AS diferenca
UNION ALL
SELECT
  'fato_itens.freight_value',
  ROUND((SELECT SUM(freight_value) FROM gold.fato_itens), 2),
  ROUND((SELECT SUM(freight_value) FROM silver.items), 2),
  ROUND(
    (SELECT SUM(freight_value) FROM gold.fato_itens)
      - (SELECT SUM(freight_value) FROM silver.items), 2
  )
UNION ALL
SELECT
  'fato_pagamentos.payment_value',
  ROUND((SELECT SUM(payment_value) FROM gold.fato_pagamentos), 2),
  ROUND((SELECT SUM(payment_value) FROM silver.payments), 2),
  ROUND(
    (SELECT SUM(payment_value) FROM gold.fato_pagamentos)
      - (SELECT SUM(payment_value) FROM silver.payments), 2
  );
