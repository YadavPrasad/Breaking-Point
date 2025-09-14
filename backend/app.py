import os
import joblib
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# =========================
# Setup directories
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_DIR = os.path.join(BASE_DIR, "model_artifacts")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")  # container path

# =========================
# Load artifacts safely
# =========================
def try_load(path):
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"[WARN] Could not load {path}: {e}")
        return None

model = try_load(os.path.join(ARTIFACT_DIR, "best_model.pkl"))
encoders = try_load(os.path.join(ARTIFACT_DIR, "encoders.pkl"))
scaler = try_load(os.path.join(ARTIFACT_DIR, "scaler.pkl"))
tfidf = try_load(os.path.join(ARTIFACT_DIR, "tfidf.pkl"))
y_encoder = try_load(os.path.join(ARTIFACT_DIR, "y_encoder.pkl"))

label_enc_cols = ["manufacturer_id", "name_manufacturer", "country_device", "status"]
numeric_cols = ["number_device", "quantity_in_commerce"]
text_cols = ["name", "action_summary", "reason"]

# =========================
# Setup Flask app
# =========================
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# =========================
# Frontend serving
# =========================
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path:
        requested = os.path.join(FRONTEND_DIR, path)
        if os.path.exists(requested) and os.path.isfile(requested):
            return send_from_directory(FRONTEND_DIR, path)

    index_path = os.path.join(FRONTEND_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIR, 'index.html')

    return jsonify({"message": "Backend running. Frontend not found on server."})

# =========================
# Prediction endpoint
# =========================
@app.route('/predict', methods=['POST'])
def predict():
    if model is None or encoders is None or scaler is None or tfidf is None or y_encoder is None:
        return jsonify({"error": "Model artifacts not loaded on server."}), 503

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Encode label features
        label_features = []
        for col in label_enc_cols:
            val = str(data.get(col, "Unknown"))
            try:
                encoded = encoders[col].transform([val])[0]
            except Exception:
                encoded = 0
            label_features.append(encoded)

        # Process numeric features
        numeric_features = []
        for col in numeric_cols:
            raw = str(data.get(col, "0"))
            cleaned = "".join([ch for ch in raw if ch.isdigit() or ch == "."])
            try:
                num_val = float(cleaned) if cleaned != "" else 0.0
            except Exception:
                num_val = 0.0
            numeric_features.append(num_val)

        numeric_scaled = scaler.transform([numeric_features])[0]

        # TF-IDF for text fields
        text_input = " ".join([str(data.get(col, "")) for col in text_cols])
        text_vector = tfidf.transform([text_input]).toarray()[0]

        # Combine all features
        features = np.hstack([label_features, numeric_scaled, text_vector])

        # Predict
        pred_encoded = int(model.predict([features])[0])
        pred_decoded = int(y_encoder.inverse_transform([pred_encoded])[0])
        proba = model.predict_proba([features])[0]

        return jsonify({
            "prediction": pred_decoded,
            "probabilities": {str(cls): float(prob) for cls, prob in zip(y_encoder.classes_, proba)}
        })

    except Exception as e:
        app.logger.exception("Prediction error")
        return jsonify({"error": str(e)}), 500

# =========================
# Run app
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
