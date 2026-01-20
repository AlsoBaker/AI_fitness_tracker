import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import tempfile

st.set_page_config(page_title="AI Fitness Planner", page_icon="🏋️")

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.7
)

st.title("🏋️ Personalized Workout & Diet Planner")
st.caption("AI-powered fitness planning for students")

age = st.number_input("Age", 16, 65, step=1)
gender = st.segmented_control("Gender",["Male", "Female", "Prefer not to say"])
goal = st.segmented_control("Fitness Goal",["Fat Loss", "Muscle Gain", "Maintenance"])
diet = st.selectbox("Diet Preference",["Vegetarian", "Non-Vegetarian", "Vegan"])
budget = st.select_slider("Budget",options=["Low", "Medium", "High"])
equipment = st.selectbox("Workout Type",["Home", "Gym", "No Equipment"])
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

def create_pdf(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    for line in text.split("\n"):
        story.append(Paragraph(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), styles["Normal"]))
    doc.build(story)
    return temp_file.name

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
        plan_text = response.content

    st.subheader("📋 Your Personalized Fitness Plan")
    st.write(plan_text)

    pdf_path = create_pdf(plan_text)

    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download Plan as PDF",
            data=pdf_file,
            file_name="Personalized_Fitness_Plan.pdf",
            mime="application/pdf"
        )