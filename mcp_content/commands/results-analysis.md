---
description: Alias of /analyze: reads real campaign metrics and recommends next steps
argument-hint: "[product]"
---

Follow the `metrics-reading` skill in full.

## Steps
1. Read `meta-ads-config.json` and any existing files for the product in the connected folder (`research-`, `market-`, `audience-`, `offer-`, `creatives/`). If the config is missing, suggest `/setup`.
2. Pull real pains, desires and objections from those files. If none exist, ask the user for the 2-3 main ones before generating. Never invent numbers, results or testimonials.
3. Only analyse after the minimum test period in campaign-[product].md. Pull data with `get_insights` or ask the user to paste metrics from Ads Manager.
4. Save the result as `results-[product].md` in the connected folder.

## Output
Present the result clearly and suggest the next command in the cycle: `/research` → `/creative` → `/campaign` → `/publish` → `/analyze`.
