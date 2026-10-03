---
name: meta-ads-campaign
description: "Meta Ads Campaign — Specialized skill for creating, optimizing, and managing ad campaigns on Meta (Facebook and Instagram)."
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Meta Ads Campaign

This skill enables you to structure, launch, and optimize ad campaigns on Meta, focusing on results like sales, leads, and qualified traffic, using the platform's best practices.

---

## Keywords

Conversion Campaigns, Custom Audiences, Lookalike Audiences, Campaign Budget Optimization (CBO), Advantage+ Placements, Pixel Events, ROAS (Return on Ad Spend), CPC (Cost Per Click), CTR (Click-Through Rate), Dynamic Product Ads (DPA), Meta A/B Testing, Events Manager.

---

## Quick Start

1.  **Set Up Pixel and Events**: Install the Meta Pixel on the site and configure the "Purchase," "Add to Cart," and "ViewContent" conversion events in Events Manager, prioritizing "Purchase" for sales campaigns.
2.  **Create a Sales Campaign (Conversion)**: Start a new campaign in Ads Manager, selecting the "Sales" objective and enabling Campaign Budget Optimization (CBO) with a daily budget of $150.
3.  **Target Strategic Audiences**: Create one ad set with a 1% Lookalike audience of existing buyers and another with detailed interests (e.g.: "ecommerce," "women's fashion"), excluding existing buyers from both.
4.  **Develop Creatives and Copy**: Upload 3-5 creative variations (static images, short videos, carousel) and 2-3 different ad texts, each with a clear CTA like "Shop Now."
5.  **Activate and Monitor**: Publish the campaign and start monitoring the main metrics (ROAS, CPA, CTR) after 72 hours to identify the best-performing ads and ad sets.

---

## Core Workflows

### Workflow 1: Sales Campaign Launch for Ecommerce with an Optimized Pixel

This workflow details creating a campaign focused on generating direct sales for an ecommerce store, using the Meta Pixel for optimization.

1.  **Meta Pixel Verification and Setup**:
    *   Open Events Manager in Meta Business Suite.
    *   Confirm the Pixel is active and receiving data for the "Purchase," "Add to Cart," and "ViewContent" events.
    *   In the "Aggregated Events Settings" panel, verify that "Purchase" is prioritized as the highest-value optimization event for the ecommerce domain.

2.  **Campaign Structure in Ads Manager**:
    *   **Campaign Level**:
        *   Click "Create," select the "Sales" (Conversions) objective.
        *   Name the campaign: `CAM_SALES_MAIN_PRODUCT_20240720_CBO`.
        *   Enable "Campaign Budget Optimization (CBO)."
        *   Set the campaign daily budget to $250.

3.  **Ad Set Configuration (Level 1: Buyer Lookalike)**:
    *   **Name**: `ADSET_LLK1%BUYERS_EXC_BUYERS_ADVTPLUS`.
    *   **Conversion Event**: Select "Website" and choose the "Purchase" event.
    *   **Audience**:
        *   Select a Custom Audience "1% Lookalike of Existing Buyers" (based on a customer file or pixel "Purchase" events).
        *   Under "Exclude," add the Custom Audience "Buyers in the last 180 days" to avoid hitting recent customers.
    *   **Placements**: Select "Advantage+ Placements" (Recommended).
    *   **Bid Control**: Leave open for the algorithm to optimize automatically (Lowest Cost bid strategy).

4.  **Ad Set Configuration (Level 2: Detailed Interests)**:
    *   **Name**: `ADSET_INTERESTS_ONLINE_FASHION_25-55_ADVTPLUS`.
    *   **Conversion Event**: Select "Website" and choose the "Purchase" event.
    *   **Audience**:
        *   **Age**: 25-55.
        *   **Gender**: Women (or all, depending on the product).
        *   **Detailed Targeting**: Include interests like "Ecommerce," "Online shopping," "Women's fashion," "Clothing," "Online store."
        *   Under "Exclude," add the Custom Audience "Buyers in the last 180 days."
    *   **Placements**: Select "Advantage+ Placements."
    *   **Bid Control**: Leave open.

5.  **Ad Creation (3-5 per Ad Set)**:
    *   For each set, create 3-5 distinct ads.
    *   **Format**: Vary between single image, video, and carousel.
    *   **Creatives**: Use high-quality images of products in use, short videos (15-30s) demonstrating benefits.
    *   **Primary Text**: Write 2-3 copy variations highlighting different value propositions (e.g.: "comfort," "style," "promotion").
    *   **Headline**: Short and impactful (e.g.: "New Collection!", "Free Shipping!").
    *   **Description**: Optional, to complement the headline.
    *   **Call to Action (CTA)**: "Shop Now."
    *   **Website URL**: Direct link to the product or category page.
    *   **Ad Name**: `AD_VIDEO_PROD_MODEL_CTA_SHOP`.

