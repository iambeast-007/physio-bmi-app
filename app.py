import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import base64
from io import BytesIO

# --- Custom background setup ---
import streamlit as st
import base64
from streamlit_option_menu import option_menu

# --- Page setup
st.set_page_config(page_title="Physio BMI App", page_icon="🏥", layout="centered")

# --- Helper: convert image to Base64
def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# --- Session initialization
for key in ["profile_photo", "show_uploader", "selected_page"]:
    if key not in st.session_state:
        if key == "selected_page":
            st.session_state[key] = "Home"
        elif key == "show_uploader":
            st.session_state[key] = False
        else:
            st.session_state[key] = None


def add_translucent_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <style>
        /* --- MAIN BACKGROUND SETUP --- */
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* --- FIX: Extend overlay to include Streamlit header/navbar --- */
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(255, 255, 255, 0.22);  /* slightly lighter overlay */
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            z-index: 0;
        }}

        /* --- FIX: Keep main content ABOVE overlay --- */
        [data-testid="stAppViewContainer"] > div:first-child {{
            position: relative;
            z-index: 1;
            color: #111 !important;              /* Dark text for contrast */
            text-shadow: 0 0 1px rgba(255,255,255,0.3); /* gentle glow */
        }}

        /* --- Make headings darker and sharper --- */
        h1, h2, h3, h4, h5, h6 {{
            color: #0a0a0a !important;
            font-weight: 700 !important;
            text-shadow: 0 1px 1px rgba(255,255,255,0.3);
        }}

        /* --- Improve paragraph and label text readability --- */
        p, label, span, div, .stMarkdown, .stTextInput, .stSelectbox, .stRadio, .stMetric {{
            color: #1a1a1a !important;
            font-weight: 500 !important;
        }}

        /* --- SIDEBAR FIX: Stop it from crossing top navbar --- */
        section[data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.75) !important;
            backdrop-filter: blur(6px) !important;
            -webkit-backdrop-filter: blur(6px) !important;
            margin-top: 4.5rem !important;
            height: calc(100vh - 4.5rem) !important;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
        }}

        /* --- Sidebar Text Readability --- */
        section[data-testid="stSidebar"] * {{
            color: #0d0d0d !important;
            font-weight: 600 !important;
        }}
        </style>
    """, unsafe_allow_html=True)



# Use your local background file
add_translucent_bg("background.jpg")


def load_logo(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_logo("logo.png")


# Centered logo + brand header
st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: -20px;
        margin-bottom: 10px;
    ">
        <img src="data:image/png;base64,{logo_base64}"
             width="120"
             style="border-radius:15px; box-shadow:0 0 10px rgba(0,0,0,0.2);" />
        <h2 style="color:#2E8B57; margin-bottom:5px; margin-left: 15px;">Ur_FitBuddy_App💪</h2>
        <p style="font-size:14px; color:#444; margin-top:0;">Biswa's A2Z Fitness Dashboard</p>
    </div>
""", unsafe_allow_html=True)


selected = option_menu(
    menu_title=None,
    options=[
        "Home",
        "BMI Calculator",
        "Body Fat % Estimator",
        "Waist-to-Height Ratio",
        "Water & Calorie Guide",
        "TDEE Calculator",
        "Calorie Calculator",
        "About"
    ],
    icons=[
        "house", "calculator", "activity", "rulers", "droplet", "fire", "apple", "info-circle"
    ],
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0.3rem 0.5rem",
            "background": "linear-gradient(90deg, #e8f5e9, #c8e6c9, #a5d6a7)",  # 🌿 green tone
            "box-shadow": "0 3px 8px rgba(0,0,0,0.15)",
            "border": "1px solid rgba(46,139,87,0.3)",
            "white-space": "nowrap",
            "margin-bottom": "12px",
            "backdrop-filter": "blur(8px)",
            "overflow": "hidden",
            "position": "relative",
        },
        "nav-link": {
            "font-size": "13px",
            "font-weight": "600",
            "color": "#0f5132",
            "padding": "0.6rem 0.9rem",
            "margin": "0 3px",
            "border-radius": "6px",
            "transition": "all 0.3s ease-in-out",
        },
        "nav-link:hover": {
            "background-color": "rgba(46,139,87,0.1)",
            "color": "#1b5e20",
        },
        "nav-link-selected": {
            "background": "linear-gradient(90deg, #2E8B57, #3CB371)",  # deep green
            "color": "white",
            "border-radius": "6px",
            "box-shadow": "0 3px 8px rgba(46,139,87,0.25)",
        },
    }
)

