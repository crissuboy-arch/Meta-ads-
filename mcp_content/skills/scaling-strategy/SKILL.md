---
name: scaling-strategy
description: "Scaling Strategy — Specialized skill for scaling strategy"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Scaling Strategy

This skill enables you to implement and optimize scaling strategies for digital ad campaigns on Meta Ads, Google Ads, and TikTok Ads, maximizing ROAS and conversion volume.

---

## Keywords

Vertical scaling, horizontal scaling, CBO, ABO, Target ROAS, Lookalike audiences, Performance Max, Broad audiences, Bid cap, Cost cap, Creative refresh, Ad fatigue, Budget allocation, Incrementality test.

---

## Quick Start

1.  Analyze the ROAS or CPA of active campaigns over the last 72 hours to identify those performing 20% above target with room to scale.
2.  Increase the budget of CBO campaigns (Meta Ads) by 15-20% every 48-72 hours, as long as ROAS stays stable or with a controlled drop (max 10%).
3.  Duplicate the ad set with the best ROAS/CPA (Google Ads) and test a 10% lower Target CPA or a 15% higher Target ROAS, using the same creative and audience.
4.  Launch a test campaign (TikTok Ads) with a 1% Lookalike audience based on "Buyers (last 90 days)" and a $150/day budget.

---

## Core Workflows

### Workflow 1: Sustainable Vertical Scaling on Meta Ads with CBO

This workflow details the budget increase strategy for Meta Ads conversion campaigns, focusing on ROAS sustainability and "ad fatigue" prevention.

**Detailed Steps:**

1.  **Candidate Campaign Identification:**
    *   Monitor Sales (CBO) campaigns that consistently deliver a ROAS at least 20% above target over the last 3 to 5 days.
    *   **Example:** "Sales - Winter Collection 2024" campaign with an average ROAS of 3.5x over the last 72h, while the target ROAS is 2.8x. Current budget $600/day, generating 15-20 purchases per day.
    *   Check that the main ad set isn't running high frequency (> 3.0 in 7 days) or a sharply rising CPM, indicating "ad fatigue."

2.  **Attribution Window and Stability Analysis:**
    *   Confirm that ROAS is stable in the main attribution window (e.g.: 7-day click, 1-day view).
    *   Check the daily and weekly cost per purchase (CPA). Avoid scaling if the CPA is fluctuating a lot or trending up over the last 24-48h.
    *   **Example:** The average CPA is $40. Don't scale if the CPA of the last 24h is $55, even with a good overall ROAS.

3.  **Gradual Budget Increase:**
    *   Increase the CBO campaign budget in 15-20% increments every 48-72 hours.
    *   **Practical Example:**
        *   Initial budget: $600/day.
        *   Increase 1 (Day 1): $600 + 20% = $720/day.
        *   Wait 48-72h, monitor ROAS and CPA.
        *   If ROAS > 3.0x: Increase 2 (Day 3/4): $720 + 20% = $864/day.
        *   Continue this process, always watching the metrics.
    *   **Tip:** Larger increases can "shock" the algorithm, leading to higher CPA and lower ROAS temporarily.

4.  **Continuous Maintenance and Optimization:**
    *   While scaling, keep testing new creatives within the same CBO campaign. Pause ads with CTR below 1.5% or CPM significantly above the campaign average.
    *   Monitor ad frequency and CPM. If frequency goes above 3.5 in 7 days and CPM rises 20% with no ROAS improvement, it's time to refresh creatives or expand the audience.
    *   **Example:** If a video that performed well now has a 1.2% CTR and a $50 CPM, while the average is $35, pause it and insert a new video with a different angle.

### Workflow 2: Horizontal Audience and Platform Expansion on Google Ads and TikTok Ads

This workflow focuses on finding new sources of conversion volume, expanding to new audiences and exploring other platforms.

**Detailed Steps:**

1.  **Expansion Opportunity Identification:**
    *   Analyze the volume ceiling of current campaigns. A Google Search campaign with 5x ROAS but spending only $200/day out of a potential $1,000/day budget indicates limited volume for the current audience.
    *   Consider the marketing funnel stage. If retargeting campaigns and 1% lookalikes are saturated, explore wider lookalikes or open audiences.

2.  **Lookalike Audience Testing on TikTok Ads:**
    *   Create different Lookalike audience segments based on high-intent pixel events, such as "Add to Cart" or "Begin Checkout."
    *   **Practical Example:**
        *   Create a 1% Lookalike audience based on "Begin Checkout (last 60 days)."
        *   Create another 3% Lookalike audience based on "Viewed Product Page (last 90 days)."
        *   Launch separate test campaigns for each, with an initial budget of $100-150/day per audience, optimizing for "Purchase." Use top-performing Meta Ads creatives or new TikTok-native creatives.
        *   **Bid Settings (TikTok Ads):** Try a $45 `Bid Cap` or a $38 `Cost Cap` to control the initial CPA.

