import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

input_file = ROOT / "data" / "eurusd_features.csv"

df = pd.read_csv(input_file)

# =====================================
# FUTURE RETURN TARGET
# =====================================

LOOKAHEAD = 120

df["future_close"] = df["close"].shift(-LOOKAHEAD)

df["future_return"] = (
    (df["future_close"] - df["close"])
    / df["close"]
)

# Remove rows without future data
df = df.dropna()

# =====================================
# SAVE
# =====================================

output_file = ROOT / "data" / "eurusd_returns.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nRETURN LABELS CREATED")

print("\nRows:", len(df))

print("\nFuture Return Statistics")

print(df["future_return"].describe())