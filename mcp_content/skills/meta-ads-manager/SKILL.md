---
name: meta-ads-manager
description: Use this skill when creating a campaign in Meta Ads (Facebook/Instagram) through the Windsor.ai connector — campaign, ad set and ad creation, always created PAUSED, plus status checks. Trigger when the user says "publish campaign," "launch an ad," "create it on Meta," or runs /publish.
---

# Creating campaigns on Meta through the connector

All creation goes through the **Windsor.ai connector** (tools `get_connectors`, `list_actions`, `execute_action`, `upload_files`, `get_data`). The user connected their own Meta Ads account there. The system never asks for, stores or types the user's Facebook password or access token. If the connector is not installed or the Meta Ads account is not connected, stop and send the user to `START-HERE.md`, step 2.

## Golden rules — real money involved

1. **Everything is created PAUSED.** Never pass `status: "active"` on create. Nothing spends until the user says so.
2. **Show before you create.** Before each level (campaign, ad set, ad) show exactly what will be created and wait for an explicit "yes". Never chain levels without a checkpoint.
3. **Enabling is a separate decision.** Only call `enable_campaign`, `enable_adset` or `enable_ad` after the user explicitly confirms the total daily spend and says to turn it on. Repeat the daily budget back to them in plain currency.
4. **Never invent IDs.** Page ID, Pixel ID and ad account ID come from the user or from the connector. If you are missing one, ask.
5. **No edits to live ads without asking.** Budget changes, creative swaps and pauses all need the user's go-ahead.

## Before creating anything

1. Call `get_connectors` and confirm `facebook` (Meta Ads) has an account. Use that account id in every `execute_action` call. If several accounts exist, ask which one.
2. Read `campaign-[product].md` and `meta-ads-config.json` from the connected folder.
3. Collect what the brief does not already have: **Facebook Page ID**, **Pixel ID** (for sales campaigns), destination URL, and the creative files.
4. Call `list_actions` for `facebook` once per session and read the schema before you use an action. Do not assume a parameter exists.

## Flow

1. **Campaign** — `create_campaign`
   - `objective`: a Meta outcome objective, e.g. `OUTCOME_SALES`, `OUTCOME_LEADS`, `OUTCOME_TRAFFIC`, `OUTCOME_ENGAGEMENT`.
   - `special_ad_categories`: `[]` unless the ads fall in a regulated category (housing, employment, credit). Ask if unsure.
   - Budget: amounts are in the account currency's **minor unit** (5000 means 50.00). Zero-decimal currencies (JPY, KRW, CLP and others) use whole units. Confirm the converted number with the user in normal currency.
   - Name it so it is easy to find: `[product] — test [date]`.
   - Status stays `paused`.
2. **Ad set(s)** — `create_adset`, one per test audience in the brief
   - Needs `campaign_id`, `name`, `optimization_goal`, `billing_event`, and `targeting` (countries, ages, genders, interests, placements).
   - For sales: `optimization_goal` `OFFSITE_CONVERSIONS` with `promoted_object` `{"pixel_id": "<id>", "custom_event_type": "PURCHASE"}`. If the Purchase event is not firing yet, tell the user the campaign will not learn properly and offer to optimise for `LANDING_PAGE_VIEWS` or an upper-funnel event first.
   - If the budget is not set at campaign level, set `daily_budget` here.
   - **Regulated regions:** ads delivered to the EU need `dsa_beneficiary` and `dsa_payor`. Brazil, Taiwan, Singapore, Thailand, Australia and India need `regional_regulated_categories` plus `regional_regulation_identities` with verified beneficiary and payer IDs from Meta Business settings. If the user has not set these up, say so before trying and let them prepare it. Do not make up values.
3. **Creatives** — images
   - `create_ad_image` needs files, so use `upload_files` (it opens an upload widget in the chat) and read back the `image_hash`. Videos: `create_ad_video` takes a public URL.
4. **Ads** — `create_ad`
   - Provide `adset_id`, `name`, `page_id`, `link`, `message` (primary text), `headline`, `description`, `image_hash` or `image_url`, and `call_to_action_type` (for example `LEARN_MORE` or `SHOP_NOW`).
   - Use the approved copy from `creatives/[product]/variations.md` exactly as approved.
5. **Review** — summarise everything created, with IDs, in one table. Ask the user to open Ads Manager and look at it once before enabling.
6. **Enable** — only on explicit confirmation (see rule 3). Enable the ads, then the ad set, then the campaign. Meta then reviews the ads; this can take minutes to hours.

## If something fails

- Read the exact error returned. Common causes: a missing required field, an unsupported objective/goal pairing, missing regional identities, or a Page the account cannot use.
- Fix only what the error cites. Do not retry the same call unchanged. After two failed attempts, stop and explain to the user in plain language.
- If a created ad is rejected after review, read Meta's reason in the data, fix only the cited point (copy, image or link) following `ad-copywriting` and `creative-score`, and ask before resubmitting.

## After publishing

Verify with `get_data` (call `get_fields` first) that names, budgets and statuses match the brief. Report the result. Never claim it was created correctly without checking.

## What this skill does not do

It does not promise results, does not change a payment method, and does not delete anything (there is no delete action). To remove something, pause it and tell the user to delete it in Ads Manager.
