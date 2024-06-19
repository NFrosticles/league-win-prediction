import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Example data
data = {
    'player_win_rate': [0.55, 0.60, 0.50, 0.65],
    'player_kda': [3.0, 2.5, 1.8, 4.0],
    'champion_win_rate': [0.53, 0.49, 0.56, 0.52],
    'champion_kda': [2.8, 3.2, 1.5, 4.1],
    'champion_id': [157, 245, 41, 64]
}

df = pd.DataFrame(data)

# One-hot encode champion IDs
encoder = OneHotEncoder()
encoded_champions = encoder.fit_transform(df[['champion_id']])

# Normalize numerical features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[['player_win_rate', 'player_kda', 'champion_win_rate', 'champion_kda']])

# Combine features
X = pd.concat([pd.DataFrame(scaled_features), pd.DataFrame(encoded_champions.toarray())], axis=1)

# Example target variable
y = [1, 0, 1, 0]  # 1 for win, 0 for loss

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")


# Save the model and encoders
print("Saving model...")
joblib.dump(model, 'model.pkl')
print("Model saved as model.pkl")

print("Saving encoder...")
joblib.dump(encoder, 'encoder.pkl')
print("Encoder saved as encoder.pkl")

print("Saving scaler...")
joblib.dump(scaler, 'scaler.pkl')
print("Scaler saved as scaler.pkl")

