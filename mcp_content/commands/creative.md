---
description: Writes ad variations from the research, hooks included, and scores each one with the quality checklist
argument-hint: "[product] — needs research-[product].md"
---

Write the creatives following the `ad-copywriting` and `creative-hooks` skills, then evaluate each one with `creative-score`. All three, in this order.

## Steps
1. Read `meta-ads-config.json` and `research-[product].md`. If the research is missing, suggest `/research [product]` first. Do not invent keywords, numbers or testimonials.
2. Write **3 variations**, each testing a different angle (main pain / direct benefit / proof or demonstration), always anchored in the real pains and terms from the research.
3. For each: primary text, headline, description, CTA button, and a concrete description of the visual or video (do not generate the image; describe what it must show).
4. Run the `creative-score` checklist on each. A variation that fails a mandatory item is marked "adjust" with the specific reason, then fixed and re-scored.
5. Save to `creatives/[product]/variations.md`: the variations, the checklist result and which are approved for the campaign.

## Output
Present the three variations and the checklist result. Be clear that the checklist reduces rejection risk; it does not predict performance. Suggest `/campaign [product]`.
