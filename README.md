# GitHub Microservice

This microservice handles interactions with the GitHub API to fetch repository statistics and other GitHub-related data. It requires JWT authentication for all endpoints.

## Features
- Protected endpoints with JWT authentication
- Fetches repository statistics
- Retrieves commit history
- Provides aggregated GitHub metrics

## Setup
1. Create a `.env` file in the root directory with the following variables:
```bash
JWT_SECRET_KEY=your-secret-key  # Must match api_gateway's secret
GITHUB_TOKEN=your_github_token
PORT=5001
GITHUB_OWNER=ITAKEA
GITHUB_REPO=kode_fra_undervisning_e24
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
python app.py
```

## Docker
To build and run with Docker:
```bash
docker build -t github-microservice .
docker run -p 5001:5001 \
  -e GITHUB_TOKEN=your_github_token \
  -e JWT_SECRET_KEY=your-secret-key \
  -e GITHUB_OWNER=ITAKEA \
  -e GITHUB_REPO=kode_fra_undervisning_e24 \
  github-microservice
```

## API Endpoints
- GET `/` - Shows available API endpoints
- GET `/github/stats` - Retrieves GitHub repository statistics (requires JWT token)
  ```bash
  curl -H "Authorization: Bearer your_jwt_token" http://localhost:5001/github/stats
  ```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET_KEY` | Yes | - | Secret key for JWT validation (must match api_gateway) |
| `GITHUB_TOKEN` | Yes | - | GitHub Personal Access Token for API access |
| `PORT` | No | 5001 | Port to run the service on |
| `GITHUB_OWNER` | Yes | - | GitHub repository owner (organization or user) |
| `GITHUB_REPO` | Yes | - | GitHub repository name |

## Dependencies
See `requirements.txt` for a full list of Python dependencies.

## Security Note
Ensure that the JWT_SECRET_KEY matches the one used in the api_gateway service to allow proper token validation across services.
