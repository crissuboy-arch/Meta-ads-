---
name: sales-page-audit
description: Use this skill to audit a sales/product page BEFORE building the campaign — it gives an objective conversion-readiness score based on a CRO checklist, never a sales forecast. Trigger when the user says "audit my page," "review my product," "will this sell well," or runs /audit.
---

# Conversion Readiness Audit

## About the score this skill produces

This skill gives a **page readiness score (1-10)**, not a purchase probability. Nobody — not this skill, not any AI tool — knows the real chance of someone buying before running real traffic; that depends on the audience, the offer, the price, and timing, and only the market answers that. Whenever the score is presented to the user, make this distinction explicit: it's a score of **how well the page follows proven conversion best practices and removes friction**, used only to decide whether to go in with a bigger budget or test small first.

## How to audit

1. Open the sales page (via Claude in Chrome if rendering is needed, or read the provided HTML/URL).
2. Rate each criterion below as **met / partial / not met**.
3. Calculate the score: each "met" = 1 point, "partial" = 0.5, "not met" = 0, across 10 criteria → final score from 0 to 10.

## Criteria (10, equal weight)

1. **Promise clarity within 5 seconds**: you can understand what it is, who it's for, and the main benefit without scrolling.
2. **Headline is a benefit, not a label** (same bar as the `ad-copywriting` skill).
3. **Real, visible social proof**: testimonial, review, customer count, case study — verifiable, not generic.
4. **Answers the niche's obvious objections**: price, does it actually work, is it safe, timeline — use the real objections collected in `research-[product].md` if it exists.
5. **Single, repeated CTA**: the same action at multiple points on the page, with no competing CTAs muddying the decision.
6. **Clear offer**: exactly what the person receives, visible price (or a clear process to find out the price), payment method.
7. **Guarantee or risk reducer**: refund policy, trial, support — anything that reduces the fear of making the wrong purchase.
8. **Mobile-first**: readable text and a buy button reachable without effort on a phone (most paid traffic comes from mobile).
9. **Load speed**: the page shouldn't hang or lag (that kills the click you paid to bring in).
10. **Message match with the ad**: the page delivers exactly what the ad copy promises (same language, same offer) — check against `creatives/[product]/variations.md` if it already exists.

## Output

Save `audit-[product].md` in the connected folder with:

- Final score (0-10) and the criterion-by-criterion breakdown
- The 2-3 points weighing most against the score, with a concrete fix suggestion
- A starting-budget recommendation based on the score (not a guarantee — a prudence call):
  - **Score ≥ 8**: the page is ready; go with the standard daily budget from the config.
  - **Score 5-7.9**: fine to test, but suggest starting with half the standard budget until the page proves it converts incoming traffic.
  - **Score < 5**: recommend fixing the critical points before spending on traffic — sending paid clicks to a weak page is the most expensive way to find that out.

Make it clear to the user: this budget recommendation is a prudent starting point, the final call is theirs, and `/campaign` will use this score to suggest the initial budget.