3.  **Expansion to Google Performance Max:**
    *   For Google Ads, if Search and Shopping campaigns have hit their limit, set up a Performance Max campaign.
    *   **Detailed Setup:**
        *   Include all asset types (text, image, video), product feeds (if ecommerce), and audience signals (customer lists, website visitors, remarketing lists).
        *   **Audience Signal Example:** Uploaded customer email list (Match Rate > 60%), website visitors list (last 180 days), and interests like "Online Clothing Buyers."
        *   Set `Target ROAS` (if ecommerce) or `Target CPA` (if lead gen) based on the account's average performance (e.g.: 300% Target ROAS if the average is 350%).
        *   Start with a budget 20-30% of what you spend on the top-performing Search and Shopping campaigns, and scale gradually.

4.  **Results Analysis and Budget Reallocation:**
    *   After 7-10 days of testing, compare the CPA and ROAS of the new audiences/campaigns with the account benchmarks.
    *   **Example:**
        *   If the TikTok Ads 1% Lookalike hits a $42 CPA and 2.5x ROAS (target: CPA < $45, ROAS > 2.2x), increase its budget by 20%.
        *   If the Google Ads Performance Max campaign hits 3.2x ROAS (target: 3.0x), reallocate 20% of the budget from less efficient Google Shopping campaigns to it.
    *   Deactivate or adjust campaigns that don't hit the expected metrics after the test period.

---

## Templates

### Meta Ads Budget Increase Plan (CBO)

```
Campaign ID: 987654321 - Sales - Women's Summer Shoes
Objective: Increase purchase volume by 30% keeping ROAS > 2.8x
Current Budget (CBO): $800/day
Average ROAS (7D): 3.6x
Average CPA (7D): $45
Average Frequency (7D): 2.8
Step 1: Increase budget to $960 (+20%) on 08/01/2024 at 2:00 PM ET.
Notes: Monitor CPM, Frequency, 1D Click ROAS, and 1D Click CPA over the next 48h.
Step 2 (if ROAS >= 3.0x in 48h): Increase to $1,150 (+20%) on 08/03/2024 at 2:00 PM ET.
Contingency: If ROAS drops below 2.7x or CPA rises above $55, revert to the previous budget and analyze creative performance. Plan an A/B test of new creatives.
```

### Google Ads Performance Max Audience Test Plan

```
Campaign Name: PMax - Market Expansion - Premium Product
Objective: Generate 100 new conversions (purchases) with CPA < $70 and ROAS > 3.0x
Daily Budget: $300
Start Date: 08/05/2024
End Date (Initial Test): 08/19/2024 (14 days)
Audience Signals:
  - Current Customer List (Hashed Email): Upload complete.
  - Website Visitors (Last 90 days): Included.
  - Custom Segment: People who searched "women's luxury watch," "handmade jewelry."
  - Interests: Luxury product buyers, fashion enthusiasts.
Assets:
  - Headlines: "Exclusive Luxury Watches," "Limited Collection," "Style and Sophistication."
  - Descriptions: "Discover the elegance of our new watch collection," "Unique design, superior quality, fast delivery."
  - Images: 5 high-resolution product images.
  - Videos: 2 short videos (15s, 30s) with lifestyle product content.
  - Product Feed: Connected to Google Merchant Center.
Bid Strategy: Maximize conversion value with a 320% Target ROAS.
Monitoring Metrics: ROAS, CPA, Conversion Volume, Customer Acquisition Cost.
Post-Test Action: If ROAS > 3.0x, scale the budget 25% weekly. If ROAS < 2.5x, pause and review assets and audience signals.
```

---

## Checklist

- [x] Check campaign ROAS/CPA over the last 72h and 7 days, identifying trends.
- [x] Analyze "Ad Fatigue" (frequency, CPM, CTR) of the highest-spend creatives on Meta/TikTok Ads.
- [x] Confirm the attribution window and model (e.g.: 7D click, 1D view) to ensure consistent data.
- [x] Assess whether operations capacity (inventory, logistics, support) can absorb the increase in traffic/sales.
- [x] Test new creative angles and formats (video, carousel, image) in scaling campaigns at least weekly.
- [x] Implement "bid cap" or "cost cap" strategies on Meta/TikTok Ads to control cost per result in test campaigns.
- [x] Segment lookalike audiences into different percentages (1%, 3%, 5%) for performance and expansion testing.
- [x] Allocate 10-20% of the total paid media budget to incremental tests of new audiences, platforms, or formats.
- [x] Review account health (Meta: Account Quality; Google: Optimization Score recommendations) to identify technical or policy issues.
- [x] Consider the impact of seasonality, events, or upcoming promotions on scaling performance.
- [x] Analyze competitive share of voice on Google Search to identify opportunities for more aggressive bids.
- [x] Check landing page quality to ensure they're optimized for conversion at high volume.

