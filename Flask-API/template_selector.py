import os
import json
from jinja2 import Environment, FileSystemLoader
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_available_templates():
    """Get list of available templates"""
    template_dir = "templates"
    if not os.path.exists(template_dir):
        template_dir = "Flask-API/Portfolio/templates"
    
    templates = []
    if os.path.exists(template_dir):
        for file in os.listdir(template_dir):
            if file.endswith('.html'):
                templates.append(file)
    return templates

def select_template():
    """Allow user to select a template"""
    templates = get_available_templates()
    
    if not templates:
        print("❌ No templates found!")
        return None
    
    print("📋 Available Templates:")
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template}")
    
    while True:
        try:
            choice = int(input("\nSelect template number: ")) - 1
            if 0 <= choice < len(templates):
                return templates[choice]
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")

def collect_portfolio_data():
    """Collect portfolio data from user"""
    print("\n📝 Enter your portfolio information:")
    
    data = {
        "name": input("Your Name: "),
        "about": input("About Me (brief description): "),
        "education": input("Education: "),
        "skills": [],
        "experience": [],
        "projects": [],
        "certifications": []
    }
    
    # Collect skills
    print("\nEnter your skills (type 'done' when finished):")
    while True:
        skill = input("Skill: ")
        if skill.lower() == 'done':
            break
        data["skills"].append(skill)
    
    # Collect experience
    print("\nEnter your experience (type 'done' when finished):")
    while True:
        exp = input("Experience: ")
        if exp.lower() == 'done':
            break
        data["experience"].append(exp)
    
    # Collect projects
    print("\nEnter your projects (type 'done' when finished):")
    while True:
        project = input("Project: ")
        if project.lower() == 'done':
            break
        data["projects"].append(project)
    
    # Collect certifications
    print("\nEnter your certifications (type 'done' when finished):")
    while True:
        cert = input("Certification: ")
        if cert.lower() == 'done':
            break
        data["certifications"].append(cert)
    
    return data

def generate_portfolio_with_template(template_name, data):
    """Generate portfolio using selected template and data"""
    try:
        # Try different template directories
        template_dirs = ["templates", "Flask-API/Portfolio/templates", "."]
        env = None
        
        for template_dir in template_dirs:
            if os.path.exists(os.path.join(template_dir, template_name)):
                env = Environment(loader=FileSystemLoader(template_dir))
                break
        
        if not env:
            print(f"❌ Template {template_name} not found!")
            return False
        
        template = env.get_template(template_name)
        html_content = template.render(**data)
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", "portfolio.html")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\n✅ Portfolio generated successfully!")
        print(f"📁 Output: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating portfolio: {str(e)}")
        return False

def main():
    """Main function to run the template selector"""
    print("🌉 PathBridge Portfolio Generator")
    print("=" * 40)
    
    # Step 1: Select template
    template_name = select_template()
    if not template_name:
        return
    
    print(f"\n✅ Selected template: {template_name}")
    
    # Step 2: Collect data
    data = collect_portfolio_data()
    
    # Step 3: Generate portfolio
    generate_portfolio_with_template(template_name, data)

if __name__ == "__main__":
    main()