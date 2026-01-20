import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="AI Fitness Planner",
    page_icon="🏋️",
    layout="centered"
)

theme = st.toggle("🌙 Dark Mode")

if theme:
    bg_color = "#0e1117"
    card_color = "#1c1f26"
    text_color = "#ffffff"
else:
    bg_color = "#f9fafb"
    card_color = "#ffffff"
    text_color = "#000000"

st.markdown(
    f"""
    <style>
    /* App background */
    body {{
        background-color: {bg_color};
        color: {text_color};
    }}

    /* Main app container */
    section[data-testid="stAppViewContainer"] {{
        background-color: {bg_color};
        color: {text_color};
    }}

    /* Card styling */
    .card {{
        padding: 20px;
        border-radius: 12px;
        background-color: {card_color};
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }}

    /* Text inputs & labels */
    label, p, span, div {{
        color: {text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.7
)

st.title("🏋️ Personalized Workout & Diet Planner")
st.caption("AI-powered fitness planning for students")

st.markdown("## 📝 Enter Your Details")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 16, 65, step=1)
        gender = st.radio("Gender", ["Male", "Female", "Prefer not to say"])
        goal = st.radio("Fitness Goal", ["Fat Loss", "Muscle Gain", "Maintenance"])

    with col2:
        diet = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        budget = st.radio("Budget", ["Low", "Medium", "High"])
        equipment = st.radio("Workout Type", ["Home", "Gym", "No Equipment"])

    st.markdown("### 📊 Body Details")
    height = st.number_input("Height (cm)", 120, 220, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 65)

    time = st.slider("⏱️ Workout Time (minutes per day)", 15, 120, 30, step=5)

    bmi = round(weight / ((height / 100) ** 2), 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 24.9:
        bmi_status = "Normal"
    elif bmi < 29.9:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    st.markdown(
        f"""
        **📌 Your BMI:** `{bmi}`  
        **🧠 BMI Category:** **{bmi_status}**
        """
    )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
generate = st.button("🚀 Generate My Personalized Plan", use_container_width=True)

if generate:
    prompt = f"""
You are a certified fitness trainer and nutritionist.

Create a personalized workout and diet plan for a student:

Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
BMI: {bmi} ({bmi_status})
Fitness Goal: {goal}
Diet Preference: {diet}
Budget: {budget}
Workout Type: {equipment}
Workout Time: {time} minutes per day

Rules:
- Student friendly language
- Affordable Indian food options
- No supplements
- Adjust plan according to BMI
- 5-day workout plan
- 1-day sample diet plan
"""

    with st.spinner("💪 Creating your personalized fitness plan..."):
        response = llm.invoke([HumanMessage(content=prompt)])

    st.markdown("## 📋 Your Personalized Fitness Plan")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(response.content)
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption("Made with ❤️ using Streamlit & LLaMA (Groq)")