---
name: campaign-audit
description: "Campaign Audit — Specialized skill for campaign audits"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Campaign Audit

This skill enables detailed, actionable audits of Meta Ads, Google Ads, and TikTok Ads campaigns to optimize performance and maximize return on investment (ROAS).

---

## Keywords

Campaign audit, Meta Ads, Google Ads, TikTok Ads, performance optimization, ROAS, CPC, CTR, CPA, audience targeting, creatives, bidding strategies, account structure, conversion funnel, data analysis, tracking pixel, conversion events, negative keywords.

---

## Quick Start

1.  **Access and Data Export**: Get full access to the ad accounts (Meta Ads Manager, Google Ads, TikTok Ads Manager). Export performance reports for the last 30-90 days, broken down by campaign, ad set/ad group, and ad/creative. Include metrics like impressions, clicks, CTR, CPC, CPM, total cost, conversions, cost per conversion (CPA), and conversion value (ROAS).
2.  **Tracking Verification**: Confirm the correct implementation of the Meta Pixel, Google Ads Tag, and TikTok Pixel, and verify that essential conversion events (PageView, AddToCart, Purchase, Lead) are firing correctly with values attributed where applicable. Use Meta Events Manager, Google Tag Assistant, and the TikTok Pixel Helper.
3.  **Macro Performance Analysis**: Compare overall account performance against predefined goals and industry benchmarks. Identify campaigns with ROAS below target, very high CPA, or very low CTR.
4.  **Anomaly Detection**: Look for abrupt spikes or drops in key metrics. Investigate the context: budget changes, new creatives, audience changes, or seasonality.

---

## Core Workflows

### Workflow 1: Audit of Campaign Structure, Objectives, and Targeting

This workflow focuses on validating the strategic foundation of the campaigns, ensuring the account structure and audience targeting are aligned with business objectives and optimized for performance.

**Detailed Steps:**

1.  **Campaign Objective Validation**:
    *   **Meta Ads**: In each campaign, open "Campaign Settings" and check the "Campaign Objective." An e-commerce campaign with a "Traffic" or "Engagement" objective is a common mistake. The ideal for direct sales is "Sales," or "Leads" for lead capture.
        *   **Example**: Fashion e-commerce client. Main sales campaign configured as "Traffic." **Action**: Change the objective to "Sales" and select optimization for "Purchases" so the algorithm focuses on users most likely to buy.
    *   **Google Ads**: In "Campaign Settings," review the "Campaign Objective." For e-commerce, make sure it's "Sales" or "Leads," optimizing for "Purchases" or "Form Submits."
        *   **Example**: Search campaign for a SaaS with a "Website Traffic" objective. **Action**: Switch to "Leads" and optimize for "Form Submit" or "Free Trial Start."
    *   **TikTok Ads**: Check the "Advertising Objective." For sales, prioritize "Sales" or "Lead Generation."
        *   **Example**: Digital product campaign using "Reach." **Action**: Switch to "Sales" or "Lead Generation" with optimization for "Complete Payment" or "Form Submit."

2.  **Account Structure and Granularity Analysis**:
    *   Assess whether the account is organized logically: campaigns by objective, audience type (prospecting, remarketing), funnel stage (top, mid, bottom), or product/service.
    *   Check for too many ad sets/ad groups with very small budgets, which dilute the algorithms' learning.
    *   **Meta Ads Example**: 15 prospecting ad sets, each at $10/day. **Action**: Consolidate similar audiences into 3-5 ad sets at $50-$100/day to give more power to CBO (Campaign Budget Optimization) or ABO (Ad Set Budget Optimization) and let the algorithm find the ideal audience.
    *   **Google Ads Example**: 5 identical ad groups in keywords, only changing match type. **Action**: Consolidate into 1-2 ad groups with tightly themed keywords, leveraging match types within the same group.

