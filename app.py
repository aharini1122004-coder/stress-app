import streamlit as st
import joblib
import numpy as np
import os

# ------------------ LOAD MODEL ------------------
model_path = os.path.join(os.path.dirname(__file__), "stress_model.pkl")
model = joblib.load(model_path)

# ------------------ PAGE SETTINGS ------------------
st.set_page_config(page_title="Stress Predictor", layout="centered")

st.title("💳 Customer Stress Prediction")
st.markdown("### ML + Rule-Based Financial Analysis")

st.divider()

# ------------------ INPUTS ------------------
col1, col2 = st.columns(2)

with col1:
    util = st.number_input("Avg Utilization Ratio (0–1)", min_value=0.0, max_value=1.0)
    trans_amt = st.number_input("Total Transaction Amount (₹)", min_value=0.0)
    credit = st.number_input("Credit Limit (₹)", min_value=1.0)

with col2:
    balance = st.number_input("Total Revolving Balance (₹)", min_value=0.0)
    trans_ct = st.number_input("Total Transaction Count", min_value=0)

st.divider()

# ------------------ LIVE ANALYSIS ------------------
st.subheader("📊 Live Financial Indicators")

spending_ratio = trans_amt / credit if credit > 0 else 0
st.write(f"💰 Spending Ratio: {round(spending_ratio, 2)}")

if spending_ratio < 0.3:
    st.success("🟢 Safe spending level")
elif spending_ratio < 0.6:
    st.warning("🟡 Moderate spending")
else:
    st.error("🔴 High spending risk")

# ------------------ RULE-BASED FUNCTION ------------------
def rule_based(util, trans_amt, credit, balance):
    score = 0
    spending_ratio = trans_amt / credit

    if util > 0.7:
        score += 2
    elif util > 0.4:
        score += 1

    if spending_ratio > 0.5:
        score += 2
    elif spending_ratio > 0.3:
        score += 1

    if balance > 2000:
        score += 2
    elif balance > 1000:
        score += 1

    if score >= 4:
        return "High Stress", score
    elif score >= 2:
        return "Medium Stress", score
    else:
        return "Low Stress", score

# ------------------ PREDICTION ------------------
if st.button("🔍 Predict Stress Level"):

    data = np.array([[util, trans_amt, credit, balance, trans_ct]])
    ml_pred = model.predict(data)[0]

    labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}
    ml_result = labels[ml_pred]

    rule_result, score = rule_based(util, trans_amt, credit, balance)

    st.divider()
    st.subheader("📊 Results")

    col1, col2 = st.columns(2)

    # ML Result
    with col1:
        st.markdown("### 🤖 ML Prediction")
        if ml_result == "Low Stress":
            st.success(ml_result)
        elif ml_result == "Medium Stress":
            st.warning(ml_result)
        else:
            st.error(ml_result)

    # Rule Result
    with col2:
        st.markdown("### 📏 Rule-Based")
        if rule_result == "Low Stress":
            st.success(rule_result)
        elif rule_result == "Medium Stress":
            st.warning(rule_result)
        else:
            st.error(rule_result)

    # ------------------ EXPLANATION ------------------
    st.divider()
    st.subheader("🧠 Explanation")

    st.write(f"• Spending Ratio: {round(spending_ratio, 2)}")
    st.write(f"• Rule Score: {score}")

    if spending_ratio > 0.3:
        st.write("⚠️ High spending compared to credit limit")
    if balance > 1000:
        st.write("⚠️ High revolving balance")
    if util > 0.4:
        st.write("⚠️ High credit utilization")

    if spending_ratio < 0.3 and balance < 500 and util < 0.3:
        st.success("✅ Customer is financially stable")

    st.caption("ML prediction is based on trained data patterns and may differ from rule-based logic.")
