# DAX measures (written against the model in data_model.md; not yet executed in Power BI Desktop)

```dax
Total Order Amount   = SUM ( orders_clean[order_amount] )
Total Items          = SUM ( orders_clean[item_quantity] )
Total Discount       = SUM ( orders_clean[discount] )
Total Delivery Fee   = SUM ( orders_clean[delivery_fee] )
Total Packaging Fee  = SUM ( orders_clean[packaging_fee] )
Total Tax            = SUM ( orders_clean[tax] )
Total Orders         = DISTINCTCOUNT ( orders_clean[order_id] )
Total Restaurants    = DISTINCTCOUNT ( restaurants_clean[restaurant_id] )
Average Order Value  = DIVIDE ( [Total Order Amount], [Total Orders] )
Average Restaurant Rating = AVERAGE ( restaurants_clean[restaurant_rating] )
Delivered Orders     = CALCULATE ( [Total Orders], orders_clean[order_status] = "Delivered" )
Cancelled Orders     = CALCULATE ( [Total Orders], orders_clean[order_status] = "Cancelled" )
Cancellation Rate    = DIVIDE ( [Cancelled Orders], [Total Orders] )
Vehicle Count        = DISTINCTCOUNT ( orders_clean[delivery_vehicle_id] )
Revenue MoM %        =
VAR Prev = CALCULATE ( [Total Order Amount], DATEADD ( DimDate[Date], -1, MONTH ) )
RETURN DIVIDE ( [Total Order Amount] - Prev, Prev )
```
Date table:
```dax
DimDate = ADDCOLUMNS ( CALENDAR ( DATE(2025,11,1), DATE(2026,9,30) ),
  "Year", YEAR ( [Date] ), "MonthNumber", MONTH ( [Date] ),
  "MonthName", FORMAT ( [Date], "MMM" ), "YearMonth", FORMAT ( [Date], "YYYY-MM" ) )
```
Plain English: `Total Orders` uses DISTINCTCOUNT so an order is never counted twice; `Vehicle Count` is the number of
*distinct vehicles that delivered at least one order* in the filter context (not fleet size); `Revenue MoM %` shifts the
date filter back one month and compares. **Total Order Amount includes cancelled/refunded orders** (matches the
reference dashboard); filter on `order_status = "Delivered"` for realised revenue.
