from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from Portfolio.generator import generate_portfolio
import os
import re

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Allow Next.js frontend to connect (http://localhost:3000 by default)

@app.route("/", methods=["POST"])
def create_portfolio():
    """
    Endpoint to receive portfolio data from the frontend,
    generate the portfolio HTML content, and return it.
    """
    try:
        data = request.get_json()

        if not data:
            # Note: For production, consider returning a full HTML error page
            return "No input data provided", 400

        # Generate the portfolio as an HTML string
        html_content = generate_portfolio(data)

        # Return the HTML content directly to the frontend
        return html_content, 200

    except Exception as e:
        # For a full application, you might want a more detailed log or error page.
        print(f"An error occurred: {e}")
        return "An internal server error occurred.", 500


@app.route("/download-html", methods=["GET"])
def download_html():
    """Download the generated portfolio as HTML file"""
    try:
        html_path = os.path.join("output", "portfolio.html")
        if os.path.exists(html_path):
            return send_file(html_path, as_attachment=True, download_name="portfolio.html")
        else:
            return "No portfolio found. Generate one first.", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/download-txt", methods=["GET"])
def download_txt():
    """Download the generated portfolio HTML as TXT file for editing"""
    try:
        html_path = os.path.join("output", "portfolio.html")
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment; filename=portfolio.txt'
            return response
        else:
            return "No portfolio found. Generate one first.", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # In a production environment, you would use a production WSGI server like Gunicorn
    app.run(port=8000, debug=True)
