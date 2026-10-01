---
name: meta-ads-manager
description: Use this skill when publishing a campaign in Meta Ads Manager (Facebook/Instagram) via the browser — campaign, ad set, and ad creation, plus status verification. Trigger when the user says "publish campaign," "launch an ad," "put it live on Meta," or runs /publish.
---

# Publishing in Ads Manager (via browser)

All publishing happens with the user's own logged-in session in Claude in Chrome, at business.facebook.com/adsmanager. The system never asks for, stores, or types the user's Meta password/token on their behalf.

## Golden rule — real money involved

Before clicking publish at any level (campaign, ad set, or ad), show the user exactly what's about to be created and ask for explicit confirmation. Never publish levels automatically in sequence without a checkpoint — a budget or audience mistake published without review costs the user real money.

## Flow

1. **Login**: navigate to `business.facebook.com/adsmanager`. If it asks for login, ask the user to log in manually — never fill in credentials.
2. **Create campaign**: "Create" → choose the objective defined in `campaign-[product].md` → name the campaign identifiably (e.g., `[product] — test [date]`).
3. **Budget**: set it at campaign (CBO) or ad set level per the brief — use exactly the brief's daily value; never round up without flagging it.
4. **Ad set(s)**: for each test audience in the brief — location, age, gender, interests (verify each suggested interest exists in the picker; if not under that exact name, find the closest match and flag the swap to the user) and placements (Advantage+ unless the brief says otherwise).
5. **Ads**: for each approved creative — upload primary text, headline, description, CTA, and the image/video (if the user already has the file ready in the connected folder; otherwise flag that the visual file is missing before publishing).
6. **Pre-publish review**: show a screenshot of each level (campaign/ad set/ad) to the user for final confirmation.
7. **Publish** and wait for the status to move from "In review" to "Active" or "Rejected" (Meta's review can take minutes to hours — don't stall the conversation waiting; tell the user they can check later with `/analyze` or by asking for status again).

## If an ad gets rejected

Read the exact reason Meta gives in the interface (it shows on the ad itself). Fix only the cited point (copy, image, or destination link) following the `ad-copywriting` and `creative-score` skills, and resubmit for review — never resubmit without understanding the reason.

## Post-publish verification

Confirm: campaign name, configured budget matches the brief, audiences match the brief, and the status of each ad. Report all of it to the user — never assume it published correctly without checking the final screen.
