---
description: Step-by-step Meta Pixel and Conversions API setup, test events and sales webhook (Hotmart, Kiwify, Stripe)
argument-hint: "[product or platform] — optional"
---

Guide the user through tracking setup following the `pixel-tracking-setup` and `conversion-tracking` skills.

## Steps
1. Ask where the product is sold (own site, Hotmart, Kiwify, Stripe, Shopify) and whether a Pixel already exists.
2. Walk through: Pixel installed on the sales page, PageView firing, the checkout or lead event, the **Purchase** event and how it reaches Meta (platform pixel integration, Conversions API or a sales webhook), and event deduplication.
3. Tell the user how to verify: Events Manager → Test events, then a real test purchase. Do not mark tracking as confirmed until the user says the Purchase event appeared.
4. Update `campaign.purchaseEventConfirmed` in `meta-ads-config.json` only after that confirmation.

## Output
A short checklist with what is done and what is missing. Be explicit that without a working Purchase event, a sales campaign cannot optimise properly.
