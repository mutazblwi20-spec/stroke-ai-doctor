import streamlit as st
import pickle
import numpy as np
import json
from datetime import datetime

from ai_features import (
    risk_level,
    smart_advice,
    confidence_score,
    health_indicators,
    draw_gauge
)

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="AI Stroke Doctor",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Stroke Prediction System")
st.markdown("### Intelligent Medical Decision Support")

# =============================
# LOAD MODEL
# =============================
model = pickle.load(open("stroke_model.pkl", "rb"))

# =============================
# SIDEBAR INPUTS
# =============================
st.sidebar.header("Patient Information")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.slider("Age", 1, 100, 40)
hypertension = st.sidebar.selectbox("Hypertension", ["No", "Yes"])
heart_disease = st.sidebar.selectbox("Heart Disease", ["No", "Yes"])
ever_married = st.sidebar.selectbox("Ever Married", ["No", "Yes"])

work_type = st.sidebar.selectbox(
    "Work Type",
    ["Private", "Self-employed", "Govt_job", "children", "Never_worked"]
)

residence = st.sidebar.selectbox(
    "Residence Type",
    ["Urban", "Rural"]
)

glucose = st.sidebar.slider("Average Glucose Level", 50.0, 300.0, 100.0)
bmi = st.sidebar.slider("BMI", 10.0, 50.0, 25.0)

smoking = st.sidebar.selectbox(
    "Smoking Status",
    ["never smoked", "formerly smoked", "smokes"]
)

# =============================
# ENCODING (IMPORTANT)
# =============================
gender = 1 if gender == "Male" else 0
hypertension = 1 if hypertension == "Yes" else 0
heart_disease = 1 if heart_disease == "Yes" else 0
ever_married = 1 if ever_married == "Yes" else 0
residence = 1 if residence == "Urban" else 0

work_map = {
    "Private":0,
    "Self-employed":1,
    "Govt_job":2,
    "children":3,
    "Never_worked":4
}

smoke_map = {
    "never smoked":0,
    "formerly smoked":1,
    "smokes":2
}

work_type = work_map[work_type]
smoking = smoke_map[smoking]

# =============================
# PREDICTION
# =============================
if st.sidebar.button("🔍 Predict"):

    data = np.array([[
        gender,
        age,
        hypertension,
        heart_disease,
        ever_married,
        work_type,
        residence,
        glucose,
        bmi,
        smoking
    ]])

    prob = model.predict_proba(data)[0][1]
    risk_percent = round(prob * 100, 2)

    level, color = risk_level(prob)
    advice = smart_advice(prob, bmi, glucose)
    confidence = confidence_score(prob)
    indicators = health_indicators(age, bmi, glucose)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Prediction Result")
        st.markdown(f"## {level}")
        st.metric("Stroke Risk", f"{risk_percent}%")
        st.metric("AI Confidence", f"{confidence}%")

    with col2:
        fig = draw_gauge(risk_percent)
        st.pyplot(fig)

    st.subheader("Health Indicators")

    for name, status in indicators:
        st.write(f"**{name}:** {status}")

    st.subheader("Medical Advice")
    st.info(advice)

    # SAVE HISTORY
    record = {
        "date": str(datetime.now()),
        "risk": risk_percent
    }

    try:
        with open("patients.json","r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(record)

    with open("patients.json","w") as f:
        json.dump(history,f,indent=4)

    st.success("Patient saved successfully ✅")

# =============================
# HISTORY
# =============================
st.divider()
st.subheader("📋 Patient History")

try:
    with open("patients.json","r") as f:
        history = json.load(f)

    for h in reversed(history[-5:]):
        st.write(f"{h['date']} — Risk: {h['risk']}%")

except:
    st.write("No history yet.")
