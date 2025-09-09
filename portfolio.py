import google.generativeai as genai
from google.api_core import exceptions
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("Error: Please set GEMINI_API_KEY in .env file")
    exit(1)

genai.configure(api_key=api_key)

def enhance_with_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        if response.text:
            return response.text.strip()
        return prompt  
    except exceptions.NotFound:
        print("Error: Gemini API model not found. Please check your API key and model version.")
        return prompt
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return prompt

name = input("Enter your name: ")
education = input("Enter your education details: ")
skills = input("Enter your skills (comma separated): ")
project = input("Enter a project title and details: ")
experience = input("Enter your experience/internship: ")
certifications = input("Enter your certifications (optional): ")

skills_prompt = f"""
Rewrite and expand the following skills into a professional format suitable for a student portfolio.
Explain technical expertise and practical applications where possible. 
Keep it concise but impactful .
Skills: {skills}
"""

project_prompt = f"""
Write a polished description for this student project.
Highlight the purpose, technologies used, outcomes, and the student's role.
Keep it professional and around .
Project: {project}
"""

experience_prompt = f"""
Create a professional description of the following experience or internship. 
Use bullet points if possible, focusing on key responsibilities, tools/technologies, and achievements.
Make it sound like resume-style content.
Experience: {experience}
"""

certifications_prompt = f"""
Format the following certifications professionally for a portfolio. 
Include the certification name, issuing organization, and (if available) year of completion.
List them as bullet points.
Certifications: {certifications}
"""

education_prompt = f"""
Summarize the student's education details into a professional format for a portfolio.
Include degree, field of study, institution, and any honors/achievements.
Keep it 2–3 sentences long.
Education: {education}
"""

about_prompt = f"""
Write a professional 'About Me' section for a student named {name}.
Base it on the following:
- Education: {education}
- Skills: {skills}
- Projects: {project}
- Experience: {experience}
- Certifications: {certifications}

Guidelines:
- Length: 3–4 sentences.
- Tone: Confident, positive, and professional.
- Focus: Career goals, technical strengths, and key achievements.
- Make it sound like a student who is career-ready.
"""

skills_final = enhance_with_gemini(skills_prompt)
project_final = enhance_with_gemini(project_prompt)
experience_final = enhance_with_gemini(experience_prompt)
certifications_final = enhance_with_gemini(certifications_prompt)
education_final = enhance_with_gemini(education_prompt)
about_final = enhance_with_gemini(about_prompt)

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{name}'s Portfolio</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1, h2 {{ color: #2c3e50; }}
        p {{ font-size: 16px; line-height: 1.5; }}
        ul {{ margin: 0; padding-left: 20px; }}
        .section {{ margin-bottom: 30px; }}
    </style>
</head>
<body>
    <h1>{name}'s Portfolio</h1>
    <div class="section">
        <h2>About Me</h2>
        <p>{about_final}</p>
    </div>
    <div class="section">
        <h2>Education</h2>
        <p>{education_final}</p>
    </div>
    <div class="section">
        <h2>Skills</h2>
        <p>{skills_final}</p>
    </div>
    <div class="section">
        <h2>Projects</h2>
        <p>{project_final}</p>
    </div>
    <div class="section">
        <h2>Experience</h2>
        <p>{experience_final}</p>
    </div>
    <div class="section">
        <h2>Certifications</h2>
        <p>{certifications_final}</p>
    </div>
</body>
</html>
"""

with open("portfolio.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("\n✅ Portfolio generated successfully! Open 'portfolio.html' in your browser.")
