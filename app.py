import streamlit as st

# --- Page setup
st.set_page_config(page_title="Physiotherapist BMI App", page_icon="🏥", layout="centered")

# --- Header
st.title("🏥 Physiotherapist BMI Calculator")
st.caption("A simple web app to calculate BMI and provide basic health advice.")

# --- User input
st.header("Enter your details")
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=120, value=25)
height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=65.0)

# --- BMI calculation
if st.button("Calculate BMI"):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 2)

    # --- BMI categorization
    if bmi < 18.5:
        category = "Underweight"
        advice = "You may need to gain some weight. Consult your physiotherapist for strength-building exercises."
    elif bmi < 25:
        category = "Normal weight"
        advice = "Great! Maintain your healthy lifestyle and regular exercises."
    elif bmi < 30:
        category = "Overweight"
        advice = "You might benefit from regular physical activity and a balanced diet."
    else:
        category = "Obesity"
        advice = "Consider consulting your physiotherapist for a personalized workout plan."

    # --- Display results
    st.success(f"Your BMI is **{bmi}**")
    st.info(f"Category: **{category}**")
    st.write(advice)

    # --- Optional: Show some quick suggestions
    st.subheader("💡 Physiotherapist Recommendations")
    if category == "Underweight":
        st.write("- Include protein-rich foods in your diet.")
        st.write("- Do strength training 3x a week.")
    elif category == "Normal weight":
        st.write("- Keep up regular stretching and posture exercises.")
        st.write("- Stay hydrated and maintain good sleep.")
    elif category == "Overweight":
        st.write("- Try brisk walking or swimming for 30 mins/day.")
        st.write("- Reduce processed foods and sugar intake.")
    else:
        st.write("- Consult a physiotherapist for a tailored low-impact workout plan.")
        st.write("- Start slow — focus on consistency over intensity.")

# --- Footer
st.divider()
st.caption("Developed with ❤️ using Streamlit | Physiotherapy Health Tool")
