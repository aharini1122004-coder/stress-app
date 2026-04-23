import streamlit as st
import joblib
import numpy as np
import os

model_path = os.path.join(os.path.dirname(__file__), "stress_model.pkl")
model = joblib.load(model_path)

st.title("💳 Customer Stress Prediction")

util = st.number_input("Avg Utilization Ratio")
trans_amt = st.number_input("Total Transaction Amount")
credit = st.number_input("Credit Limit")
balance = st.number_input("Total Revolving Balance")
trans_ct = st.number_input("Total Transaction Count")

if st.button("Predict"):
    data = np.array([[util, trans_amt, credit, balance, trans_ct]])
    prediction = model.predict(data)[0]

    labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}

    st.success(f"Predicted Stress Level: {labels[prediction]}")
