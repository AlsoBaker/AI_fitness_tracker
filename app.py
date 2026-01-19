import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="AI Fitness Planner")

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    model_name="llama3-8b-8192"
)

st.title("🏋️ Personalized Workout & Diet Planner")

age = st.number_input("Age", 16, 60)
goal = st.selectbox("Fitness Goal", ["Fat Loss", "Muscle Gain", "Maintenance"])
diet = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
budget = st.selectbox("Budget", ["Low", "Medium", "High"])
equipment = st.selectbox("Workout Type", ["Home", "Gym", "No Equipment"])
time = st.slider("Workout Time (minutes)", 15, 90, 30)

if st.button("Generate My Plan"):
    prompt = f"""
You are a certified fitness trainer.

Create a personalized workout and diet plan for a student:
Age: {age}
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