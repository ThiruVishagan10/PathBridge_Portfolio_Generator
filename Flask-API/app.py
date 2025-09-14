from flask import Flask, request, jsonify, render_template, session, send_file
from flask_cors import CORS
import os
import json
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.secret_key = 'portfolio_generator_secret_key'
CORS(app, supports_credentials=True)

def get_available_templates():
    """Get list of available templates"""
    return [
        {'name': 'Modern', 'file': 'template_modern.html', 'description': 'Modern glassmorphism design with video background'},
        {'name': 'Creative', 'file': 'template_creative.html', 'description': 'Creative design with animations and unique layouts'},
        {'name': 'Minimal', 'file': 'tamplate_minimal.html', 'description': 'Clean minimal design focused on content'}
    ]

@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page with template selection or generate portfolio"""
    if request.method == 'POST':
        # Handle portfolio generation at root endpoint
        return generate_portfolio()
    
    # GET request - return API info
    templates = get_available_templates()
    return jsonify({
        'message': 'PathBridge Portfolio Generator API',
        'available_templates': templates,
        'endpoints': {
            'GET /templates': 'Get available templates',
            'GET /api/templates': 'Template API - Get available templates',
            'GET /api/template/<name>': 'Template API - Get specific template',
            'POST /': 'Generate portfolio with template and data',
            'POST /generate': 'Generate portfolio with template and data'
        }
    })

@app.route('/templates', methods=['GET'])
def get_templates():
    """Get available templates"""
    templates = get_available_templates()
    return jsonify({'templates': templates})

@app.route('/template', methods=['GET', 'POST'])
def get_template():
    """Get available templates or handle template selection"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Check if this is template selection (only templateName) or portfolio generation
        if data and len(data) == 1 and 'templateName' in data:
            # Template selection
            template_name = data.get('templateName')
            if template_name:
                session['selected_template'] = template_name
                return jsonify({
                    'success': True,
                    'message': f'Template {template_name} selected',
                    'selected_template': template_name
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'templateName is required'
                }), 400
        else:
            # Portfolio generation
            return generate_portfolio()
    
    # GET request - return templates
    templates = get_available_templates()
    return jsonify({'templates': templates})

@app.route('/api/templates', methods=['GET'])
def api_get_templates():
    """Template API - Get available templates"""
    templates = get_available_templates()
    return jsonify({
        'success': True,
        'templates': templates
    })

@app.route('/api/template/<template_name>', methods=['GET'])
def api_get_template_details(template_name):
    """Template API - Get specific template details"""
    templates = get_available_templates()
    template = next((t for t in templates if t['name'] == template_name), None)
    
    if not template:
        return jsonify({
            'success': False,
            'error': f'Template {template_name} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'template': template
    })

