---
description: Writes a UGC-style script with a strong opening, proof, objection handling and CTA
argument-hint: "[product] [approx. length, optional]"
---

Follow the `ugc-script` skill in full.

## Steps
1. Read `meta-ads-config.json` and any existing files for the product in the connected folder (`research-`, `market-`, `audience-`, `offer-`, `creatives/`). If the config is missing, suggest `/setup`.
2. Pull real pains, desires and objections from those files. If none exist, ask the user for the 2-3 main ones before generating. Never invent numbers, results or testimonials.
3. Write the full script with timing marks, plus a clean version with only the spoken lines.
4. Save the result as `creatives/[product]/ugc-[date].md` in the connected folder.

## Output
Present the result clearly and suggest the next command in the cycle: `/research` → `/creative` → `/campaign` → `/publish` → `/analyze`.
