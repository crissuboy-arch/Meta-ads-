---
name: keyword-research
description: Use this skill to discover what people actually search on Google about a product/niche before writing any ad — autocomplete, related questions, search intent. Trigger when the user says "research keywords," "what are people searching for," "market research," or runs /research.
---

# Search Intent Research

Goal: ad copy can't be born from guesswork. It's born from what the audience is already typing into Google about the problem/product.

## Sources (in this order)

1. **Google autocomplete**: type the base term into Google (via Claude in Chrome or search) and collect the suggested completions (e.g., "teeth whitening" → "teeth whitening cost," "does teeth whitening hurt," "does at-home teeth whitening work").
2. **"People also ask"**: collect the questions shown on the results page for the base term and 2-3 variations.
3. **Related searches** at the bottom of the results.
4. **Comparative terms**: search "[product] worth it," "[product] vs [alternative]," "does [product] work" — these carry the highest commercial intent.

## Intent classification

- **Informational** ("what is," "how does it work," "what is it for"): audience still educating themselves — good for content/authority creative, not for a direct buy CTA.
- **Commercial** ("best," "worth it," "comparison," "options"): audience comparing — good for creative with social proof and a differentiator.
- **Transactional** ("price," "where to buy," "book," "near me"): audience ready — good for a direct conversion CTA.

## Extracting pains and objections

Every question with a doubtful or resistant tone ("does it hurt," "is it safe," "does it really work," "is it worth the price," "any side effects") is a real audience objection — it becomes a hook or a direct answer in the ad copy (the `ad-copywriting` skill uses this).

## Translating into Meta Ads interests

At the end, suggest 5-8 real interests from the Ads Manager audience picker that connect to the terms found. Use only category names that plausibly exist in the picker (niche brands, activities, publications) — if unsure of the exact name, suggest the term and mark it "verify in the picker when building the campaign" instead of inventing an interest name.

## Best practices

- Never invent exact search volume (there's no access to real volume data without authenticated Google Keyword Planner/Trends) — report qualitative relative frequency ("shows up in almost every variation," "appears in just 1 search") instead of fabricated numbers.
- Quality over quantity: 15-20 well-classified terms beat 100 generic ones.
- Log the source of each pain/objection (which search it came from) for traceability.
