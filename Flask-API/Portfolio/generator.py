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

    # ✅ Generate skills based on GitHub projects
    def generate_skills_from_projects(projects):
        language_count = {}
        total_projects = len(projects)
        
        # Count languages from projects
        for project in projects:
            lang = project.get("language", "")
            if lang and lang != "Not specified":
                language_count[lang] = language_count.get(lang, 0) + 1
        
        # Calculate percentages and create skills
        skills_with_percentages = []
        for lang, count in language_count.items():
            # Base percentage on project count, with minimum 60% and maximum 95%
            percentage = min(95, max(60, int((count / total_projects) * 100) + 40))
            skills_with_percentages.append({"name": lang, "percentage": percentage})
        
        # Add common web technologies if not present
        existing_langs = [skill["name"] for skill in skills_with_percentages]
        common_skills = {
            "HTML/CSS": 85,
            "Git": 90,
            "REST APIs": 80
        }
        
        for skill, percentage in common_skills.items():
            if not any(existing in skill for existing in existing_langs):
                skills_with_percentages.append({"name": skill, "percentage": percentage})
        
        return skills_with_percentages
    
    # Get projects for skill analysis
    raw_projects = data.get("projects", [])
    if raw_projects:
        enhanced_skills = generate_skills_from_projects(raw_projects)
    else:
        # Fallback to manual skills if no projects
        skills_data = data.get("skills", "")
        if isinstance(skills_data, str):
            raw_skills = [s.strip() for s in skills_data.split(",") if s.strip()]
        else:
            raw_skills = skills_data if isinstance(skills_data, list) else []
        enhanced_skills = [{"name": skill, "percentage": 80} for skill in raw_skills] if raw_skills else []

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
    print(f"Raw achievements data: {raw_achievements}")
    print(f"Raw achievements type: {type(raw_achievements)}")
    
    # Handle different data formats
    if isinstance(raw_achievements, str):
        # If it's a string, split by comma or newline
        raw_achievements = [a.strip() for a in raw_achievements.replace('\n', ',').split(',') if a.strip()]
    elif not isinstance(raw_achievements, list):
        raw_achievements = []
    
    enhanced_achievements = []
    for achievement in raw_achievements:
        print(f"Processing achievement: {achievement}, type: {type(achievement)}")
        # Convert to string if it's not already
        achievement_str = str(achievement).strip() if achievement else ""
        if achievement_str:
            enhanced_desc = enhance_content(
                "Transform this achievement into a compelling professional accomplishment with specific details and impact:",
                achievement_str
            )
            enhanced_achievements.append(enhanced_desc)
        else:
            print(f"Achievement filtered out: {achievement}")
    print(f"Final enhanced achievements: {enhanced_achievements}")

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
