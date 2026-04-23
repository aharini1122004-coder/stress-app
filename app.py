st.subheader("📊 Live Financial Indicators")

if credit > 0:
    spending_ratio = trans_amt / credit
else:
    spending_ratio = 0

# Show ratio
st.write(f"💰 Spending Ratio: {round(spending_ratio,2)}")

# Color indicator
if spending_ratio < 0.3:
    st.success("🟢 Safe spending level")
elif spending_ratio < 0.6:
    st.warning("🟡 Moderate spending")
else:
    st.error("🔴 High spending risk")

# Suggestions
st.subheader("💡 Suggestions")

if spending_ratio > 0.5:
    st.warning("Reduce your spending compared to credit limit")

if balance > 1000:
    st.warning("Try to reduce your revolving balance")

if util > 0.4:
    st.warning("Keep credit utilization below 30%")

if spending_ratio < 0.3 and balance < 500 and util < 0.3:
    st.success("Great! You are maintaining low financial stress 🎉")
           
