from flask import Flask, jsonify
import requests
import os
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
PORT = int(os.getenv('PORT', 5001))
jwt = JWTManager(app)

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

@app.route('/')
def home():
    return jsonify({
        "service": "GitHub Microservice",
        "available_endpoints": [
            {
                "path": "/github/stats",
                "method": "GET",
                "description": "Get GitHub repository statistics",
                "authentication": "JWT required"
            }
        ]
    })

@app.route('/github/stats', methods=['GET'])
@jwt_required()
def get_github_stats():
    try:
        # Get the current user from the JWT token
        current_user = get_jwt_identity()
        
        # Get repository owner and name from environment variables
        owner = os.getenv('GITHUB_OWNER')
        repo = os.getenv('GITHUB_REPO')
        
        # Get repository info
        repo_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
        repo_response = requests.get(repo_url, headers=get_headers())
        repo_data = repo_response.json()

        # Get recent commits
        commits_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"
        since = datetime.now() - timedelta(days=30)
        commits_response = requests.get(
            commits_url,
            headers=get_headers(),
            params={"since": since.isoformat()}
        )
        commits_data = commits_response.json()

        stats = {
            "repository": {
                "name": repo_data.get("name"),
                "stars": repo_data.get("stargazers_count"),
                "forks": repo_data.get("forks_count"),
                "open_issues": repo_data.get("open_issues_count")
            },
            "recent_commits": len(commits_data),
            "requested_by": current_user
        }

        return jsonify(stats)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
