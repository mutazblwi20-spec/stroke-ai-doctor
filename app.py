import streamlit as st
import pickle
import numpy as np
import json
import os
from datetime import datetime

from ai_features import (
    smart_advice,
    confidence_score,
    health_indicators,
    draw_gauge,
    risk_level
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Stroke Doctor",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# MEDICAL UI STYLE
# =====================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(120deg,#f4f8fb,#ffffff);
}

h1 {
    text-align:center;
    color:#0b5394;
}

section[data-testid="stSidebar"] {
    background:#eaf3fb;
}

.stButton>button {
    background:#0b5394;
    color:white;
    border-radius:12px;
    height:3em;
    width:100%;
    font-size:16px;
}

.metric-card{
    padding:15px;
    border-radius:12px;
    background:white;
    box-shadow:0px 4px 15px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("🧠 AI Stroke Prediction System")
st.markdown("### Intelligent Medical Decision Support")

# =====================================================
# LOAD MODEL (SAFE + CACHED)
# =====================================================

@st.cache_resource
def load_model():

    if not os.path.exists("stroke_model.pkl"):
        st.error("❌ stroke_model.pkl not found in repository")
        st.stop()

    try:
        with open("stroke_model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error("❌ Model loading failed")
        st.code(str(e))
        st.stop()

model = load_model()

# =====================================================
# SIDEBAR INPUTS
# =====================================================

st.sidebar.header("👤 Patient Information")

patient_name = st.sidebar.text_input("Patient Name")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.slider("Age", 1, 100, 40)

hypertension = st.sidebar.selectbox("Hypertension", ["No", "Yes"])
heart_disease = st.sidebar.selectbox("Heart Disease", ["No", "Yes"])
ever_married = st.sidebar.selectbox("Ever Married", ["No", "Yes"])

work_type = st.sidebar.selectbox(
    "Work Type",
    ["Private", "Self-employed", "Govt_job", "children", "Never_worked"]
)

residence = st.sidebar.selectbox("Residence Type", ["Urban", "Rural"])

glucose = st.sidebar.slider("Average Glucose Level", 50.0, 300.0, 100.0)
bmi = st.sidebar.slider("BMI", 10.0, 50.0, 25.0)

smoking = st.sidebar.selectbox(
    "Smoking Status",
    ["never smoked", "formerly smoked", "smokes"]
)

# =====================================================
# ENCODING (MATCH TRAINING DATA)
# =====================================================

gender = 1 if gender == "Male" else 0
hypertension = 1 if hypertension == "Yes" else 0
heart_disease = 1 if heart_disease == "Yes" else 0
ever_married = 1 if ever_married == "Yes" else 0
residence = 1 if residence == "Urban" else 0

work_map = {
    "Private": 0,
    "Self-employed": 1,
    "Govt_job": 2,
    "children": 3,
    "Never_worked": 4
}

smoke_map = {
    "never smoked": 0,
    "formerly smoked": 1,
    "smokes": 2
}

work_type = work_map[work_type]
smoking = smoke_map[smoking]

# =====================================================
# PREDICTION
# =====================================================

if st.sidebar.button("🔍 Predict"):

    if patient_name.strip() == "":
        st.warning("⚠️ Please enter patient name")
        st.stop()

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

    # Prevent feature mismatch crash
    if hasattr(model, "n_features_in_"):
        if data.shape[1] != model.n_features_in_:
            st.error(
                f"Model expects {model.n_features_in_} features "
                f"but received {data.shape[1]}"
            )
            st.stop()

    prob = model.predict_proba(data)[0][1]
    risk_percent = round(prob * 100, 2)

    # ================= Diagnosis =================

    if prob >= 0.35:   # 👈 improved threshold
        diagnosis = "⚠️ Stroke Risk Detected"
        color = "red"
    else:
        diagnosis = "✅ No Stroke Detected"
        color = "green"

    level, _ = risk_level(prob)
    confidence = confidence_score(prob)
    indicators = health_indicators(age, bmi, glucose)
    advice = smart_advice(prob, bmi, glucose)

    col1, col2 = st.columns(2)

    # RESULT
    with col1:
        st.subheader("Prediction Result")
        st.markdown(f"## :{color}[{diagnosis}]")
        st.metric("Stroke Risk", f"{risk_percent}%")
        st.metric("AI Confidence", f"{confidence}%")

    # GAUGE
    with col2:
        st.pyplot(draw_gauge(risk_percent))

    # HEALTH INDICATORS
    st.subheader("🩺 Health Indicators")

    for name, status in indicators:
        st.write(f"**{name}:** {status}")

    # ADVICE
    st.subheader("💡 Medical Advice")
    st.info(advice)

    # ================= SAVE HISTORY =================

    record = {
        "name": patient_name,
        "date": str(datetime.now()),
        "risk": risk_percent,
        "diagnosis": diagnosis
    }

    try:
        with open("patients.json", "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(record)

    with open("patients.json", "w") as f:
        json.dump(history, f, indent=4)

    st.success("✅ Patient saved successfully")

# =====================================================
# HISTORY
# =====================================================

st.divider()
st.subheader("📋 Patient History")

try:
    with open("patients.json", "r") as f:
        history = json.load(f)

    for h in reversed(history[-5:]):
        st.write(
            f"👤 {h['name']} | {h['date']} | "
            f"Risk: {h['risk']}% | {h['diagnosis']}"
        )
except:
    st.write("No history yet.")
