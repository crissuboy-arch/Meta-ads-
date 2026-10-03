---
description: Creates the campaign, ad sets and ads in Meta with this server's Meta tools — always paused
argument-hint: "[product] — needs a confirmed campaign-[product].md"
---

Create the campaign following the `meta-ads-manager` skill. Everything is created **paused**. Nothing spends until the user explicitly asks to enable it.

## Steps
1. Read `campaign-[product].md` and `meta-ads-config.json` (`meta.adAccountId`, `meta.pageId`, `campaign.pixelId`). If any is missing, ask for it. Never invent IDs.
2. Check the connection: call `list_ad_accounts`. If it returns no accounts or says Meta is not connected, stop and tell the user to open the app → Connect ad accounts → Connect with Facebook.
3. Show the final summary: objective, daily budget in normal currency, duration, audiences, creatives, destination URL, and the note that everything will be created paused.
4. Create level by level with a checkpoint before each one: campaign, then ad sets, then (after the image upload) ads. Ask for an explicit "yes" before each level.
5. After creation, verify with `list_objects` that names, budgets and statuses match the brief.
6. Ask the user to open Ads Manager and review. Only enable when they confirm the total daily spend and ask to turn it on.

## Output
A table with campaign, ad set and ad names, IDs and status. Update `campaign-[product].md` with the date, IDs and status. Suggest waiting for the minimum test period before `/analyze [product]`.
