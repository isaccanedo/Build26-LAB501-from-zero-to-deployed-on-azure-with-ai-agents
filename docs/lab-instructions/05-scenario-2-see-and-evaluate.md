# Scenario 2 — See It & Evaluate It (~10 min)

Architecture diagrams are either stale, wrong, or don't exist. AI can generate them instantly — but are they accurate?

## Part A — Generate the Diagram (~4 min)

**Say to Copilot:**

```
Visualize the resources in my resource group as an architecture diagram.
```

### 5️⃣ `azure-resource-visualizer` activates

Watch how it:
- Queries Azure Resource Graph to inventory every resource in your resource group
- Maps relationships: Container App → Container Apps Environment → Log Analytics, Container App → ACR
- Generates a Mermaid diagram with labeled subgraphs, resource types, and connection arrows
- Outputs renderable markdown you can paste into any Mermaid viewer

> 💡 **Skill spotlight:** The visualizer doesn't just list resources — it infers relationships from resource properties (e.g., `environmentId` links the Container App to its Environment). It's reading the ARM resource model, not guessing from names. Note that some connections — like the Cosmos DB dependency — are only discoverable through the Container App's environment variables, not through ARM resource properties, so the visualizer may not capture them automatically.

> 💡 **What about Cosmos DB?** Your app connects to a pre-provisioned Cosmos DB that may be in a different resource group. Check whether the visualizer captures this cross-resource-group dependency or if it only shows resources within the deployment's resource group. This is a common gap in auto-generated diagrams.

---

## Part B — Evaluate the Diagram (~6 min)

Open the generated markdown and review critically:

- Did it capture the deployed resources (Container App, Environment, ACR, Log Analytics)?
- Are the relationships correct? Does it show ACR → Container App pull?
- Does it show the Cosmos DB dependency? If not, that's a significant omission — the app won't work without it.
- What's missing that you'd need for a production architecture review?

**Say to Copilot:**

```
What's missing from this architecture for a production deployment? The app also connects to an existing Cosmos DB for its data.
```

Compare the AI's recommendations against your own findings from Scenario 1B.

✅ **Checkpoint:** You have a Mermaid diagram showing your deployed resources with connection arrows. To render it: copy the Mermaid block from Copilot's output and paste into [mermaid.live](https://mermaid.live), use VS Code with a Mermaid extension, or commit the markdown file to a GitHub repo — GitHub renders Mermaid diagrams natively in markdown files.

**Takeaway:** `azure-resource-visualizer` is excellent for discovery ("what exists right now?") but requires expert review for documentation ("is this complete and accurate?"). The diagram reflects deployed state within a resource group, not the full picture — cross-resource-group dependencies like your Cosmos DB connection are your job to document.

---

**Next:** [Scenario 3 — Break It & Triage It →](06-scenario-3-break-and-triage.md)
