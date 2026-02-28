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
# SIDEBAR INPUTS (>6 inputs)
# =============================
st.sidebar.header("Patient Data")

age = st.sidebar.slider("Age", 1, 100, 40)
hypertension = st.sidebar.selectbox("Hypertension", [0,1])
heart_disease = st.sidebar.selectbox("Heart Disease", [0,1])
glucose = st.sidebar.slider("Glucose Level", 50.0, 300.0, 100.0)
bmi = st.sidebar.slider("BMI", 10.0, 50.0, 25.0)
smoking = st.sidebar.selectbox("Smoking Status", [0,1])

# =============================
# PREDICTION BUTTON
# =============================
if st.sidebar.button("🔍 Predict"):

    data = np.array([[age,
                      hypertension,
                      heart_disease,
                      glucose,
                      bmi,
                      smoking]])

    prob = model.predict_proba(data)[0][1]
    risk_percent = round(prob * 100, 2)

    level, color = risk_level(prob)
    advice = smart_advice(prob, bmi, glucose)
    confidence = confidence_score(prob)
    indicators = health_indicators(age, bmi, glucose)

    col1, col2 = st.columns(2)

    # RESULT
    with col1:
        st.subheader("Prediction Result")
        st.markdown(f"## {level}")
        st.metric("Stroke Risk", f"{risk_percent}%")
        st.metric("AI Confidence", f"{confidence}%")

    # GAUGE
    with col2:
        fig = draw_gauge(risk_percent)
        st.pyplot(fig)

    # HEALTH INDICATORS
    st.subheader("Health Indicators")

    for name, status in indicators:
        st.write(f"**{name}:** {status}")

    # ADVICE
    st.subheader("Medical Advice")
    st.info(advice)

    # =============================
    # SAVE PATIENT RECORD
    # =============================
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
# SHOW HISTORY
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
