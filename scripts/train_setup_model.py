import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parent.parent

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    ROOT / "data" / "eurusd_setup_labeled.csv"
)

# =====================================
# FEATURES
# =====================================

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

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

# =====================================
# MODEL
# =====================================

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=20,
    random_state=42
)

model.fit(X_train, y_train)

# =====================================
# TEST RESULTS
# =====================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n======================")
print("SETUP MODEL RESULTS")
print("======================")

print(
    f"Accuracy: {accuracy*100:.2f}%"
)

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# =====================================
# LATEST SETUP
# =====================================

latest = X.iloc[-1:]

probabilities = model.predict_proba(
    latest
)[0]

loss_probability = probabilities[0]
win_probability = probabilities[1]

print("\n======================")
print("LATEST SETUP")
print("======================")

print(
    f"TP Probability : {win_probability*100:.2f}%"
)

print(
    f"SL Probability : {loss_probability*100:.2f}%"
)

# =====================================
# FEATURE IMPORTANCE
# =====================================

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\nFEATURE IMPORTANCE\n")

print(importance)

# =====================================
# HIGH CONFIDENCE TRADES
# =====================================

all_probs = model.predict_proba(X_test)

tp_probs = all_probs[:,1]

high_confidence = tp_probs >= 0.70

if high_confidence.sum() > 0:

    filtered_accuracy = (
        y_test[high_confidence]
        ==
        predictions[high_confidence]
    ).mean()

    print("\n======================")
    print("70%+ PROBABILITY TRADES")
    print("======================")

    print(
        "Trades:",
        high_confidence.sum()
    )

    print(
        f"Accuracy: {filtered_accuracy*100:.2f}%"
    )
else:

    print(
        "\nNo trades above 70% probability."
    )

    # =====================================
# THRESHOLD REPORT
# =====================================

print("\n======================")
print("THRESHOLD REPORT")
print("======================")

all_probs = model.predict_proba(X_test)
tp_probs = all_probs[:, 1]

thresholds = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]

for threshold in thresholds:

    mask = tp_probs >= threshold

    trades = mask.sum()

    if trades == 0:
        continue

    accuracy = (
        y_test[mask] ==
        predictions[mask]
    ).mean()

    actual_win_rate = (
        y_test[mask]
    ).mean()

    print(f"\nThreshold: {threshold:.0%}")
    print(f"Trades: {trades}")
    print(f"Accuracy: {accuracy*100:.2f}%")
    print(f"Actual Win Rate: {actual_win_rate*100:.2f}%")

    import joblib

joblib.dump(
    model,
    "models/eurusd_model.pkl"
)

print("Model saved.")