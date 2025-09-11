import os
import joblib
from flask import Flask, request, jsonify, send_from_directory
import numpy as np
from flask_cors import CORS

# =========================
# Setup directories and load artifacts
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_DIR = os.path.join(BASE_DIR, "model_artifacts")
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

# Load artifacts
model = joblib.load(os.path.join(ARTIFACT_DIR, "best_model.joblib"))
label_encoders = joblib.load(os.path.join(ARTIFACT_DIR, "label_encoders.joblib"))
tfidf = joblib.load(os.path.join(ARTIFACT_DIR, "tfidf_reason.joblib"))

# =========================
# Setup Flask app
# =========================

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)  # allows frontend JS to call backend without CORS issues

@app.route('/')
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Extract features
        country_event = data.get("country_event", "")
        determined_cause = data.get("determined_cause", "")
        status = data.get("status", "")
        risk_class = data.get("risk_class", "")
        reason = data.get("reason", "")

        # Encode categorical features safely
        def safe_transform(label, encoder_name):
            try:
                return label_encoders[encoder_name].transform([label])[0]
            except ValueError:
                # If unseen label, assign a default value (e.g., 0)
                return 0

        country_event_encoded = safe_transform(country_event, "country_event")
        determined_cause_encoded = safe_transform(determined_cause, "determined_cause")
        status_encoded = safe_transform(status, "status")
        risk_class_encoded = safe_transform(risk_class, "risk_class")

        # TF-IDF for reason (handle empty reason)
        reason_vector = tfidf.transform([reason if reason else ""]).toarray()[0]

        # Combine features
        features = np.hstack([
            [country_event_encoded, determined_cause_encoded, status_encoded, risk_class_encoded],
            reason_vector
        ])

        # Predict
        probability = float(model.predict_proba([features])[0][1])
        prediction = int(model.predict([features])[0])

        return jsonify({
            "probability": round(probability, 4),
            "prediction": prediction
        })

    except Exception as e:
        # Return error with message for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

