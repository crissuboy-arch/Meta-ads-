---
description: Starts from the user's REAL accounts: shows what is running now across all Business Managers, then proposes the next step. No generic questionnaire.
argument-hint: "(no arguments — it reads the accounts first)"
---

Start from data, not from a questionnaire. Never open with a list of questions you could answer with a tool. This command does not publish or spend anything.

## Steps
1. Call `list_ad_accounts`.
   - If it fails or returns nothing: say the Meta account is not connected, tell the user to open the app → **Connect ad accounts** → Connect with Facebook (or paste a Business Manager token), and stop there.
2. Call `account_overview` with `date_preset: "today"`. Show one compact table grouped by Business Manager: account, status, active campaigns, spend, results, ROAS. Collapse accounts with no active campaigns and no spend into a single line ("N accounts idle: …"). Keep each account's own currency; never add different currencies.
3. Add **at most 3 observations** taken from the numbers, for example: an account with spend but zero results; an account whose status is not ACTIVE (disabled, unsettled, in review); an account with active campaigns but no spend today (not delivering). If everything is quiet, say so.
4. Offer the next step as a short menu based on what you saw:
   - **See how everything is performing** → `/daily-check`
   - **Create a new campaign** → `/campaign` (see below)
   - **Audit a page, offer or account** → `/audit` or `/full-audit`
   - **Fix tracking before spending** → `/tracking`
5. If the user picks a new campaign, ask in **one message, at most 4 questions**, and only for what you cannot infer: what is being sold + the link of the page, the country/language, the daily test budget, and the goal (sales, leads, messages, traffic). Before asking, look at what already exists (`list_objects`, `list_pixels`, `list_pages`) and reuse the Page, Pixel, currency and objective that the account already uses. Offer them as defaults instead of asking.

## Rules
- Answer in the user's language.
- Do not ask about the Pixel, Page or creatives before checking whether the tools already tell you.
- Finish with the single next command and why.
