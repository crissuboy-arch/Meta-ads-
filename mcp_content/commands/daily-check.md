---
description: Daily performance check across ALL connected accounts and Business Managers: what is running, what is working, what needs attention. Reads only; changes nothing.
argument-hint: "[today | yesterday | last_7d]  (default: today)"
---

Follow the `metrics-reading` skill. This command only reads. It never pauses, enables or edits anything without an explicit yes.

## Steps
1. Period: `$ARGUMENTS` if given, otherwise `today`. Call `account_overview` for that period, and once more for `last_7d` as the account's own baseline.
2. For every account that has active campaigns or spend, call `get_insights` with `level: "campaign"` for the period, and `list_objects` (`campaigns`) to get status and daily budget. For the 3 campaigns with the most spend, also call `get_insights` with `level: "ad"` to find the weakest and strongest ads.
3. Judge each campaign against **that account's own 7-day numbers**, not against invented targets. Flag, with the numbers that justify it:
   - spend today with zero results while the 7-day baseline has results;
   - cost per result clearly above the 7-day average;
   - CTR very low on 1,000+ impressions (likely a creative or audience problem);
   - ads with status DISAPPROVED or WITH_ISSUES, or accounts that are not ACTIVE;
   - active campaigns that are not spending (budget, learning limited, review).
   Say plainly when there is too little data to judge (early in the day, few impressions). Never present noise as a trend.
4. If the user has told you their break-even ROAS or target cost per result, use it. If not and it matters, ask once.

## Output
1. **Overview table** grouped by Business Manager (account, status, active campaigns, spend, results, cost/result, ROAS), each in its own currency.
2. **Needs attention now** — a short numbered list: what, which campaign/ad, the numbers, and a suggested action.
3. **Working well** — what to protect or scale, with the numbers.
4. End by asking which suggested actions to apply. Only after a clear "yes" use `set_status` (pause) or propose other changes. Enabling anything that is paused still needs the budget confirmation described in the `meta-ads-manager` skill.
