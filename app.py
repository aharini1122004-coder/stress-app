import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("stress_model.pkl")

st.title("💳 Financial Stress Detection App")

st.write("Upload your credit card transaction data")

# Upload file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # Required features (MUST match training)
    features = [
        'Avg_Utilization_Ratio',
        'Total_Trans_Amt',
        'Credit_Limit',
        'Total_Revolving_Bal',
        'Total_Trans_Ct'
    ]

    # Check if columns exist
    if all(col in df.columns for col in features):

        X = df[features]

        # Predict
        predictions = model.predict(X)

        # Convert numbers to labels
        stress_map = {
            0: "Low Stress",
            1: "Medium Stress",
            2: "High Stress"
        }

        df['Predicted_Stress'] = [stress_map[p] for p in predictions]

        st.subheader("📊 Prediction Results")
        st.dataframe(df)

    else:
        st.error("❌ Required columns missing in uploaded file")

else:
    st.info("Please upload a CSV file to continue")
