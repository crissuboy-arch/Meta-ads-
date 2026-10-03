---
description: Alias of /audit: full diagnosis of page, offer, copy, creatives and audience
argument-hint: "[product] [URL, optional]"
---

Follow the `full-account-diagnosis` skill in full.

## Steps
1. Read `meta-ads-config.json` and any existing files for the product in the connected folder (`research-`, `market-`, `audience-`, `offer-`, `creatives/`). If the config is missing, suggest `/setup`.
2. Pull real pains, desires and objections from those files. If none exist, ask the user for the 2-3 main ones before generating. Never invent numbers, results or testimonials.
3. Run the complete diagnosis, run any missing sub-skill first, and compute the weighted overall score and ordered priorities.
4. Save the result as `diagnosis-[product].md` in the connected folder.

## Output
Present the result clearly and suggest the next command in the cycle: `/research` → `/creative` → `/campaign` → `/publish` → `/analyze`.
