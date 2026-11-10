import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from src.analysis import FEATURES, TARGET, load_data, candidates


class FifaTests(unittest.TestCase):
    def test_target_is_value_not_wage(self):
        with tempfile.TemporaryDirectory() as d:
            frame = pd.DataFrame(np.ones((4, len(FEATURES))), columns=FEATURES)
            frame["sofifa_id"] = [1, 2, 3, 4]
            frame["value_eur"] = [100.0, 200.0, np.nan, 0.0]
            frame["wage_eur"] = 999.0
            p = Path(d) / "f.csv"
            frame.to_csv(p, index=False)
            data, quality = load_data(p)
            self.assertEqual(TARGET, "value_eur")
            self.assertEqual(data[TARGET].tolist(), [100.0, 200.0])
            self.assertEqual(quality["objetivos_excluidos"], 2)
            self.assertNotIn("wage_eur", data)
            self.assertNotIn("sofifa_id", data)

    def test_no_target_proxies(self):
        for name in ["value_eur", "wage_eur", "release_clause_eur", "sofifa_id"]:
            self.assertNotIn(name, FEATURES)

    def test_imputation_fits_training_only(self):
        X = pd.DataFrame(np.arange(120, dtype=float).reshape(10, 12), columns=FEATURES)
        X.loc[0, "pace"] = np.nan
        y = np.arange(10) * 100 + 1000
        model = candidates()["ridge_log"].fit(X, y)
        medians = model.regressor_.named_steps["imputer"].statistics_.copy()
        model.predict(X.fillna(100) * 1.1)
        np.testing.assert_allclose(medians, X.median())
        np.testing.assert_array_equal(
            medians, model.regressor_.named_steps["imputer"].statistics_
        )


if __name__ == "__main__":
    unittest.main()
