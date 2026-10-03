---
name: metrics-reading
description: Use this skill to interpret Meta Ads campaign metrics pasted manually by the user (CPM, CPC, CTR, CPA, ROAS, frequency, impressions, reach, conversions) and suggest the next step. It never pulls data automatically — it works only with what the user pastes. Trigger when the user says "analyze my results," "are these metrics good," "what should I do with these numbers," or runs /results-analysis.
---

# Reading Manually Pasted Metrics

This skill never accesses Ads Manager directly to pull data — it works only with what the user pastes into the chat (screenshot, table, text). If a metric important to the read is missing, ask for it specifically — never estimate or invent the value.

## What each metric indicates (limited on its own — read them together)

- **CPM** (cost per 1,000 impressions): reflects audience competition and creative quality/relevance. CPM rising over days with the same audience usually signals creative fatigue.
- **CTR** (click-through rate): reflects hook/creative strength and audience relevance. Low CTR with normal CPM → the problem is the creative, not the audience.
- **CPC** (cost per click): a combination of CPM and CTR — don't read it in isolation; check those two first.
- **Frequency**: how many times the same person saw the ad. Above ~3-4 on a small audience usually signals fatigue — CTR drops and CPM rises along with it.
- **CPA** (cost per result/acquisition): the metric that matters most for business decisions — compare it against how much the user can afford to pay per result (if they share that) before calling it "good" or "bad."
- **ROAS** (return on ad spend): only base scale/pause decisions on this when the user shares the product's margin/profit — a "positive" ROAS can still lose money if the margin is thin.
- **Reach vs. Impressions**: impressions far above reach on a small audience reinforces the frequency/fatigue diagnosis.
- **Page conversion rate** (conversions ÷ clicks, if the user provides it): separates an ad problem (unqualified traffic) from a page/offer problem (good traffic that doesn't convert).

## Combined diagnosis (common patterns)

- Good CTR + high CPA → traffic is clicking but not converting: review the page/offer (`/audit` or `/offer`), not the creative.
- Low CTR + normal CPM → weak creative/hook: review with `creative-hooks` and test a new angle.
- Rising CPM + high frequency → creative fatigue: swap the creative or broaden the audience.
- Too little data (low click/result volume) → don't draw conclusions yet, a small sample misleads; tell the user that instead of recommending a hasty change.

## Output

Present: a read of each relevant metric, the most likely combined diagnosis, and 1-2 concrete next steps (which system command to use — `/hooks`, `/offer`, `/full-audit`, `/ab-test` — per the diagnosis). Never promise future results ("this will improve X%") — only point to the most likely cause and the recommended action.
