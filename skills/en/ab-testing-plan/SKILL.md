---
name: ab-testing-plan
description: Use this skill to create an A/B testing plan for creative, copy, audience, offer, CTA, and format before or during a Meta Ads campaign. Trigger when the user says "test plan," "what should I test first," "A/B test," or runs /ab-test.
---

# A/B Testing Plan

## Core principle

Test **one variable at a time** within each test (don't change copy AND audience AND creative at once — if the result moves, you won't know what caused it). Each test round isolates 1 variable.

## Recommended priority order

Test first what has the highest potential impact and is cheapest to figure out:

1. **Offer/sales angle**: if the offer doesn't resonate, no creative tweak saves the campaign — test 2-3 different angles (from `market-[product].md`) first, with the same basic creative.
2. **Hook/creative**: once the offer has validated an angle, test 2-4 different hooks for that angle (use `creative-hooks`).
3. **Format**: the same hook/angle in Feed vs. Reels vs. Carousel — different audiences consume different formats differently.
4. **Audience**: once creative and format are validated, test cold audiences vs. different interests.
5. **CTA**: fine-tuning, usually last — tends to have less impact than the items above.

## Test setup

For each test, define:
- **Isolated variable** and its 2-3 variations.
- **What stays fixed** (everything else in the campaign).
- **Decision metric**: which metric picks the winner (CTR for hook/creative, CPA/ROAS for offer and audience — never decide on CTR alone when the goal is sales).
- **Minimum budget and duration**: recommend running until there's enough data per variation (rule of thumb: at least ~50 clicks or ~3-4 days, whichever comes later, before declaring a winner — small-sample decisions are usually wrong).
- **Kill criteria**: when to pause the losing variation (e.g., CPA 50% above the best variation once the minimum volume is reached).

## Output

Save `ab-test-[product].md` with the prioritized test sequence, what each test will answer, and the decision criteria. This plan feeds the ad set structure in `/campaign` (each tested variation becomes a separate ad set/ad) and the results reading in `/results-analysis`.
