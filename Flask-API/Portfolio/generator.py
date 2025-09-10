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
        "about": enhance_content("Rewrite as a professional 2-sentence bio:", data.get("about", "")),
        "education": f"{data.get('degree', '')} - {data.get('collegeName', '')}, {data.get('yearOfPassing', '')}",
        "skills": [enhance_content("Return only the skill name:", skill.strip()) for skill in data.get("skills", "").split(",") if skill.strip()],
        "projects": data.get("projects", []),
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
