"""MicroClime engine: TabPFN predicts thermal comfort, Gemma explains it."""
import itertools
import os
from pathlib import Path
import pandas as pd
import requests

# Load .env file automatically
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

SURFACES = ["asphalt", "concrete", "brick", "grass"]
FEATURES = ["surface_type", "shade_level", "breeze_felt"]
TARGET = "perceived_heat"
REQUIRED = FEATURES + [TARGET]


def load_log(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing columns: {missing}")
    df = df.dropna(subset=REQUIRED).copy()
    if len(df) < 5:
        raise ValueError("Need at least 5 logged rows.")
    return df


def _encode(df: pd.DataFrame) -> pd.DataFrame:
    x = df[FEATURES].copy()
    x["surface_type"] = x["surface_type"].map({s: i for i, s in enumerate(SURFACES)}).fillna(0)
    return x.astype(float)


def predict_zones(df: pd.DataFrame):
    """Return (zones_df, model_name). Zones = every surface/shade/breeze combo, scored."""
    df = load_log(df)
    grid = pd.DataFrame(
        list(itertools.product(SURFACES, range(1, 6), [0, 1])), columns=FEATURES
    )
    x_train, y_train, x_grid = _encode(df), df[TARGET].astype(float), _encode(grid)

    try:
        from tabpfn import TabPFNRegressor
        from tabpfn.constants import ModelVersion

        model = TabPFNRegressor.create_default_for_version(ModelVersion.V3)
        name = "TabPFN-3 (tabular foundation model, local)"
    except Exception as e:  # TabPFN not installed -> still usable
        from sklearn.ensemble import RandomForestRegressor

        print(f"[MicroClime] TabPFN unavailable: {e}")
        model, name = RandomForestRegressor(n_estimators=200, random_state=0), "RandomForest (fallback)"

    try:
        model.fit(x_train, y_train)
    except Exception as e:  # e.g. TabPFN weights unavailable offline
        from sklearn.ensemble import RandomForestRegressor

        print(f"[MicroClime] TabPFN fit failed: {e}")
        model, name = RandomForestRegressor(n_estimators=200, random_state=0), "RandomForest (fallback)"
        model.fit(x_train, y_train)

    grid["predicted_heat"] = model.predict(x_grid).round(2)
    return grid.sort_values("predicted_heat").reset_index(drop=True), name


def _fallback_advice(zones: pd.DataFrame) -> str:
    best, worst = zones.iloc[0], zones.iloc[-1]
    return (
        f"Seek out {best.surface_type} with shade level {int(best.shade_level)}"
        f"{' and a breeze' if best.breeze_felt else ''} (predicted heat {best.predicted_heat}/5). "
        f"Avoid {worst.surface_type} with shade level {int(worst.shade_level)} at midday "
        f"(predicted heat {worst.predicted_heat}/5). Now go outside and find it!"
    )


def gemma_advice(zones: pd.DataFrame, place: str = "my neighborhood"):
    """Ask a local Gemma (Ollama) for advice. Returns (text, source)."""
    prompt = (
        f"You are a friendly outdoor guide. A walker in {place} logged heat comfort "
        "(1=cool, 5=hot). A tabular model predicted these zones:\n"
        f"COOLEST:\n{zones.head(3).to_string(index=False)}\n"
        f"HOTTEST:\n{zones.tail(3).to_string(index=False)}\n"
        "In under 70 words, give a practical walking recommendation: where to go, what "
        "to avoid, and end by encouraging them to put the screen away."
    )
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    model = os.environ.get("GEMMA_MODEL", "gemma2:2b")
    try:
        r = requests.post(
            f"{host}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["response"].strip(), f"Gemma via Ollama ({model}, local)"
    except Exception:
        # try gemma:2b or gemma3:1b if specified
        return _fallback_advice(zones), "Offline template (Ollama not running)"
