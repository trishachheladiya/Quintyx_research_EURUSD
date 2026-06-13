import pandas as pd
from pathlib import Path
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

ROOT = Path(__file__).resolve().parent.parent

csv_path = ROOT / "data" / "EURUSD_H1_201801020000_202606050900.csv"

# =========================
# LOAD DATA
# =========================

df = pd.read_csv(csv_path, sep="\t")

df["datetime"] = pd.to_datetime(
    df["<DATE>"] + " " + df["<TIME>"]
)

df.rename(columns={
    "<OPEN>": "open",
    "<HIGH>": "high",
    "<LOW>": "low",
    "<CLOSE>": "close"
}, inplace=True)

# =========================
# EMA FEATURES
# =========================

df["ema20"] = EMAIndicator(
    close=df["close"],
    window=20
).ema_indicator()

df["ema50"] = EMAIndicator(
    close=df["close"],
    window=50
).ema_indicator()

df["ema200"] = EMAIndicator(
    close=df["close"],
    window=200
).ema_indicator()

# =========================
# RSI
# =========================

df["rsi14"] = RSIIndicator(
    close=df["close"],
    window=14
).rsi()

# =========================
# ATR
# =========================

atr = AverageTrueRange(
    high=df["high"],
    low=df["low"],
    close=df["close"],
    window=14
)

df["atr14"] = atr.average_true_range()

# =========================
# TREND FEATURES
# =========================

df["distance_from_ema20"] = (
    (df["close"] - df["ema20"])
    / df["ema20"]
)

df["distance_from_ema50"] = (
    (df["close"] - df["ema50"])
    / df["ema50"]
)

df["distance_from_ema200"] = (
    (df["close"] - df["ema200"])
    / df["ema200"]
)

# EMA slopes

df["ema20_slope"] = (
    df["ema20"] -
    df["ema20"].shift(5)
)

df["ema50_slope"] = (
    df["ema50"] -
    df["ema50"].shift(5)
)

df["ema200_slope"] = (
    df["ema200"] -
    df["ema200"].shift(5)
)

# =========================
# MOMENTUM FEATURES
# =========================

df["return_1"] = (
    df["close"].pct_change(1)
)

df["return_5"] = (
    df["close"].pct_change(5)
)

df["return_24"] = (
    df["close"].pct_change(24)
)

df["return_72"] = (
    df["close"].pct_change(72)
)

# =========================
# VOLATILITY FEATURES
# =========================

df["volatility_24"] = (
    df["close"]
    .pct_change()
    .rolling(24)
    .std()
)

df["volatility_72"] = (
    df["close"]
    .pct_change()
    .rolling(72)
    .std()
)

# =========================
# TIME FEATURES
# =========================

df["hour"] = (
    df["datetime"].dt.hour
)

df["day_of_week"] = (
    df["datetime"].dt.dayofweek
)

# =========================
# CLEAN
# =========================

df = df.dropna()

# =========================
# SAVE
# =========================

output_file = (
    ROOT / "data" / "eurusd_features.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\nFEATURE BUILD COMPLETE")
print("\nRows:", len(df))
print("\nColumns:")

for col in df.columns:
    print(col)