3.  **Audience Targeting Audit**:
    *   **Audience Overlap**: Use the "Audience Overlap" tool in Meta Ads Manager to identify audiences that intersect significantly (above 20-30%). Overlap can cause internal competition and drive up CPM.
        *   **Example**: "Fitness Interests" audience and "People who follow gyms" audience in the same top-of-funnel. **Action**: Exclude one from the other or test separate campaigns to see which performs better.
    *   **Audience Exclusions**: Verify that remarketing audiences are being excluded from prospecting campaigns. Existing customers or converted leads should be excluded from "first purchase" campaigns.
        *   **Meta Ads Example**: Prospecting campaign with no exclusion for "Purchasers last 90 days." **Action**: Add the "Purchasers last 90 days" list as an exclusion to avoid spending on people who already bought.
    *   **Audience Size**: Assess whether the audience is too narrow (few impressions) or too broad (high CPM, low relevance).
        *   **TikTok Ads Example**: Audience based on very specific interests (<500K people in the US). **Action**: Expand related interests or use 1% lookalike audiences to gain scale.

### Workflow 2: Creative, Bidding, and Keyword Performance Analysis

This workflow dives into the tactical elements of the campaigns, evaluating ad effectiveness, bid optimization, and keyword relevance to ensure the budget is generating the best possible return.

**Detailed Steps:**

1.  **Creative and Ad Performance**:
    *   **Meta Ads/TikTok Ads**: Analyze CTR (Click-Through Rate), VTR (View-Through Rate for video), CPM (Cost per 1,000 Impressions), and conversion rate per ad/creative.
        *   **Example**: Ad A (video) has a 2.5% CTR and $30 CPA, while Ad B (image) has a 0.8% CTR and $80 CPA. **Action**: Pause Ad B, allocate more budget to Ad A, and create variations of Ad A.
        *   **Benchmark**: Ideal CTR for Meta/TikTok is generally above 1.5% for prospecting and 3%+ for remarketing. VTR above 30% is good for short videos.
    *   **Google Ads (Search)**: Evaluate keyword "Quality Score" and "Ad Relevance." A low "Quality Score" indicates problems in the keyword - ad - landing page relationship.
        *   **Example**: Keyword "digital marketing course" with a 3/10 Quality Score. **Action**: Improve ad copy to include the keyword more, ensure the landing page has relevant content for "digital marketing course," and add more negative keywords.

2.  **Bidding Strategy and Budget Optimization**:
    *   **Meta Ads/TikTok Ads**: Verify the bidding strategy is aligned with the objective (e.g., "Cost per Result" to maximize conversions, "Highest Volume" for the learning phase).
        *   **Example**: Sales campaign using "Lowest Bid" (highest volume) but with a very high CPA. **Action**: Switch to "Cost per Result" and set a target Cost per Purchase (CPA) of, say, $45, to give the algorithm clearer instruction.
    *   **Google Ads**: Analyze the bidding strategy (e.g., "Maximize Conversions," "Target ROAS," "Manual CPC"). For performance campaigns, "Maximize Conversions" or "Target ROAS" are generally more effective.
        *   **Example**: E-commerce campaign on "Manual CPC" with low ROAS. **Action**: Switch to "Maximize Conversion Value" with a 300% Target ROAS (3x the investment) for automatic optimization.
    *   **Budget Distribution**: Observe where the budget is being consumed and whether it's generating proportional results.
        *   **Example**: Campaign X consuming 70% of the total budget but generating only 30% of conversions. **Action**: Reduce Campaign X's budget and reallocate to campaigns with better ROAS or CPA.

3.  **Keyword Analysis (Google Ads)**:
    *   **Search Terms Report**: Identify search terms generating clicks but no conversions, or irrelevant terms.
        *   **Example**: Campaign for "SEO consulting" is getting clicks for "free seo course." **Action**: Add "course," "free," and "gratis" as exact or phrase match negative keywords.
    *   **Keyword Match Types**: Verify that match types (exact `[keyword]`, phrase `"keyword"`, broad `keyword`) are being used strategically to control traffic and relevance.
        *   **Example**: All keywords on broad match, resulting in very generic search terms. **Action**: Convert top-performing keywords to phrase and exact match, and use broad match in a more controlled way for discovery.

