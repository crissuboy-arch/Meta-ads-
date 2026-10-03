---
description: One-time setup — business, default audience, budget, and the Meta account details needed to create campaigns
---

Set up the environment. Follow this order.

## 1. Working folder
Check that the user has a folder connected. If not, ask them to connect one (for example "Campaigns"). Everything — config, research, creatives, briefs — is saved there so it persists between sessions.

## 2. Existing config
Look for `meta-ads-config.json`. If it exists, show a short summary and ask what to update. If not, collect the data below.

## 3. Business data (ask via a form or short questions)
- Product and a one-line positioning (what, for whom)
- Default market: country/region and language
- Default audience: age range, gender if relevant (always editable per campaign)
- Default daily test budget (suggest a sensible minimum for the objective, never promise results)
- Default objective: sales, leads, messages, traffic
- Default destination URL
- Pixel and Conversions API: installed? Purchase event confirmed in Events Manager → Test events?
- Publishing mode: `confirm` (default and recommended: confirm each level before it is created) — explain that everything is created paused either way, and that nothing is enabled without an explicit yes.

## 4. Meta account details (needed by /publish)
- Call `get_connectors` and show the Meta Ads (`facebook`) accounts connected in Windsor. Ask which one to use and save its id and name.
- Ask for the **Facebook Page ID** that will run the ads and the **Pixel ID**. Tell the user where to find them: Page → About → Page transparency (Page ID); Events Manager → Data sources (Pixel ID).
- If the ads will run in the EU or in Brazil, Taiwan, Singapore, Thailand, Australia or India, explain that Meta requires verified beneficiary/payer details and ask whether they are set up in Meta Business settings.
- Never ask for a password or access token. If the connector or account is not connected, stop and send the user to START-HERE.md, step 2.

## 5. Save
Write `meta-ads-config.json` in the connected folder:

```json
{
  "business": { "name": "", "positioning": "", "defaultUrl": "" },
  "audience": { "market": "", "language": "", "ageMin": 18, "ageMax": 65, "gender": "all" },
  "campaign": { "defaultObjective": "OUTCOME_SALES", "defaultDailyBudget": 20, "pixelId": "", "purchaseEventConfirmed": false },
  "publishMode": "confirm",
  "meta": { "adAccountId": "", "adAccountName": "", "pageId": "" }
}
```

## 6. Finish
Confirm what was saved and explain the cycle: `/research` → `/creative` → `/campaign` → `/publish` → `/analyze`.
