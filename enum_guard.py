"""enum-guard: check CSV columns against allowed value sets from a JSON config."""
import argparse, csv, json, sys
from collections import Counter

def check(path, rules, case_sensitive=True):
    norm = (lambda s: s) if case_sensitive else (lambda s: s.lower())
    allowed = {c: {norm(v) for v in vals} for c, vals in rules.items()}
    bad = {c: Counter() for c in rules}
    n = 0
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        missing = [c for c in rules if c not in (r.fieldnames or [])]
        if missing:
            raise ValueError(f"columns not in file: {missing}")
        for row in r:
            n += 1
            for c, ok in allowed.items():
                v = (row[c] or "").strip()
                if norm(v) not in ok:
                    bad[c][v] += 1
    return {"rows": n, "violations": {c: dict(b) for c, b in bad.items() if b}}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv"); p.add_argument("rules", help='JSON like {"status": ["active", "closed"]}')
    p.add_argument("--ignore-case", action="store_true")
    a = p.parse_args(argv)
    with open(a.rules, encoding="utf-8") as f:
        rules = json.load(f)
    rep = check(a.csv, rules, not a.ignore_case)
    print(json.dumps(rep, indent=2))
    return 1 if rep["violations"] else 0

if __name__ == "__main__":
    sys.exit(main())
