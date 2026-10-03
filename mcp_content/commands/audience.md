---
description: Defines the target audience and test audiences for a campaign
argument-hint: "[product]"
---

Follow the `audience-targeting` skill in full.

## Steps
1. Read `meta-ads-config.json` and any existing files for the product in the connected folder (`research-`, `market-`, `audience-`, `offer-`, `creatives/`). If the config is missing, suggest `/setup`.
2. Pull real pains, desires and objections from those files. If none exist, ask the user for the 2-3 main ones before generating. Never invent numbers, results or testimonials.
3. Define the core audience and 2-3 test audiences, with the reason for each.
4. Save the result as `audience-[product].md` in the connected folder.

## Output
Present the result clearly and suggest the next command in the cycle: `/research` → `/creative` → `/campaign` → `/publish` → `/analyze`.
