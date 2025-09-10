import os
from jinja2 import Environment, FileSystemLoader
from .enhancer import enhance_content


def generate_portfolio(data: dict) -> str:
    """
    Generate a portfolio HTML file using user-provided data.
    
    Args:
        data (dict): Dictionary with keys like name, about, education, skills, experience, projects, certifications.
    
    Returns:
        str: Path to the generated portfolio HTML file.
    """

    # ✅ Process data according to new structure
    enhanced_data = {
        "name": data.get("name", ""),
        "about": enhance_content("Transform this into a compelling professional bio that highlights key strengths, experience, and passion. Make it engaging and concise (2-3 sentences):", data.get("about", "")),
        "education": f"{data.get('degree', '')} - {data.get('collegeName', '')}, {data.get('yearOfPassing', '')}",
        "skills": [enhance_content("Return only the skill name:", skill.strip()) for skill in data.get("skills", "").split(",") if skill.strip()],
        "linkedinUrl": data.get("linkedinUrl", ""),
        "githubUrl": data.get("githubUrl", ""),
        "projects": [{"name": project.get("name", ""), "description": enhance_content("Rewrite this project description to be more compelling and professional. Highlight the key technologies, features, and impact. Keep it concise but impressive:", project.get("description", ""))} for project in data.get("projects", [])],
        "experience": data.get("experiences", []),
        "certifications": data.get("certifications", []),
    }

    # ✅ Jinja2 setup (looks for template in Portfolio/templates/)
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
