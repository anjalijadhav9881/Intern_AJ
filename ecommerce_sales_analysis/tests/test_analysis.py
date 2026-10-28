"""Tests for the sales analysis pipeline.

Run with either:
    python -m unittest discover -s tests -v
    pytest -v
"""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import main  # noqa: E402


def make_df(rows):
    return pd.DataFrame(rows, columns=main.REQUIRED_COLUMNS)


GOOD = [
    ["2025-01-05", "Books", 2, 10.0, "North"],
    ["2025-02-10", "Electronics", 1, 300.0, "South"],
    ["2025-02-11", "books", 3, 10.0, " North "],
]


class CleaningTests(unittest.TestCase):
    def test_standardises_text_and_computes_revenue(self):
        df, log = main.clean_data(make_df(GOOD))
        self.assertEqual(set(df["product_category"]), {"Books", "Electronics"})
        self.assertEqual(set(df["region"]), {"North", "South"})
        self.assertAlmostEqual(df["revenue"].sum(), 350.0)
        self.assertEqual(log["rows_out"], 3)

    def test_removes_duplicates_missing_and_invalid(self):
        rows = GOOD + [GOOD[0], ["2025-03-01", "Sports", 2, None, "East"],
                       ["2025-03-02", "Sports", -1, 5.0, "East"]]
        df, log = main.clean_data(make_df(rows))
        self.assertEqual(log["duplicates_removed"], 1)
        self.assertEqual(log["missing_removed"], 1)
        self.assertEqual(log["invalid_removed"], 1)
        self.assertEqual(len(df), 3)

    def test_bad_dates_are_dropped(self):
        _, log = main.clean_data(make_df(GOOD + [["not-a-date", "Books", 1, 5.0, "West"]]))
        self.assertEqual(log["missing_removed"], 1)

    def test_empty_after_cleaning_raises(self):
        with self.assertRaises(main.DataError):
            main.clean_data(make_df([["2025-01-01", "Books", -1, 5.0, "North"]]))


class AnalysisTests(unittest.TestCase):
    def test_metrics(self):
        df, _ = main.clean_data(make_df(GOOD))
        r = main.analyze(df)
        self.assertAlmostEqual(r["total_revenue"], 350.0)
        self.assertEqual(r["top_category"], "Electronics")
        self.assertEqual(r["orders"], 3)
        self.assertEqual(len(r["monthly"]), 2)


class LoadingTests(unittest.TestCase):
    def test_missing_file_raises(self):
        with self.assertRaises(main.DataError):
            main.load_data(Path("does_not_exist.csv"))

    def test_missing_columns_raises(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.csv"
            p.write_text("a,b\n1,2\n")
            with self.assertRaisesRegex(main.DataError, "Missing required columns"):
                main.load_data(p)

    def test_empty_file_raises(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "empty.csv"
            p.write_text("")
            with self.assertRaises(main.DataError):
                main.load_data(p)


class PipelineTests(unittest.TestCase):
    def test_full_pipeline_creates_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            (tmp / "data").mkdir()
            csv = tmp / "data" / "in.csv"
            make_df(GOOD).to_csv(csv, index=False)
            with mock.patch.object(main, "VIZ_DIR", tmp / "viz"), \
                 mock.patch.object(main, "REPORT_DIR", tmp / "report"), \
                 mock.patch.object(main, "BASE_DIR", tmp):
                out = main.run(csv)
            self.assertTrue(out["report"].exists())
            self.assertEqual(len(list((tmp / "viz").glob("*.png"))), 3)


if __name__ == "__main__":
    unittest.main()