@app.route('/generate', methods=['POST'])
def generate_portfolio():
    """Generate portfolio with selected template and data"""
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug logging
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        template_name = data.get('templateName', 'Modern')  # Default to Modern
        portfolio_data = data.copy()  # Use entire data
        
        print(f"Template: {template_name}, Portfolio data keys: {list(portfolio_data.keys()) if isinstance(portfolio_data, dict) else 'Not a dict'}")
        
        # Remove templateName from portfolio data to avoid conflicts
        if 'templateName' in portfolio_data:
            del portfolio_data['templateName']
        
        if not portfolio_data or not portfolio_data.get('name'):
            return jsonify({'error': 'Portfolio data with name is required'}), 400
        
        # Fetch GitHub projects if GitHub URL is provided
        if portfolio_data.get('githubUrl') and not portfolio_data.get('projects'):
            try:
                import requests
                github_username = portfolio_data['githubUrl'].split('github.com/')[1].split('/')[0]
                response = requests.get(f'https://api.github.com/users/{github_username}/repos?sort=updated&per_page=6')
                
                if response.status_code == 200:
                    repos = response.json()
                    portfolio_data['projects'] = [{
                        'name': repo['name'],
                        'description': repo['description'] or f"A {repo['language']} project",
                        'url': repo['html_url'],
                        'language': repo['language']
                    } for repo in repos if not repo['fork']]
                    print(f"Fetched {len(portfolio_data['projects'])} GitHub projects")
            except Exception as e:
                print(f"Error fetching GitHub projects: {e}")
        
        # Enhance content with AI
        try:
            from Portfolio.enhancer import enhance_content
            if portfolio_data.get('about'):
                portfolio_data['about'] = enhance_content(
                    "Rewrite this about section to be more professional and engaging for a portfolio:",
                    portfolio_data['about']
                )
            if portfolio_data.get('projects'):
                for project in portfolio_data['projects']:
                    if project.get('description'):
                        project['description'] = enhance_content(
                            "Improve this project description to be more compelling and professional:",
                            project['description']
                        )
            print("Content enhanced with AI")
        except Exception as e:
            print(f"Error enhancing content: {e}")
        
        # Map template names to files
        template_map = {
            'Modern': 'template_modern.html',
            'Creative': 'template_creative.html', 
            'Minimal': 'tamplate_minimal.html'
        }
        
        template_file = template_map.get(template_name)
        if not template_file:
            return jsonify({'error': f'Template {template_name} not supported. Available: Modern, Creative, Minimal'}), 400
        
        # Check if template file exists
        template_path = os.path.join('Portfolio/templates', template_file)
        if not os.path.exists(template_path):
            return jsonify({'error': f'Template file {template_file} not found'}), 404
        
        # Generate portfolio
        env = Environment(loader=FileSystemLoader('Portfolio/templates'))
        template = env.get_template(template_file)
        html_content = template.render(**portfolio_data)
        
        # Save to output directory
        os.makedirs('output', exist_ok=True)
        output_path = os.path.join('output', 'portfolio.html')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return jsonify({
            'success': True,
            'message': 'Portfolio generated successfully',
            'output_path': output_path,
            'template_used': template_name
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview_portfolio():
    """Preview portfolio without saving"""
    try:
        data = request.get_json()
        
        template_name = data.get('templateName')
        portfolio_data = data.get('data')
        
        if not template_name or not portfolio_data:
            return jsonify({'error': 'Template name and data are required'}), 400
        
        # Map template names to files
        template_map = {
            'Modern': 'template_modern.html',
            'Creative': 'template_creative.html',
            'Minimal': 'tamplate_minimal.html'
        }
        
        template_file = template_map.get(template_name)
        if not template_file:
            return jsonify({'error': f'Template {template_name} not supported'}), 400
        
        # Generate HTML
        env = Environment(loader=FileSystemLoader('Portfolio/templates'))
        template = env.get_template(template_file)
        html_content = template.render(**portfolio_data)
        
        return jsonify({
            'success': True,
            'html_content': html_content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/portfolio-templates', methods=['GET', 'POST'])
def portfolio_templates():
    """Handle template selection from frontend"""
    if request.method == 'POST':
        data = request.get_json()
        template_name = data.get('templateName')
        
        if template_name:
            session['selected_template'] = template_name
            return jsonify({
                'success': True,
                'message': f'Template {template_name} selected',
                'selected_template': template_name
            })
        else:
            return jsonify({
                'success': False,
                'error': 'templateName is required'
            }), 400
    
    templates = get_available_templates()
    return jsonify({
        'success': True,
        'templates': templates,
        'selected_template': session.get('selected_template')
    })

@app.route('/generate-portfolio', methods=['POST'])
def generate_portfolio_with_template():
    """Generate portfolio using template from session"""
    try:
        data = request.get_json()
        print(f"Received portfolio data: {data}")
        
        if not data:
            return jsonify({'error': 'No portfolio data provided'}), 400
        
        template_name = session.get('selected_template', 'Modern')
        print(f"Using template from session: {template_name}")
        
        # Fetch GitHub projects if GitHub URL is provided
        if data.get('githubUrl') and not data.get('projects'):
            try:
                import requests
                github_username = data['githubUrl'].split('github.com/')[1].split('/')[0]
                response = requests.get(f'https://api.github.com/users/{github_username}/repos?sort=updated&per_page=6')
                
                if response.status_code == 200:
                    repos = response.json()
                    data['projects'] = [{
                        'name': repo['name'],
                        'description': repo['description'] or f"A {repo['language']} project",
                        'url': repo['html_url'],
                        'language': repo['language']
                    } for repo in repos if not repo['fork']]
                    print(f"Fetched {len(data['projects'])} GitHub projects")
            except Exception as e:
                print(f"Error fetching GitHub projects: {e}")
        
        # Enhance content with AI
        try:
            from Portfolio.enhancer import enhance_content
            if data.get('about'):
                data['about'] = enhance_content(
                    "Rewrite this about section to be more professional and engaging for a portfolio:",
                    data['about']
                )
            if data.get('projects'):
                for project in data['projects']:
                    if project.get('description'):
                        project['description'] = enhance_content(
                            "Improve this project description to be more compelling and professional:",
                            project['description']
                        )
            print("Content enhanced with AI")
        except Exception as e:
            print(f"Error enhancing content: {e}")
        
        template_map = {
            'Modern': 'template_modern.html',
            'Creative': 'template_creative.html',
            'Minimal': 'tamplate_minimal.html'
        }
        
        template_file = template_map.get(template_name)
        if not template_file:
            return jsonify({'error': f'Template {template_name} not supported'}), 400
        
        template_path = os.path.join('Portfolio/templates', template_file)
        if not os.path.exists(template_path):
            return jsonify({'error': f'Template file {template_file} not found'}), 404
        
        env = Environment(loader=FileSystemLoader('Portfolio/templates'))
        template = env.get_template(template_file)
        html_content = template.render(**data)
        
        os.makedirs('output', exist_ok=True)
        output_path = os.path.join('output', 'portfolio.html')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return jsonify({
            'success': True,
            'message': 'Portfolio generated successfully',
            'output_path': output_path,
            'template_used': template_name
        })
        
    except Exception as e:
        print(f"Error generating portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download-html', methods=['GET'])
def download_html():
    """Download the generated portfolio HTML file"""
    try:
        output_path = os.path.join('output', 'portfolio.html')
        
        if not os.path.exists(output_path):
            return jsonify({'error': 'Portfolio not found. Please generate a portfolio first.'}), 404
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name='portfolio.html',
            mimetype='text/html'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)