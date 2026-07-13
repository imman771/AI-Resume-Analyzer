from datetime import datetime
from flask import Flask, render_template, request, send_file, send_from_directory
from PyPDF2 import PdfReader
from pymongo import MongoClient
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# =====================================
# MongoDB Connection
# =====================================

client = MongoClient("mongodb://localhost:27017/")

db = client["resume_analyzer"]

collection = db["analysis_history"]

# =====================================
# Create uploads folder if it doesn't exist
# =====================================

if not os.path.exists("uploads"):
    os.makedirs("uploads")
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# =====================================
# Skills Database
# =====================================

skills_database = [
    "python",
    "sql",
    "power bi",
    "tableau",
    "excel",
    "machine learning",
    "data science",
    "deep learning",
    "statistics",
    "pandas",
    "numpy",
    "matplotlib",
    "tensorflow",
    "pytorch",
    "flask",
    "django",
    "html",
    "css",
    "php",
    "mongodb"
]
resume_sections = [

    "education",

    "skills",

    "projects",

    "experience",

    "certifications",

    "internship",

    "languages",

    "achievements"

]
# =====================================
# Home Page
# =====================================

@app.route('/', methods=['GET', 'POST'])
def home():
    resume_rating = ""
    job_description = ""
    ats_score = 0
    matched_skills = []
    missing_skills = []
    suggestions = []
    resume_name = ""
    resume_path = None
    found_sections = []
    missing_sections = []
    completeness_score = 0
    

    if request.method == 'POST':

        job_description = request.form['job_description']
        if not job_description.strip():
            return render_template( "index.html",error="Please enter a job description.")

        resume = request.files.get('resume')
        if not resume or resume.filename == "":
            return render_template("index.html",error="Please upload a resume PDF.")

        if resume:
            if not allowed_file(resume.filename):
                return render_template("index.html",error="Only PDF files are allowed.")
            
            resume_name = resume.filename

            file_path = os.path.join(
                "uploads",
                resume.filename
            )

            resume.save(file_path)

            resume_path = file_path

            # =============================
            # Read Resume PDF
            # =============================

            reader = PdfReader(file_path)

            resume_text = ""

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    resume_text += text

            print("\nResume Text:\n")
            print(resume_text)

            # =============================
            # Extract Job Skills
            # =============================

            job_skills = []

            for skill in skills_database:

                if skill.lower() in job_description.lower():
                    job_skills.append(skill)

            print("\nJob Skills:")
            print(job_skills)

            # =============================
            # Extract Resume Skills
            # =============================

            resume_skills = []

            for skill in skills_database:

                if skill.lower() in resume_text.lower():
                    resume_skills.append(skill)

            print("\nResume Skills:")
            print(resume_skills)

            # =============================
            # Matched Skills
            # =============================

            matched_skills = []

            for skill in job_skills:

                if skill in resume_skills:
                    matched_skills.append(skill)

            print("\nMatched Skills:")
            print(matched_skills)

            # =============================
            # ATS Score
            # =============================

            if len(job_skills) > 0:

                ats_score = (
                    len(matched_skills) /
                    len(job_skills)
                ) * 100

            else:

                ats_score = 0

            ats_score = round(ats_score, 2)

            print("\nATS Score:")
            print(ats_score, "%")

            # =============================
            # Resume Strength Meter
            # =============================

            if ats_score >= 80:

                resume_rating = "Excellent"

            elif ats_score >= 60:

                resume_rating = "Good"

            elif ats_score >= 40:

                resume_rating = "Average"

            else:

                 resume_rating = "Needs Improvement"

            print("\nResume Rating:")
            print(resume_rating)

            # =============================
            # Missing Skills
            # =============================

            missing_skills = []

            for skill in job_skills:

                if skill not in resume_skills:
                    missing_skills.append(skill)
            print("\nMissing Skills:")
            print(missing_skills)
            # =====================================
            # Resume Completeness Check
            # =====================================

            found_sections = []

            missing_sections = []

            for section in resume_sections:

                if section.lower() in resume_text.lower():

                    found_sections.append(section)

                else:

                    missing_sections.append(section)

            print("\nFound Sections:")
            print(found_sections)

            print("\nMissing Resume Sections:")
            print(missing_sections)

            # =====================================
            # Resume Completeness Score
            # =====================================

            completeness_score = (
                len(found_sections) /
                len(resume_sections)
            ) * 100

            completeness_score = round(completeness_score, 2)

            print("\nResume Completeness Score:")
            print(completeness_score, "%")

            # =============================
            # Suggestions
            # =============================

            suggestions = []

# =============================
# Smart AI Suggestions
# =============================

