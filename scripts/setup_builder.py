import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    ROOT / "data" / "eurusd_features.csv"
)

# =========================
# LONG SETUP
# =========================

long_setup = (
    (df["ema20"] > df["ema50"])
    &
    (df["ema50"] > df["ema200"])
    &
    (df["close"] > df["ema20"])
    &
    (df["rsi14"] > 55)
)

# =========================
# SHORT SETUP
# =========================

short_setup = (
    (df["ema20"] < df["ema50"])
    &
    (df["ema50"] < df["ema200"])
    &
    (df["close"] < df["ema20"])
    &
    (df["rsi14"] < 45)
)

df["setup"] = 0

df.loc[long_setup, "setup"] = 1
df.loc[short_setup, "setup"] = -1

setups = df[df["setup"] != 0]

output_file = (
    ROOT / "data" / "eurusd_setups.csv"
)

setups.to_csv(
    output_file,
    index=False
)

print("\nSETUPS CREATED")

print(
    "\nLong Setups:",
    (setups["setup"] == 1).sum()
)

print(
    "Short Setups:",
    (setups["setup"] == -1).sum()
)

print(
    "\nTotal Setups:",
    len(setups)
)