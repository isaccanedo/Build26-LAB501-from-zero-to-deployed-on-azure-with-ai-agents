# Troubleshooting

## Cosmos DB connection fails locally
**Symptom:** `python app.py` shows authentication or connection errors.
**Cause:** The app uses `DefaultAzureCredential`, which requires an active Azure CLI login.
**Fix:** Run `az login` and ensure you're on the correct subscription. Verify `COSMOS_ENDPOINT` in `.env` matches your provisioned Cosmos DB.

## ACR name contains hyphens → Deployment fails
**Symptom:** `azd up` fails with an error about invalid ACR name.
**Cause:** ACR names must be alphanumeric. Hyphens in your AZD environment name propagate to the registry name.
**Fix:** Use an environment name without hyphens (e.g., `lab501app`). Re-run `azd init` with a new name.

## AZD deploys to wrong subscription
**Symptom:** Resources appear in an unexpected subscription, or you get permission errors.
**Cause:** AZD maintains its own subscription config, separate from `az account show`.
**Fix:** Run `azd env set AZURE_SUBSCRIPTION_ID $(az account show --query id -o tsv)` to align.

## Container App can't connect to Cosmos DB after deployment
**Symptom:** The app deploys but shows database errors when accessed.
**Cause:** The Container App doesn't have the right permissions or environment variables to reach Cosmos DB.
**Fix:** Verify the `COSMOS_ENDPOINT`, `COSMOS_DATABASE`, and `COSMOS_CONTAINER` environment variables are set on the Container App. If using managed identity, ensure the system-assigned identity has the appropriate Cosmos DB RBAC role assigned.

## `az containerapp ingress update` hangs for 2+ minutes
**Symptom:** The command appears stuck after running.
**Cause:** The CLI waits for the new Container Apps revision to activate.
**Fix:** This is expected behavior. Wait for it to complete — do not Ctrl+C.

## First request after deploy returns timeout or slow response
**Symptom:** `curl` times out or takes >10 seconds on first request.
**Cause:** New revision is activating (cold start). `minReplicas: 1` is set, but initial activation still takes time.
**Fix:** Wait ~15 seconds after deployment completes, then retry.

## KQL query returns no results in Scenario 4
**Symptom:** Queries return empty tables.
**Cause:** Log Analytics ingestion has ~5 minute latency. Metrics have ~15 minute latency.
**Fix:** Wait 5 minutes after Scenario 3, then retry the query.

## `az monitor scheduled-query create` fails with "command not found"
**Symptom:** CLI doesn't recognize the `scheduled-query` command.
**Cause:** The preview CLI extension isn't installed.
**Fix:** Run `az extension add --name scheduled-query --yes`

## Docker build fails during `azd up`
**Symptom:** Deployment fails with Docker-related error.
**Cause:** Docker Desktop isn't running.
**Fix:** Start Docker Desktop and verify with `docker version`. Then re-run `azd up`.

## Python dependency install fails
**Symptom:** `pip install -r requirements.txt` fails with errors.
**Cause:** Missing system dependencies or wrong Python version.
**Fix:** Verify you're running Python 3.13+ with `python --version`. Try `pip install --upgrade pip` first.

## PowerShell quote escaping in KQL queries
**Symptom:** KQL `where Reason_s == "ProbeFailed"` fails with syntax errors in PowerShell.
**Cause:** PowerShell handles double quotes differently than bash.
**Fix:** Use the `has` operator instead: `where Reason_s has "ProbeFailed"`. The AI typically handles this automatically.

## Gunicorn port mismatch after deployment
**Symptom:** The Container App shows 503 even after a fresh deploy.
**Cause:** The ingress target port doesn't match gunicorn's bind port (8000).
**Fix:** Ensure the Container App ingress target port is set to `8000` (matching the `Dockerfile` CMD: `gunicorn --bind 0.0.0.0:8000`).

---

**Back to:** [Overview](00-overview.md) | [What's Next →](09-whats-next.md)
