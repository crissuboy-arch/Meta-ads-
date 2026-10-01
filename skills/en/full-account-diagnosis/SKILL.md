---
name: full-account-diagnosis
description: Use this skill to run a complete diagnosis of a campaign or product — page, offer, copy, creatives, audience, and CTA — consolidating the other skills into one overall score and priority list. Trigger when the user says "full audit," "overall diagnosis," "what's blocking my campaign," or runs /full-audit.
---

# Full Diagnosis

This skill doesn't replace the specific skills — it **orchestrates** what already exists and fills in what's missing, then consolidates everything into a single report with priorities.

## Steps

1. Check which files already exist in the connected folder for the product: `market-[product].md`, `audit-[product].md`, `offer-[product].md`, `audience-[product].md`, `creatives/[product]/variations.md`.
2. For whatever **doesn't exist**, run the corresponding skill now (don't skip steps out of laziness, but tell the user what's being generated):
   - No page evaluated → run `sales-page-audit`.
   - No offer evaluated → run `offer-evaluation`.
   - No audience defined → run `audience-targeting`.
   - No copy/creative → don't generate it from scratch here; flag that copy doesn't exist yet and suggest `/creative` separately (a diagnosis evaluates what exists — it doesn't create new copy on its own).
3. If the user pastes real metrics from a campaign already running, also apply the `metrics-reading` skill and include it in the diagnosis.

## Overall score

Calculate an overall score (0-100) as a weighted average of the available partial scores:
- Page/offer: 40% (audit score + offer score, averaged)
- Audience: 20% (qualitative: well defined = 20, partial = 10, missing = 0)
- Copy/creative: 20% (use the `creative-score` checklist result if it exists; if there's no copy yet, don't score this slice and recalculate the weight proportionally across the rest)
- Real campaign metrics (if any): 20% — CPA/ROAS against the expectation the user provided

Make it clear: the overall score measures the **soundness of the whole setup** — it doesn't predict sales results.

## Output

Save `diagnosis-[product].md` with: overall score, the score of each block, and an **ordered priority list** (what to fix first has the highest impact and is cheapest to solve — usually offer/page before creative, creative before audience, audience before CTA). For each priority, point to the system command that resolves it (`/offer`, `/audit`, `/creative`, `/hooks`, `/audience`, `/ab-test`).
