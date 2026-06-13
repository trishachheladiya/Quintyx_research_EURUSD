import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

ROOT = Path(__file__).resolve().parent.parent

data_file = ROOT / "data" / "eurusd_returns.csv"

df = pd.read_csv(data_file)

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

y = df["future_return"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print("\n========================")
print("RETURN MODEL RESULTS")
print("========================")

print(f"MAE: {mae:.6f}")

latest = X.iloc[-1:]

expected_return = model.predict(
    latest
)[0]

print(
    f"\nExpected 24H Return: {expected_return:.4%}"
)

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