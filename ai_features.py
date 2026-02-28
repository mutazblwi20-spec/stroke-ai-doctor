import numpy as np
import matplotlib.pyplot as plt

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
# Smart Medical Advice
# =============================
def smart_advice(prob, bmi, glucose):

    if prob < 0.25:
        return "Maintain healthy lifestyle and regular exercise."

    elif prob < 0.50:
        return "Monitor blood pressure and maintain balanced diet."

    elif prob < 0.75:
        return "Medical consultation recommended. Reduce stress and monitor glucose."

    else:
        return "Immediate medical consultation required."


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

    if len(indicators) == 0:
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


# =============================
# Trend Chart
# =============================
def trend_chart(history):

    risks = [h["risk"] for h in history]

    fig, ax = plt.subplots()

    ax.plot(risks, marker="o")
    ax.set_title("Patient Risk Trend")
    ax.set_ylabel("Risk %")
    ax.set_xlabel("Visits")

    return fig
