-- Recalculate positions for all placements based on new book width (3.5cm instead of 4cm)
-- This proportionally adjusts positions from old zone calculation to new zone calculation

-- For each shelf, recalculate positions based on:
-- Old zones: floor(widthCm / 4)
-- New zones: floor(widthCm / 3.5)
-- New position: floor((old_position / old_zones) * new_zones)

UPDATE "BookPlacement"
SET position = CAST(
  FLOOR(
    (position::FLOAT / GREATEST(1, FLOOR(s."widthCm" / 4.0))) * 
    GREATEST(1, FLOOR(s."widthCm" / 3.5))
  ) AS INTEGER
)
FROM "Shelf" s
WHERE "BookPlacement"."shelfId" = s.id;
