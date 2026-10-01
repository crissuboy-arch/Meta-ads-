---
name: google-ads-manager
description: Use this skill when publishing a Google Ads Search campaign via the browser — campaign creation, ad groups, keywords, responsive search ads, and status verification. Trigger when the user says "publish on Google Ads," "advertise on Google," "search campaign," or runs /google-ads.
---

# Publishing on Google Ads (via browser)

All publishing happens with the user's own logged-in session in Claude in Chrome, at ads.google.com. The system never asks for, stores, or types the user's Google password/token on their behalf. Same golden rule as `meta-ads-manager`: real money, explicit confirmation before every publish.

## Key differences from Meta

- Google Ads (Search) is **intent** advertising, not interruption: the audience is already actively searching — which is why the keywords from `research-[product].md` (mainly **transactional** and **commercial** intent) are the heart of the campaign here, far more than the interests used on Meta.
- There's no "visual creative" in a standard search ad — the ad is text only (Responsive Search Ad/RSA): headlines and descriptions that Google tests and recombines automatically.
- There's a **Quality Score** concept (keyword + ad + landing page relevance) — which is why running `/audit` on the landing page first helps avoid pricier CPCs from low relevance.

## Flow

1. **Login**: navigate to `ads.google.com`. If it asks for login, ask the user to log in manually.
2. **Create campaign**: choose an objective compatible with the config (default: Sales or Leads, campaign type "Search") → name it identifiably (e.g., `[product] — Search [date]`).
3. **Budget and bids**: use the daily value defined in `campaign-[product].md` (the same score-based suggestion logic from the audit applies here) → simple bidding strategy to start (Maximize Clicks or manual CPC with a cap); avoid automated conversion strategies before there's data volume/tracked conversions.
4. **Ad groups and keywords**: 1 group per intent theme (e.g., "transactional" separate from "commercial"), using the keywords from `research-[product].md`. Set phrase or exact match to control spend better at the start — avoid broad match without negative search-term control.
5. **Negative keywords**: add terms clearly outside the audience (e.g., "free," "course," "jobs" if not applicable) so you don't pay for irrelevant clicks.
6. **Responsive search ad**: upload 3 to 15 headlines and 2 to 4 descriptions per group, using copy from the `ad-copywriting` skill adapted to Google's short text format (no emojis, headline up to 30 characters, description up to 90).
7. **Ad extensions (assets)**: fill in with real data from the config — sitelinks, call (phone/WhatsApp), callouts, structured snippets. Extensions increase the space your ad occupies at no extra cost and improve relevance.
8. **Pre-publish review**: show a screenshot of each level (campaign/group/ad) to the user for final confirmation, same as the Meta flow.
9. **Publish** and wait for the status ("Under review," "Active," "Disapproved").

## If an ad gets disapproved

Read the exact reason inside Google Ads. Adjust following the policy (health/finance claims have their own rules, stricter than Meta's in some points) and resubmit.

## Post-publish verification

Confirm: budget, keywords, and match types match the brief, extensions are filled in, and the status of each ad. Report everything to the user.
