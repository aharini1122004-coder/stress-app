import streamlit as st
import joblib
import numpy as np
import os

# Load model
model_path = os.path.join(os.path.dirname(__file__), "stress_model.pkl")
model = joblib.load(model_path)

# Page config
st.set_page_config(page_title="Stress Predictor", layout="centered")

# Title
st.title("💳 Customer Stress Prediction")
st.markdown("### Analyze customer financial stress using ML")

st.divider()

# Layout in 2 columns
col1, col2 = st.columns(2)

with col1:
    util = st.number_input("Avg Utilization Ratio", min_value=0.0, max_value=1.0)
    trans_amt = st.number_input("Total Transaction Amount", min_value=0.0)
    credit = st.number_input("Credit Limit", min_value=1.0)

with col2:
    balance = st.number_input("Total Revolving Balance", min_value=0.0)
    trans_ct = st.number_input("Total Transaction Count", min_value=0)

st.divider()

# Predict button
if st.button("🔍 Predict Stress Level"):

    if credit == 0:
        st.error("Credit limit cannot be zero")
    else:
        data = np.array([[util, trans_amt, credit, balance, trans_ct]])
        prediction = model.predict(data)[0]

        labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}

        result = labels[prediction]

        # Color output
        if result == "Low Stress":
            st.success(f"✅ {result}")
            st.info("Customer is financially stable.")
        elif result == "Medium Stress":
            st.warning(f"⚠️ {result}")
            st.info("Customer shows moderate financial pressure.")
        else:
            st.error(f"🚨 {result}")
            st.info("Customer may be under high financial stress.")

