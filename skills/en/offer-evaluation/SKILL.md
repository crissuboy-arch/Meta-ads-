---
name: offer-evaluation
description: Use this skill to evaluate the strength of an offer (promise, headline, bonuses, price, guarantee, unique mechanism, differentiators, CTA) and give it a score from 0 to 100. It doesn't predict sales — it measures the offer's structural soundness. Trigger when the user says "evaluate my offer," "score my offer," "is my offer good," or runs /offer.
---

# Offer Strength Evaluation (0-100)

## About the score

It measures how closely the offer follows the proven structure of offers that convert — it's not a forecast of how many sales it will generate (only the market answers that). Always communicate this distinction when presenting the result, same logic as the `sales-page-audit` skill.

## The 8 criteria (12.5 points each = 100)

1. **Core promise**: is it specific, measurable, or vivid enough? ("lose weight" = weak; "sleep through the night without waking up 3 times" = strong).
2. **Headline**: communicates the promise in one sentence, with no explanation needed.
3. **Unique mechanism**: is there a "why it works" that's different from the niche's obvious/generic answer? (Products without a unique mechanism compete on price alone).
4. **Real differentiators**: 2-3 concrete reasons to pick this product over a competitor (not vague "quality" — something verifiable).
5. **Bonuses**: they exist, they're relevant to the main promise (not random items just to inflate perceived value), and they have clear perceived value.
6. **Price and anchoring**: is there a comparison that justifies the price (cost of the problem, price of the alternative, total stacked value)?
7. **Guarantee/risk reducer**: it exists, it's clear, and it actually reduces the fear of buying the wrong thing?
8. **Offer CTA**: the requested action is obvious, and what the person gets by acting is immediate and clear.

Each criterion: 12.5 (strong) / 6 (partial) / 0 (missing or weak).

## Output

Save `offer-[product].md` with: final score, criterion-by-criterion breakdown, and the 2-3 points dragging the score down the most, with a concrete fix suggestion (never rewrite the entire offer unasked — suggest the targeted adjustment). If `market-[product].md` exists, check whether the promise and chosen angle align with the pains/desires already mapped.

How to read the bands (communicate as guidance, not a verdict):
- **80-100**: structurally strong offer; it can move to copy and campaign.
- **50-79**: functional offer, but with points to strengthen before scaling budget.
- **Below 50**: worth revisiting the offer before investing in traffic — the problem is usually not the ad, it's the offer behind it.
