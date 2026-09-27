# LEGO Set Browser — Sample App

A Flask web application that browses a LEGO set catalog stored in Azure Cosmos DB. This is the starter app for **Build 2026 — LAB501**.

## Prerequisites

- Python 3.13+
- An Azure Cosmos DB account with the LEGO dataset loaded
- Azure CLI logged in (for `DefaultAzureCredential`)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy the environment sample and fill in your values
cp .env.sample .env

# 3. Run locally
python app.py
```

The app will be available at `http://localhost:5000`.

## Running with Docker

```bash
docker build -t lego-set-browser .
docker run -p 8000:8000 lego-set-browser
```

## Project Structure

```
src/
├── app.py                 # Flask application (routes + Cosmos DB queries)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image definition
├── .dockerignore          # Docker build exclusions
├── .env.sample            # Environment variable template
├── static/css/style.css   # Custom CSS (Star Wars theme)
└── templates/
    ├── base.html          # Layout template
    ├── home.html          # Landing page with featured sets
    ├── browse.html        # Paginated browse/search/filter page
    ├── detail.html        # Individual set detail page
    └── 404.html           # Custom 404 page
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `COSMOS_ENDPOINT` | Cosmos DB account endpoint | *(see .env.sample)* |
| `COSMOS_DATABASE` | Database name | `LegoDatabase` |
| `COSMOS_CONTAINER` | Container name | `legoSets` |
| `AZURE_CLIENT_ID` | Managed Identity client ID (optional) | — |
