import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

input_file = ROOT / "data" / "eurusd_features.csv"

df = pd.read_csv(input_file)

TP = 0.0030
SL = 0.0015

targets = []

look_ahead = 48

for i in range(len(df)):

    if i + look_ahead >= len(df):
        targets.append(None)
        continue

    entry = df.loc[i, "close"]

    tp_price = entry + TP
    sl_price = entry - SL

    future = df.iloc[i+1:i+look_ahead+1]

    label = None

    for _, row in future.iterrows():

        high = row["high"]
        low = row["low"]

        if high >= tp_price:
            label = 1
            break

        if low <= sl_price:
            label = 0
            break

    if label is None:
        label = 0

    targets.append(label)

df["target"] = targets

df = df.dropna()

output_file = (
    ROOT / "data" / "eurusd_labeled.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\nLabels Created")

print(
    "\nWinning Trades:",
    (df["target"] == 1).sum()
)

print(
    "Losing Trades:",
    (df["target"] == 0).sum()
)

print(
    "\nWin Rate:",
    round(
        df["target"].mean()*100,
        2
    ),
    "%"
)