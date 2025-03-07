import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

DATA_PATH = os.path.join(os.path.dirname(__file__), "reservations.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.pkl")

# ✅ Function to train the model
def train_demand_model():
    try:
        if not os.path.exists(DATA_PATH):
            print("❌ ERROR: CSV file not found!")
            return None
        
        data = pd.read_csv(DATA_PATH)

        if data.empty:
            print("❌ ERROR: CSV file is empty")
            return None

        required_columns = {"station_id", "day", "hour", "demand"}
        if not required_columns.issubset(data.columns):
            print("❌ ERROR: Missing columns in CSV.")
            return None

        X = data[['station_id', 'day', 'hour']]
        y = data['demand']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X_train, y_train)

        joblib.dump(model, MODEL_PATH)  # ✅ Save trained model
        print("✅ Model trained & saved successfully!")
        return model

    except Exception as e:
        print("❌ ERROR training demand model:", e)
        return None
def predict_demand(station_id, day, hour):
    """Predict demand based on station, day, and hour."""
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)  # ✅ Load the saved model
        prediction = model.predict([[station_id, day, hour]])[0]
        return round(float(prediction), 2)
    return "Error: Model not trained"

# ✅ Function to append new reservation data & decide if retraining is needed
def add_reservation_to_csv(station_id, day, hour):
    try:
        new_data = pd.DataFrame([[station_id, day, hour, 1.0]], columns=["station_id", "day", "hour", "demand"])
        
        if not os.path.exists(DATA_PATH):
            new_data.to_csv(DATA_PATH, index=False)
        else:
            new_data.to_csv(DATA_PATH, mode='a', header=False, index=False)

        # ✅ Check if we should retrain (every 15 reservations)
        data = pd.read_csv(DATA_PATH)
        total_reservations = len(data)

        if total_reservations % 15 == 0:  # Retrain only every 15 new bookings
            print(f"🔄 Retraining model after {total_reservations} reservations...")
            train_demand_model()
        else:
            print(f"✅ New reservation added. Total count: {total_reservations}. Waiting for next retrain.")

    except Exception as e:
        print("❌ ERROR adding reservation data:", e)

# ✅ Load model (train if not already trained)
if os.path.exists(MODEL_PATH):
    print("✅ Loading pre-trained model...")
    demand_model = joblib.load(MODEL_PATH)
else:
    print("🔄 No trained model found. Training now...")
    demand_model = train_demand_model()