# --- CSS FIX for chamfered corners ---
st.markdown("""
<style>
/* Remove default grey background */
div[data-testid="stHorizontalBlock"] {
    background: transparent !important;
}

/* Chamfered corners for the menu container */
div[data-testid="stHorizontalBlock"] > div:first-child {
    clip-path: polygon(
        10px 0%, calc(100% - 10px) 0%, 
        100% 10px, 100% calc(100% - 10px), 
        calc(100% - 10px) 100%, 10px 100%, 
        0% calc(100% - 10px), 0% 10px
    );
}

/* Smooth hover animation for links */
ul.nav > li > a:hover {
    transform: translateY(-2px);
    transition: all 0.2s ease-in-out;
}

/* Compact responsive tweaks */
@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"] > div:first-child {
        clip-path: polygon(
            6px 0%, calc(100% - 6px) 0%, 
            100% 6px, 100% calc(100% - 6px), 
            calc(100% - 6px) 100%, 6px 100%, 
            0% calc(100% - 6px), 0% 6px
        );
    }
}
</style>
""", unsafe_allow_html=True)


# Maintain same selection state logic
if selected != st.session_state.selected_page:
    st.session_state.selected_page = selected
    st.rerun()



# --- PAGE LOGIC ---
selected = st.session_state.selected_page

