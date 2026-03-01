# ai_features.py

import matplotlib.pyplot as plt

# =====================================
# 🌐 TRANSLATIONS (AI TEXTS)
# =====================================

AI_TEXT = {

    "English": {
        "age_low": "Age Risk: Low",
        "age_high": "Age Risk: High",

        "bmi_normal": "BMI: Normal",
        "bmi_over": "BMI: Overweight",
        "bmi_obese": "BMI: Obese",

        "glucose_normal": "Glucose: Normal",
        "glucose_high": "Glucose: High",

        "advice_low": "Maintain a healthy lifestyle.",
        "advice_mid": "Improve diet and increase physical activity.",
        "advice_high": "Consult a doctor immediately and monitor health."
    },

    "العربية": {
        "age_low": "خطر العمر: منخفض",
        "age_high": "خطر العمر: مرتفع",

        "bmi_normal": "مؤشر الكتلة: طبيعي",
        "bmi_over": "مؤشر الكتلة: زيادة وزن",
        "bmi_obese": "مؤشر الكتلة: سمنة",

        "glucose_normal": "السكر: طبيعي",
        "glucose_high": "السكر: مرتفع",

        "advice_low": "حافظ على نمط حياة صحي.",
        "advice_mid": "حسّن نظامك الغذائي وزد النشاط البدني.",
        "advice_high": "راجع الطبيب فوراً وراقب حالتك الصحية."
    }
}


def T(lang, key):
    return AI_TEXT[lang][key]

# =====================================
# RISK LEVEL
# =====================================
def risk_level(prob):
    if prob < 0.3:
        return "Low Risk", "green"
    elif prob < 0.6:
        return "Medium Risk", "orange"
    else:
        return "High Risk", "red"

# =====================================
# HEALTH INDICATORS
# =====================================
def health_indicators(age, bmi, glucose, language):

    indicators = []

    # AGE
    if age > 60:
        indicators.append(("Age", T(language, "age_high")))
    else:
        indicators.append(("Age", T(language, "age_low")))

    # BMI
    if bmi < 25:
        indicators.append(("BMI", T(language, "bmi_normal")))
    elif bmi < 30:
        indicators.append(("BMI", T(language, "bmi_over")))
    else:
        indicators.append(("BMI", T(language, "bmi_obese")))

    # GLUCOSE
    if glucose > 140:
        indicators.append(("Glucose", T(language, "glucose_high")))
    else:
        indicators.append(("Glucose", T(language, "glucose_normal")))

    return indicators

# =====================================
# SMART ADVICE
# =====================================
def smart_advice(prob, bmi, glucose, language):

    if prob < 0.3:
        return T(language, "advice_low")
    elif prob < 0.6:
        return T(language, "advice_mid")
    else:
        return T(language, "advice_high")

# =====================================
# CONFIDENCE
# =====================================
def confidence_score(prob):
    return round(70 + prob * 30, 2)

# =====================================
# GAUGE CHART
# =====================================
def draw_gauge(percent):

    fig, ax = plt.subplots()

    ax.pie(
        [percent, 100 - percent],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.3}
    )

    ax.text(0, 0, f"{percent}%", ha="center", va="center", fontsize=20)
    ax.axis("equal")

    return fig