---

## Templates

### Simplified Campaign Audit Report (Meta Ads)

```
## Simplified Audit Report - "Direct Sales - Prospecting" Campaign (Meta Ads)

**Analysis Period:** 01/01/2024 - 01/31/2024
**Total Spend:** $5,000.00
**Results:** 50 Purchases
**Average CPA:** $100.00
**ROAS:** 1.8 (Conversion Value: $9,000.00)
**CPA Benchmark:** $70.00
**ROAS Benchmark:** 3.0

---

**1. Structure and Objective:**
*   **Current Status:** "Traffic" objective set for an e-commerce campaign. Campaign budget (CBO) active, 8 active ad sets.
*   **Problem:** The "Traffic" objective doesn't optimize for "Purchases," resulting in low-value clicks and a high CPA. Too many ad sets dilute budget and algorithmic learning.
*   **Recommendation:** Change the campaign objective to "Sales." Consolidate ad sets by theme or audience into 3-4 ad sets, with focused CBO budget.

**2. Audience Targeting:**
*   **Current Status:** "Casual Fashion Interests" audience and "Engaged Shoppers Behavior" with 35% overlap. "30-day Purchasers" exclusion missing.
*   **Problem:** Audience overlap raises cost and internal competition. Missing exclusions spend on users who already converted.
*   **Recommendation:** Exclude "30-day Purchasers" from the prospecting campaign. Test overlapped audiences in separate campaigns or combine the top performers.

**3. Creative and Ads:**
*   **Current Status:** Ad A (Product video) - CTR 2.8%, CPA $75. Ad B (Static image) - CTR 0.9%, CPA $120. Ad C (Carousel) - CTR 1.5%, CPA $90.
*   **Problem:** Ad B is performing well below average, pulling the overall CPA up.
*   **Recommendation:** Pause Ad B. Allocate more budget to Ad A. Create 2-3 new variations of Ad A and test.

**4. Bidding Strategy:**
*   **Current Status:** "Lowest Bid" strategy with no cost cap.
*   **Problem:** No control over cost per result, contributing to the above-benchmark CPA.
*   **Recommendation:** Switch the bidding strategy to "Cost per Result" with a target CPA cap of $70.00.

**Urgent Action Summary:**
1.  **Change the campaign objective to "Sales."**
2.  **Consolidate ad sets.**
3.  **Exclude "30-day Purchasers" from prospecting.**
4.  **Pause Ad B and create variations of Ad A.**
5.  **Switch bidding strategy to "Cost per Result" (Target CPA $70.00).**
```

### Post-Audit Action Plan (Google Ads)

```
## Post-Audit Action Plan - "SEO Consulting Service" Campaign (Google Ads)

**Analysis Period:** 02/01/2024 - 02/29/2024
**Total Spend:** $3,500.00
**Results:** 15 Leads (Form)
**Average CPA:** $233.33
**ROAS:** N/A (service, CPA-focused)
**CPA Benchmark:** $150.00

---

**1. Tracking and Conversions:**
*   **Issue Identified:** "Form Submit" conversion tag firing multiple times per session, inflating the lead count.
*   **Action:** Review the Google Ads Tag implementation via Google Tag Manager. Add a once-per-page firing rule or use GA4 "Form Submit" events for more accurate counting.
*   **Owner:** Development/Analytics Team
*   **Deadline:** 03/05/2024

**2. Keywords and Relevance:**
*   **Issue Identified:** Search Terms Report shows clicks for "seo course" and "free seo." Keyword "seo consulting" with a 4/10 Quality Score.
*   **Action:** Add "course," "free," "learn" as phrase and exact match negative keywords. Optimize ad copy and the landing page to feature "seo consulting" more prominently, aiming to raise the Quality Score.
*   **Owner:** Media Buyer
*   **Deadline:** 03/07/2024

**3. Bidding and Budget Optimization:**
*   **Issue Identified:** "Maximize Clicks" bidding strategy with a very high CPA.
*   **Action:** Switch the bidding strategy to "Maximize Conversions" with a $150.00 target CPA. Adjust the daily budget from $120 to $100 to keep CPA within the initial target while optimizing.
*   **Owner:** Media Buyer
*   **Deadline:** 03/04/2024

**4. Ad Extensions (Assets):**
*   **Issue Identified:** Only basic sitelink extensions active. Missing callout and structured snippet extensions focused on the consulting differentiators.
*   **Action:** Create and implement callout extensions with "Certified Specialists," "Personalized Support," "Proven Results." Add a structured snippet for "Services: SEO Audit, On-page Optimization, Link Building."
*   **Owner:** Media Buyer
*   **Deadline:** 03/08/2024

**Monitoring:** Track CPA and lead volume daily for the first 2 weeks after implementation.
```

