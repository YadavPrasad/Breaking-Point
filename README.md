# 🏥 Medical Equipment Failure Prediction  
A Machine Learning powered web application that predicts the failure risk of medical devices based on maintenance history, downtime, and usage patterns.  
Built using **Python, Flask, HTML, CSS, and Scikit-learn**.

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" />
  <img src="https://img.shields.io/badge/Flask-Backend-green" />
  <img src="https://img.shields.io/badge/ML-RandomForest-yellow" />
  <img src="https://img.shields.io/badge/UI-HTML%20%2F%20CSS-pink" />
</p>

---

## 📌 **Project Summary**

Medical equipment failures can cause serious risk in hospitals.  
This ML system predicts whether a device will:

- **FAIL**
- **or NOT FAIL**

based on key operational parameters.

This helps hospitals plan preventive maintenance and reduce risk.

---

## 🧠 **Features**

✔ Predict equipment failure  
✔ Beautiful UI (HTML + CSS only)  
✔ Flask backend  
✔ Machine Learning model (Random Forest)  
✔ Failure probability output  
✔ Simple and fast  
✔ Works offline  
✔ Easy to deploy  

---

## 🧾 **Input Features**

| Feature | Description |
|--------|-------------|
| Age | Equipment age in years |
| Maintenance Cost | Annual maintenance cost |
| Downtime | Total downtime hours |
| Maintenance Frequency | Number of services |
| Failure Event Count | Previous failures |
| Purchase Date | Extracted into Year / Month / Day |

---

## 🧠 **ML Model Details**

- Algorithm: **Random Forest Classifier**
- Libraries used:
  - scikit-learn
  - pandas
  - joblib

Model saved as:

equipment_failure_model.pkl

yaml
Copy code

---

## 📂 **Project Structure**

predictingmedicalequipmentfailure/
│
└── backend/
├── app.py
├── index.html
├── equipment_failure_model.pkl

yaml
Copy code

---

## 🖥️ **Frontend (index.html)**

- Clean, modern, centered UI  
- Single-page application  
- Built using only HTML + CSS (no JS needed)  
- Form posts directly to Flask backend  

---

## 🧩 **Backend (Flask)**

Backend features:

- Serves UI
- Loads ML model
- Handles form submission
- Returns prediction + probability
- Works locally on port 5000

Routes:

GET /
POST /predict_form

yaml
Copy code

---

## ▶️ **How To Run The Project**

### **1️⃣ Install dependencies**
```bash
pip install flask flask-cors pandas scikit-learn joblib
2️⃣ Navigate to backend folder
bash
Copy code
cd backend
3️⃣ Run Flask server
bash
Copy code
python app.py
4️⃣ Open in browser
cpp
Copy code
http://127.0.0.1:5000
5️⃣ Enter details → Get prediction 🎯
🖼️ Screenshots
Add your own screenshots here:

🏠 Home Page
scss
Copy code
![Home Page](screenshots/home.png)
📊 Prediction Result
scss
Copy code
![Result Page](screenshots/result.png)
🛠️ Technologies Used
Python

Flask

HTML

CSS

Scikit-learn

Joblib

Pandas

🔮 Future Enhancements
Database integration (MongoDB / MySQL)

Device health analytics dashboard

Role-based login system

API deployment (Render / Railway / AWS)

Real-time failure alerts

Full hospital maintenance suite

🤝 Contributing
Pull requests are welcome!
If you'd like to improve UI, model accuracy, or add features, feel free to open an issue.

⭐ Support This Project
If you like this project:

⭐ Star this repo
🍴 Fork it
🐛 Submit issues

Your support motivates me to build more ML projects ❤️

👨‍💻 Developer
Vignesh
Machine Learning Developer
Final Year Student 🚀

yaml
Copy code

---

# 🚀 BONUS — Want the GitHub **description**, **tags**, and **repo name**?
Example:

**Repository Name:**  
`medical-equipment-failure-prediction`

**Short Description:**  
Machine Learning model + Flask UI to predict medical equipment failure risk.

**Tags:**  
`machine-learning` `flask` `prediction` `medical-devices` `random-forest` `html` `css` `python` `healthcare-ai`






