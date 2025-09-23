import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os

MODEL_FILE = "optimized_expense_model.pkl"
CSV_FILE = "expenses.csv"

def prepare_features(df):
    """Add extra features from Date"""
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayOfWeek'] = df['Date'].dt.day_name()       # Monday, Tuesday, etc.
    df['Month'] = df['Date'].dt.month                # 1-12
    df['IsWeekend'] = (df['Date'].dt.weekday >= 5).astype(int)  # 1 if Sat/Sun
    return df

def train_model(csv_file=CSV_FILE):
    """Train and save optimized model"""
    if not os.path.isfile(csv_file):
        print("No CSV found to train on.")
        return None

    df = pd.read_csv(csv_file)
    if df.empty or 'Category' not in df.columns:
        print("CSV has no valid data.")
        return None

    df = prepare_features(df)

    # Features
    text_feature = 'Description'
    numeric_features = ['Amount']
    categorical_features = ['DayOfWeek', 'Month', 'IsWeekend']
    X = df[[text_feature] + numeric_features + categorical_features]
    y = df['Category']

    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(), text_feature),
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )

    # Full pipeline
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', MultinomialNB())
    ])

    # Train model
    model.fit(X, y)

    # Save model
    joblib.dump(model, MODEL_FILE)
    print(f"Optimized model trained and saved as '{MODEL_FILE}'")
    return model

def load_model():
    """Load saved optimized model"""
    if os.path.isfile(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        print("⚠️ No trained model found.")
        return None

def predict_category(description, amount, date=None):
    """Predict category using optimized model"""
    model = load_model()
    if model is None:
        return None

    if date is None:
        date = pd.Timestamp.now()

    # Prepare a single sample DataFrame
    sample = pd.DataFrame([{
        'Description': description,
        'Amount': amount,
        'Date': pd.to_datetime(date)
    }])

    sample = prepare_features(sample)

    # Keep only required columns
    sample = sample[['Description', 'Amount', 'DayOfWeek', 'Month', 'IsWeekend']]
    prediction = model.predict(sample)[0]
    return prediction