# Missing Skills Suggestions
            for skill in missing_skills:

                if skill == "python":
                 suggestions.append(
                 "🐍 Add Python to improve your programming profile."
                )

                elif skill == "sql":
                    suggestions.append(
                    "🗄️ Add SQL to strengthen your database skills."
                )

                elif skill == "tableau":
                    suggestions.append(
                    "📊 Add Tableau to improve your data visualization profile."
                )

                elif skill == "power bi":
                    suggestions.append(
                    "📈 Add Power BI to showcase business intelligence skills."
                )

                elif skill == "excel":
                    suggestions.append(
                    "📑 Add Excel to improve your data analysis profile."
                )

                elif skill == "machine learning":
                    suggestions.append(
                     "🤖 Add Machine Learning to match AI-related jobs."
                )

                elif skill == "statistics":
                    suggestions.append(
                    "📉 Add Statistics to strengthen analytical capability."
                )

                else:
                    suggestions.append(
                    f"✅ Consider adding {skill.title()} to improve ATS matching."
                )


# Missing Resume Sections Suggestions
            for section in missing_sections:

                if section == "experience":
                    suggestions.append(
                "💼 Add an Experience section to increase recruiter confidence."
                )

                elif section == "projects":
                    suggestions.append(
                    "🚀 Add projects with measurable achievements."
                )

                elif section == "certifications":
                    suggestions.append(
                    "🏆 Include relevant certifications."
                )

                elif section == "internship":
                    suggestions.append(
                    "🎯 Add internship experience if available."
                )

                elif section == "achievements":
                    suggestions.append(
                    "🥇 Highlight your achievements to stand out."
                )

                else:
                     suggestions.append(
                    f"📄 Consider adding a {section.title()} section."
                )   

                print("\nSuggestions:")
                print(suggestions)
        #Recomandation based on ATS Score#
                if ats_score >= 85:
                    recommendation = "Excellent! Your resume is ready."

                elif ats_score >= 70:
                    recommendation = "Good resume. Minor improvements recommended."

                elif ats_score >= 55:
                    recommendation = "Average resume. Add more skills and projects."

                else:
                    recommendation = "Improve your resume before applying."
            
        # =============================
        # Save Analysis in MongoDB
        # =============================

                analysis = {

                    "resume_name": resume_name,

                    "job_description": job_description,

                    "job_skills": job_skills,

                    "resume_skills": resume_skills,

                    "matched_skills": matched_skills,

                    "missing_skills": missing_skills,

                    "found_sections": found_sections,

                    "missing_resume_sections": missing_sections,

                    "resume_completeness_score": completeness_score,

                    "resume_rating": resume_rating,

                    "suggestions": suggestions,

                    "ats_score": ats_score,

                    "matched_count": len(matched_skills),

                    "missing_count": len(missing_skills),

                    "recommendation": recommendation

            }
                print("\n===== Analysis Data =====")
                print(analysis)
                result = collection.insert_one(analysis)
                print("Inserted ID:", result.inserted_id)

                print("\n✅ Analysis Saved Successfully to MongoDB")

    return render_template("index.html",

        job_description=job_description,

        ats_score=ats_score,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        resume_name=resume_name,

        resume_path=resume_path,

        suggestions=suggestions,

        found_sections=found_sections,

        missing_sections=missing_sections,

        completeness_score=completeness_score,

        resume_rating=resume_rating

)
# =====================================
# Download PDF Report
# =====================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

@app.route("/download_report")
def download_report():

    latest_analysis = collection.find_one(
        sort=[("_id", -1)]
    )

    if latest_analysis is None:
        return "No analysis found. Please analyze a resume first."
    
    pdf_file = "Resume_Report.pdf"

    c = canvas.Canvas(pdf_file, pagesize=letter)

    width, height = letter
# =====================================
# Create Skill Match Chart
# =====================================

    matched = len(latest_analysis["matched_skills"])
    missing = len(latest_analysis["missing_skills"])

    plt.figure(figsize=(3,3))

    plt.pie([matched, missing],
    labels=None,
    colors=["green", "red"],
    autopct="%1.0f%%",
    startangle=90)
    plt.axis("equal")

    chart_path = os.path.join(app.root_path, "static", "images", "skill_chart.png")

    plt.savefig(chart_path, bbox_inches="tight")

    plt.close()

# =====================================
# Continue PDF
# =====================================
    c.rect(
    30,
    30,
    550,
    730
)

# =====================================
# Report Title
# =====================================

    c.setFillColor(colors.HexColor("#0d6efd"))

    c.rect(
        0,
        height-70,
        width,
        70,
        fill=1,
    stroke=0
)

# White Title

    c.setFillColor(colors.white)

    c.setFont("Helvetica-Bold", 24)

    c.drawCentredString(
    width/2,
    height-45,
    "AI Resume Analyzer Report")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)

    generated_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    c.drawString(60,height - 85,f"Generated On: {generated_time}")

# Back to Black

    c.setFillColor(colors.black)