# --- HOME PAGE
if selected == "Home":
    st.title("🏠 Welcome to Physio BMI Dashboard")
    st.write("""
    Track your BMI, estimate your body fat %, analyze your waist-to-height ratio,  
    calculate your TDEE, and get personalized calorie & water advice — all in one place! 💪
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/706/706164.png", width=220)


# --- BMI CALCULATOR (Compact Column Layout)
elif selected == "BMI Calculator":
    st.title("⚖️ BMI Calculator")
    st.caption("Get a full health analysis including BMI category, workout tips, diet suggestions, and calorie needs.")

    # --- Input Fields in Columns ---
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        activity_level = st.selectbox(
            "Activity Level",
            [
                "Sedentary (little or no exercise)",
                "Lightly active (1-3 days/week)",
                "Moderately active (3-5 days/week)",
                "Very active (6-7 days/week)",
                "Super active (physical job or athlete)"
            ]
        )
    with col2:
        height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
        weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=65.0)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        

    st.markdown("---")

    # --- BMI Calculation ---
    if st.button("Calculate BMI"):
        height_m = height_cm / 100
        bmi = round(weight_kg / (height_m ** 2), 2)
        st.metric("Your BMI", bmi)

        # --- BMI Category ---
        if bmi < 18.5:
            category = "Underweight 🧍‍♂️"
            color = "orange"
            advice = "Increase calorie intake with healthy, nutrient-rich foods."
        elif 18.5 <= bmi < 25:
            category = "Normal Weight ✅"
            color = "green"
            advice = "Maintain with balanced diet and regular exercise."
        elif 25 <= bmi < 30:
            category = "Overweight ⚠️"
            color = "yellow"
            advice = "Add moderate cardio and control portion sizes."
        else:
            category = "Obese 🚨"
            color = "red"
            advice = "Consult a nutritionist and start a gradual fitness plan."

        st.markdown(f"### 🩺 BMI Category: <span style='color:{color};'>{category}</span>", unsafe_allow_html=True)
        st.info(f"💡 **Recommendation:** {advice}")



# --- BODY FAT % ESTIMATOR
elif selected == "Body Fat % Estimator":
    st.title("💪 Body Fat Percentage Estimator")
    st.caption("Estimate your body fat % using the Deurenberg formula.")
    
    col1, col2 = st.columns(2)
    with col1:
        bmi = st.number_input("Enter your BMI", 10.0, 50.0, 22.0)
    with col2:    
        age = st.number_input("Age", 1, 120, 25)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    if st.button("Calculate Body Fat %"):
        bf = round(1.20 * bmi + 0.23 * age - (16.2 if gender == "Male" else 5.4), 1)
        st.metric("Estimated Body Fat %", f"{bf}%")


# --- WAIST-TO-HEIGHT RATIO
elif selected == "Waist-to-Height Ratio":
    st.title("📏 Waist-to-Height Ratio (WtHR)")

    st.caption("Calculate your Waist-to-Height Ratio to assess health risks.")
    
    col1, col2 = st.columns(2)
    with col1:
        height_cm = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
    with col2:
        waist_cm = st.number_input("Waist Circumference (cm)", 40.0, 200.0, 80.0)
    if st.button("Calculate WtHR"):
        whtr = round(waist_cm / height_cm, 2)
        st.metric("Waist-to-Height Ratio", whtr)

# --- WATER & CALORIE GUIDE
elif selected == "Water & Calorie Guide":
    st.title("💧 Water & Calorie Recommendations")
    st.caption("Get personalized daily water and calorie needs based on your stats.")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 120, 25)
        weight_kg = st.number_input("Weight (kg)", 10.0, 300.0, 65.0)
    with col2:
        height_cm = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

    if st.button("Calculate Recommendations"):
        water_liters = round(weight_kg * 0.033, 2)
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + (5 if gender == "Male" else -161)
        calories = {
            "Maintain Weight": int(bmr * 1.55),
            "Mild Weight Loss": int(bmr * 1.35),
            "Weight Loss": int(bmr * 1.2),
            "Weight Gain": int(bmr * 1.8)
        }
        st.subheader("💧 Daily Water Intake")
        st.markdown(f"👉 Drink around **{water_liters} liters/day**.")
        st.subheader("🔥 Calorie Recommendations")
        for goal, cal in calories.items():
            st.markdown(f"- **{goal}:** {cal} kcal/day")


# --- TDEE CALCULATOR (Upgraded)
elif selected == "TDEE Calculator":
    st.title("🔥 TDEE Calculator (Total Daily Energy Expenditure)")
    st.caption("Understand your daily energy burn and how much you should eat to meet your goals.")

    st.header("🧮 Enter Your Details")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 120, 25)
        weight_kg = st.number_input("Weight (kg)", 10.0, 300.0, 65.0)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    with col2:
        height_cm = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
        activity_level = st.selectbox(
        "Activity Level",
        ["Sedentary (little or no exercise)",
         "Lightly active (1-3 days/week)",
         "Moderately active (3-5 days/week)",
         "Very active (6-7 days/week)",
         "Super active (physical job or athlete)"]
    )
    

    if st.button("Calculate TDEE"):
        # --- Calculate BMR (Mifflin-St Jeor Equation)
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + (5 if gender == "Male" else -161)

        # --- Activity multipliers
        multipliers = {
            "Sedentary (little or no exercise)": 1.2,
            "Lightly active (1-3 days/week)": 1.375,
            "Moderately active (3-5 days/week)": 1.55,
            "Very active (6-7 days/week)": 1.725,
            "Super active (physical job or athlete)": 1.9
        }

        tdee = int(bmr * multipliers[activity_level])

        # --- Display Results
        st.success(f"### 🔥 Your Total Daily Energy Expenditure (TDEE): **{tdee} kcal/day**")
        st.write(f"Your **Basal Metabolic Rate (BMR)** is approximately **{int(bmr)} kcal/day**.")
        st.caption(f"Activity Level: {activity_level}")

        # --- Calorie Goals
        st.markdown("### 🎯 Daily Calorie Targets")
        st.info(f"**Maintain Weight:** {tdee} kcal/day")
        st.warning(f"**Lose Weight (≈15% deficit):** {int(tdee * 0.85)} kcal/day")
        st.success(f"**Gain Muscle (≈15% surplus):** {int(tdee * 1.15)} kcal/day")

        st.divider()

        # --- Educational Section
        st.header("📘 What is TDEE?")
        st.write("""
        **TDEE (Total Daily Energy Expenditure)** is the *total amount of energy* your body burns in one day, 
        accounting for your metabolism, physical activity, and even the energy used to digest food.
        """)

        st.subheader("1️⃣ Basal Metabolic Rate (BMR)")
        st.write("""
        - This is your **resting metabolism**, the energy required just to keep you alive — 
          breathing, maintaining body temperature, and powering vital organs.
        - It's measured when you're at rest, not digesting, and in a comfortable temperature.
        - Formula used here (Mifflin–St Jeor):
            \n
            **Men:** 10 × weight(kg) + 6.25 × height(cm) − 5 × age + 5  
            **Women:** 10 × weight(kg) + 6.25 × height(cm) − 5 × age − 161
        """)

        st.subheader("2️⃣ Activity Level")
        st.write("""
        This represents how much you move throughout the day, including both workouts and regular movement:
        - Sedentary → little or no exercise  
        - Lightly active → light exercise (1–3 days/week)  
        - Moderately active → exercise (3–5 days/week)  
        - Very active → intense training (6–7 days/week)  
        - Super active → physically demanding job or athlete
        """)

        st.subheader("3️⃣ Thermic Effect of Food (TEF)")
        st.write("""
        - The **energy used to digest and process food**, typically about **10%** of your total calorie intake.
        - Protein has the highest thermic effect, meaning high-protein diets can slightly boost calorie burn.
        """)

        st.subheader("⚙️ How TDEE is Calculated")
        st.markdown("""
        The TDEE is estimated using this relationship:

        \n
        🔹 **TDEE = BMR × Activity Level Factor**
        \n
        This gives the total number of calories your body uses per day.
        """)

        st.info("""
        💡 **Example:**
        If your BMR is 1600 kcal and you are 'Moderately active' (×1.55),  
        your TDEE = 1600 × 1.55 = **2480 kcal/day**.
        """)

        st.divider()
        st.caption("📊 Tip: Recalculate your TDEE every few months as your weight or activity level changes.")

# --- CALORIE CALCULATOR (ENHANCED with Macronutrient Table)
elif selected == "Calorie Calculator":
    st.title("🍎 Calorie Calculator")
    st.caption("Find how many calories you should eat daily based on your goal — maintain, lose, or gain weight.")

    st.header("🧮 Enter Your Details")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 120, 25)
        weight_kg = st.number_input("Weight (kg)", 10.0, 300.0, 65.0)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    with col2:
        height_cm = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
        activity_level = st.selectbox(
        "Activity Level",
        ["Sedentary (little or no exercise)",
         "Lightly active (1-3 days/week)",
         "Moderately active (3-5 days/week)",
         "Very active (6-7 days/week)",
         "Super active (physical job or athlete)"]
        )
        goal = st.selectbox("Fitness Goal", ["Maintain Weight", "Lose Weight", "Gain Muscle"])
    
    goal_intensity = st.radio("Goal Intensity", ["Moderate (15%)", "Aggressive (25%)"], horizontal=True)

    if "calorie_result" not in st.session_state:
        st.session_state.calorie_result = None

    if st.button("Calculate Calories"):
        # Step 1: Calculate BMR
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + (5 if gender == "Male" else -161)
        activity_multipliers = {
            "Sedentary (little or no exercise)": 1.2,
            "Lightly active (1-3 days/week)": 1.375,
            "Moderately active (3-5 days/week)": 1.55,
            "Very active (6-7 days/week)": 1.725,
            "Super active (physical job or athlete)": 1.9
        }
        tdee = bmr * activity_multipliers[activity_level]

        # Step 2: Adjust for goal
        intensity_factor = 0.85 if goal_intensity == "Moderate (15%)" else 0.75
        surplus_factor = 1.15 if goal_intensity == "Moderate (15%)" else 1.25

        if goal == "Maintain Weight":
            target_calories = tdee
        elif goal == "Lose Weight":
            target_calories = tdee * intensity_factor
        else:
            target_calories = tdee * surplus_factor

        target_calories = int(target_calories)

        # Step 3: Macronutrient breakdown
        protein_cal = target_calories * 0.3
        carb_cal = target_calories * 0.45
        fat_cal = target_calories * 0.25

        protein_g = round(protein_cal / 4)
        carb_g = round(carb_cal / 4)
        fat_g = round(fat_cal / 9)

        # Store results in session_state for persistence
        st.session_state.calorie_result = {
            "target_calories": target_calories,
            "goal": goal,
            "goal_intensity": goal_intensity,
            "protein_g": protein_g,
            "carb_g": carb_g,
            "fat_g": fat_g
        }

    # --- Display stored results (always visible once calculated)
    if st.session_state.calorie_result:
        r = st.session_state.calorie_result
        st.success(f"### 🎯 Recommended Daily Calorie Intake: **{r['target_calories']} kcal/day**")
        st.caption(f"Goal: {r['goal']} | Intensity: {r['goal_intensity']}")

        st.subheader("💪 Macronutrient Breakdown (approx.)")
        st.markdown(
            f"""
            - 🥩 **Protein:** {r['protein_g']} g (~30%)  
            - 🍚 **Carbs:** {r['carb_g']} g (~45%)  
            - 🥑 **Fats:** {r['fat_g']} g (~25%)
            """
        )

        st.markdown("---")
        st.info("""
        ⚡ **How This Works:**
        - Your **TDEE** is calculated first — total calories burned daily.  
        - Based on your goal, a calorie **deficit** (for fat loss) or **surplus** (for muscle gain) is applied.  
        - Then macronutrients are distributed to ensure energy balance and performance.
        """)

    # --- Macronutrient Table (Now stays interactive)
    st.markdown("## 🧾 Macronutrients in Common Foods")
    st.caption("Use this chart to plan your meals based on your daily macronutrient goals.")

    import pandas as pd
    data = {
        "Category": (
            ["Fruit"] * 9 +
            ["Vegetables"] * 7 +
            ["Proteins"] * 7 +
            ["Common Meals/Snacks"] * 10 +
            ["Beverages/Dairy"] * 10
        ),
        "Food": [
            "Apple", "Banana", "Grapes", "Orange", "Pear", "Peach", "Pineapple", "Strawberry", "Watermelon",
            "Asparagus", "Broccoli", "Carrots", "Cucumber", "Eggplant", "Lettuce", "Tomato",
            "Beef (cooked)", "Chicken (cooked)", "Tofu", "Egg", "Fish (Catfish, cooked)", "Pork (cooked)", "Shrimp (cooked)",
            "Bread (white)", "Butter", "Caesar salad", "Cheeseburger", "Hamburger", "Dark Chocolate",
            "Corn", "Pizza", "Potato", "Rice",
            "Beer", "Coca-Cola", "Diet Coke", "Milk (1%)", "Milk (2%)", "Milk (Whole)",
            "Orange Juice", "Apple Cider", "Yogurt (low-fat)", "Yogurt (non-fat)"
        ],
        "Serving Size": [
            "1 (4 oz.)", "1 (6 oz.)", "1 cup", "1 (4 oz.)", "1 (5 oz.)", "1 (6 oz.)", "1 cup", "1 cup", "1 cup",
            "1 cup", "1 cup", "1 cup", "4 oz.", "1 cup", "1 cup", "1 cup",
            "2 oz.", "2 oz.", "4 oz.", "1 large", "2 oz.", "2 oz.", "2 oz.",
            "1 slice", "1 tbsp", "3 cups", "1 sandwich", "1 sandwich", "1 oz.",
            "1 cup", "1 slice (14\")", "6 oz.", "1 cup cooked",
            "1 can", "1 can", "1 can", "1 cup", "1 cup", "1 cup",
            "1 cup", "1 cup", "1 cup", "1 cup"
        ],
        "Protein (g)": [
            0.27, 1.85, 1.15, 0.79, 0.54, 1.2, 0.84, 1.11, 0.93,
            2.95, 2.57, 1.19, 0.67, 0.98, 0.5, 1.58,
            14.2, 16, 7.82, 6.29, 9.96, 15.82, 15.45,
            1.91, 0.12, 16.3, 14.77, 14.61, 1.57, 4.3, 13.32, 4.47, 4.2,
            1.64, 0, 0, 8.22, 8.05, 7.86, 1.74, 0.15, 12.86, 13.01
        ],
        "Carbs (g)": [
            14.36, 38.85, 28.96, 11.79, 21.91, 12.59, 19.58, 12.75, 11.48,
            5.2, 6.04, 12.26, 2.45, 5.88, 1.63, 7.06,
            0, 0, 2.72, 0.38, 4.84, 0, 0.69,
            12.65, 0.01, 21.12, 31.75, 26.81, 16.84, 30.49, 33.98, 36.47, 44.08,
            12.64, 39, 0, 12.18, 11.42, 11.03, 25.79, 28.97, 17.25, 17.43
        ],
        "Fat (g)": [
            0.18, 0.56, 0.26, 0.23, 0.17, 0.33, 0.19, 0.5, 0.23,
            0.16, 0.34, 0.31, 0.18, 0.18, 0.08, 0.36,
            10.4, 1.84, 3.06, 4.97, 8.24, 8.26, 1.32,
            0.82, 11.52, 45.91, 15.15, 10.97, 9.19, 1.64, 12.13, 0.22, 0.44,
            0, 0, 0, 2.37, 4.81, 7.93, 0.5, 0.27, 3.8, 0.41
        ]
    }

    df = pd.DataFrame(data)

    # === FILTER CONTROLS (outside button scope)
    st.subheader("🔎 Explore Foods by Category or Search")
    col1, col2 = st.columns([1, 2])

    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + sorted(df["Category"].unique().tolist())
        )

    with col2:
        search_query = st.text_input("Search Food (e.g., Chicken, Banana)", "")

    filtered_df = df.copy()
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]
    if search_query.strip():
        filtered_df = filtered_df[
            filtered_df["Food"].str.contains(search_query, case=False, na=False)
        ]

    if filtered_df.empty:
        st.warning("No matching foods found. Try a different search term or category.")
    else:
        st.dataframe(filtered_df, use_container_width=True)

    st.caption("💡 Tip: Use this table to plan meals that match your calorie and macronutrient goals.")



# --- ABOUT PAGE
elif selected == "About":
    st.title("ℹ️ About This App")
    st.write("""
    **Physio BMI App** helps you calculate BMI, TDEE, body fat %, and water/calorie needs,  
    offering practical diet and fitness advice tailored to your lifestyle.  
    Built with ❤️ using **Streamlit**.
    """)

st.divider()
st.caption("Developed with ❤️ using Streamlit | Physiotherapy Health Tool")


# --- Scroll-to-top floating button (fixed version) ---
st.markdown("""
<style>
/* Scroll-to-top button styling */
#scrollTopBtn {
    display: none;
    position: fixed;
    bottom: 70px;
    right: 22px;
    z-index: 9999;
    background: linear-gradient(90deg, #2E8B57, #3CB371);
    color: white;
    border: none;
    outline: none;
    cursor: pointer;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    font-size: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
    transition: all 0.3s ease;
}

/* Hover glow */
#scrollTopBtn:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 6px 14px rgba(46, 139, 87, 0.4);
}

/* Mobile tweak */
@media (max-width: 768px) {
    #scrollTopBtn {
        bottom: 60px;
        right: 15px;
        width: 50px;
        height: 50px;
        font-size: 22px;
    }
}
</style>

<!-- Button HTML (using an up-arrow SVG for cleaner visuals) -->
<button id="scrollTopBtn" title="Go to top">
    ⬆️
</button>

<script>
document.addEventListener("DOMContentLoaded", function() {
    const scrollTopBtn = document.getElementById("scrollTopBtn");
    window.addEventListener("scroll", function() {
        if (window.scrollY > 250) {
            scrollTopBtn.style.display = "block";
        } else {
            scrollTopBtn.style.display = "none";
        }
    });

    scrollTopBtn.addEventListener("click", function() {
        window.scrollTo({top: 0, behavior: "smooth"});
    });
});
</script>
""", unsafe_allow_html=True)
