import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import joblib
import os

ACCOUNT = 108308441
PASSWORD = "_6LaKvUp"
SERVER = "MetaQuotes-Demo"

if not mt5.initialize():
    print("MT5 Init Failed")
    print(mt5.last_error())
    quit()

if not mt5.login(ACCOUNT, PASSWORD, SERVER):
    print("Login Failed")
    print(mt5.last_error())
    mt5.shutdown()
    quit()

print("Connected Successfully")
# =====================
# GET DATA
# =====================

symbol = "EURUSD"

mt5.symbol_select(symbol, True)

rates = mt5.copy_rates_from_pos(
    symbol,
    mt5.TIMEFRAME_H1,
    0,
    500
)

if rates is None:
    print("MT5 returned None")
    print(mt5.last_error())
    mt5.shutdown()
    quit()

df = pd.DataFrame(rates)

if df.empty:
    print("No data returned")
    mt5.shutdown()
    quit()

df["time"] = pd.to_datetime(df["time"], unit="s")

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

df["rsi14"] = 100 - (100 / (1 + rs))

# ATR

high_low = df["high"] - df["low"]
high_close = np.abs(df["high"] - df["close"].shift())
low_close = np.abs(df["low"] - df["close"].shift())

tr = pd.concat(
    [high_low, high_close, low_close],
    axis=1
).max(axis=1)

df["atr14"] = tr.rolling(14).mean()

# Distances

df["distance_from_ema20"] = df["close"] - df["ema20"]
df["distance_from_ema50"] = df["close"] - df["ema50"]
df["distance_from_ema200"] = df["close"] - df["ema200"]

# Slopes

df["ema20_slope"] = df["ema20"] - df["ema20"].shift(5)
df["ema50_slope"] = df["ema50"] - df["ema50"].shift(5)
df["ema200_slope"] = df["ema200"] - df["ema200"].shift(5)

# Returns

df["return_1"] = df["close"].pct_change(1)
df["return_5"] = df["close"].pct_change(5)
df["return_24"] = df["close"].pct_change(24)
df["return_72"] = df["close"].pct_change(72)

# Volatility

df["volatility_24"] = df["return_1"].rolling(24).std()
df["volatility_72"] = df["return_1"].rolling(72).std()

# Time Features

df["hour"] = df["time"].dt.hour
df["day_of_week"] = df["time"].dt.dayofweek

# Remove NaNs

df = df.dropna()

# =====================
# FEATURES LIST
# =====================

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

latest = df.iloc[-1:]

X_live = latest[features]

# =====================
# LOAD MODEL
# =====================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

model_path = os.path.join(
    BASE_DIR,
    "models",
    "eurusd_model.pkl"
)

model = joblib.load(model_path)

# =====================
# PREDICTION
# =====================

prob = model.predict_proba(X_live)[0]

win_prob = prob[1] * 100

# =====================
# ENTRY / SL / TP
# =====================

latest_close = float(latest["close"].iloc[0])
atr = float(latest["atr14"].iloc[0])
ema50 = float(latest["ema50"].iloc[0])

if latest_close > ema50:

    direction = "BUY"

    entry = latest_close
    sl = entry - atr
    tp = entry + (2 * atr)

else:

    direction = "SELL"

    entry = latest_close
    sl = entry + atr
    tp = entry - (2 * atr)

# =====================
# OUTPUT
# =====================

print("\n======================")
print("QUINTYX LIVE SIGNAL")
print("======================")

print("Time       :", latest["time"].iloc[0])
print("Symbol     :", symbol)
print("Direction  :", direction)

print(f"Entry      : {entry:.5f}")
print(f"SL         : {sl:.5f}")
print(f"TP         : {tp:.5f}")

print(f"Probability: {win_prob:.2f}%")

if win_prob >= 70:
    print("Grade      : A+ SETUP")

elif win_prob >= 60:
    print("Grade      : GOOD SETUP")

else:
    print("Grade      : NO TRADE")

mt5.shutdown()

# =====================
# AUTO EXECUTION
# =====================

if win_prob >= 70:

    positions = mt5.positions_get(symbol="EURUSD")

    if positions is not None and len(positions) > 0:
        print("\nPosition already open")
        mt5.shutdown()
        quit()

    tick = mt5.symbol_info_tick(symbol)

    if direction == "BUY":

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_BUY,
            "price": tick.ask,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 999999,
            "comment": "Quintyx BUY",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

    else:

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_SELL,
            "price": tick.bid,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 999999,
            "comment": "Quintyx SELL",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

    result = mt5.order_send(request)

    print("\nTRADE EXECUTED")
    print(result)

else:

    print("\nNo trade. Probability below 70%")