---

## Checklist

- [X]  Verify the campaign objective is aligned with the business goal (Sales, Leads, Traffic).
- [X]  Confirm the correct implementation and firing of conversion events (Meta Pixel, Google Tag, TikTok Pixel).
- [X]  Analyze audience overlap between ad sets (Meta Ads).
- [X]  Audit audience exclusions (purchasers, leads, irrelevant visitors) in prospecting campaigns.
- [X]  Review CTR, VTR (video), CPM, and CPA/ROAS performance by creative/ad.
- [X]  Validate bidding strategy and budget (CBO/ABO, Target CPA, Target ROAS) for optimization.
- [X]  In Google Ads, analyze the Search Terms Report and add negative keywords.
- [X]  In Google Ads, check keyword Quality Score and ad relevance.
- [X]  Evaluate the coherence between ad, landing page, and offer (message match).
- [X]  Analyze budget distribution across campaigns and ad sets, identifying waste.
- [X]  Check ad display frequency to avoid creative fatigue.
- [X]  Review demographic and geographic targeting, adjusting based on performance data.

---

## Reference Metrics

| Metric               | Benchmark (Prospecting) | Benchmark (Remarketing) | Target (E-commerce) | Target (Lead Gen) |
|-----------------------|------------------------|-------------------------|-------------------|-------------------------|
| **CTR (Meta/TikTok)** | 1.0% - 2.0%            | 3.0% - 5.0%             | > 1.8%            | > 1.5%                  |
| **CTR (Google Search)**| 3.0% - 6.0%            | N/A                     | > 4.5%            | > 4.0%                  |
| **CPC (Meta/TikTok)** | $0.80 - $2.50      | $0.30 - $1.00       | < $1.50         | < $2.00               |
| **CPC (Google Search)**| $2.00 - $8.00      | N/A                     | < $5.00         | < $6.00               |
| **ROAS (Meta/Google)**| 1.5 - 2.5              | 4.0 - 8.0               | > 3.0             | N/A                     |
| **CPA (Meta/Google)** | $50 - $150         | $10 - $40           | N/A               | < $80                 |
| **CPM (Meta/TikTok)** | $15 - $35          | $5 - $15            | < $25           | < $30                 |
| **Conversion Rate** | 1.0% - 3.0%            | 5.0% - 10.0%            | > 2.5%            | > 2.0%                  |

*Note: Benchmarks can vary significantly by industry, product, price, and region.*

---

## Common Mistakes

1.  **Incorrect or Broken Conversion Tracking**: The Meta pixel or Google Ads tag isn't firing correctly, or conversion events are set up wrong (e.g., Purchase without value).
    *   **How to avoid it**: Always use Google Tag Manager (GTM) to manage tags. After any implementation or change, immediately verify event firing using Google Tag Assistant, the Meta Pixel Helper, or the TikTok Pixel Helper, plus each platform's "Events Manager," testing the real conversion flow.
