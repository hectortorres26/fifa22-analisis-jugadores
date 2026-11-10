"""Predicción de la valoración value_eur de FIFA 22, no del salario wage_eur."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import clone
from sklearn.compose import TransformedTargetRegressor
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from .common import configure_plots, save_json, provenance, save_figure

FEATURES = [
    "age",
    "height_cm",
    "weight_kg",
    "overall",
    "potential",
    "international_reputation",
    "pace",
    "shooting",
    "passing",
    "dribbling",
    "defending",
    "physic",
]
TARGET = "value_eur"
SEED = 42


def load_data(path):
    raw = pd.read_csv(path, low_memory=False)
    required = ["sofifa_id", TARGET] + FEATURES
    if not set(required).issubset(raw.columns):
        raise ValueError("Faltan columnas del esquema de FIFA 22.")
    if raw.sofifa_id.isna().any() or raw.sofifa_id.duplicated().any():
        raise ValueError("sofifa_id debe ser único y no nulo.")
    raw[FEATURES + [TARGET]] = raw[FEATURES + [TARGET]].apply(
        pd.to_numeric, errors="raise"
    )
    # Nunca imputar la variable objetivo: excluir valores desconocidos o no positivos.
    valid = raw[TARGET].notna() & np.isfinite(raw[TARGET]) & (raw[TARGET] > 0)
    data = raw.loc[valid, FEATURES + [TARGET]].copy()
    if data.empty:
        raise ValueError("No hay valoraciones positivas para modelar.")
    if np.isinf(data[FEATURES].to_numpy()).any():
        raise ValueError("Hay atributos infinitos.")
    if data[FEATURES].isna().all().any():
        raise ValueError("Existe una variable sin observaciones.")
    return data, {
        "filas_originales": len(raw),
        "objetivos_excluidos": int((~valid).sum()),
        "nulos_features": data[FEATURES].isna().sum().to_dict(),
    }


def candidates():
    def pre(model, scale=False):
        steps = [("imputer", SimpleImputer(strategy="median", add_indicator=True))]
        if scale:
            steps.append(("scaler", StandardScaler()))
        return Pipeline(steps + [("model", model)])

    return {
        "base_mediana": pre(DummyRegressor(strategy="median")),
        "ridge_log": TransformedTargetRegressor(
            regressor=pre(Ridge(alpha=10), True), func=np.log1p, inverse_func=np.expm1
        ),
        "gradient_boosting_log": TransformedTargetRegressor(
            regressor=pre(
                HistGradientBoostingRegressor(
                    max_iter=200,
                    max_leaf_nodes=15,
                    l2_regularization=10,
                    early_stopping=False,
                    random_state=SEED,
                )
            ),
            func=np.log1p,
            inverse_func=np.expm1,
        ),
    }


def evaluate(y, pred):
    return {
        "mae_eur": float(mean_absolute_error(y, pred)),
        "rmse_eur": float(np.sqrt(mean_squared_error(y, pred))),
        "r2": float(r2_score(y, pred)),
    }


def run(data_path, output_dir="reports"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    configure_plots()
    data, quality = load_data(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        data[FEATURES], data[TARGET], test_size=0.2, random_state=SEED
    )
    assert set(X_train.index).isdisjoint(X_test.index)
    models = candidates()
    cv = KFold(5, shuffle=True, random_state=SEED)
    cv_rows = []
    for name, model in models.items():
        s = cross_validate(
            model,
            X_train,
            y_train,
            cv=cv,
            scoring="neg_mean_absolute_error",
            n_jobs=1,
            error_score="raise",
        )
        cv_rows.append(
            {
                "modelo": name,
                "mae_cv_eur": float(-s["test_score"].mean()),
                "desviacion_cv_eur": float(s["test_score"].std(ddof=1)),
            }
        )
    chosen = min(cv_rows, key=lambda r: r["mae_cv_eur"])["modelo"]
    fitted = clone(models[chosen]).fit(X_train, y_train)
    pred = fitted.predict(X_test)
    baseline = clone(models["base_mediana"]).fit(X_train, y_train)
    selected = evaluate(y_test, pred)
    base = evaluate(y_test, baseline.predict(X_test))
    errors = np.abs(y_test.to_numpy() - pred)
    rng = np.random.default_rng(SEED)
    boots = [
        float(errors[rng.integers(0, len(errors), len(errors))].mean())
        for _ in range(500)
    ]
    importance = permutation_importance(
        fitted,
        X_test,
        y_test,
        scoring="neg_mean_absolute_error",
        n_repeats=5,
        random_state=SEED,
        n_jobs=1,
    )
    imp = pd.DataFrame(
        {
            "variable": FEATURES,
            "incremento_mae_eur": importance.importances_mean,
            "desviacion": importance.importances_std,
        }
    ).sort_values("incremento_mae_eur", ascending=False)
    imp.to_csv(output / "importancia_variables.csv", index=False)
    error_table = (
        pd.DataFrame(
            {
                "rango_valor": pd.cut(
                    y_test,
                    [0, 1e6, 5e6, 20e6, np.inf],
                    labels=["≤1 M€", "1–5 M€", "5–20 M€", ">20 M€"],
                ),
                "error_absoluto": errors,
            }
        )
        .groupby("rango_valor", observed=True)
        .agg(n=("error_absoluto", "size"), mae_eur=("error_absoluto", "mean"))
    )
    error_table.to_csv(output / "error_por_rango.csv")
    summary = {
        "target": TARGET,
        "unidad": "EUR de valoración en FIFA 22",
        "features": FEATURES,
        "seed": SEED,
        "n_jugadores": len(data),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "calidad": quality,
        "cv": cv_rows,
        "modelo_seleccionado": chosen,
        "test": selected,
        "baseline_test": base,
        "reduccion_mae_vs_base": 1 - selected["mae_eur"] / base["mae_eur"],
        "mae_ic95_bootstrap_eur": np.quantile(boots, [0.025, 0.975]).tolist(),
        "fuente": provenance(data_path),
    }
    save_json(output / "metrics.json", summary)
    pd.DataFrame(cv_rows).to_csv(output / "validacion_cruzada.csv", index=False)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), layout="constrained")
    axes[0].hist(np.log10(data[TARGET]), bins=35, color="#23788e")
    axes[0].set(
        title="Distribución de valoraciones",
        xlabel="log10(valor en EUR)",
        ylabel="Jugadores",
    )
    density = axes[1].hexbin(
        y_test / 1e6, pred / 1e6, gridsize=35, mincnt=1, bins="log", cmap="viridis"
    )
    fig.colorbar(
        density, ax=axes[1], shrink=0.7, label="Jugadores por celda (escala log)"
    )
    lim = max(float(y_test.max()), float(pred.max())) / 1e6
    axes[1].plot([0, lim], [0, lim], linestyle="--", color="#d66a38")
    axes[1].set(
        title="Prueba reservada",
        xlabel="Valor real del juego (M€)",
        ylabel="Valor estimado (M€)",
    )
    top = imp.head(6).iloc[::-1]
    axes[2].barh(top.variable, top.incremento_mae_eur / 1e6, color="#23788e")
    axes[2].set(title="Importancia por permutación", xlabel="Aumento de MAE (M€)")
    fig.suptitle(
        f"FIFA 22 | MAE {selected['mae_eur']/1e6:.2f} M€ · R² {selected['r2']:.3f}",
        fontsize=17,
    )
    save_figure(fig, output / "evaluacion.png")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", default="data/players_22.csv")
    p.add_argument("--output", default="reports")
    a = p.parse_args()
    r = run(a.data, a.output)
    print(
        f"Modelo: {r['modelo_seleccionado']}; MAE: {r['test']['mae_eur']:,.0f} EUR; R2: {r['test']['r2']:.4f}"
    )
