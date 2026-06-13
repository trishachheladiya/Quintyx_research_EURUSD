import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parent.parent

data_file = ROOT / "data" / "eurusd_labeled.csv"

df = pd.read_csv(data_file)

# Features
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

X = df[features]
y = df["target"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

# Train Model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n======================")
print("MODEL RESULTS")
print("======================")
print(f"Accuracy: {accuracy:.2%}")

# Current Market State
latest = X.iloc[-1:]

buy_probability = model.predict_proba(
    latest
)[0][1]

sell_probability = model.predict_proba(
    latest
)[0][0]

print("\nLATEST MARKET STATE")
print(f"Buy Probability : {buy_probability:.2%}")
print(f"Sell Probability: {sell_probability:.2%}")

# ======================
# FEATURE IMPORTANCE
# ======================

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\nFEATURE IMPORTANCE")
print(importance)