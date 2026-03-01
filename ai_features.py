# =====================================================
# 🧠 AI MEDICAL FEATURES
# =====================================================

import matplotlib.pyplot as plt

# =====================================================
# HEALTH INDICATORS
# =====================================================

def health_indicators(age, bmi, glucose):

    indicators = []

    # AGE
    if age >= 60:
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


# =====================================================
# SMART MEDICAL ADVICE (🔥 NEW LOGIC)
# =====================================================

def smart_advice(prob, bmi, glucose):

    # HIGH RISK
    if prob >= 0.6:
        return (
            "⚠️ High stroke risk detected.\n\n"
            "• Consult a doctor immediately.\n"
            "• Monitor blood pressure daily.\n"
            "• Reduce salt and sugar intake.\n"
            "• Stop smoking immediately.\n"
            "• Perform medical tests as soon as possible."
        )

    # MEDIUM RISK
    elif prob >= 0.25:
        return (
            "🟠 Moderate stroke risk.\n\n"
            "• Increase physical activity (30 min daily).\n"
            "• Improve diet and reduce processed food.\n"
            "• Control weight and blood sugar.\n"
            "• Regular medical checkups recommended."
        )

    # LOW RISK
    else:
        return (
            "✅ Low stroke risk.\n\n"
            "• Maintain a healthy lifestyle.\n"
            "• Exercise regularly.\n"
            "• Keep balanced nutrition.\n"
            "• Continue periodic health monitoring."
        )


# =====================================================
# CONFIDENCE SCORE
# =====================================================

def confidence_score(prob):
    return round(70 + prob * 30, 2)


# =====================================================
# GAUGE CHART
# =====================================================

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
