---
description: Builds the campaign structure (objective, budget, audiences, placements) as a brief
argument-hint: "[product] — needs approved creatives in creatives/[product]/"
---

Build the campaign brief from `meta-ads-config.json`, `research-[product].md` and `creatives/[product]/variations.md`.

## Steps
1. Confirm at least one creative is approved. If not, suggest `/creative [product]`.
2. If `audit-[product].md` exists, read its score and budget recommendation. If not, suggest `/audit [product]` (not blocking).
3. Define, confirming each item with the user:
   - **Objective** (sales, leads, messages, traffic). For sales, confirm the Pixel Purchase event is working; if not, suggest `/tracking` first.
   - **Daily budget**, starting from the config default adjusted by the audit score. If the user has less, rebuild the structure with fewer audiences and ads rather than shrinking everything until it produces no data. Say the minimum daily amount below which testing is not worth it.
   - **Test length**: at least 3-4 days before any optimisation decision.
   - **Structure**: for a sales test, one campaign with campaign-level budget, 2-3 ad sets (one per angle or audience), 1-2 creatives each. Use the `meta-ads-campaign` and `budget-allocation` skills.
   - **Audiences**: location and age from the config plus the interests from the research.
   - **Placements**: automatic (Advantage+) unless there is a specific reason.
   - **Kill rule**: pause any ad set with zero results after spending about twice the target cost per result.
4. Save `campaign-[product].md`, ready for `/publish`.

## Output
Present the full brief for review. The brief only becomes a campaign when the user confirms; `/publish` never runs by itself. Suggest `/publish [product]`.
