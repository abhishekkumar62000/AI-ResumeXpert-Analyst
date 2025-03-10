# Import Important Library
import streamlit as st
import google.generativeai as genai
import webbrowser
from PyPDF2 import PdfReader
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Set page configuration
st.set_page_config(page_title="AI Resume Reviewer", page_icon="📄", layout="wide")

# Fetch API key from Streamlit Secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Ensure the API key is set
if not GEMINI_API_KEY:
    st.error("⚠ GEMINI API Key is missing. Set it in Streamlit Secrets!")
else:
    genai.configure(api_key=GEMINI_API_KEY)

import google.api_core.exceptions  # Add this import

# List available models to verify the model name
try:
    available_models = genai.list_models()
    model_names = [model.name for model in available_models]
    
    # Verify if the desired model is in the list
    desired_model_name = "models/gemini-1.5-flash-latest"  # Replace with the correct model name
    if desired_model_name in model_names:
        model = genai.GenerativeModel(desired_model_name)
    else:
        st.error(f"⚠ Model '{desired_model_name}' not found. Available models: {model_names}")
        st.stop()
except google.api_core.exceptions.PermissionDenied as e:
    st.error("⚠ Permission denied. Please check your API key permissions.")
    st.stop()
except google.api_core.exceptions.InvalidArgument as e:
    st.error("⚠ Invalid argument. Please check the model name and API key.")
    st.stop()
except Exception as e:
    st.error(f"⚠ An unexpected error occurred: {e}")
    st.stop()