2.  **Overly Broad Audience Targeting Without Exclusions**: Prospecting campaigns running without excluding remarketing audiences or recent purchasers. This wastes budget, because you're hitting people who already know or bought the product with top-of-funnel ads.
    *   **How to avoid it**: Always create and use remarketing exclusion audiences (e.g., "Website visitors last 30 days," "Purchasers last 90 days") in prospecting campaigns. On Meta Ads, use the "Audience Overlap" tool to identify and resolve conflicts between ad sets.
3.  **Creative/Ad Fatigue at High Frequency**: An ad with high frequency (e.g., 3.5+ in 7 days) to the same audience tends to lose performance, driving CPM up and CTR down, because the audience has already seen the ad several times.
    *   **How to avoid it**: Monitor the "Frequency" metric weekly. When it hits 2.5-3.0, prepare new creatives or pause fatigued ads. Always test new creative and copy variations to keep the audience engaged.
4.  **Improper Use of Keyword Match Types (Google Ads)**: Leaving all keywords on broad match with no control results in irrelevant traffic and overspend.
    *   **How to avoid it**: Use a strategic combination of exact match `[terms]`, phrase match `"terms"`, and broad match `terms`. Start with phrase and exact for high-intent keywords and use broad for controlled discovery, always closely monitoring the Search Terms Report to add negatives.
5.  **Lack of Consistent A/B Testing on Creatives and Offers**: Running the same ad combination for long periods without testing variations prevents discovering higher-performing elements.
    *   **How to avoid it**: Implement an A/B testing routine. Create 2-3 creative variations (images, videos, copies) per ad set every 2-4 weeks. Test different calls to action (CTAs) and offers to identify which generate the best CPA or ROAS.

---

## Advanced Tips

1.  **Post-Click Funnel Analysis with GA4**: Don't stop at ad platform metrics. Integrate Google Analytics 4 (GA4) to understand user behavior *after* the ad click. Analyze metrics like bounce rate, time on page, pages per session, and the path to conversion. This reveals landing page or checkout flow problems that ad platforms don't show.
    *   **Practical Example**: A Meta Ads campaign has a high CTR and good CPC, but GA4 shows an 80% bounce rate on the landing page. This indicates that, while the ad attracts clicks, the destination page isn't relevant or engaging enough.
2.  **Creative "Decay Rate" Audit**: Monitor the performance decline (CTR, CPA) of creatives over time. Build a daily or weekly performance chart for each main ad. Identify the point where a creative starts to "wear out" the audience and plan its replacement *before* performance drops drastically.
    *   **Practical Example**: A TikTok Ads video performs excellently for 3 weeks, but in week 4 its CTR falls from 2.0% to 0.8% and CPA doubles. That's the "decay rate" kicking in, signaling it's time to test a new video.
3.  **Using Automated Rules for Optimization at Scale**: For accounts with many campaigns and ad sets, set up automated rules for daily optimizations.
    *   **Practical Example (Meta Ads)**: Create a rule to pause ads with CPA > $100 and impressions > 5,000 in the last 3 days. Or a rule to increase the budget of campaigns with ROAS > 4.0 by 10% daily, capped at a maximum.
4.  **Multi-Touch Attribution Analysis**: Use attribution models that go beyond "last click," like "linear," "position-based," or "time decay" in Google Analytics or Google Ads. This helps you value top-of-funnel channels (Meta Ads prospecting, Google Display) that contribute to the customer journey but don't get the final credit.
    *   **Practical Example**: A TikTok Ads branding campaign may not generate direct conversions (last click), but with multi-touch attribution you see that many users exposed to it later convert via organic search or Google Ads.
5.  **Advanced Segmentation by LTV (Lifetime Value)**: If LTV data is available, create custom audiences and campaigns focused on high-value customers. In Meta Ads, for example, you can create a custom audience of "Purchasers with LTV > X" and use it for upsell/cross-sell campaigns or as a seed for high-value Lookalikes.
    *   **Practical Example**: A SaaS company identifies its highest-LTV customers. It creates a 1% lookalike audience based on them and targets prospecting campaigns with exclusive offers, attracting users most likely to become valuable customers.
