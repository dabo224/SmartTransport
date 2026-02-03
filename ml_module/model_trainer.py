import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

def train_model():
    # Load data
    try:
        df = pd.read_csv('ml_module/traffic_data.csv')
    except FileNotFoundError:
        print("Data file not found. Running simulator first...")
        from data_simulator import generate_traffic_data
        generate_traffic_data(5000)
        df = pd.read_csv('ml_module/traffic_data.csv')

    # Features and Target
    X = df[['hour', 'day_of_week', 'road_type', 'weather_condition', 'avg_speed']]
    y = df['traffic_level']

    # Preprocessing
    categorical_features = ['day_of_week', 'road_type', 'weather_condition']
    numeric_features = ['hour', 'avg_speed']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # Model Pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    print("Training model...")
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, 'ml_module/traffic_model.joblib')
    print("Model saved to 'ml_module/traffic_model.joblib'")

if __name__ == "__main__":
    train_model()