def chat_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text if response else "No response received."
    except google.api_core.exceptions.NotFound as e:
        st.error("⚠ Model not found. Please check the model name and API key.")
        return "Model not found."
    except google.api_core.exceptions.PermissionDenied as e:
        st.error("⚠ Permission denied. Please check your API key permissions.")
        return "Permission denied."
    except google.api_core.exceptions.InvalidArgument as e:
        st.error("⚠ Invalid argument. Please check the model name and API key.")
        return "Invalid argument."
    except Exception as e:
        st.error(f"⚠ An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"

# Your other code remains the same
import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.run(asyncio.sleep(0))  # ✅ Ensure a running event loop

# UI Improvements
st.title("🚀AI ResumeXpert Analyst 🤖")
st.markdown("Upload your resume to get detailed AI feedback, ATS analysis, and job match insights!🧠")
st.caption("📝 Rewrite. 🚀 Rank. 🎯 Recruit – AI ResumeXpert at Your Service!👨‍💻")

AI_path = "AI.png"  # Ensure this file is in the same directory as your script
try:
    st.sidebar.image(AI_path)
except FileNotFoundError:
    st.sidebar.warning("AI.png file not found. Please check the file path.")

image_path = "image.png"  # Ensure this file is in the same directory as your script
try:
    st.sidebar.image(image_path)
except FileNotFoundError:
    st.sidebar.warning("image.png file not found. Please check the file path.")

# Sidebar Navigation
with st.sidebar:
    st.header("⚙️ App Features")

    tab_selection = st.radio("Select a Feature:", [
        "📂 Upload Resume",
        "📊 Job Match Analysis",
        "🚀 AI Project Suggestions",
        "🤷‍♂ ATS Score Checker",
        "📊 AI-Powered Resume Ranking",
        "💡 AI Career Roadmap & Skills Guide",
        "🛠 Missing Skills & How to Learn Them",
        "📜 Certifications & Course Recommendations",
        "💰 Expected Salaries & Job Roles",
        "📢 Resume Feedback via AI Chat",
        "📢 Personalized Job Alerts",
        "💡 Soft Skills Analysis & Improvement"
    ])

    st.markdown("👨👨‍💻Developer:- Abhishek❤️Yadav")
    
    developer_path = "my.jpg"  # Ensure this file is in the same directory as your script
    try:
        st.sidebar.image(developer_path)
    except FileNotFoundError:
        st.sidebar.warning("my.jpg file not found. Please check the file path.")

def extract_text(file):
    if file.name.endswith(".pdf"):
        pdf_reader = PdfReader(file)
        return "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return "❌ Unsupported file format. Upload a PDF or DOCX."

def analyze_resume(text):
    prompt = f"""
    You are an expert AI Resume Reviewer. Analyze the following resume thoroughly and provide structured insights on:
    0️⃣ *first Full Detail Analysis of Resume Files and Display all details of the resume*
    1️⃣ *Strengths:* What makes this resume stand out? Identify key skills, achievements, and formatting positives.
    2️⃣ *Areas for Improvement:* Highlight missing elements, weak points, and vague descriptions that need enhancement.
    3️⃣ *Formatting Suggestions:* Provide recommendations for a more professional and ATS-compliant structure.
    4️⃣ *ATS Compliance Check:* Analyze the resume for ATS-friendliness, including keyword optimization and readability.
    5️⃣ *Overall Rating:* Score the resume on a scale of 1 to 10 with justification.
    
    Resume:
    {text}
    """
    return chat_with_gemini(prompt)

def match_job_description(resume_text, job_desc):
    prompt = f"""
    You are an AI Job Fit Analyzer. Compare the given resume with the provided job description and generate a structured report:
    
    ✅ *Matching Skills:* Identify skills in the resume that match the job description.
    ❌ *Missing Skills:* Highlight missing key skills that the candidate needs to acquire.
    📊 *Fit Percentage:* Provide a percentage match score based on skillset, experience, and qualifications.
    🏆 *Final Verdict:* Clearly state whether the candidate is a "Good Fit" or "Needs Improvement" with reasons.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_desc}
    """
    return chat_with_gemini(prompt)

def get_resume_score(resume_text):
    prompt = f"""
    As an AI Resume Scorer, evaluate the resume across different factors and provide a structured breakdown:
    
    🎯 *Skills Match:* XX% (How well the skills align with industry requirements)
    📈 *Experience Level:* XX% (Assessment of experience depth and relevance)
    ✨ *Formatting Quality:* XX% (Resume structure, clarity, and ATS compliance)
    🔍 *Overall Strength:* XX% (General effectiveness of the resume)
    
    Provide the final *Resume Score (0-100)* with a breakdown and actionable insights for improvement.
    
    Resume:
    {resume_text}
    """
    return chat_with_gemini(prompt)

def get_improved_resume(resume_text):
    prompt = f"""
    Optimize the following resume to enhance its professionalism, clarity, and ATS compliance:
    
    - ✅ Fix grammar and spelling errors
    - 🔥 Improve clarity, conciseness, and professionalism
    - ✨ Optimize formatting for readability and ATS-friendliness
    - 📌 Ensure keyword optimization to improve job match chances
    - 🏆 Enhance overall presentation while maintaining content integrity
    
    Resume:
    {resume_text}
    
    Provide only the improved resume text.
    """
    return chat_with_gemini(prompt)

def create_pdf(text, filename="Optimized_Resume.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(50, 750, text)
    c.save()
    return filename

# Create Section-wise Tabs
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
resume_text = None
if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("✅ Resume Uploaded Successfully!")

if tab_selection == "📂 Upload Resume":
    st.subheader("📂 Upload Resume")
    if uploaded_file:
        # AI Resume Analysis
        feedback = analyze_resume(resume_text)
        score_feedback = get_resume_score(resume_text)

        st.subheader("📝 AI Feedback")
        st.write(feedback)
        
        st.subheader("⭐ Resume Score & ATS Breakdown")
        st.write(score_feedback)
        
        if st.button("🚀 Improve Resume & Download"):
            improved_resume_text = get_improved_resume(resume_text)
            updated_pdf = create_pdf(improved_resume_text)
            st.success("🎉 Resume Improved Successfully!")
            st.download_button("⬇ Download Optimized Resume", open(updated_pdf, "rb"), file_name="Optimized_Resume.pdf")

elif tab_selection == "📊 Job Match Analysis":
    st.subheader("📊 Job Match Analysis")
    job_desc = st.text_area("📌 Paste Job Description Here:")
    if job_desc and resume_text:
        st.write("🔍 Analyzing job fit...")
        job_fit_feedback = match_job_description(resume_text, job_desc)
        st.subheader("📊 Job Fit Analysis")
        st.write(job_fit_feedback)

elif tab_selection == "🚀 AI Project Suggestions":
    st.subheader("🚀 AI-Powered Project Suggestions")
    if resume_text:
        if st.button("📌 Get Project Ideas Based on Resume"):
            def suggest_projects(resume_text):
                prompt = f"""
                You are an AI Project Advisor. Based on the following resume, suggest relevant AI projects:

                ✅ *Project Ideas*: List 3-5 project ideas that align with the user's skills and experience.
                🔧 *Project Details*: Provide a brief description and key objectives for each project.
                📈 *Skill Development*: Explain how each project will help in skill enhancement and career growth.

                Resume:
                {resume_text}
                """
                return chat_with_gemini(prompt)

            project_suggestions = suggest_projects(resume_text)
            st.write(project_suggestions)

elif tab_selection == "🤷‍♂ ATS Score Checker":
    st.subheader("🤷‍♂ ATS Score Checker")
    if resume_text:
        if st.button("🔍 Check ATS Score"):
            def check_ats_score(resume_text):
                prompt = f"""
                You are an AI ATS Score Checker. Analyze the following resume for ATS compliance and provide a score:

                ✅ *ATS Compatibility*: Score out of 100 based on keyword optimization, formatting, and readability.
                ❌ *Areas for Improvement*: Highlight specific issues that need to be addressed for better ATS compliance.
                
                Resume:
                {resume_text}
                """
                response = chat_with_gemini(prompt)
                score = int(response.split("Score:")[-1].split("/")[0].strip())
                feedback = response.split("Areas for Improvement:")[-1].strip()
                return score, feedback

            ats_score, ats_feedback = check_ats_score(resume_text)
            st.markdown(f"### ✅ Your ATS Score: *{ats_score}/100*")
            if ats_score < 80:
                st.warning("⚠ Your resume needs improvement!")
                st.write(ats_feedback)
            else:
                st.success("🎉 Your resume is ATS-friendly!")

elif tab_selection == "📊 AI-Powered Resume Ranking":
    st.subheader("📊 AI-Powered Resume Ranking")
    uploaded_files = st.file_uploader("Upload Multiple Resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
    if uploaded_files:
        resume_texts = []
        file_names = []
        
        for file in uploaded_files:
            text = extract_text(file)
            if text.startswith("❌"):
                st.error(f"❌ Unable to process: {file.name}")
            else:
                resume_texts.append(text)
                file_names.append(file.name)

        if len(resume_texts) > 0:
            if st.button("🚀 Rank Resumes"):
                ranked_resumes = []
                
                for i, text in enumerate(resume_texts):
                    rank_prompt = f"""
                    You are an AI Resume Evaluator. Assess the following resume based on:
                    ✅ **ATS Compatibility**
                    ✅ **Readability & Formatting**
                    ✅ **Job Fit & Skills Alignment**
                    
                    Give a **score out of 100** and a brief analysis.

                    Resume:
                    {text}
                    """
                    score_response = chat_with_gemini(rank_prompt)
                    try:
                        score = int(score_response.split("Score:")[-1].split("/")[0].strip())
                    except (IndexError, ValueError):
                        score = 0
                    ranked_resumes.append((file_names[i], score))

                ranked_resumes.sort(key=lambda x: x[1], reverse=True)

                st.subheader("🏆 Ranked Resumes")
                for i, (name, score) in enumerate(ranked_resumes, start=1):
                    st.write(f"**{i}. {name}** - **Score: {score}/100**")

elif tab_selection == "💡 AI Career Roadmap & Skills Guide":
    st.subheader("💡 AI Career Roadmap & Skills Guide")
    if resume_text:
        if st.button("🚀 Get Career Insights"):
            def generate_career_roadmap(resume_text):
                prompt = f"""
                You are an AI Career Advisor. Based on the following resume, suggest the best career path:

                ✅ *Current Strengths & Skills*: Identify the user's key strengths.
                🚀 *Best Career Path*: Recommend an ideal career direction.
                📈 *Career Growth Roadmap*:
                   - 🔹 Entry-Level Roles
                   - 🔸 Mid-Level Roles
                   - 🔺 Senior-Level Roles
                🔮 *Future Industry Trends*: Emerging trends & opportunities.

                Resume:
                {resume_text}
                """
                return chat_with_gemini(prompt)

            career_guidance = generate_career_roadmap(resume_text)
            st.write(career_guidance)

elif tab_selection == "🛠 Missing Skills & How to Learn Them":
    st.subheader("🛠 Missing Skills & How to Learn Them")
    if resume_text:
        if st.button("📚 Identify Missing Skills"):
            def find_missing_skills(resume_text):
                prompt = f"""
                You are an AI Skill Analyzer. Analyze the following resume and provide missing skills:

                ✅ *Existing Skills*: List the current skills of the user.
                ❌ *Missing Skills*: Identify skills required for industry standards.
                🎯 *How to Learn Them*: Provide learning resources (courses, books, projects).
                🔥 *Importance of These Skills*: Explain how these skills will improve job opportunities.

                Resume:
                {resume_text}
                """
                return chat_with_gemini(prompt)

            missing_skills = find_missing_skills(resume_text)
            st.write(missing_skills)

elif tab_selection == "📜 Certifications & Course Recommendations":
    st.subheader("📜 Certifications & Course Recommendations")
    if resume_text:
        if st.button("🎓 Get Course Recommendations"):
            def recommend_certifications(resume_text):
                prompt = f"""
                You are an AI Career Coach. Analyze the following resume and suggest relevant certifications & courses:

                ✅ *Top 5 Certifications*: Industry-recognized certifications that align with the user’s skills and career path.
                📚 *Top 5 Online Courses*: From platforms like Coursera, Udemy, LinkedIn Learning, or edX.
                🔥 *Why These Certifications?*: Explain why these certifications/courses will boost their career.
                🛠 *Preparation Resources*: Provide book or website recommendations.

                Resume:
                {resume_text}
                """
                return chat_with_gemini(prompt)

            courses = recommend_certifications(resume_text)
            st.write(courses)

elif tab_selection == "💰 Expected Salaries & Job Roles":
    st.subheader("💰 Expected Salaries & Job Roles")
    if resume_text:
        if st.button("💼 Get Salary & Job Role Insights"):
            def get_salary_and_jobs(resume_text):
                prompt = f"""
                You are an AI Career Consultant. Analyze the following resume and provide structured salary insights:

                💼 *Best Job Roles*: Suggest top job roles based on user’s skills, experience, and industry trends.
                🌎 *Salary Estimates by Region*:
                   - *USA*: $XX,XXX - $XX,XXX per year
                   - *UK*: £XX,XXX - £XX,XXX per year
                   - *India*: ₹XX,XX,XXX - ₹XX,XX,XXX per year
                   - *Remote/Global*: $XX,XXX per year (varies based on employer)
                📈 *Career Growth Insights*: How salaries and opportunities increase with upskilling.
                🔥 *Top Industries Hiring*: Which industries are in demand for the user's skills?

                Resume:
                {resume_text}
                """
                return chat_with_gemini(prompt)

            salary_and_jobs = get_salary_and_jobs(resume_text)
            st.write(salary_and_jobs)

elif tab_selection == "📢 Resume Feedback via AI Chat":
    st.subheader("📢 Ask AI About Your Resume")
    st.markdown("💬 Type any question about your resume, and AI will provide detailed guidance!")

    if resume_text:
        user_question = st.text_input("❓ Ask anything about your resume:")
        
        if user_question:
            with st.spinner("🤖 AI is analyzing your resume..."):
                prompt = f"""
                You are an expert AI Resume Consultant. A user has uploaded their resume and is asking the following question:

                *Question:* {user_question}
                
                *Resume:* 
                {resume_text}

                Provide a *detailed, structured, and insightful* response, including:
                - *Key observations* from their resume.
                - *Actionable improvements* tailored to their experience.
                - *Industry best practices* for better job opportunities.
                """
                response = chat_with_gemini(prompt)
                st.write("💡 *AI Response:*")
                st.write(response)

elif tab_selection == "📢 Personalized Job Alerts":
    st.subheader("🔔 Personalized Job Alerts")

    job_title = st.text_input("🎯 Enter Job Title (e.g., Data Scientist, Software Engineer)")
    location = st.text_input("📍 Preferred Location (e.g., Remote, New York, Bangalore)")
    
    if st.button("🔍 Find Jobs Now"):
        if job_title and location:
            st.success(f"🔗 Here are job links for **{job_title}** in **{location}**:")

            indeed_url = f"https://www.indeed.com/jobs?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}"
            linkedin_url = f"https://www.linkedin.com/jobs/search?keywords={job_title.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
            naukri_url = f"https://www.naukri.com/{job_title.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
            google_jobs_url = f"https://www.google.com/search?q={job_title.replace(' ', '+')}+jobs+in+{location.replace(' ', '+')}"

            st.markdown(f"[🟢 Indeed Jobs]({indeed_url})")
            st.markdown(f"[🔵 LinkedIn Jobs]({linkedin_url})")
            st.markdown(f"[🟠 Naukri Jobs]({naukri_url})")
            st.markdown(f"[🔴 Google Jobs]({google_jobs_url})")

            webbrowser.open(indeed_url)
            webbrowser.open(linkedin_url)
            webbrowser.open(naukri_url)
            webbrowser.open(google_jobs_url)
        else:
            st.error("⚠️ Please enter both job title and location to get job alerts.")

elif tab_selection == "💡 Soft Skills Analysis & Improvement":
    st.subheader("💡 Soft Skills Analysis & Improvement")

    if uploaded_file:
        resume_text = extract_text(uploaded_file)  # Ensure resume_text is defined
        soft_skills_prompt = f"""
        You are an AI Soft Skills Analyzer. Based on the resume, identify the candidate's **soft skills** and suggest ways to improve them:
        
        ✅ **Identified Soft Skills**
        ✅ **Why these skills are important**
        ✅ **Recommended activities to strengthen them**
        ✅ **Online courses or books to improve them**
        
        Resume:
        {resume_text}
        """
        if st.button("📚 Get Soft Skills Insights"):
            soft_skills_analysis = chat_with_gemini(soft_skills_prompt)
            st.write(soft_skills_analysis)
    else:
        st.warning("Please upload a resume to analyze soft skills.")
