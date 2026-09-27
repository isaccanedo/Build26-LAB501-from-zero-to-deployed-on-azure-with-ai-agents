# Train the Trainer — LAB501

So you're delivering **LAB501: From Zero to Deployed on Azure with AI Agents**. This page is the short version of "what do I read first?" — it points you at the material you need, in the order you need it.

## 1. Get the shape of the lab (~15 min)

Read these, in order, before anything else:

1. [`docs/lab-instructions/00-overview.md`](../docs/lab-instructions/00-overview.md) — the abstract, target architecture diagram, the **6 Azure skills** used, and the section-by-section timing (Ship → Harden → See → Break → Investigate).
2. [`README.md`](../README.md) — the attendee landing page. This is what your audience sees first.

By the end of this you should be able to answer: *which skill activates in which scenario, and why?*

## 2. Run the lab yourself end-to-end (~75 min)

Don't skip this. AI is non-deterministic — you need to see what the demo actually does on your own machine before you do it on stage.

Walk through every step in `docs/lab-instructions/` in order:

| # | File | What you're rehearsing |
|---|------|------------------------|
| 1 | [`01-prerequisites.md`](../docs/lab-instructions/01-prerequisites.md) | Tools attendees need (Skillable VM has them pre-installed) |
| 2 | [`02-login-and-launch.md`](../docs/lab-instructions/02-login-and-launch.md) | Azure / GitHub / Copilot CLI login + Azure Skills plugin install |
| 3 | [`03-getting-started.md`](../docs/lab-instructions/03-getting-started.md) | Cloning the starter app and verifying the Flask + Cosmos DB checkpoint |
| 4 | [`04-scenario-1-ship-and-harden.md`](../docs/lab-instructions/04-scenario-1-ship-and-harden.md) | The big one: `azure-prepare` → `azure-validate` → `azure-deploy` chain that ships **both** the Flask Container App and the Python Function App, then `azure-rbac` hardening |
| 5 | [`05-scenario-2-see-and-evaluate.md`](../docs/lab-instructions/05-scenario-2-see-and-evaluate.md) | `azure-resource-visualizer` diagram + critical review |
| 6 | [`06-scenario-3-break-and-triage.md`](../docs/lab-instructions/06-scenario-3-break-and-triage.md) | Break ingress port, watch `azure-diagnostics` reason to root cause |
| 7 | [`07-scenario-4-investigate-and-operationalize.md`](../docs/lab-instructions/07-scenario-4-investigate-and-operationalize.md) | KQL post-mortem + scheduled-query alert rule |
| 8 | [`08-troubleshooting.md`](../docs/lab-instructions/08-troubleshooting.md) | **Bookmark this.** Most likely failures and fixes. |
| 9 | [`09-whats-next.md`](../docs/lab-instructions/09-whats-next.md) | What you point attendees to at the end |

## 3. Know your safety net

- **Yolo mode** — Scenario 1 suggests `/yolo` in Copilot CLI to skip approval prompts. Decide ahead of time whether you'll demo with it on (faster) or off (more pedagogical). Practice both.
- **Troubleshooting playbook** — keep [`08-troubleshooting.md`](../docs/lab-instructions/08-troubleshooting.md) open in a second tab. It covers the common Cosmos DB RBAC, ingress port, and log-ingestion-latency issues.
- **AI variance** — the prompts are tested, but output differs run-to-run. Coach attendees to focus on *which skill activated* and *why*, not on matching your screen exactly.
- **Permissions** — some hardening operations need Owner / User Access Administrator. On the lab VM this is fine; for outside-the-lab delivery, flag it.

## 4. Delivery tips

- **Three demo timings** to memorize: Scenario 1 ~25 min, Scenario 4 ~15 min, everything else ~10 min each. Leave 5 min buffer at the end for Q&A.
- **`azd up` takes a few minutes.** Use that time to walk through the generated `infra/` Bicep with the audience — that's where the "evaluate the AI" part of the lab lives.
- **Scenario 3** — after running `az containerapp ingress update --target-port 9999`, the new revision takes 30s–2min to activate. Don't Ctrl+C; talk through what's happening.
- **Log ingestion latency** — Container App system logs take ~5 min to reach Log Analytics. Plan Scenario 4 so the data has had time to land.

## 5. Resources to share with attendees

Point attendees to:
- [`README.md`](../README.md) — the lab repo landing page (includes the "Keep Learning with Copilot" prompts)
- [`docs/lab-instructions/09-whats-next.md`](../docs/lab-instructions/09-whats-next.md) — extension ideas (private endpoints, VNet, Key Vault, CI/CD with OIDC, Terraform)
- <https://aka.ms/build26-next-steps> — official Build 2026 next steps

## Found a problem while rehearsing?

Open an issue at <https://github.com/microsoft/Build26-LAB501/issues> so the next trainer doesn't hit it too.
