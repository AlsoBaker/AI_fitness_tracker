import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="AI Fitness Planner", page_icon="🏋️")

light_bg = st.toggle("🌤️ Light Background")

if light_bg:
    st.markdown(
        """
        <style>
        section[data-testid="stAppViewContainer"] {
            background-color: #f4f7fb;
        }
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

age = st.number_input("Age", 16, 65, step=1)
gender = st.radio("Gender", ["Male", "Female", "Prefer not to say"])
goal = st.radio("Fitness Goal", ["Fat Loss", "Muscle Gain", "Maintenance"])
diet = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
budget = st.radio("Budget", ["Low", "Medium", "High"])
equipment = st.radio("Workout Type", ["Home", "Gym", "No Equipment"])

height = st.number_input("Height (cm)", 120, 220, 170)
weight = st.number_input("Weight (kg)", 30, 200, 65)

time = st.slider("Workout Time (minutes)", 15, 120, 30, step=5)

bmi = round(weight / ((height / 100) ** 2), 2)

if bmi < 18.5:
    bmi_status = "Underweight"
elif bmi < 24.9:
    bmi_status = "Normal"
elif bmi < 29.9:
    bmi_status = "Overweight"
else:
    bmi_status = "Obese"

st.info(f"📊 BMI: {bmi} ({bmi_status})")

if st.button("Generate My Plan"):
    prompt = f"""
You are a certified fitness trainer and nutritionist.

Create a personalized workout and diet plan for a student:

Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
BMI: {bmi} ({bmi_status})
Goal: {goal}
Diet: {diet}
Budget: {budget}
Workout Type: {equipment}
Workout Time: {time} minutes per day

Rules:
- Student friendly
- Affordable Indian food options
- No supplements
- Adjust plan according to BMI
- 5-day workout plan
- 1-day sample diet plan
"""

    with st.spinner("Generating your plan..."):
        response = llm.invoke([HumanMessage(content=prompt)])

    st.subheader("📋 Your Personalized Fitness Plan")
    st.write(response.content)