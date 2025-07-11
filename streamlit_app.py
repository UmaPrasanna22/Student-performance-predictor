import streamlit as st
import numpy as np
import joblib

# Load trained model and expected feature names
model = joblib.load('../model.pkl')
feature_names = joblib.load('../features.pkl')

st.set_page_config(page_title="🎓 Final Grade Predictor", layout="centered")
st.title("🎓 Student Final Grade Predictor (G3)")

st.markdown("Predict a student’s final performance using their academic, personal, and social information.")

input_dict = {}

# === Section: Student Background ===
st.header("👤 Student Background")

# input_dict['school'] = 0 if st.selectbox("School", ["Gabriel Pereira (GP)", "Mousinho da Silveira (MS)"]) == "Gabriel Pereira (GP)" else 1
sex_option = st.selectbox("Sex", ["Female", "Male", "Other"])
input_dict['sex'] = {"Female": 0, "Male": 1, "Other": 2}[sex_option]
input_dict['age'] = st.slider("Age", 15, 22, 17)
input_dict['address'] = 1 if st.selectbox("Home Address", ["Urban", "Rural"]) == "Urban" else 0
input_dict['famsize'] = 1 if st.selectbox("Family Size", ["GT3 (Greater than 3)", "LE3 (3 or less)"]) == "GT3 (Greater than 3)" else 0
input_dict['Pstatus'] = 1 if st.selectbox("Parent Cohabitation Status", ["Together (T)", "Apart (A)"]) == "Apart (A)" else 0

# === Section: Parental Info ===
st.header("👨‍👩‍👧 Parental Information")
edu_labels = {
    0: "None",
    1: "Primary Education (4th grade)",
    2: "5th to 9th grade",
    3: "Secondary Education",
    4: "Higher Education"
}
input_dict['Medu'] = st.selectbox("Mother's Education", list(edu_labels.values()))
input_dict['Medu'] = list(edu_labels.keys())[list(edu_labels.values()).index(input_dict['Medu'])]
input_dict['Fedu'] = st.selectbox("Father's Education", list(edu_labels.values()))
input_dict['Fedu'] = list(edu_labels.keys())[list(edu_labels.values()).index(input_dict['Fedu'])]

jobs = ["teacher", "health", "services", "at_home", "other"]
input_dict['Mjob'] = jobs.index(st.selectbox("Mother's Job", jobs))
input_dict['Fjob'] = jobs.index(st.selectbox("Father's Job", jobs))

input_dict['guardian'] = ["mother", "father", "other"].index(st.selectbox("Guardian", ["mother", "father", "other"]))

# Reason for choosing the school
reason_options = ["home", "reputation", "course", "other"]
input_dict['reason'] = reason_options.index(
    st.selectbox("Reason for Choosing School", reason_options)
)


# === Section: Study & Support ===
st.header("📚 Study & Support")

input_dict['traveltime'] = st.slider("Travel Time to School (1=<15min, 4=>1hr)", 1, 4, 1)
input_dict['studytime'] = st.slider("Weekly Study Time (1=<2h, 4=>10h)", 1, 4, 2)
input_dict['failures'] = st.slider("Number of Past Failures", 0, 3, 0)

yn = lambda label: 1 if st.radio(label, ["Yes", "No"]) == "Yes" else 0
input_dict['schoolsup'] = yn("Extra Educational Support?")
input_dict['famsup'] = yn("Family Educational Support?")
input_dict['paid'] = yn("Extra Paid Classes?")

# === Section: Activities & Goals ===
st.header("🎯 Activities & Education Goals")

input_dict['activities'] = yn("Extracurricular Activities?")
input_dict['nursery'] = yn("Attended Nursery School?")
input_dict['higher'] = yn("Aspires Higher Education?")
input_dict['internet'] = yn("Internet Access at Home?")
#input_dict['romantic'] = yn("Currently in a Romantic Relationship?")

# === Section: Social Life & Health ===
st.header("💬 Social Life & Health")

input_dict['famrel'] = st.slider("Family Relationship Quality (1–5)", 1, 5, 4)
input_dict['freetime'] = st.slider("Free Time After School (1–5)", 1, 5, 3)
input_dict['goout'] = st.slider("Going Out with Friends (1–5)", 1, 5, 3)
#input_dict['Dalc'] = st.slider("Workday Alcohol Consumption (1–5)", 1, 5, 1)
#input_dict['Walc'] = st.slider("Weekend Alcohol Consumption (1–5)", 1, 5, 2)
input_dict['health'] = st.slider("Current Health Status (1–5)", 1, 5, 5)
input_dict['absences'] = st.slider("School Absences", 0, 93, 4)

# === Section: Grades ===
st.header("🧮 Previous Grades")

input_dict['G1'] = st.slider("First Period Grade (G1)", 0, 20, 10)
input_dict['G2'] = st.slider("Second Period Grade (G2)", 0, 20, 10)

# Build input array in correct order
input_array = np.array([input_dict[feat] for feat in feature_names]).reshape(1, -1)

# Prediction
if st.button("🎯 Predict Final Grade"):
    prediction = model.predict(input_array)[0]
    st.success(f"📘 Predicted Final Grade (G3): **{round(prediction, 2)} / 20**")