### Workflow 2: Post-Launch Optimization for High ROAS

This workflow focuses on how to analyze and optimize a sales campaign that's already running, aiming to improve Return on Ad Spend (ROAS).

1.  **Aggregated Data Analysis (after 5-7 days of campaign)**:
    *   **Ads Manager**: Open the "Breakdowns" panel and analyze performance by "Ad Set," "Ad," "Age," "Gender," and "Placement."
    *   **Focal Metrics**: ROAS, Cost Per Acquisition (CPA), CTR (Link Click-Through Rate), CPM (Cost Per 1,000 Impressions), Frequency.

2.  **Identifying and Pausing Inefficiencies**:
    *   **Low-Performing Ads**: Pause creatives with CTR below 1.0% and CPA significantly above the target benchmark (e.g.: CPA > $120).
    *   **Low-ROAS Ad Sets**: If an ad set has ROAS consistently below 1.5x and is spending a lot, consider pausing it or refining it drastically.

3.  **Duplication and Expansion of Winners**:
    *   **Winning Ad Sets**: Duplicate ad sets with ROAS above 3.0x. When duplicating, make small changes:
        *   **Variation 1**: Keep the same audience, test new creatives.
        *   **Variation 2**: Test a 1-2% Lookalike based on the original audience, or slightly expand interest targeting.
    *   **Winning Creatives**: Take the creatives with the highest CTR and lowest CPA and create new variations of them (e.g.: change the video music, alter the primary text).

4.  **Budget Adjustment (CBO)**:
    *   If the campaign as a whole is performing well (ROAS above target), raise the campaign budget by 10-20% every 3-4 days to let the algorithm scale without destabilizing optimization.
    *   If the campaign is below target ROAS but some ad sets are doing well, CBO is already reallocating. Don't cut the budget drastically — focus on pausing low-performing elements.

5.  **Structured A/B Tests**:
    *   Use Meta's A/B Test tool to compare critical variations. Example:
        *   **Hypothesis**: A new unboxing video will generate a CTR 50% higher than the current static image.
        *   **Setup**: Create an A/B Test comparing the static image ad (Control) with the unboxing video ad (Variation). Meta will split the audience and budget equally.
        *   **Analysis**: After 7-10 days, analyze the results to see which variation delivered better ROAS and CTR.

---

## Templates

### Sales Ad Copy Template (Physical Product)

```
[Product Name] - Transform your [Benefit Area]!

Tired of [Customer Pain]? Meet [Product Name], the perfect solution for [Benefit 1] and [Benefit 2].

✨ **Key Features:**
- Premium material for [Material Advantage]
- Ergonomic design for [Comfort/Ease]
- [Unique feature] that guarantees you [Exclusive Benefit]

🔥 **Exclusive Limited-Time Offer!**
From $ [Old Price] for only **$ [New Price]**!
🚚 FREE shipping nationwide.

Click "Shop Now" and get yours before it sells out!
#MetaAds #Ecommerce #SpecialOffer #[BrandName] #[ProductName] #Transformation
```

### Meta Ads Campaign Naming Structure Template

```
**Campaign Naming:**
CAM_OBJECTIVE_PRODUCT/SERVICE_DATE_STRATEGY

Example: `CAM_SALES_MARKETING_COURSE_20240720_CBO_LLK`
(Sales campaign for a Marketing Course, started on 07/20/2024, using Campaign Budget Optimization and a Lookalike audience)

**Ad Set Naming:**
ADSET_AUDIENCE_TYPE_PLACEMENT_OPTIMIZATION

Example: `ADSET_LLK1%BUYERS_EXC_BUYERS_ADVTPLUS_PURCHASE`
(Ad set for 1% Lookalike of Buyers, excluding Buyers, with Advantage+ Placements, optimizing for Purchase)

**Ad Naming:**
AD_CREATIVE_COPY_CTA

Example: `AD_VIDEO_TESTIMONIAL_BENEFIT_1_SHOP`
(Ad with Testimonial Video creative, Copy focused on Benefit 1, with Shop Now CTA)
```

---

## Checklist

- [x] Meta Pixel installed and correctly verifying "Page View," "Add to Cart," and "Purchase" events.
- [x] Domain verified in Business Manager for aggregated events optimization.
- [x] Campaigns configured with the correct objective (Sales for conversions, Leads for forms, Traffic for visits).
- [x] Campaign Budget Optimization (CBO) enabled for campaigns with multiple ad sets.
- [x] Custom Audiences (site visitors, profile engagers) and Lookalikes (1-3% of buyers or leads) created and updated.
- [x] Minimum of 3 diverse creatives (video, image, carousel) per ad set for testing.
- [x] Ad texts (copy) clear, with strong calls to action (CTAs) aligned with the objective.
- [x] Destination links (URL) working, pointing to the correct page and tracked with UTM parameters.
- [x] Advantage+ Placements selected to maximize reach and automatic optimization.
- [x] Irrelevant audiences excluded (e.g.: existing customers in prospecting campaigns, visitor Lookalike audience in Retargeting campaigns).

