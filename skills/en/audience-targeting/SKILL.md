---
name: audience-targeting
description: Use this skill to build a customer avatar, interests, behaviors, and cold/warm/hot audience segmentation for Meta Ads campaigns. Trigger when the user says "build my avatar," "define my audience," "who is my ideal customer," or runs /audience.
---

# Audience and Avatar Definition

## Avatar

Build a concrete profile (not "women 25-45 interested in beauty" — too generic to guide copy or targeting). Include: approximate age, life context relevant to the product, what they're trying to solve right now, what they've already tried before, where they spend time online. If `market-[product].md` exists, use the pains/desires already mapped instead of reinventing them.

## Interests and behaviors (for the Ads Manager audience picker)

Suggest 8-12 plausibly real interests in Meta's picker — brands, publications, activities, niche pages — and flag when you're unsure of the exact name ("verify in the picker when building the campaign," never invent an interest name). Split them into 2-3 thematic groups (e.g., competitor interests, related lifestyle interests, purchase-behavior interests) to make later audience A/B testing easier.

## Audience temperature

- **Cold**: never had contact with the brand. Targeting by interests/behaviors/demographics. Creative must educate and spark first interest — pain/identification hooks work well here.
- **Warm**: already had some contact (followed the profile, visited the site, engaged with content) but hasn't bought. Ideal for retargeting via custom audiences (website visitors, Instagram/Facebook engagement) — creative can assume the person already knows the product and focus on objection handling/social proof.
- **Hot**: already showed strong intent (abandoned cart, started checkout, contact/customer list). Creative can be more direct: offer, real urgency (never manufactured), specific social proof.

## Output

Save `audience-[product].md` with: the avatar description, the interest list by thematic group, and the cold/warm/hot segmentation with a recommendation of which custom audience type to use at each temperature (the `meta-ads-manager` uses this when building ad sets in `/campaign` and `/publish`).
