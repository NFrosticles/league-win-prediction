from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model and encoders
model = joblib.load('../models/model.pkl')
encoder = joblib.load('../models/encoder.pkl')
scaler = joblib.load('../models/scaler.pkl')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = [
        data['player_win_rate'],
        data['player_kda'],
        data['champion_win_rate'],
        data['champion_kda']
    ]
    champion_id = data['champion_id']

    # Encode and scale features
    encoded_champion = encoder.transform([[champion_id]]).toarray()
    scaled_features = scaler.transform([features])

    # Combine features
    input_features = pd.concat([pd.DataFrame(scaled_features), pd.DataFrame(encoded_champion)], axis=1)

    # Predict win probability
    win_prob = model.predict_proba(input_features)[0][1]
    return jsonify({'win_probability': win_prob})


if __name__ == '__main__':
    app.run(debug=True)