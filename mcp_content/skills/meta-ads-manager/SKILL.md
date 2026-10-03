---
name: meta-ads-manager
description: Use this skill when creating a campaign in Meta Ads (Facebook/Instagram) through this server's own Meta tools — campaign, ad set and ad creation, always created PAUSED, plus status checks. Trigger when the user says "publish campaign," "launch an ad," "create it on Meta," or runs /publish.
---

# Creating campaigns on Meta with this server's tools

All creation goes through the tools of **this server**: `list_ad_accounts`, `list_pages`, `list_pixels`, `create_campaign`, `create_adset`, `create_ad`, `list_objects`, `get_insights`, `set_status`. The user connected their own Meta account inside the app (page *Conectar contas de anúncio*). You never see, ask for or type a password or access token. If a tool says the Meta account is not connected or the token expired, stop and tell the user to open the app → Connect ad accounts → Connect with Facebook.

## Golden rules — real money involved

1. **Everything is created PAUSED.** Never pass `status: "active"` on create. Nothing spends until the user says so.
2. **Show before you create.** Before each level (campaign, ad set, ad) show exactly what will be created and wait for an explicit "yes". Never chain levels without a checkpoint.
3. **Enabling is a separate decision.** Only call `set_status` with `ACTIVE` (and `user_confirmed: true`) after the user explicitly confirms the total daily spend and says to turn it on. Repeat the daily budget back to them in plain currency.
4. **Never invent IDs.** Page ID, Pixel ID and ad account ID come from the user or from the connector. If you are missing one, ask.
5. **No edits to live ads without asking.** Budget changes, creative swaps and pauses all need the user's go-ahead.

## Before creating anything

1. Call `list_ad_accounts` and use its `account_id` as `ad_account_id` in every call. If several accounts exist, ask which one.
2. Read `campaign-[product].md` and `meta-ads-config.json` from the connected folder.
3. Collect what the brief does not already have: **Facebook Page ID** (`list_pages`), **Pixel ID** (`list_pixels`, for sales campaigns), destination URL, and the creative image links (public https URLs).
4. Read each tool's input schema before using it. Do not assume a parameter exists.

## Flow

1. **Campaign** — `create_campaign`
   - `objective`: a Meta outcome objective, e.g. `OUTCOME_SALES`, `OUTCOME_LEADS`, `OUTCOME_TRAFFIC`, `OUTCOME_ENGAGEMENT`.
   - `special_ad_categories`: `[]` unless the ads fall in a regulated category (housing, employment, credit). Ask if unsure.
   - Budget: pass `daily_budget` in **normal currency** (10 means 10.00); the server converts it to Meta's minor unit. Repeat the number back to the user.
   - Name it so it is easy to find: `[product] — test [date]`.
   - Status stays `paused`.
2. **Ad set(s)** — `create_adset`, one per test audience in the brief
   - Needs `campaign_id`, `name`, `optimization_goal`, `billing_event`, and `targeting` (countries, ages, genders, interests, placements).
   - For sales: `optimization_goal` `OFFSITE_CONVERSIONS` with `promoted_object` `{"pixel_id": "<id>", "custom_event_type": "PURCHASE"}`. If the Purchase event is not firing yet, tell the user the campaign will not learn properly and offer to optimise for `LANDING_PAGE_VIEWS` or an upper-funnel event first.
   - If the budget is not set at campaign level, set `daily_budget` here.
   - **Regulated regions:** ads delivered to the EU need `dsa_beneficiary` and `dsa_payor`. Brazil, Taiwan, Singapore, Thailand, Australia and India need `regional_regulated_categories` plus `regional_regulation_identities` with verified beneficiary and payer IDs from Meta Business settings. If the user has not set these up, say so before trying and let them prepare it. Do not make up values.
3. **Creatives** — images
   - Images are passed to `create_ad` as `image_url`, a **public https link** the user provides (for example a hosted file). Meta downloads it. Video ads are not supported by these tools yet: tell the user to add the video in Ads Manager.
4. **Ads** — `create_ad`
   - Provide `adset_id`, `name`, `page_id`, `link`, `message` (primary text), `headline`, `description`, `image_url` (or `image_hash`), and `call_to_action_type` (for example `LEARN_MORE` or `SHOP_NOW`).
   - Use the approved copy from `creatives/[product]/variations.md` exactly as approved.
5. **Review** — summarise everything created, with IDs, in one table. Ask the user to open Ads Manager and look at it once before enabling.
6. **Enable** — only on explicit confirmation (see rule 3), with `set_status`. Enable the ads, then the ad set, then the campaign. Meta then reviews the ads; this can take minutes to hours.

## If something fails

- Read the exact error returned. Common causes: a missing required field, an unsupported objective/goal pairing, missing regional identities, or a Page the account cannot use.
- Fix only what the error cites. Do not retry the same call unchanged. After two failed attempts, stop and explain to the user in plain language.
- If a created ad is rejected after review, read Meta's reason in the data, fix only the cited point (copy, image or link) following `ad-copywriting` and `creative-score`, and ask before resubmitting.

## After publishing

Verify with `list_objects` (levels `campaigns`, `adsets`, `ads`) that names, budgets and statuses match the brief. Report the result. Never claim it was created correctly without checking.

## What this skill does not do

It does not promise results, does not change a payment method, and does not delete anything (there is no delete tool). To remove something, pause it and tell the user to delete it in Ads Manager.
