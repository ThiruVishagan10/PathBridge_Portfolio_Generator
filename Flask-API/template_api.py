from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_available_templates():
    """Get list of available templates"""
    return [
        {'name': 'Modern', 'file': 'template_portfolio.html', 'description': 'Modern glassmorphism design with video background'},
        {'name': 'Creative', 'file': 'template_creative.html', 'description': 'Creative design with animations and unique layouts'},
        {'name': 'Minimal', 'file': 'template_minimal.html', 'description': 'Clean minimal design focused on content'}
    ]

@app.route('/', methods=['GET'])
def index():
    """API info"""
    return jsonify({
        'message': 'Template Selection API',
        'endpoints': {
            'GET /templates': 'Get available templates'
        }
    })

@app.route('/templates', methods=['GET'])
def get_templates():
    """Get available templates"""
    templates = get_available_templates()
    return jsonify({'templates': templates})

if __name__ == '__main__':
    app.run(debug=True, port=8001)