# =====================================
# Basic Details
# =====================================

    y = 680

   # Resume Details Heading
    c.setFillColor(colors.darkblue)

    c.setFont("Helvetica-Bold", 18)

    c.drawString(50, y, "Resume Details")

    # underline
    c.line(60, y-5, 260, y-5)

    c.setFillColor(colors.black)


    y -= 25

    c.setFont("Helvetica", 12)

    c.drawString(
    60,
    y,
    f"Resume Name : {latest_analysis['resume_name']}"
)

    y -= 20

    c.drawString(
    60,
    y,
    f"ATS Score : {latest_analysis['ats_score']}%"
    )
    

    y -= 20

    c.drawString(
    60,
    y,
    f"Resume Completeness : {latest_analysis['resume_completeness_score']}%"
)

    y -= 20

    rating = latest_analysis["resume_rating"]
 # Resume Rating
    c.drawString(
        60,
        y,
        "Resume Strength :"
)

    ats = latest_analysis["ats_score"]

    if ats >= 85:
        badge = "Excellent"
        badge_color = colors.green
    elif ats >= 70:
        badge = "Very Good"
        badge_color = colors.darkgreen
    elif ats >= 55:
        badge = "Good"
        badge_color = colors.blue
    elif ats >= 40:
        badge = "Average"
        badge_color = colors.orange
    else:
        badge = "Needs Improvement"
        badge_color = colors.red

    c.setFillColor(badge_color)
    c.roundRect(180, y-6, 120, 20, 5, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(240, y, badge)

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)

    c.setFillColor(colors.black)
    # =====================================
# Matched Skills
# =====================================

    y -= 30

    c.setFillColor(colors.darkblue)

    c.setFont("Helvetica-Bold", 18)

    c.drawString(50, y, "Matched Skills")

    c.line(50, y-5, 300, y-5)

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)

    y -= 20
    for skill in latest_analysis["matched_skills"]:
      c.drawString(70, y, f"✓ {skill.title()}")
      y -= 18

# =====================================
# Missing Skills
# =====================================

    y -= 15
    c.setFillColor(colors.darkblue)

    c.setFont("Helvetica-Bold", 18)

    c.drawString(50, y, "Missing Skills")

    c.line(50, y-5, 300, y-5)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)

    y -= 30

    for skill in latest_analysis["missing_skills"]:
        c.drawString(70, y, f"✗ {skill.title()}")
        y -= 18

# =====================================
# Suggestions
# =====================================

    y -= 15

    c.setFillColor(colors.darkblue)

    c.setFont("Helvetica-Bold", 18)

    c.drawString(50, y, "Suggestions")

    c.line(50, y-5, 300, y-5)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)

    y -= 20

    for suggestion in latest_analysis["suggestions"]:

     lines = simpleSplit( "• " + suggestion,"Helvetica", 12, 320)

     for line in lines:
        c.drawString(70, y, line)
        y -= 18
    total_skills = len(latest_analysis["job_skills"])
    matched_count = len(latest_analysis["matched_skills"])
    missing_count = len(latest_analysis["missing_skills"])

    if total_skills > 0:
        match_percentage = round((matched_count / total_skills) * 100, 2)
    else:
        match_percentage = 0
    y -= 5
# ==========================
# Resume Summary
# ==========================

    y -= 20

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)

    c.drawString(60, y, "Resume Summary")

    c.line(60, y-5, 260, y-5)

    y -= 30

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)

    c.drawString(60, y, f"ATS Score : {latest_analysis['ats_score']}%")

    y -= 20
    c.drawString(60, y, f"Resume Rating : {latest_analysis['resume_rating']}")

    y -= 20

    c.drawString(
    60,
    y,
    f"Job Skills : {total_skills}"
)


    y -= 20

    c.drawString(
    60,
    y,
    f"Matched Skills : {matched_count}"
)

    y -= 20

    c.drawString(
    60,
    y,
    f"Missing Skills : {missing_count}"
)

    y -= 20

    c.drawString(
    60,
    y,
    f"Match Percentage : {match_percentage}%"
)

    y -= 20
    c.drawString(60, y, f"Recommendation : {latest_analysis['recommendation']}")
    # =====================================
# Footer
# =====================================

    c.setFont("Helvetica-Oblique", 9)

    c.setFillColor(colors.grey)

    c.drawCentredString(
    width/2,
    20,
    "Generated by AI Resume Analyzer"
)
# ===========================
# Skill Match Chart
# ===========================

    chart_x = 360
    chart_y = 380

# Title
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)

    c.drawCentredString(chart_x + 95, 575, "Skill Match Chart")

# Underline
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)

    c.line(chart_x,570,chart_x + 190,570)

# Pie Chart
    c.drawImage(chart_path,chart_x,chart_y,width=190,height=190)

    c.setFillColor(colors.black)
# Save PDF
    c.save()
    return send_file(
      pdf_file,
      as_attachment=True
)
# =====================================
# Run Flask
# =====================================


if __name__ == '__main__':
    app.run(debug=True)
    