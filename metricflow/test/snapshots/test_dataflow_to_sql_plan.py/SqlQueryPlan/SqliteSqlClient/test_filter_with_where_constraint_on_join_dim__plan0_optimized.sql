-- Constrain Output with WHERE
-- Pass Only Elements:
--   ['bookings', 'is_instant']
-- Aggregate Measures
-- Compute Metrics via Expressions
SELECT
  SUM(bookings) AS bookings
  , is_instant
FROM (
  -- Join Standard Outputs
  -- Pass Only Elements:
  --   ['bookings', 'is_instant', 'listing__country_latest']
  SELECT
    subq_13.bookings AS bookings
    , subq_13.is_instant AS is_instant
    , listings_latest_src_10003.country AS listing__country_latest
  FROM (
    -- Read Elements From Data Source 'bookings_source'
    -- Plot by Time Dimension 'ds'
    -- Pass Only Elements:
    --   ['bookings', 'is_instant', 'listing']
    SELECT
      1 AS bookings
      , is_instant
      , listing_id AS listing
    FROM (
      -- User Defined SQL Query
      SELECT * FROM ***************************.fct_bookings
    ) bookings_source_src_10000
  ) subq_13
  LEFT OUTER JOIN
    ***************************.dim_listings_latest listings_latest_src_10003
  ON
    subq_13.listing = listings_latest_src_10003.listing_id
) subq_18
WHERE listing__country_latest = 'us'
GROUP BY
  is_instant