---

## Reference Metrics

| Metric               | Benchmark (Ecommerce) | Target (Ecommerce) |
|-----------------------|---------------------------------|----------------------------|
| ROAS (Return on Ad Spend) | 2.0x - 3.0x                     | 3.5x - 5.0x                |
| CPA (Cost Per Acquisition/Purchase) | $50 - $150                  | $30 - $80              |
| CTR (Link Click-Through Rate) | 1.5% - 2.5%                     | 2.8% - 4.5%                |
| CPM (Cost Per 1,000 Impressions) | $15 - $40                   | $10 - $30              |
| Conversion Rate (click to purchase) | 1.5% - 2.5%                     | 2.8% - 4.0%                |
| Frequency (Prospecting Campaigns) | 2.0 - 3.5                       | 2.5 - 4.0                  |

---

## Common Mistakes

1.  **Poorly configured Meta Pixel or non-prioritized events**: Causes ineffective optimization and inaccurate reporting, resulting in lost conversions or campaigns spending on the wrong events.
    *   **How to avoid it**: Open "Events Manager," use the "Test Events" tool to simulate actions on the site (e.g.: add to cart, complete purchase) and verify Meta records the events correctly. In the "Aggregated Events Settings" panel, make sure "Purchase" is the highest-priority event for sales campaigns.

2.  **Audiences too broad without targeting or too narrow with low volume**: Leads to inefficient spend on uninterested people or limited scale that prevents growth.
    *   **How to avoid it**: For prospecting, start with 1% Lookalike audiences of high-value customers or detailed interests with Potential Reach between 1 million and 5 million. For remarketing, use custom audiences of "Website visitors in the last 30-90 days" or "People who added to cart but didn't buy." Monitor audience size in Ads Manager to ensure it isn't below 500,000 for prospecting, which can limit delivery.

3.  **Not testing or refreshing enough creatives and copy**: Results in ad fatigue, CTR decline, and CPM/CPA increases over time, as the same audience sees the same ads repeatedly.
    *   **How to avoid it**: Always start ad sets with at least 3-5 creative variations (videos, images, carousel) and 2-3 primary text variations. Monitor the campaign's "Frequency." When frequency exceeds 3.5-4.0 in prospecting campaigns and CTR starts to drop, it's a clear sign to create new creatives and copy, or test new angles on existing ads.

---

## Advanced Tips

1.  **Strategic Use of Dynamic Product Ads (DPA) for the Full Funnel**: Don't limit DPAs to remarketing only. Create prospecting campaigns with DPA, targeting Lookalike audiences or broad interests. Meta will show the most relevant products from your catalog to new users, increasing the chance of an initial conversion. Make sure you have a robust, up-to-date product catalog in Commerce Manager.

2.  **Campaign Budget Optimization (CBO) with Funnel Structure (TOFU/MOFU/BOFU)**: Structure a single CBO campaign and create ad sets representing the funnel stages:
    *   **TOFU (Top of Funnel)**: 1-3% Lookalike audience of visitors/engagers, broad interests.
    *   **MOFU (Middle of Funnel)**: Retargeting of site visitors 7-30 days, Instagram/Facebook engagers 30-90 days.
    *   **BOFU (Bottom of Funnel)**: Retargeting of "Added to cart but didn't buy," 1% Lookalike of high-value buyers.
    The CBO will allocate the budget to the ad sets generating the most results, optimizing spend across funnel phases.

3.  **Automated Rules Implementation for Proactive Management**: Configure automated rules in Ads Manager to optimize campaigns without constant manual intervention. Examples:
    *   `Pause Ad`: If ROAS over the last 3 days is < 1.0 and spend > $50.
    *   `Increase Budget`: If campaign ROAS over the last 7 days is > 4.0, increase the daily budget by 15% (limit to one increase per week).
    *   `Notify`: If an ad set's CPM exceeds $50 over the last 24 hours, send a notification.

4.  **Value-Based Lookalike Audiences for Qualified Scaling**: When creating a Lookalike audience, use a customer data source that includes "Customer Value" (Lifetime Value - LTV). Meta will then find users similar to your most profitable customers, enabling audience expansion that maintains conversion quality and high ROAS.

5.  **A/B Testing Bid or Optimization Variations**: Beyond creatives and audiences, use Meta's A/B Test tool to compare different bid strategies (e.g.: lowest cost vs. an $80 bid cap per purchase) or different optimization events (e.g.: optimizing for "Purchase" vs. "Add to Cart" in a complex funnel). This provides insights into which bidding or optimization approach maximizes your ROAS and conversion volume.
