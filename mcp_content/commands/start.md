---
description: Welcome + quick diagnosis of where you are, then tells you which command to run first
argument-hint: "(no arguments — it asks what it needs)"
---

Welcome the user to **Meta Ads Expert PRO** and find out where they are, so you can point them to the right first command. This command does not research, publish or spend anything.

## Ask (short blocks, one at a time or grouped)

1. What do you sell? (one sentence)
2. Who is it for, and what country/language will you advertise in?
3. Daily budget for the test?
4. Do you have a sales page? (ask for the link)
5. Do you have the Meta Pixel installed and the Purchase event working?
6. Do you already have creatives (images/videos)?
7. Goal: direct sales, leads, WhatsApp/Direct messages, or traffic?
8. Is your Meta account connected in the app (Connect ad accounts)? Check with `list_ad_accounts`. If not, tell the user to connect it there.

## Recommend a sequence

- No setup yet → `/setup`
- No market research → `/research [product]`
- Offer or price unclear → ask to run the `offer-evaluation` skill
- Weak or unknown sales page → `/audit [product]`
- Pixel/Purchase not confirmed and goal is sales → `/tracking` before any spend
- Ready → `/creative` → `/campaign` → `/publish`

End with the single next command to run and why.
