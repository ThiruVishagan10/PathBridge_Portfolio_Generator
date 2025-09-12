from flask import Flask, request, send_file, make_response, jsonify
from flask_cors import CORS
from Portfolio.generator import generate_portfolio
from github_fetcher import fetch_github_repos
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app, origins=["*"], allow_headers=["Content-Type"], methods=["GET", "POST"])

@app.route("/", methods=["GET"])
def home():
    return "Portfolio Generator API is running!", 200

@app.route("/test", methods=["POST"])
def test():
    """Quick test endpoint"""
    return jsonify({"status": "success", "message": "Server is responding"}), 200

@app.route("/", methods=["POST"])
def create_portfolio():
    """
    Endpoint to receive portfolio data from the frontend,
    generate the portfolio HTML content, and return it.
    """
    try:
        data = request.get_json()
        if not data:
            return "No input data provided", 400

        # ✅ If GitHub URL is provided → fetch repos
        github_url = data.get("githubUrl")
        if github_url:
            try:
                username = github_url.rstrip("/").split("/")[-1]
                github_projects = fetch_github_repos(username, max_repos=10)
                manual_projects = data.get("projects", [])
                data["projects"] = manual_projects + github_projects
            except Exception as github_error:
                print(f"GitHub fetch failed: {github_error}")
                pass

        # ✅ Generate the portfolio
        print("Starting portfolio generation...")
        html_content = generate_portfolio(data)
        print("Portfolio generation completed successfully")
        return html_content, 200

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Detailed error: {error_details}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/download-html", methods=["GET"])
def download_html():
    """Download the generated portfolio as viewable HTML file"""
    try:
        html_path = os.path.join("output", "portfolio.html")
        if os.path.exists(html_path):
            return send_file(html_path, as_attachment=True, download_name="my_portfolio.html", mimetype='text/html')
        else:
            return "No portfolio found. Generate one first.", 404
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/download-txt", methods=["GET"])
def download_txt():
    """Download the generated portfolio as TXT file for viewing source"""
    try:
        html_path = os.path.join("output", "portfolio.html")
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/plain; charset=utf-8'
            response.headers['Content-Disposition'] = 'attachment; filename="portfolio_source.txt"'
            return response
        else:
            return "No portfolio found. Generate one first.", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/download-code", methods=["GET"])
def download_code():
    """Download the generated portfolio source code as HTML file for editing"""
    try:
        html_path = os.path.join("output", "portfolio.html")
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.headers['Content-Disposition'] = 'attachment; filename="portfolio_code.html"'
            return response
        else:
            return "No portfolio found. Generate one first.", 404
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/fetch_projects", methods=["POST"])
def fetch_projects():
    """Standalone API to fetch GitHub repositories for a given GitHub URL"""
    try:
        data = request.json
        github_url = data.get("github_url")

        if not github_url:
            return jsonify({"error": "GitHub URL required"}), 400

        username = github_url.rstrip("/").split("/")[-1]
        projects = fetch_github_repos(username)

        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
