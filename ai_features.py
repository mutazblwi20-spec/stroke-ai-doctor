import matplotlib.pyplot as plt
import random

# =============================
# Risk Level Analyzer
# =============================
def risk_level(prob):

    if prob < 0.25:
        return "🟢 Low Risk", "green"

    elif prob < 0.50:
        return "🟡 Moderate Risk", "orange"

    elif prob < 0.75:
        return "🔴 High Risk", "red"

    else:
        return "🚨 Critical Risk", "darkred"


# =============================
# Smart Medical Advice (Dynamic)
# =============================
def smart_advice(prob, bmi, glucose):

    low = [
        "Maintain regular exercise.",
        "Keep balanced nutrition.",
        "Continue healthy lifestyle."
    ]

    medium = [
        "Monitor blood pressure weekly.",
        "Reduce sugar intake.",
        "Increase physical activity."
    ]

    high = [
        "Consult a doctor soon.",
        "Control stress and cholesterol.",
        "Monitor glucose daily."
    ]

    critical = [
        "Immediate medical consultation required.",
        "Visit emergency care if symptoms appear.",
        "High stroke risk — medical supervision needed."
    ]

    if prob < 0.25:
        return random.choice(low)
    elif prob < 0.50:
        return random.choice(medium)
    elif prob < 0.75:
        return random.choice(high)
    else:
        return random.choice(critical)


# =============================
# AI Confidence Score
# =============================
def confidence_score(prob):
    return round(abs(prob - 0.5) * 200, 2)


# =============================
# Health Indicators
# =============================
def health_indicators(age, bmi, glucose):

    indicators = []

    if age > 60:
        indicators.append(("Age Risk", "High"))

    if bmi > 30:
        indicators.append(("BMI", "Obese"))

    if glucose > 140:
        indicators.append(("Glucose", "High"))

    if not indicators:
        indicators.append(("Health Status", "Normal"))

    return indicators


# =============================
# Gauge Chart
# =============================
def draw_gauge(risk):

    fig, ax = plt.subplots()

    ax.pie(
        [risk, 100-risk],
        startangle=90,
        wedgeprops=dict(width=0.35)
    )

    ax.text(
        0, 0,
        f"{risk}%",
        ha='center',
        va='center',
        fontsize=22,
        fontweight='bold'
    )

    return fig
