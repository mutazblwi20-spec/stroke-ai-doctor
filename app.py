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

# =====================================================
# 🌐 GLOBAL LANGUAGE SYSTEM (FULL PROJECT TRANSLATION)
# =====================================================

translations = {

    "English": {
        "title": "🧠 AI Stroke Prediction System",
        "subtitle": "Intelligent Medical Decision Support",

        "patient_info": "👤 Patient Information",
        "patient_name": "Patient Name",
        "gender": "Gender",
        "age": "Age",
        "hypertension": "Hypertension",
        "heart": "Heart Disease",
        "married": "Ever Married",
        "work": "Work Type",
        "residence": "Residence Type",
        "glucose": "Average Glucose Level",
        "bmi": "BMI",
        "smoking": "Smoking Status",

        "predict": "🔍 Predict",

        "result": "Prediction Result",
        "risk": "Stroke Risk",
        "confidence": "AI Confidence",
        "health": "🩺 Health Indicators",
        "advice": "💡 Medical Advice",

        "saved": "✅ Patient saved successfully",
        "history": "📋 Patient History",
        "no_history": "No history yet",

        "enter_name": "⚠️ Please enter patient name",

        "stroke": "⚠️ Stroke Detected",
        "no_stroke": "✅ No Stroke"
    },

    "العربية": {
        "title": "🧠 نظام التنبؤ بالجلطات الدماغية",
        "subtitle": "نظام دعم القرار الطبي الذكي",

        "patient_info": "👤 بيانات المريض",
        "patient_name": "اسم المريض",
        "gender": "الجنس",
        "age": "العمر",
        "hypertension": "ضغط الدم",
        "heart": "أمراض القلب",
        "married": "متزوج سابقاً",
        "work": "نوع العمل",
        "residence": "مكان السكن",
        "glucose": "مستوى السكر",
        "bmi": "مؤشر كتلة الجسم",
        "smoking": "حالة التدخين",

        "predict": "🔍 توقع",

        "result": "نتيجة التشخيص",
        "risk": "نسبة الخطر",
        "confidence": "ثقة النموذج",
        "health": "🩺 المؤشرات الصحية",
        "advice": "💡 نصائح طبية",

        "saved": "✅ تم حفظ المريض بنجاح",
        "history": "📋 سجل المرضى",
        "no_history": "لا يوجد سجل بعد",

        "enter_name": "⚠️ الرجاء إدخال اسم المريض",

        "stroke": "⚠️ مصاب بجلطة محتملة",
        "no_stroke": "✅ غير مصاب"
    }
}

# language selector
language = st.sidebar.selectbox(
    "🌐 Language / اللغة",
    ["English", "العربية"]
)

def T(key):
    return translations[language][key]

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Stroke Doctor",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# 🎨 MEDICAL UI DESIGN
# =====================================================
st.markdown("""
<style>
.stApp {background:#f4f8fb;}
h1 {text-align:center;color:#0b5394;}
section[data-testid="stSidebar"] {background:#eaf3fb;}
.stButton>button {
    background:#0b5394;
    color:white;
    border-radius:10px;
    height:3em;
    width:100%;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.title(T("title"))
st.markdown(f"### {T('subtitle')}")

# =====================================================
# LOAD MODEL
# =====================================================
@st.cache_resource
def load_model():
    if not os.path.exists("stroke_model.pkl"):
        st.error("Model missing")
        st.stop()
    return pickle.load(open("stroke_model.pkl","rb"))

model = load_model()

# =====================================================
# SIDEBAR INPUTS
# =====================================================
st.sidebar.header(T("patient_info"))

patient_name = st.sidebar.text_input(T("patient_name"))

gender = st.sidebar.selectbox(T("gender"), ["Male","Female"])
age = st.sidebar.slider(T("age"),1,100,40)

hypertension = st.sidebar.selectbox(T("hypertension"),["No","Yes"])
heart_disease = st.sidebar.selectbox(T("heart"),["No","Yes"])
ever_married = st.sidebar.selectbox(T("married"),["No","Yes"])

work_type = st.sidebar.selectbox(
    T("work"),
    ["Private","Self-employed","Govt_job","children","Never_worked"]
)

residence = st.sidebar.selectbox(
    T("residence"),
    ["Urban","Rural"]
)

glucose = st.sidebar.slider(T("glucose"),50.0,300.0,100.0)
bmi = st.sidebar.slider(T("bmi"),10.0,50.0,25.0)

smoking = st.sidebar.selectbox(
    T("smoking"),
    ["never smoked","formerly smoked","smokes"]
)

# =====================================================
# ENCODING
# =====================================================
gender = 1 if gender=="Male" else 0
hypertension = 1 if hypertension=="Yes" else 0
heart_disease = 1 if heart_disease=="Yes" else 0
ever_married = 1 if ever_married=="Yes" else 0
residence = 1 if residence=="Urban" else 0

work_map={"Private":0,"Self-employed":1,"Govt_job":2,"children":3,"Never_worked":4}
smoke_map={"never smoked":0,"formerly smoked":1,"smokes":2}

work_type=work_map[work_type]
smoking=smoke_map[smoking]

# =====================================================
# PREDICTION
# =====================================================
if st.sidebar.button(T("predict")):

    if patient_name.strip()=="":
        st.warning(T("enter_name"))
        st.stop()

    data=np.array([[gender,age,hypertension,
                    heart_disease,ever_married,
                    work_type,residence,
                    glucose,bmi,smoking]])

    prob=model.predict_proba(data)[0][1]
    risk_percent=round(prob*100,2)

    diagnosis=T("stroke") if prob>=0.5 else T("no_stroke")
    color="red" if prob>=0.5 else "green"

    advice=smart_advice(prob,bmi,glucose)
    confidence=confidence_score(prob)
    indicators=health_indicators(age,bmi,glucose)

    col1,col2=st.columns(2)

    with col1:
        st.subheader(T("result"))
        st.markdown(f"## :{color}[{diagnosis}]")
        st.metric(T("risk"),f"{risk_percent}%")
        st.metric(T("confidence"),f"{confidence}%")

    with col2:
        st.pyplot(draw_gauge(risk_percent))

    st.subheader(T("health"))
    for name,status in indicators:
        st.write(f"**{name}:** {status}")

    st.subheader(T("advice"))
    st.info(advice)

    record={
        "name":patient_name,
        "date":str(datetime.now()),
        "risk":risk_percent,
        "diagnosis":diagnosis
    }

    try:
        history=json.load(open("patients.json"))
    except:
        history=[]

    history.append(record)
    json.dump(history,open("patients.json","w"),indent=4)

    st.success(T("saved"))

# =====================================================
# HISTORY
# =====================================================
st.divider()
st.subheader(T("history"))

try:
    history=json.load(open("patients.json"))
    for h in reversed(history[-5:]):
        st.write(
            f"👤 **{h['name']}** | {h['date']} | "
            f"{T('risk')}: {h['risk']}% | {h['diagnosis']}"
        )
except:
    st.write(T("no_history"))
