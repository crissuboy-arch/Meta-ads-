---
description: Full diagnosis of the sales page, offer, copy, creatives and audience, with a score and priorities
argument-hint: "[product] [page URL, optional] [pasted metrics, optional]"
---

Run the full diagnosis following the `full-account-diagnosis` skill, with `sales-page-audit`, `offer-evaluation` and `landing-page-ads-match` as needed.

## Steps
1. Determine the product. Check which files already exist in the connected folder (`research-`, `audit-`, `offer-`, `creatives/.../variations.md`).
2. Run the skill for anything missing and tell the user what is being generated.
3. If the user pastes real campaign metrics, apply `metrics-reading` and `campaign-audit` and include the result.
4. Calculate the overall weighted score and an ordered priority list.
5. Save `audit-[product].md`.

## Output
The score, the top fixes in order, and the suggested next command.
