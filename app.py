import streamlit as st
import pymupdf
from google import genai
from dotenv import load_dotenv
import os

# --------------------------------
# Load Gemini API Key
# --------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="SmartCareer AI",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------
# Title
# --------------------------------

st.title("🎯 SmartCareer AI")

st.subheader(
    "Agentic AI-Powered Resume, Job Description & Interview Preparation Assistant"
)

st.write(
    "Upload your resume and enter a job description "
    "to analyze skills, identify skill gaps, and prepare for interviews."
)


# --------------------------------
# Resume Upload
# --------------------------------

st.subheader("📄 Upload Your Resume")

resume = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"]
)

resume_text = ""

if resume is not None:

    st.success("Resume uploaded successfully! ✅")

    pdf = pymupdf.open(
        stream=resume.read(),
        filetype="pdf"
    )

    for page in pdf:
        resume_text += page.get_text()

    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=300
    )


# --------------------------------
# Job Description
# --------------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the Job Description here",
    height=300,
    placeholder="Paste the complete job description here..."
)


# --------------------------------
# Skills List
# --------------------------------

skills = [
    "Python",
    "SQL",
    "OOP",
    "Problem-solving",
    "Data structures",
    "Algorithms",
    "Git",
    "GitHub",
    "APIs",
    "Flask",
    "FastAPI",
    "Generative AI",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "Machine Learning",
    "Deep Learning",
    "Communication"
]


# --------------------------------
# Job Description Analyzer
# --------------------------------

found_skills = []

if job_description.strip():

    st.success(
        "Job Description added successfully! ✅"
    )

    jd_lower = job_description.lower()

    for skill in skills:

        if skill.lower() in jd_lower:
            found_skills.append(skill)

    st.subheader("🔍 Required Skills")

    if found_skills:

        for skill in found_skills:
            st.write("✅", skill)

    else:

        st.write(
            "No skills detected from the current skill list."
        )


# --------------------------------
# Skill Gap Analysis
# --------------------------------

if resume_text and job_description.strip():

    resume_lower = resume_text.lower()

    matching_skills = []
    missing_skills = []

    for skill in found_skills:

        if skill.lower() in resume_lower:
            matching_skills.append(skill)

        else:
            missing_skills.append(skill)

    st.subheader("📊 Skill Gap Analysis")

    # Matching Skills
    st.write("### 🟢 Matching Skills")

    if matching_skills:

        for skill in matching_skills:
            st.write("✅", skill)

    else:

        st.write(
            "No matching skills found."
        )

    # Missing Skills
    st.write("### 🔴 Missing Skills")

    if missing_skills:

        for skill in missing_skills:
            st.write("❌", skill)

    else:

        st.write(
            "No major skill gaps found! 🎉"
        )


# --------------------------------
# Gemini AI Interview Preparation
# --------------------------------

if resume_text and job_description.strip():

    st.subheader("🤖 AI Interview Preparation")

    if st.button("Generate AI Interview Questions"):

        with st.spinner("Gemini AI is analyzing your resume and job description..."):

            prompt = f"""
You are an expert career and interview preparation assistant.

Analyze the candidate's resume and the provided job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Create personalized interview preparation.

Provide the response in the following sections:

1. JOB ROLE
Identify the main job role.

2. IMPORTANT REQUIRED SKILLS
List the most important skills required for this job.

3. MATCHING SKILLS
Identify skills that the candidate has which match the job.

4. MISSING SKILLS
Identify important skills required by the job that are not clearly present in the resume.

5. TECHNICAL INTERVIEW QUESTIONS
Generate 8 technical questions based on the job description and the candidate's skills.

6. RESUME-BASED QUESTIONS
Generate 5 questions based specifically on the candidate's resume/projects.

7. HR QUESTIONS
Generate 5 HR interview questions suitable for this job.

8. PREPARATION TIPS
Give 5 practical preparation recommendations based on the skill gaps.

Keep the response clear and suitable for a final-year engineering student.
"""

            try:

                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt
                )

                st.success(
                    "AI Interview Preparation generated successfully! 🎯"
                )

                st.markdown(response.text)

            except Exception as e:

                st.error(
                    f"Gemini AI error: {e}"
                )


# --------------------------------
# Footer
# --------------------------------

st.divider()

st.caption(
    "SmartCareer AI | Generative AI + Agentic AI Career Assistant"
)
# --------------------------------
# Personalized Learning Plan
# --------------------------------

if resume_text and job_description.strip():

    st.subheader("📚 Personalized Learning Plan")

    if st.button("Generate Learning Plan"):

        learning_prompt = f"""
You are a career learning assistant.

Based on the candidate's resume and job description below,
create a personalized learning plan.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Create a simple 7-day learning plan.

For each day provide:
- Topic
- What to learn
- Practical task

Focus mainly on skills required by the job that are missing
or weak in the candidate's resume.

Keep the plan suitable for a final-year engineering student.
"""

        with st.spinner("Creating your personalized learning plan..."):

            try:

                learning_response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=learning_prompt
                )

                st.success(
                    "Personalized learning plan generated! 📚"
                )

                st.markdown(
                    learning_response.text
                )

            except Exception as e:

                st.error(
                    f"Learning plan error: {e}"
                )