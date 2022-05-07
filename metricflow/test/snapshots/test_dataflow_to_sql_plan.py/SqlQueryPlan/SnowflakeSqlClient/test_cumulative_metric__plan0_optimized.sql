-- Read Elements From Data Source 'revenue'
-- Plot by Time Dimension 'ds'
-- Pass Only Elements:
--   ['txn_revenue', 'ds__month']
-- Aggregate Measures
-- Compute Metrics via Expressions
SELECT
  SUM(revenue) AS trailing_2_months_revenue
  , DATE_TRUNC('month', created_at) AS ds__month
FROM (
  -- User Defined SQL Query
  SELECT * FROM ***************************.fct_revenue
) revenue_src_10005
GROUP BY
  DATE_TRUNC('month', created_at)
