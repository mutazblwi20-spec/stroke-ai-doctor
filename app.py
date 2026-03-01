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
    draw_gauge
)

# =====================================================
# 🌐 LANGUAGE SYSTEM
# =====================================================

translations = {

"English":{
"title":"🧠 AI Stroke Prediction System",
"subtitle":"Intelligent Medical Decision Support",
"patient_info":"👤 Patient Information",
"patient_name":"Patient Name",
"gender":"Gender",
"age":"Age",
"hypertension":"Hypertension",
"heart":"Heart Disease",
"married":"Ever Married",
"work":"Work Type",
"residence":"Residence Type",
"glucose":"Average Glucose Level",
"bmi":"BMI",
"smoking":"Smoking Status",
"predict":"🔍 Predict",
"result":"Prediction Result",
"risk":"Stroke Risk",
"confidence":"AI Confidence",
"health":"🩺 Health Indicators",
"advice":"💡 Medical Advice",
"history":"📋 Patient History",
"saved":"✅ Patient saved successfully",
"enter_name":"⚠️ Please enter patient name",
"stroke":"⚠️ Stroke Detected",
"no_stroke":"✅ No Stroke"
},

"العربية":{
"title":"🧠 نظام التنبؤ بالجلطات الدماغية",
"subtitle":"نظام دعم القرار الطبي الذكي",
"patient_info":"👤 بيانات المريض",
"patient_name":"اسم المريض",
"gender":"الجنس",
"age":"العمر",
"hypertension":"ضغط الدم",
"heart":"أمراض القلب",
"married":"متزوج سابقاً",
"work":"نوع العمل",
"residence":"مكان السكن",
"glucose":"مستوى السكر",
"bmi":"مؤشر كتلة الجسم",
"smoking":"حالة التدخين",
"predict":"🔍 توقع",
"result":"نتيجة التشخيص",
"risk":"نسبة الخطر",
"confidence":"ثقة النموذج",
"health":"🩺 المؤشرات الصحية",
"advice":"💡 نصائح طبية",
"history":"📋 سجل المرضى",
"saved":"✅ تم حفظ المريض بنجاح",
"enter_name":"⚠️ الرجاء إدخال اسم المريض",
"stroke":"⚠️ مصاب بجلطة محتملة",
"no_stroke":"✅ غير مصاب"
}
}

language = st.sidebar.selectbox("🌐 Language / اللغة",["English","العربية"])
T=lambda k: translations[language][k]

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(page_title="AI Stroke Doctor",layout="wide")

# RTL Arabic
if language=="العربية":
    st.markdown("""
    <style>
    body {direction:rtl;}
    .stMarkdown,label{text-align:right;}
    </style>
    """,unsafe_allow_html=True)

# UI STYLE
st.markdown("""
<style>
.stApp{background:#f4f8fb;}
section[data-testid="stSidebar"]{background:#eaf3fb;}
.stButton>button{
background:#0b5394;color:white;border-radius:10px;height:3em;width:100%;
}
</style>
""",unsafe_allow_html=True)

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

model=load_model()

# =====================================================
# VALUE MAP SYSTEM (🔥 FIX)
# =====================================================

def selectbox_map(label,options):
    display=list(options.keys())
    value_map=options
    choice=st.sidebar.selectbox(label,display)
    return value_map[choice]

st.sidebar.header(T("patient_info"))

patient_name=st.sidebar.text_input(T("patient_name"))

gender=selectbox_map(T("gender"),
{"Male":"Male","Female":"Female"} if language=="English"
else {"ذكر":"Male","أنثى":"Female"})

age=st.sidebar.slider(T("age"),1,100,40)

hypertension=selectbox_map(T("hypertension"),
{"No":"No","Yes":"Yes"} if language=="English"
else {"لا":"No","نعم":"Yes"})

heart_disease=selectbox_map(T("heart"),
{"No":"No","Yes":"Yes"} if language=="English"
else {"لا":"No","نعم":"Yes"})

ever_married=selectbox_map(T("married"),
{"No":"No","Yes":"Yes"} if language=="English"
else {"لا":"No","نعم":"Yes"})

work_type=selectbox_map(T("work"),
{"Private":"Private","Self-employed":"Self-employed",
"Govt_job":"Govt_job","children":"children","Never_worked":"Never_worked"}
if language=="English"
else {"قطاع خاص":"Private","عمل حر":"Self-employed",
"حكومي":"Govt_job","طفل":"children","لم يعمل":"Never_worked"})

residence=selectbox_map(T("residence"),
{"Urban":"Urban","Rural":"Rural"} if language=="English"
else {"مدينة":"Urban","ريف":"Rural"})

glucose=st.sidebar.slider(T("glucose"),50.0,300.0,100.0)
bmi=st.sidebar.slider(T("bmi"),10.0,50.0,25.0)

smoking=selectbox_map(T("smoking"),
{"never smoked":"never smoked",
"formerly smoked":"formerly smoked",
"smokes":"smokes"}
if language=="English"
else {"لا يدخن":"never smoked",
"مدخن سابق":"formerly smoked",
"مدخن":"smokes"})

# =====================================================
# ENCODING
# =====================================================

gender=1 if gender=="Male" else 0
hypertension=1 if hypertension=="Yes" else 0
heart_disease=1 if heart_disease=="Yes" else 0
ever_married=1 if ever_married=="Yes" else 0
residence=1 if residence=="Urban" else 0

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

    confidence=confidence_score(prob)
    indicators=health_indicators(age,bmi,glucose,language)
    advice=smart_advice(prob,bmi,glucose,language)

    c1,c2=st.columns(2)

    with c1:
        st.subheader(T("result"))
        st.markdown(f"## :{color}[{diagnosis}]")
        st.metric(T("risk"),f"{risk_percent}%")
        st.metric(T("confidence"),f"{confidence}%")

    with c2:
        st.pyplot(draw_gauge(risk_percent))

    st.subheader(T("health"))
    for n,s in indicators:
        st.write(f"**{n}:** {s}")

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
        st.write(f"👤 {h['name']} | {h['date']} | {h['risk']}% | {h['diagnosis']}")
except:
    st.write("—")
