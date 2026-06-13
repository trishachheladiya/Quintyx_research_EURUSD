import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

csv_path = ROOT / "data" / "EURUSD_H1_201801020000_202606050900.csv"

df = pd.read_csv(
    csv_path,
    sep="\t"
)

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== COLUMN NAMES =====")
print(df.columns)

print("\n===== SHAPE =====")
print(df.shape)