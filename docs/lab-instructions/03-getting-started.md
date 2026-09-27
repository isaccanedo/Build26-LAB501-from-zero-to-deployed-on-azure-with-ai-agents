# Getting Started — Set Up the Starter App

Set up the starter app using the following instructions.

## 1. Clone the Lab Repository

Open a new PowerShell session, clone the lab repo, and navigate into it:

```powershell
git clone https://github.com/microsoft/Build26-LAB501.git
```
```powershell
cd Build26-LAB501
```

## 2. Copy the Starter App

The `src/` directory contains a ready-to-go Python Flask application — a LEGO set browser backed by Azure Cosmos DB. Copy it to a new `lego-set-browser` working directory and initialize it as its own Git repo:

```powershell
Copy-Item -Recurse src lego-set-browser
```
```powershell
cd lego-set-browser
```
```powershell
git config --global user.name "Your Name"
```
```powershell
git config --global user.email "you@example.com"
```
```powershell
git init
```
```powershell
git add -A
```
```powershell
git commit -m "init"
```
If you run into an issue, please try typing out the command and run one command at a time. 

All subsequent commands should be run from the `lego-set-browser` directory.

> 💡 **What's in the starter app?** `app.py` is a Flask web application with routes for browsing, searching, and viewing LEGO sets. It connects to an Azure Cosmos DB to query set data. `requirements.txt` defines the Python dependencies (Flask, azure-cosmos, azure-identity, gunicorn). A `Dockerfile` is included for containerized deployment. The app uses `DefaultAzureCredential` for passwordless authentication to Cosmos DB.

## 3. Local Testing

We will intentionally skip local testing during the onsite labs to allow more time to finish the lab.

---

**Next:** [Scenario 1 — Ship It & Harden It →](04-scenario-1-ship-and-harden.md)
