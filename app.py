import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import time

# --- Page setup
st.set_page_config(page_title="BMI App", page_icon="🏥", layout="centered")

# --- Dummy credentials
USER_CREDENTIALS = {
    "Arka": "admin123",
    "testuser": "test123"
}

# --- Helpers
def login(username, password):
    return username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password

def image_to_base64(image):
    """Convert image to base64 string for embedding in HTML"""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# --- Session Initialization
for key in ["logged_in", "username", "profile_photo", "show_uploader"]:
    if key not in st.session_state:
        if key == "logged_in":
            st.session_state[key] = False
        elif key == "show_uploader":
            st.session_state[key] = False
        else:
            st.session_state[key] = None

# --- Sidebar Login Section
if not st.session_state.logged_in:
    st.sidebar.header("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password")

else:
    # --- Load or create avatar
    if st.session_state.profile_photo:
        image = st.session_state.profile_photo
    else:
        image = Image.new("RGB", (180, 180), (220, 220, 220))  # Default grey avatar (bigger now)

    img_str = image_to_base64(image)

    # --- Sidebar Profile + Functional ✏️ Button (same row)
    col1, col2 = st.sidebar.columns([3, 1], vertical_alignment="center")

    with col1:
        st.markdown(
            f"""
            <style>
            .profile-container {{
                margin-left: 5px;
            }}
            .profile-container img {{
                width: 110px;
                height: 110px;
                border-radius: 50%;
                border: 3px solid #4CAF50;
                object-fit: cover;
                box-shadow: 0 0 8px rgba(0,0,0,0.3);
            }}
            </style>
            <div class="profile-container">
                <img src="data:image/png;base64,{img_str}" alt="Profile">
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button("✏️", key="edit_icon"):
            st.session_state.show_uploader = not st.session_state.show_uploader

    # --- Upload box (only when toggled)
    if st.session_state.show_uploader:
        uploaded_file = st.sidebar.file_uploader(
            "Upload new profile photo", type=["jpg", "jpeg", "png"]
        )
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB").resize((180, 180))
            st.session_state.profile_photo = image
            st.session_state.show_uploader = False
            st.success("✅ Profile photo updated successfully!")
            time.sleep(0.4)
            st.rerun()

    # --- Welcome Note
    st.sidebar.markdown(f"### 👋 Welcome, **{st.session_state.username}!**")

    # --- Logout Button
    if st.sidebar.button("🚪 Logout"):
        for k in ["logged_in", "username", "profile_photo", "show_uploader"]:
            st.session_state[k] = False if k == "logged_in" else None if k != "show_uploader" else False
        st.rerun()

# --- Main Page ---
st.title("🏥 BMI Calculator")
st.caption("A simple web app to calculate BMI and provide basic health advice.")

if not st.session_state.logged_in:
    st.warning("🔒 Please log in from the sidebar to access the BMI calculator.")
    st.info("Try credentials:\n- Arka / admin123\n- testuser / test123")
    st.stop()

# --- BMI Form ---
st.header("Enter your details")
name = st.text_input("Name", value=st.session_state.username or "")
age = st.number_input("Age", min_value=1, max_value=120, value=25)
height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=65.0)

# --- BMI calculation
if st.button("Calculate BMI"):
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 2)

    # --- Category logic with fun icons
    if bmi < 18.5:
        category = "Underweight"
        advice = "You may need to gain some weight. Consult your physiotherapist."
        icon = "🦴"  # skinny bone
    elif bmi < 25:
        category = "Normal weight"
        advice = "Great! Maintain your healthy lifestyle and regular exercises."
        icon = "🧘"  # calm yoga
    elif bmi < 30:
        category = "Overweight"
        advice = "You might benefit from regular physical activity and a balanced diet."
        icon = "🍔"  # burger fun
    else:
        category = "Obesity"
        advice = "Consult your physiotherapist for a personalized workout plan."
        icon = "🐻‍❄️"  # heavy cartoon bear

    # --- Display result with icon and colors
    st.markdown(
        f"""
        <div style='text-align:center;'>
            <h2 style='color:#4CAF50;'>Your BMI is <b>{bmi}</b></h2>
            <h3>{icon} <b>{category}</b> {icon}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(advice)

    # --- Extra Recommendations
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



# if st.button("Calculate BMI"):
#     height_m = height_cm / 100
#     bmi = round(weight_kg / (height_m ** 2), 2)

#     if bmi < 18.5:
#         category, advice = "Underweight", "You may need to gain some weight. Consult your physiotherapist."
#     elif bmi < 25:
#         category, advice = "Normal weight", "Great! Maintain your healthy lifestyle and regular exercises."
#     elif bmi < 30:
#         category, advice = "Overweight", "You might benefit from regular physical activity and a balanced diet."
#     else:
#         category, advice = "Obesity", "Consult your physiotherapist for a personalized workout plan."

#     st.success(f"Your BMI is **{bmi}**")
#     st.info(f"Category: **{category}**")
#     st.write(advice)

st.divider()
st.caption("Developed with ❤️ using Streamlit | Physiotherapy Health Tool")
