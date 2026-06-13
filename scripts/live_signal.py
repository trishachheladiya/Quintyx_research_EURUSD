import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import joblib

# =====================
# CONNECT MT5
# =====================

if not mt5.initialize():
    print("MT5 Failed")
    quit()

# =====================
# GET DATA
# =====================

rates = mt5.copy_rates_from_pos(
    "EURUSD",
    mt5.TIMEFRAME_H1,
    0,
    500
)

df = pd.DataFrame(rates)

df["time"] = pd.to_datetime(
    df["time"],
    unit="s"
)

# =====================
# FEATURES
# =====================

df["ema20"] = df["close"].ewm(span=20).mean()
df["ema50"] = df["close"].ewm(span=50).mean()
df["ema200"] = df["close"].ewm(span=200).mean()

# RSI

delta = df["close"].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

df["rsi14"] = 100 - (
    100 / (1 + rs)
)

# ATR

high_low = df["high"] - df["low"]

high_close = np.abs(
    df["high"] - df["close"].shift()
)

low_close = np.abs(
    df["low"] - df["close"].shift()
)

tr = pd.concat(
    [high_low, high_close, low_close],
    axis=1
).max(axis=1)

df["atr14"] = tr.rolling(14).mean()

# Distances

df["distance_from_ema20"] = (
    df["close"] - df["ema20"]
)

df["distance_from_ema50"] = (
    df["close"] - df["ema50"]
)

df["distance_from_ema200"] = (
    df["close"] - df["ema200"]
)

# Slopes

df["ema20_slope"] = (
    df["ema20"] - df["ema20"].shift(5)
)

df["ema50_slope"] = (
    df["ema50"] - df["ema50"].shift(5)
)

df["ema200_slope"] = (
    df["ema200"] - df["ema200"].shift(5)
)

# Returns

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

# Volatility

df["volatility_24"] = (
    df["return_1"]
    .rolling(24)
    .std()
)

df["volatility_72"] = (
    df["return_1"]
    .rolling(72)
    .std()
)

# Time Features

df["hour"] = df["time"].dt.hour
df["day_of_week"] = (
    df["time"].dt.dayofweek
)

# =====================
# LATEST ROW
# =====================

latest = df.iloc[-1:]

features = [
    "ema20",
    "ema50",
    "ema200",
    "rsi14",
    "atr14",
    "distance_from_ema20",
    "distance_from_ema50",
    "distance_from_ema200",
    "ema20_slope",
    "ema50_slope",
    "ema200_slope",
    "return_1",
    "return_5",
    "return_24",
    "return_72",
    "volatility_24",
    "volatility_72",
    "hour",
    "day_of_week"
]

X_live = latest[features]

# =====================
# LOAD MODEL
# =====================

model = joblib.load(
    "models/eurusd_model.pkl"
)

prob = model.predict_proba(
    X_live
)[0]

win_prob = prob[1] * 100



latest_close = float(latest["close"].iloc[0])
atr = float(latest["atr14"].iloc[0])

# Direction

if latest_close > float(latest["ema50"].iloc[0]):
    direction = "BUY"

    entry = latest_close
    sl = entry - atr
    tp = entry + (2 * atr)

else:
    direction = "SELL"

    entry = latest_close
    sl = entry + atr
    tp = entry - (2 * atr)


print("\n===================")
print("LIVE SIGNAL")
print("===================")

print(f"Direction : {direction}")
print(f"Entry     : {entry:.5f}")
print(f"SL        : {sl:.5f}")
print(f"TP        : {tp:.5f}")
print(f"Probability: {win_prob:.2f}%")

if win_prob >= 70:
    print("\nA+ SETUP")

elif win_prob >= 60:
    print("\nGOOD SETUP")

else:
    print("\nNO TRADE")