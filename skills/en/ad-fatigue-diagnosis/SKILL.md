---
name: ad-fatigue-diagnosis
description: "Ad Fatigue Diagnosis — Specialized skill for diagnosing ad fatigue"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Ad Fatigue Diagnosis

This skill enables Claude to identify, analyze, and prescribe solutions for ad fatigue across Meta Ads, Google Ads, and TikTok Ads campaigns, optimizing performance and cost per result.

---

## Keywords

Ad fatigue, Frequency, Declining CTR, Rising CPM, Increasing cost per result, Meta Ads, Google Ads, TikTok Ads, Creative optimization, Ad rotation, Audience targeting, High CPA, Falling ROAS, Relevance diagnostics.

---

## Quick Start

1.  **Monitor Frequency**: Check the "Frequency" column in Meta Ads or TikTok Ads. Average frequency above 3.0 in 7 days for cold audiences, or 5.0 for warm audiences, should trigger an alert.
2.  **Analyze CTR and Cost Trends**: Compare Click-Through Rate (CTR) and Cost per Action (CPA/CPL) from the last 7 days against the previous 7 days. A CTR drop over 20% combined with a CPA increase over 15% are strong fatigue indicators.
3.  **Check Feedback and Relevance**: Open the "Quality Ranking" reports (Meta Ads) or "Quality Score" (Google Ads). Read ad comments for mentions like "same ad again" or "annoying" to validate fatigue.
4.  **Prepare New Assets**: Immediately start creating new creatives (images, videos, copy) and explore new audience segments for testing.

---

## Core Workflows

### Workflow 1: Predictive Ad Fatigue Diagnosis via Frequency and Engagement

**Context**: Campaigns with still-stable performance, but showing early signs of audience saturation and risk of imminent fatigue. The goal is to intervene before end-result metrics (CPA, ROAS) are severely impacted.

**Step 1: Advanced Frequency Monitoring**
*   **Action**: Open the Meta Ads dashboard (or Google Ads/TikTok Ads) and add the "Frequency" column at the Ad Set level. Export the data to a spreadsheet for historical analysis.
*   **Practical Example**: For a Meta Ads prospecting campaign (cold audience) of 1 million people, if the average "Frequency" over the last 7 days reaches 2.8, that's already a yellow flag. For a remarketing audience of 100K people, a "Frequency" of 4.5 in 7 days signals high saturation risk.
*   **Alert Threshold**: Frequency > 2.5 in 7 days for cold audiences (prospecting) or > 4.0 in 7 days for warm audiences (remarketing) requires immediate attention.

**Step 2: Combined Analysis of CTR, Frequency, and Video Completion Rate**
*   **Action**: Compare "Frequency" against "Click-Through Rate (CTR)" and, for video creatives, the "Video Completion Rate (75% or 100%)."
*   **Practical Example**: A Google Display ad that 30 days ago had Frequency 1.8 and CTR 0.9%, and now shows Frequency 3.5 and CTR 0.6%, is clearly fatigued. On TikTok Ads, a video that used to complete at 40% (75% mark) and now completes at 18% with high frequency indicates waning interest.
*   **Reference Metric**: A CTR drop > 15% combined with a Frequency increase > 10% (comparing the last 7 days to the previous 7 days) is a strong predictor. A 50% drop in video completion rate is too.

**Step 3: Checking Feedback Quality and Relevance Diagnostics (Meta Ads / Google Ads)**
*   **Action**: In Meta Ads, go to the ad level and check the "Relevance Diagnostics" (quality, engagement, conversion). In Google Ads, watch the keyword "Quality Score" and ad relevance.
*   **Practical Example**: A Meta Ads ad with below-average "Quality Ranking" and below-average "Engagement Rate Ranking," plus recurring negative comments like "I can't stand seeing this anymore," confirms fatigue and perceived irrelevance. A 3/10 Quality Score in Google Ads on highly relevant terms is also a signal.
*   **Immediate Action**: Prioritize creating entirely new creatives with distinct messaging approaches for the ads with the worst relevance diagnostics.

### Workflow 2: Reactive Optimization of Campaigns with Confirmed Ad Fatigue

**Context**: Campaign with sharply declining performance (ROAS falling, CPL/CPA rising fast) and fatigue already confirmed by the Workflow 1 indicators. The goal is to reverse the downward trend and optimize quickly.

**Step 1: Aggressive Rotation and New Creative Testing**
*   **Action**: Pause the worst-performing ads (highest frequency, lowest CTR, highest CPA) and immediately activate a new set of creatives.
*   **Practical Example**: In a Meta Ads campaign, video A had Frequency 6.1 and CTR 0.5% over the last 15 days, while video B (new) has Frequency 1.5 and CTR 2.8%. Pause video A, and launch 3-4 new variations (e.g., a video with a different angle, a static testimonial image, a benefits carousel) into the same ad set, letting the platform optimize delivery toward the most engaging ones.
*   **Strategy**: Always keep a "pool" of 3-5 fresh creatives, not directly related to the previous ones, for each ad set at high fatigue risk. Every 7-10 days, evaluate performance and replace the underperformers.

