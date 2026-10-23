# enum-guard

Catch unexpected category values before they hit your warehouse: check CSV columns against allowed value sets and get a count of every bad value.

Pure Python stdlib.

```bash
echo '{"status": ["active", "closed"], "country": ["AE", "IN"]}' > rules.json
python enum_guard.py orders.csv rules.json --ignore-case
```

Prints a JSON report and exits `1` if any value is outside its set, so it works as a pipeline gate.

```bash
python -m unittest -v
```
