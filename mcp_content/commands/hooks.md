---
description: Generates opening hooks for Feed, Stories, Reels, UGC, carousel and short video
argument-hint: "[product] [format(s) or 'all']"
---

Follow the `creative-hooks` skill in full.

## Steps
1. Read `meta-ads-config.json` and any existing files for the product in the connected folder (`research-`, `market-`, `audience-`, `offer-`, `creatives/`). If the config is missing, suggest `/setup`.
2. Pull real pains, desires and objections from those files. If none exist, ask the user for the 2-3 main ones before generating. Never invent numbers, results or testimonials.
3. For each requested format, write 3-5 hooks using different patterns from the skill (question, shock, identification, common mistake, result, confession).
4. Save the result as `creatives/[product]/hooks.md` in the connected folder.

## Output
Present the result clearly and suggest the next command in the cycle: `/research` → `/creative` → `/campaign` → `/publish` → `/analyze`.
