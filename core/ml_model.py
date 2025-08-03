from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

def train_predict(df, model_type="decision_tree"):
    # Drop NAs from indicators
    df = df.dropna(subset=['RSI', 'MACD', 'MACD_signal', 'Volume', 'close'])

    # Target: whether next day's close is higher
    df['Target'] = (df['close'].shift(-1) > df['close']).astype(int)

    # Features
    feature_cols = ['RSI', 'MACD', 'MACD_signal', 'Volume']
    X = df[feature_cols]
    y = df['Target']

    # Drop last row (since y = NaN due to shift)
    X = X[:-1]
    y = y[:-1]

    print(f"✅ Shape of X: {X.shape}")
    print(f"✅ Shape of y: {y.shape}")
    
    if X.shape[0] < 50:
        print("❌ Not enough data to train the model. At least 50 rows required.")
        return df, None, None

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    # Choose model
    if model_type == "logistic":
        model = LogisticRegression()
    else:
        model = DecisionTreeClassifier(max_depth=5)

    # Train
    model.fit(X_train, y_train)

    # Predict & Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"✅ Accuracy: {acc:.2f}")
    print("✅ Classification Report:")
    print(classification_report(y_test, y_pred))

    return df, acc, model
