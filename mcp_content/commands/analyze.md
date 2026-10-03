---
description: Pulls real performance for the campaign and suggests optimisations
argument-hint: "[product] — only after the minimum test period in campaign-[product].md"
---

Analyse real performance, never before the minimum test period set in the brief.

## Steps
1. Read `campaign-[product].md` for the launch date and minimum test period. If it has not passed, say when reliable analysis becomes possible and do not draw conclusions from a small sample.
2. Pull data with the Windsor connector: call `get_fields` for `facebook`, then `get_data` with campaign, ad set and ad names, spend, impressions, reach, clicks, CTR, CPM, results and cost per result for the test period.
3. If the connector is not available, ask the user to paste the metrics from Ads Manager and use the `metrics-reading` skill on them.
4. Compare audiences against each other and creatives against each other. Say objectively what performs better and why, using `metrics-reading`, `ad-fatigue-diagnosis` and `scaling-strategy`.
5. Suggest the next step from the data, not guesses:
   - Cost per result on target with enough volume → scale gradually (for example +20% every 2-3 days, never doubling at once).
   - A creative with a much lower CTR than the others → pause it and test a new angle with `/creative`.
   - No meaningful difference between audiences → consolidate.
   - A rejected or limited ad → explain Meta's stated reason before suggesting changes.

## Output
A short table of the metrics and a recommendation. The decision to pause, scale or change is the user's. Any change through the connector (pause, budget, creative) needs their explicit yes first.