---

## Reference Metrics

| Metric | Benchmark (US ecommerce) | Target (Example) |
|---------|-------------------------------|----------------|
| CTR     | 1.5% - 3.5%                   | > 2.0%         |
| CPC     | $0.80 - $2.50             | < $1.60      |
| CPM     | $15 - $45                 | < $32        |
| ROAS    | 2.5x - 4.0x                   | > 3.0x         |
| CPA     | $30 - $80                 | < $55        |
| Frequency (7D) | 2.5 - 3.5                   | < 3.0          |

---

## Common Mistakes

1.  **Scaling budget too aggressively**: Increasing the budget by 50% or more at once can destabilize the platforms' optimization algorithms, leading to CPA spikes and a sharp ROAS drop.
    *   **How to avoid it**: Implement gradual 15-20% budget increases every 48-72 hours, letting the algorithm adapt and find new conversion opportunities. Example: Instead of going from $500 to $1,000/day, go $500 -> $600 -> $720 -> $864.
2.  **Ignoring "Ad Fatigue"**: Continuing to run the same creatives for a long period in high-budget campaigns raises CPM and reduces CTR, since the audience has already seen the ad multiple times.
    *   **How to avoid it**: Implement a weekly creative testing and refresh schedule. Pause creatives with frequency > 3.5 (7 days) and CTR < 1.0%. Create 3-5 new creatives (videos, images, carousels) with different angles and messages to test and replace the fatigued ones.
3.  **Not expanding audience or platform alongside vertical scaling**: Focusing only on budget increases in existing campaigns limits growth potential and makes scaling unsustainable in the long run, since you hit the audience "ceiling."
    *   **How to avoid it**: Allocate 15-25% of the total budget to testing new audiences (e.g.: 3-5% lookalikes, broad audiences with strong optimization) and explore new platforms (e.g.: if the focus is Meta/Google, test TikTok Ads). Example: If you spend $2,000/day on Meta Ads, put $400/day into testing new audiences on Meta or a new campaign on TikTok.

---

## Advanced Tips

1.  **Implement Strategic Bidding with Cost/Bid Caps (Meta and TikTok Ads)**: When ROAS starts dropping at scale, use `Cost Cap` or `Bid Cap` to force the algorithm to find conversions within a specific cost limit. This can stabilize CPA, but it may reduce volume.
    *   **Practical Example**: A Meta Ads Sales campaign has an average CPA of $45. When scaling, the CPA rose to $60. Create a new ad set with a $50 `Cost Cap` to try to optimize at a controllable cost.
2.  **Use Broad Audiences with Optimized Bidding (Meta Ads and Google Performance Max)**: Instead of targeting very specific audiences, trust the algorithm to find the best buyers in broad audiences (e.g.: "United States - 18+"). This works best with well-trained pixels and lots of conversion data.
    *   **Practical Example**: On Meta Ads, create a Sales campaign with an audience with no interest/behavior targeting, only location and age, optimizing for "Purchase." On Google PMax, use all audience signals, but don't over-restrict.
3.  **Leverage "Value-Based Bidding"**: On Google Ads (Target ROAS) and Meta Ads (Maximum Value), optimize for conversion value, not just conversion. This directs traffic to customers who tend to spend more, maximizing ROAS at scale.
    *   **Practical Example**: For an ecommerce store, set the `Target ROAS` at 350% on Google Shopping. On Meta Ads, use "Maximum Value" optimization if the pixel is set up to pass purchase value.
4.  **Incrementality Testing**: To validate whether scaling is really bringing new customers rather than just cannibalizing other sources, run incrementality tests. This involves pausing ads in one region or audience segment to measure the impact on organic sales or other channels.
    *   **Practical Example**: Select 2 states with similar demographic and buying profiles. In one, temporarily pause all paid campaigns for 7-10 days (control group). In the other, keep scaling active (test group). Compare total sales (organic + direct) between groups to estimate the real increment.
5.  **Geographic Segmentation by Performance on Google Ads**: When scaling Google Search or Display campaigns, analyze performance by geographic location. If a city or state has significantly higher ROAS and lower CPA, create dedicated campaigns for that region with more aggressive budgets and optimized bids.
    *   **Practical Example**: If the Google Analytics analysis shows that Texas has a ROAS 20% higher than the national average for your Search campaigns, create a new Search campaign focused only on Texas, with a 30% higher budget and a 10% lower Target CPA.
