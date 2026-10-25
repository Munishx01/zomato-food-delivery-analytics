# Data Model (star schema)

| Table | Type | Grain | Key |
|---|---|---|---|
| `orders_clean` | Fact | one row per order | `order_id` |
| `restaurants_clean` | Dimension | one row per restaurant | `restaurant_id` |
| `DimDate` | Dimension (DAX) | one row per calendar day | `Date` |

## Relationships
| From (many) | To (one) | Cardinality | Filter direction |
|---|---|---|---|
| `orders_clean[restaurant_id]` | `restaurants_clean[restaurant_id]` | Many-to-one | Single (dimension -> fact) |
| `orders_clean[order_date]` | `DimDate[Date]` | Many-to-one | Single |

Why: the dataset has one item-quantity/amount value per order (no separate line-item table), so the fact table is
order-level and `SUM()` does not double-count. Slicers for Restaurant Name / Type / City / Area live on the restaurant
dimension; Payment Mode is a column on the fact table (low cardinality, no separate dimension needed).
Mark `DimDate` as a date table. Sort `DimDate[MonthName]` by `DimDate[MonthNumber]`.

> Status: the model definition is documented but **has not been built or validated in Power BI Desktop** (not available in the authoring environment).