**Step 2: Audience Re-Engineering and Exclusions**
*   **Action**: If the audience is saturated, expand it or create radically different new segments. Implement strict exclusions.
*   **Practical Example**: For Google Ads, if an "Affinity Interests" audience shows high frequency and high CPC, add new related interests, but also build a custom intent audience with new long-tail keywords and an exclusion audience for anyone who visited the thank-you page (purchase/lead) in the last 90 days. In Meta Ads, create a 1% Lookalike based on the most recent converters (last 7 days) and exclude everyone who engaged with the page or ads in the last 30 days.
*   **Specific Action**: For remarketing campaigns, tighten the targeting window (e.g., from 30 to 7 days) and get more aggressive with exclusions for people who already converted or engaged repeatedly without converting.

**Step 3: Tactical Budget and Bidding Strategy Adjustments**
*   **Action**: Reduce budget on ad sets with severe fatigue and reallocate to new ad sets with fresh audiences and creatives. Consider adjusting the bidding strategy.
*   **Practical Example**: A TikTok Ads ad set that used to generate leads at $12 now generates them at $45 with Frequency 7.0. Cut the daily budget from $150 to $50 and create a new ad set with unexplored creatives and audiences, allocating the remaining $100 to the new ad set.
*   **Consideration**: On platforms with automated bidding (Target CPA, Target ROAS), fatigue can drive the bid up as the system "forces" delivery. Consider testing manual or semi-automated bidding (Max Cost) in a new ad set for more cost control, especially during recovery.

---

## Templates

### Ad Fatigue Analysis Report

```
## Ad Fatigue Analysis Report - [Campaign/Ad Set Name]

**Analysis Date:** 2024-11-05
**Period Analyzed:** Last 30 days vs. previous 30 days (2024-10-06 to 2024-11-05)

**1. Main Diagnosis:**
*   **Campaign/Ad Set:** "Meta Ads - Small Business Marketing Ebook Sales - Cold Audience"
*   **Platform:** Meta Ads
*   **Overall Status:** Moderate to High Fatigue. Sharp CTR drop and CPL increase, with high frequency.

**2. Key Metrics Observed:**
*   **Average Frequency (Last 7 days):** 4.1 (+32% vs. previous period)
*   **Average Frequency (Last 30 days):** 7.8 (+20% vs. previous period)
*   **Average CTR (Last 7 days):** 0.65% (-40% vs. previous period)
*   **Cost per Lead (CPL) (Last 7 days):** $22.80 (+65% vs. previous period)
*   **CPM (Last 7 days):** $28.50 (+25% vs. previous period)
*   **Video Completion Rate (75%) (Last 7 days):** 15% (-55% vs. previous period)
*   **Comments/Feedback:** Increase in comments like "I've seen this ad a thousand times!", "Not relevant to me", "Annoying". Relevance Diagnostics (Meta Ads): "Quality Ranking" and "Engagement Rate Ranking" below average.

**3. Affected Creatives:**
*   **Creative ID 1:** [VIDEO_ID_456789] - Video "Happy Customer Testimonial"
    *   **Frequency:** 4.8
    *   **CTR:** 0.58%
    *   **CPL:** $25.00
    *   **Notes:** Main source of negative feedback and worst video completion performance.
*   **Creative ID 2:** [IMAGE_ID_123456] - Image "5 Marketing Tips Infographic"
    *   **Frequency:** 3.9
    *   **CTR:** 0.72%
    *   **CPL:** $20.50
    *   **Notes:** Declining performance, but still some residual engagement.

**4. Affected Audience:**
*   **Audience Name:** "Interests: Entrepreneurship, Small Business, Digital Marketing (US)" - Size: 9.2M
*   **Notes:** The high frequency and engagement drop indicate the most responsive segment of this audience is saturated with the current creatives.

**5. Immediate Recommendations:**
*   Pause Creative [VIDEO_ID_456789] immediately.
*   Duplicate the Ad Set and test 4 new creatives (2 videos, 2 static images) focused on new angles (e.g., "Time Savings", "More Sales", "Essential Tools").
*   Create a new 1% Lookalike audience based on leads generated in the last 14 days (for the new Ad Set).
*   Cut the current Ad Set budget by 40% and allocate it to a new Ad Set with the new creatives and audience.
*   Implement an exclusion for people who engaged with ads in the last 7 days in the original Ad Set.
*   Monitor Frequency, CTR, and CPL daily for the next 7 days in the new Ad Sets.
```
