# 🌿 ZeroGap AI: Intelligent Food Waste Forecasting

**ZeroGap AI** is a decision-support tool designed for the catering and hospitality industry. It bridges the gap between "over-ordering for safety" and "under-ordering for sustainability."

## 🚀 The Problem
Caterers often face a 30-40% food wastage rate due to inaccurate guest-to-food ratios and environmental factors. Traditional ML models often fail at "extreme surplus" scenarios because they lack real-world catering logic.

## 💡 Our Solution (The Hybrid Approach)
ZeroGap AI doesn't just rely on a Random Forest model. It uses a **Smart Guardrail System** that:
1.  **Calculates Real-Time Ratios:** Identifies when food supply exceeds human consumption limits.
2.  **Adjusts for Spoilage:** Factors in temperature (Season) and storage conditions (Room Temp vs. Refrigerated).
3.  **Predicts Actionable Metrics:** Instead of just a "Waste %", it provides the **Required Food** amount to help managers save money immediately.

## 🛠️ Tech Stack
- **Backend:** Python, Scikit-Learn (Random Forest Regressor)
- **Frontend:** Streamlit (Custom CSS for Premium UI)
- **Data:** Pandas, NumPy, StandardScaler

## 📊 Performance Testing
The model has been validated against three core scenarios:
- **Case 1 (Optimized):** 90%+ Efficiency for lean corporate events.
- **Case 2 (Standard):** ~85% Efficiency for suburban social gatherings.
- **Case 3 (High Risk):** Detects critical surplus and spoilage risks in large-scale events.



## 🚀 Quick Start: How to Run the App

If you want to run this project locally on your machine, follow these steps:

### 1. Clone the Repository
```bash
git clone

python -m venv venv
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

streamlit run app.py


```
---
*Developed to make Zero-Waste catering a reality.*
