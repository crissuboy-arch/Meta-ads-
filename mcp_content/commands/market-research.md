---
description: Maps niche, audience, competitors, pains, desires, objections and sales angles
argument-hint: "[product or niche] [market]"
---

Follow the `market-research` skill in full.

## Steps
1. Read `meta-ads-config.json` and any existing files for the product in the connected folder (`research-`, `market-`, `audience-`, `offer-`, `creatives/`). If the config is missing, suggest `/setup`.
2. Pull real pains, desires and objections from those files. If none exist, ask the user for the 2-3 main ones before generating. Never invent numbers, results or testimonials.
3. Map niche and sub-niche, audience, competitors, pains, desires, objections, promises and angles. Use web search if available, otherwise Claude in Chrome, otherwise ask the user to paste what they know and say the result rests on that.
4. Save the result as `market-[product].md` in the connected folder.

## Output
Present the result clearly and suggest the next command in the cycle: `/research` → `/creative` → `/campaign` → `/publish` → `/analyze`.
