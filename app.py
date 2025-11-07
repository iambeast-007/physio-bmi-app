import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import time
import json
import os
import hashlib

# --- Page setup
st.set_page_config(page_title="Physio BMI App", page_icon="🏥", layout="centered")

# --- Helpers
USERS_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """Return SHA256 hash of a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify hashed password"""
    return hash_password(password) == hashed

def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# --- Session Initialization
for key in ["logged_in", "username", "profile_photo", "show_uploader", "page"]:
    if key not in st.session_state:
        if key == "logged_in":
            st.session_state[key] = False
        elif key == "page":
            st.session_state[key] = "login"  # Default page
        elif key == "show_uploader":
            st.session_state[key] = False
        else:
            st.session_state[key] = None

# --- Authentication Flow ---
users = load_users()

# --- Login Page
if st.session_state.page == "login" and not st.session_state.logged_in:
    st.sidebar.header("🔐 Login to Physio BMI App")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username in users and verify_password(password, users[username]["password"]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back, {username}! 🎉")
            time.sleep(0.5)
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password.")

    if st.sidebar.button("New user? Register here ➕"):
        st.session_state.page = "register"
        st.rerun()

# --- Registration Page
elif st.session_state.page == "register" and not st.session_state.logged_in:
    st.sidebar.header("📝 Register New Account")
    new_username = st.sidebar.text_input("Choose a username")
    new_password = st.sidebar.text_input("Choose a password", type="password")
    confirm_password = st.sidebar.text_input("Confirm password", type="password")

    if st.sidebar.button("Register"):
        if new_username in users:
            st.sidebar.warning("Username already exists! Please choose another.")
        elif new_password != confirm_password:
            st.sidebar.error("Passwords do not match.")
        elif len(new_username) < 3 or len(new_password) < 4:
            st.sidebar.error("Username or password too short.")
        else:
            users[new_username] = {"password": hash_password(new_password)}
            save_users(users)
            st.sidebar.success("✅ Registration successful! Please login.")
            st.session_state.page = "login"
            st.rerun()

    if st.sidebar.button("🔙 Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# --- Main App (after login)
elif st.session_state.logged_in:
    # --- Sidebar Profile
    if st.session_state.profile_photo:
        image = st.session_state.profile_photo
    else:
        image = Image.new("RGB", (180, 180), (220, 220, 220))

    img_str = image_to_base64(image)
    col1, col2 = st.sidebar.columns([3, 1], vertical_alignment="center")

    with col1:
        st.markdown(
            f"""
            <style>
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

    if st.session_state.show_uploader:
        uploaded_file = st.sidebar.file_uploader("Upload new profile photo", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB").resize((180, 180))
            st.session_state.profile_photo = image
            st.session_state.show_uploader = False
            st.success("✅ Profile photo updated!")
            time.sleep(0.4)
            st.rerun()

    st.sidebar.markdown(f"### 👋 Welcome, **{st.session_state.username}!**")

    if st.sidebar.button("🚪 Logout"):
        for k in ["logged_in", "username", "profile_photo", "show_uploader"]:
            st.session_state[k] = False if k == "logged_in" else None
        st.session_state.page = "login"
        st.rerun()

    # --- Main BMI Page
    st.title("🏥 BMI Calculator")
    st.caption("A simple web app to calculate BMI and provide basic health advice.")

    st.header("Enter your details")
    name = st.text_input("Name", value=st.session_state.username or "")
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=65.0)

    if st.button("Calculate BMI"):
        height_m = height_cm / 100
        bmi = round(weight_kg / (height_m ** 2), 2)

        # --- BMI Logic with Icons
        if bmi < 18.5:
            category, advice, icon = "Underweight", "You may need to gain some weight. Consult your physiotherapist.", "🦴"
        elif bmi < 25:
            category, advice, icon = "Normal weight", "Great! Maintain your healthy lifestyle.", "🧘"
        elif bmi < 30:
            category, advice, icon = "Overweight", "You might benefit from regular physical activity.", "🍔"
        else:
            category, advice, icon = "Obesity", "Consult your physiotherapist for a personalized workout plan.", "🐻‍❄️"

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

    st.divider()
    st.caption("Developed with ❤️ using Streamlit | Physiotherapy Health Tool")
