# ai_features.py

import matplotlib.pyplot as plt

# =====================================
# RISK LEVEL CLASSIFICATION
# =====================================
def risk_level(prob):

    if prob < 0.25:
        return "🟢 Low Risk"

    elif prob < 0.50:
        return "🟡 Moderate Risk"

    elif prob < 0.75:
        return "🔴 High Risk"

    else:
        return "🚨 Critical Risk"


# =====================================
# SMART MEDICAL ADVICE
# =====================================
def smart_advice(prob, bmi, glucose):

    if prob < 0.30:
        return "Maintain a healthy lifestyle and exercise regularly."

    elif prob < 0.60:
        return "Improve diet, monitor blood pressure, and increase activity."

    else:
        return "High stroke risk detected. Medical consultation is strongly recommended."


# =====================================
# AI CONFIDENCE SCORE
# =====================================
def confidence_score(prob):
    return round(abs(prob - 0.5) * 200, 2)


# =====================================
# RISK FACTOR ANALYSIS ⭐
# =====================================
def risk_factor_analysis(age, glucose, bmi,
                         hypertension, heart_disease, smoking):

    factors = []

    # AGE
    if age >= 65:
        factors.append(("Age", "🔴 Very High Risk"))
    elif age >= 50:
        factors.append(("Age", "🟠 Moderate Risk"))
    else:
        factors.append(("Age", "🟢 Low Risk"))

    # GLUCOSE
    if glucose >= 200:
        factors.append(("Glucose", "🚨 Critical"))
    elif glucose >= 140:
        factors.append(("Glucose", "🟠 High"))
    else:
        factors.append(("Glucose", "🟢 Normal"))

    # BMI
    if bmi >= 30:
        factors.append(("BMI", "🟠 Obese"))
    elif bmi >= 25:
        factors.append(("BMI", "🟡 Overweight"))
    else:
        factors.append(("BMI", "🟢 Normal"))

    # HYPERTENSION
    factors.append((
        "Hypertension",
        "🔴 Present" if hypertension else "🟢 Normal"
    ))

    # HEART DISEASE
    factors.append((
        "Heart Disease",
        "🔴 High Impact" if heart_disease else "🟢 None"
    ))

    # SMOKING
    if smoking == 2:
        factors.append(("Smoking", "🟠 Active Smoker"))
    elif smoking == 1:
        factors.append(("Smoking", "🟡 Former Smoker"))
    else:
        factors.append(("Smoking", "🟢 Non Smoker"))

    return factors


# =====================================
# GAUGE CHART
# =====================================
def draw_gauge(percent):

    fig, ax = plt.subplots()

    ax.pie(
        [percent, 100 - percent],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.35}
    )

    ax.text(
        0, 0,
        f"{percent}%",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold"
    )

    ax.axis("equal")

    return fig
