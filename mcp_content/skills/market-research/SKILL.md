---
name: market-research
description: Use this skill to map niche, audience, competitors, pains, desires, objections, promises, and sales angles before building any campaign. Trigger when the user says "analyze my niche," "who are my competitors," "map my market," or runs /market-research.
---

# Market Research and Sales Angles

How this differs from the `keyword-research` skill: that one maps what people type into Google; this one maps the **market as a whole** — who buys, who sells, and which angle to enter with. The two complement each other; if `research-[product].md` already exists, reuse the pains/objections already found instead of repeating the search.

## What to gather

1. **Niche and sub-niche**: define it precisely (e.g., not "weight loss," but "women 35-50 postpartum who have tried dieting and failed").
2. **Audience**: who actually buys (not always who uses the product — e.g., gifts, kids' products).
3. **Direct competitors**: 3-5 businesses/products solving the same problem. Gather via Google search and, if the user provides them, analysis of competitor pages/ads they've already seen (never invent competitor data that wasn't verified).
4. **Pains** (what bothers them now) and **desires** (what they want to feel/become afterwards) — always in the customer's language, not the company's.
5. **Objections** that stop people from buying (price, trust, time, "I've tried before and it didn't work," category skepticism).
6. **Promises the market already uses**: what competitors promise — this exists so the user's product can differentiate, not copy.
7. **Possible sales angles**: at least 3 different ways to sell the same product (e.g., pain angle, fast-result angle, identity-transformation angle, unique-mechanism/"how it works" angle).

## Sources

- Google search (Chrome) for competitors, public reviews, niche forums/communities.
- What the user themselves already knows about the audience (ask directly: "what do your customers complain about most before buying?").
- If `research-[product].md` exists, reuse the objections and search terms already found.

## Output

Save `market-[product].md` with: defined niche, audience profile, competitor table (name, main promise, perceived weak point), list of pains/desires/objections, and 3+ sales angles with 1 example line each. This file feeds directly into `/offer`, `/hooks`, `/ugc`, and `/audience`.
