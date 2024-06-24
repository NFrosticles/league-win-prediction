import joblib

# Load pre-trained model and other necessary objects
model = joblib.load('models/model.pkl')
encoder = joblib.load('models/encoder.pkl')
scaler = joblib.load('models/scaler.pkl')

def preprocess_and_predict(mastery_data):
    # Example: extract relevant features and preprocess them
    features = [
        mastery_data['championLevel'],
        mastery_data['championPoints']
    ]
    features_scaled = scaler.transform([features])
    prediction = model.predict_proba(features_scaled)
    win_percentage = prediction[0][1] * 100  # Assuming the model's positive class is at index 1
    return win_percentage