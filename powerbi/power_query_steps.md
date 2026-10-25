# Power Query (M) steps
Set a `DataPath` parameter (Home > Manage Parameters, Text) to the absolute path of `data/processed/`.

```m
// orders_clean
let
  Source   = Csv.Document(File.Contents(DataPath & "orders_clean.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
  Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
  Typed    = Table.TransformColumnTypes(Promoted, {
      {"order_id", type text}, {"order_timestamp", type datetime}, {"order_date", type date},
      {"restaurant_id", type text}, {"cuisine", type text}, {"payment_mode", type text},
      {"order_status", type text}, {"item_quantity", Int64.Type}, {"order_amount", type number},
      {"discount", type number}, {"delivery_fee", type number}, {"packaging_fee", type number},
      {"tax", type number}, {"delivery_vehicle_id", type text}, {"is_outlier_amount", Int64.Type}}, "en-US"),
  Trimmed  = Table.TransformColumns(Typed, {{"order_status", Text.Trim, type text}, {"payment_mode", Text.Trim, type text}}),
  Dedup    = Table.Distinct(Trimmed, {"order_id"})
in Dedup
```
```m
// restaurants_clean
let
  Source   = Csv.Document(File.Contents(DataPath & "restaurants_clean.csv"), [Delimiter=",", Encoding=65001]),
  Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
  Typed    = Table.TransformColumnTypes(Promoted, {{"restaurant_rating", type number}}, "en-US")
in Typed
```
Nulls in `payment_mode` and duplicate rows were already resolved in `python/data_cleaning.py`
(null -> "Unknown", 15 exact duplicates removed); the M `Table.Distinct` is a safety net.
