import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="AI Fitness Planner")

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.7
)

st.title("🏋️ Personalized Workout & Diet Planner")

age = st.number_input("Age", 16, 65)
gender = st.radio("Gender", ["Male","Female","Prefer not to say"])
goal = st.radio("Fitness Goal", ["Fat Loss", "Muscle Gain", "Maintenance"])
diet = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
budget = st.radio("Budget", ["Low", "Medium", "High"])
equipment = st.radio("Workout Type", ["Home", "Gym", "No Equipment"])
time = st.slider("Workout Time (minutes)", 15, 120, 30)

if st.button("Generate My Plan"):
    prompt = f"""
You are a certified fitness trainer.

Create a personalized workout and diet plan for a student:
Age: {age}
Gender: {gender}
Goal: {goal}
Diet: {diet}
Budget: {budget}
Workout Type: {equipment}
Workout Time: {time} minutes

Rules:
- Student friendly
- Affordable foods
- No supplements
- Indian food options
- 5-day workout plan
- 1-day diet plan
"""

    with st.spinner("Generating your plan..."):
        response = llm.invoke([HumanMessage(content=prompt)])
        st.subheader("📋 Your Personalized Plan")
        st.write(response.content)