import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    ROOT / "data" / "eurusd_setups.csv"
)

TP_PIPS = 30
SL_PIPS = 15

PIP_SIZE = 0.0001

tp = TP_PIPS * PIP_SIZE
sl = SL_PIPS * PIP_SIZE

LOOKAHEAD = 24

df["target"] = -1

# =====================================
# TP-FIRST / SL-FIRST LABELING
# =====================================

for i in range(len(df) - LOOKAHEAD):

    entry = df.iloc[i]["close"]

    direction = df.iloc[i]["setup"]

    future = df.iloc[i+1:i+LOOKAHEAD+1]

    outcome = -1

    for _, candle in future.iterrows():

        high = candle["high"]
        low = candle["low"]

        # LONG TRADE
        if direction == 1:

            tp_hit = high >= entry + tp
            sl_hit = low <= entry - sl

            if tp_hit and sl_hit:
                outcome = 0
                break

            if tp_hit:
                outcome = 1
                break

            if sl_hit:
                outcome = 0
                break

        # SHORT TRADE
        elif direction == -1:

            tp_hit = low <= entry - tp
            sl_hit = high >= entry + sl

            if tp_hit and sl_hit:
                outcome = 0
                break

            if tp_hit:
                outcome = 1
                break

            if sl_hit:
                outcome = 0
                break

    if outcome != -1:
        df.at[df.index[i], "target"] = outcome

# Remove unlabeled trades
df = df[df["target"] != -1]

output_file = (
    ROOT / "data" / "eurusd_setup_labeled.csv"
)

df.to_csv(
    output_file,
    index=False
)

wins = (df["target"] == 1).sum()
losses = (df["target"] == 0).sum()

print("\n======================")
print("PROPER LABELING RESULTS")
print("======================")

print("Winning Trades:", wins)
print("Losing Trades :", losses)

print(
    "Win Rate:",
    round(
        wins / (wins + losses) * 100,
        2
    ),
    "%"
)