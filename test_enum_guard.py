import os, tempfile, unittest
from enum_guard import check

class T(unittest.TestCase):
    def setUp(self):
        self.p = os.path.join(tempfile.mkdtemp(), "a.csv")
        with open(self.p, "w", encoding="utf-8") as f:
            f.write("id,status\n1,active\n2,Active\n3,deleted\n4,deleted\n")
    def test_violations(self):
        r = check(self.p, {"status": ["active", "closed"]})
        self.assertEqual(r["rows"], 4)
        self.assertEqual(r["violations"], {"status": {"Active": 1, "deleted": 2}})
    def test_ignore_case(self):
        r = check(self.p, {"status": ["active", "deleted"]}, case_sensitive=False)
        self.assertEqual(r["violations"], {})
    def test_missing_col(self):
        with self.assertRaises(ValueError):
            check(self.p, {"nope": ["x"]})

if __name__ == "__main__":
    unittest.main()
