import streamlit as st
import pickle
import numpy as np
import json
import os
from datetime import datetime

from ai_features import (
    risk_level,
    smart_advice,
    confidence_score,
    health_indicators,
    draw_gauge
)

# ====================================
# PAGE CONFIG
# ====================================
st.set_page_config(
    page_title="AI Stroke Doctor",
    page_icon="🧠",
    layout="wide"
)

# ====================================
# 🌐 LANGUAGE SYSTEM
# ====================================
language = st.sidebar.selectbox(
    "🌐 Language / اللغة",
    ["English", "العربية"]
)

def t(en, ar):
    return ar if language == "العربية" else en

# ====================================
# 🎨 MEDICAL UI DESIGN
# ====================================
st.markdown("""
<style>

.stApp {
    background-color:#f4f8fb;
}

h1 {
    text-align:center;
    color:#0b5394;
}

section[data-testid="stSidebar"] {
    background-color:#eaf3fb;
}

.stButton>button {
    background-color:#0b5394;
    color:white;
    border-radius:10px;
    height:3em;
    width:100%;
    font-size:16px;
}

.stMetric {
    background-color:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ====================================
# TITLE
# ====================================
st.title(t(
    "🧠 AI Stroke Prediction System",
    "🧠 نظام التنبؤ بالجلطات الدماغية"
))

st.markdown(t(
    "### Intelligent Medical Decision Support",
    "### نظام دعم القرار الطبي الذكي"
))

# ====================================
# LOAD MODEL
# ====================================
@st.cache_resource
def load_model():
    if not os.path.exists("stroke_model.pkl"):
        st.error("❌ stroke_model.pkl not found")
        st.stop()

    with open("stroke_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()
st.success(t("✅ Model Loaded Successfully",
             "✅ تم تحميل النموذج بنجاح"))

# ====================================
# SIDEBAR INPUTS
# ====================================
st.sidebar.header(t("👤 Patient Information", "👤 بيانات المريض"))

patient_name = st.sidebar.text_input(
    t("Patient Name", "اسم المريض")
)

gender = st.sidebar.selectbox(
    t("Gender", "الجنس"),
    ["Male", "Female"]
)

age = st.sidebar.slider(
    t("Age", "العمر"), 1, 100, 40
)

hypertension = st.sidebar.selectbox(
    t("Hypertension", "ضغط الدم"),
    ["No", "Yes"]
)

heart_disease = st.sidebar.selectbox(
    t("Heart Disease", "أمراض القلب"),
    ["No", "Yes"]
)

ever_married = st.sidebar.selectbox(
    t("Ever Married", "متزوج سابقاً"),
    ["No", "Yes"]
)

work_type = st.sidebar.selectbox(
    t("Work Type", "نوع العمل"),
    ["Private", "Self-employed", "Govt_job", "children", "Never_worked"]
)

residence = st.sidebar.selectbox(
    t("Residence Type", "مكان السكن"),
    ["Urban", "Rural"]
)

glucose = st.sidebar.slider(
    t("Average Glucose Level", "مستوى السكر"),
    50.0, 300.0, 100.0
)

bmi = st.sidebar.slider(
    "BMI", 10.0, 50.0, 25.0
)

smoking = st.sidebar.selectbox(
    t("Smoking Status", "حالة التدخين"),
    ["never smoked", "formerly smoked", "smokes"]
)

# ====================================
# ENCODING
# ====================================
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

# ====================================
# PREDICTION
# ====================================
if st.sidebar.button(t("🔍 Predict", "🔍 توقع")):

    if patient_name.strip() == "":
        st.warning(t("⚠️ Please enter patient name",
                     "⚠️ الرجاء إدخال اسم المريض"))
        st.stop()

    data = np.array([[gender, age, hypertension,
                      heart_disease, ever_married,
                      work_type, residence,
                      glucose, bmi, smoking]])

    prob = model.predict_proba(data)[0][1]
    risk_percent = round(prob * 100, 2)

    # DIAGNOSIS
    if prob >= 0.5:
        diagnosis = t(
            "⚠️ Stroke Detected",
            "⚠️ مصاب بجلطة محتملة"
        )
        color = "red"
    else:
        diagnosis = t(
            "✅ No Stroke",
            "✅ غير مصاب"
        )
        color = "green"

    advice = smart_advice(prob, bmi, glucose)
    confidence = confidence_score(prob)
    indicators = health_indicators(age, bmi, glucose)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("Prediction Result", "نتيجة التشخيص"))
        st.markdown(f"## :{color}[{diagnosis}]")
        st.metric(t("Stroke Risk","نسبة الخطر"),
                  f"{risk_percent}%")
        st.metric(t("AI Confidence","ثقة النموذج"),
                  f"{confidence}%")

    with col2:
        st.pyplot(draw_gauge(risk_percent))

    st.subheader(t("🩺 Health Indicators","🩺 مؤشرات الصحة"))
    for name, status in indicators:
        st.write(f"**{name}:** {status}")

    st.subheader(t("💡 Medical Advice","💡 نصائح طبية"))
    st.info(advice)

    # SAVE HISTORY
    record = {
        "name": patient_name,
        "date": str(datetime.now()),
        "risk": risk_percent,
        "diagnosis": diagnosis
    }

    try:
        history = json.load(open("patients.json"))
    except:
        history = []

    history.append(record)
    json.dump(history, open("patients.json","w"), indent=4)

    st.success(t(
        "✅ Patient saved successfully",
        "✅ تم حفظ المريض بنجاح"
    ))

# ====================================
# HISTORY
# ====================================
st.divider()
st.subheader(t("📋 Patient History","📋 سجل المرضى"))

try:
    history = json.load(open("patients.json"))

    for h in reversed(history[-5:]):
        st.write(
            f"👤 **{h['name']}** | {h['date']} | "
            f"{t('Risk','الخطر')}: {h['risk']}% | {h['diagnosis']}"
        )
except:
    st.write(t("No history yet.","لا يوجد سجل بعد"))
