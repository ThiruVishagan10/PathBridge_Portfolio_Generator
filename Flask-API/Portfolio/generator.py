import os
from jinja2 import Environment, FileSystemLoader
from .enhancer import enhance_content, enhance_batch


def generate_portfolio(data: dict) -> str:
    """
    Generate a portfolio HTML file using user-provided data.
    
    Args:
        data (dict): Dictionary with keys like name, about, education, skills, experience, projects, certifications.
    
    Returns:
        str: Path to the generated portfolio HTML file.
    """

    # ✅ Enhance single fields
    enhanced_about = enhance_content(
        "Transform this into a compelling professional bio (2-3 sentences):",
        data.get("about", "")
    )

    # ✅ Enhance skills (batch)
    skills_data = data.get("skills", "")
    if isinstance(skills_data, str):
        raw_skills = [s.strip() for s in skills_data.split(",") if s.strip()]
    else:
        raw_skills = skills_data if isinstance(skills_data, list) else []
    enhanced_skills = enhance_batch(
        "Return only the polished skill names:",
        raw_skills
    ) if raw_skills else []

    # ✅ Enhance project descriptions (batch)
    raw_projects = data.get("projects", [])
    project_descriptions = [p.get("description", "") for p in raw_projects if p.get("description")]
    enhanced_project_descriptions = enhance_batch(
        "Rewrite each project description professionally. Highlight technologies, features, and impact:",
        project_descriptions
    )
    enhanced_projects = [
        {
            "name": raw_projects[i].get("name", ""),
            "description": enhanced_project_descriptions[i] if i < len(enhanced_project_descriptions) else raw_projects[i].get("description", ""),
            "url": raw_projects[i].get("url", ""),
            "language": raw_projects[i].get("language", ""),
            "stars": raw_projects[i].get("stars", 0),
            "forks": raw_projects[i].get("forks", 0),
        }
        for i in range(len(raw_projects))
    ]

    # ✅ Enhance certifications (batch)
    raw_certs = data.get("certifications", [])
    # Filter out empty strings and ensure we have valid certification data
    valid_certs = [cert for cert in raw_certs if cert and isinstance(cert, str) and cert.strip()]
    enhanced_certs = enhance_batch(
        "Provide detailed descriptions for these certifications including what skills they validate and their industry value:",
        valid_certs
    ) if valid_certs else []
    
    # ✅ Enhance achievements
    raw_achievements = data.get("achievements", [])
    enhanced_achievements = []
    for achievement in raw_achievements:
        if achievement and isinstance(achievement, str) and achievement.strip():
            enhanced_desc = enhance_content(
                "Transform this achievement into a compelling professional accomplishment with specific details and impact:",
                achievement
            )
            enhanced_achievements.append(enhanced_desc)

    # ✅ Enhance education
    raw_education = f"{data.get('degree', '')} - {data.get('collegeName', '')}, {data.get('yearOfPassing', '')}"
    enhanced_education = enhance_content(
        "Enhance this education information to be more descriptive and professional:",
        raw_education
    )

    # ✅ Enhance experience descriptions
    raw_experiences = data.get("experiences", [])
    enhanced_experiences = []
    for exp in raw_experiences:
        enhanced_desc = enhance_content(
            "Create a detailed professional job description with specific responsibilities, technologies used, and key achievements. Include 3-4 bullet points of what this role involves:",
            f"{exp.get('role', '')} at {exp.get('companyName', '')}"
        ) if exp.get('role') else ""
        enhanced_experiences.append({
            "role": exp.get("role", ""),
            "companyName": exp.get("companyName", ""),
            "duration": exp.get("duration", ""),
            "description": enhanced_desc
        })

    # ✅ Build enhanced data dict
    enhanced_data = {
        "name": data.get("name", ""),
        "about": enhanced_about,
        "education": enhanced_education,
        "skills": enhanced_skills,
        "linkedinUrl": data.get("linkedinUrl", ""),
        "githubUrl": data.get("githubUrl", ""),
        "projects": enhanced_projects,
        "experience": enhanced_experiences,
        "certifications": enhanced_certs,
        "achievements": enhanced_achievements,
    }

    # ✅ Jinja2 setup
    env = Environment(loader=FileSystemLoader("Portfolio/templates"))
    template = env.get_template("template_portfolio.html")

    # ✅ Render HTML
    html_content = template.render(**enhanced_data)

    # ✅ Save to output folder
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "portfolio.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_content
