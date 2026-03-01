# ai_features.py

import matplotlib.pyplot as plt

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

def health_indicators(age, bmi, glucose):

    indicators = []

    # AGE
    if age > 60:
        indicators.append(("Age", "High Risk"))
    else:
        indicators.append(("Age", "Normal"))

    # BMI
    if bmi < 25:
        indicators.append(("BMI", "Normal"))
    elif bmi < 30:
        indicators.append(("BMI", "Overweight"))
    else:
        indicators.append(("BMI", "Obese"))

    # GLUCOSE
    if glucose > 140:
        indicators.append(("Glucose", "High"))
    else:
        indicators.append(("Glucose", "Normal"))

    return indicators


# =====================================
# SMART ADVICE
# =====================================

def smart_advice(prob, bmi, glucose):

    if prob < 0.3:
        return "Maintain a healthy lifestyle."
    elif prob < 0.6:
        return "Improve diet and increase physical activity."
    else:
        return "Consult a doctor immediately and monitor health."


# =====================================
# CONFIDENCE SCORE
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
