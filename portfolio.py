import os
import json
from jinja2 import Environment, FileSystemLoader
import google.generativeai as genai


# ---------- Configure Gemini ----------
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def enhance_content(prompt, user_input):
    """Use Gemini to improve the content before injecting into the template."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"{prompt}\nUser input: {user_input}")
    return response.text if response.text else user_input

# ---------- Collect User Data ----------
def collect_user_data():
    print("📌 Please provide details for your portfolio:\n")

    name = input("Your Name: ")
    about = input("Short Bio/About You: ")
    education = input("Education: ")

    # Skills (list)
    skills = []
    print("\nEnter your skills (type 'done' when finished):")
    while True:
        skill = input("- ")
        if skill.lower() == "done":
            break
        skills.append(enhance_content("Polish this skill for a portfolio bullet.", skill))

    # Experience (list)
    experience = []
    print("\nEnter your experiences (type 'done' when finished):")
    while True:
        exp = input("- ")
        if exp.lower() == "done":
            break
        experience.append(enhance_content("Polish this work/experience item.", exp))

    # Projects (list)
    projects = []
    print("\nEnter your projects (type 'done' when finished):")
    while True:
        proj = input("- ")
        if proj.lower() == "done":
            break
        projects.append(enhance_content("Format this project description for a portfolio card.", proj))

    # Certifications (list)
    certifications = []
    print("\nEnter your certifications (type 'done' when finished):")
    while True:
        cert = input("- ")
        if cert.lower() == "done":
            break
        certifications.append(enhance_content("Polish this certification entry.", cert))

    return {
        "name": name,
        "about": about,
        "education": education,
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    }

# ---------- Generate Portfolio ----------
def generate_portfolio(data):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template_portfolio.html")

    html_content = template.render(**data)

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "portfolio.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n✅ Portfolio generated successfully! Open '{output_path}' in your browser.")

# ---------- Run ----------
if __name__ == "__main__":
    with open("sample-data.json", "r") as f:
        user_data = json.load(f)
    generate_portfolio(user_data)

