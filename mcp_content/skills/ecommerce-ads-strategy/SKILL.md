---
name: ecommerce-ads-strategy
description: "Ecommerce Ads Strategy — Specialized skill for ecommerce ads strategy"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Ecommerce Ads Strategy

This skill enables you to develop, implement, and optimize highly effective paid advertising strategies for e-commerce on Meta Ads, Google Ads, and TikTok Ads.

---

## Keywords

ROAS Optimization, Meta Ads CBO, Google Ads PMax, Advanced Lookalikes, Dynamic Retargeting, Customer LTV, TOFU MOFU BOFU Funnel Strategy, Creative A/B Testing, Behavioral Targeting, CPA Bid Strategy, GA4 Integration.

---

## Quick Start

1.  **Set Up GA4 and the Conversions API:** Implement GA4 for e-commerce event tracking (PageView, ViewItem, AddToCart, Purchase) and configure the Meta Conversions API for data redundancy.
2.  **Structure a PMax Campaign (Google Ads):** Create a Performance Max campaign focused on sales, feeding it with Merchant Center product feeds, specific asset groups, and audience signals (customer lists, website visitors).
3.  **Launch a Sales Campaign (Meta Ads):** Start a campaign with the Sales objective, using Campaign Budget Optimization (CBO), with ad sets segmented by audience (e.g.: 1-3% Lookalikes of purchasers) and dynamic product creatives.
4.  **Activate a Targeted Traffic Campaign (TikTok Ads):** Develop a Sales/Conversion campaign on TikTok Ads, targeting interests specific to the product niche (e.g.: "natural beauty," "video games") and using short, authentic videos.

---

## Core Workflows

### Workflow 1: Scaling Sales Campaigns on Meta Ads with CBO

**Objective:** Increase sales volume while maintaining ROAS (Return on Ad Spend) and CPA (Cost per Acquisition).

**Steps:**

1.  **Current Performance Analysis:** Evaluate ad sets with ROAS > 3.0 and CPA < $50.00 over the last 7 days. Identify high-performance creatives (videos, images) and audiences (interests, Lookalikes) showing consistency.
2.  **Selective Duplication into CBO:** Duplicate the winning ad sets and their creatives into a new campaign, activating Campaign Budget Optimization (CBO). Start the new campaign with a budget 20-30% higher than the sum of the original ad sets' budgets. Example: If three ad sets were spending $100/day each with good performance, the new CBO campaign can start at $360-$390/day.
3.  **Audience Expansion with Advanced Lookalikes:** Add new ad sets to the CBO campaign using 1-3% or 1-5% Lookalike audiences based on "Purchasers in the last 90 days" or "Added to Cart in the last 30 days." Test different data sources (pixel, customer lists via Customer Match).
4.  **A/B Tests of New Creative Variations:** Within the duplicated ad sets, pause creatives with CTR (Click-Through Rate) < 1.0% and start A/B tests with 2-3 new variations of UGC videos (User Generated Content) or product carousels with clear value props (e.g.: free shipping, tiered discounts). Example: Test video A (customer testimonial) vs. video B (usage demo) for the "1% Purchasers Lookalike" ad set.
5.  **Daily Monitoring and Optimization:** Track ROAS and CPA at ad set and campaign level. If an ad set underperforms the target (e.g.: ROAS < 2.0) for 3 consecutive days, reduce its bid, lower its budget (if CBO allows), or pause it. CBO will reallocate the budget to the best-performing ad sets. Example: An "Women's Fashion Interests" ad set with a 1.8 ROAS for 3 days gets paused to focus on high-performance Lookalikes.

### Workflow 2: Optimizing a Google Performance Max (PMax) Campaign for ROAS

**Objective:** Maximize return on ad spend on Google Ads, using PMax automation capabilities.

**Steps:**

1.  **Audience Signal Audit and Refresh:** Verify the relevance and freshness of audience signals. Include remarketing lists (purchasers, added to cart, website visitors), customer lists (CRM), and custom segments with high-intent search terms (e.g.: "buy [product name]," "best [product type]"). Remove outdated or low-volume lists.
2.  **Asset Group Optimization:** Analyze the performance of assets (headlines, descriptions, images, videos) within each asset group. Replace assets with "Low" or "Good" status with new assets with potential for "Best" or "Excellent." Example: Swap a generic image for a high-quality photo of the product in use, or a static video for a dynamic unboxing video.
3.  **Negative Search Term Exclusions (via Support/Account Manager):** Although PMax is automated, it's crucial to request exclusions of irrelevant or low-performance search terms through your Google rep or support, especially to avoid traffic from competitor brand terms, non-transactional informational terms, or searches with negative intent. Example: Exclude "review," "free," "problems [brand name]" if those aren't objectives.
4.  **Conversion Value Adjustment (For LTV):** If the e-commerce store has a clear LTV (Lifetime Value) per customer or product category, adjust the conversion value to reflect the average first-order LTV instead of just the initial purchase value. This lets Smart Bidding optimize for more valuable long-term customers. Example: If the average order is $150 but LTV is $300, set the conversion value to $300 for that specific conversion.
5.  **Continuous Product Feed Review and Optimization (Merchant Center):** Ensure the product feed is flawless and always up to date: high-quality images, descriptive titles with keywords, detailed descriptions, correct category attributes, updated prices, and in-stock availability. Out-of-stock products, errors, or incomplete information in the feed can negatively impact PMax.

---

## Templates

### Meta Ads - TOFU/MOFU/BOFU Campaign Structure

```
Campaign: [STORE_NAME] - Sales - [Month/Year] - [Main Objective: E.g.: New Acquisition | Retargeting]

Objective: Sales (Conversion: Purchase)
Campaign Budget Optimization (CBO): On
Daily Budget: $500.00 (Example: Adjust as needed to hit target ROAS)

Ad Set 1 (TOFU - Top of Funnel: Awareness/Discovery)
  Audience: 1-3% Lookalike (180-day Visitors) + Broad Interests (e.g.: "Sustainable Fashion," "Vegan Cooking," "Wearable Tech")
  Exclusions: Purchasers (90 days)
  Placements: Automatic (Recommended for CBO)
  Optimize for: Purchases
  Creatives: 3-5 short videos (UGC, unboxing, storytelling), 2-3 static images with a clear value prop.
  Copy: Focus on problem-solution, curiosity, product innovation.
  CTA: Learn More, Shop Now.

Ad Set 2 (MOFU - Mid Funnel: Consideration)
  Audience: Website Visitors (30 days) - Exclude Purchasers (90 days)
            Added to Cart (7 days) - Exclude Purchasers (90 days)
            Engagement Audience (Instagram/Facebook 90 days)
  Exclusions: Purchasers (90 days)
  Placements: Automatic
  Optimize for: Purchases
  Creatives: 2-3 product carousels (different angles/benefits), 1-2 product demo videos, social proof.
  Copy: Focus on specific benefits, differentiators, customer testimonials, guarantee.
  CTA: Shop Now, View Products.

Ad Set 3 (BOFU - Bottom of Funnel: Conversion/Retargeting)
  Audience: Added to Cart (30 days) - Exclude Purchasers (90 days)
            Initiated Checkout (14 days) - Exclude Purchasers (90 days)
            Viewed Product (30 days) - Exclude Purchasers (90 days)
  Exclusions: Purchasers (90 days)
  Placements: Automatic
  Optimize for: Purchases
  Creatives: 2-3 dynamic product images/videos (DPA), 1 image with a limited-time free shipping/discount coupon offer, urgency.
  Copy: Urgency, scarcity, final social proof, direct purchase CTA.
  CTA: Shop Now, Complete Purchase.
```

### Google Ads - Headlines and Descriptions for PMax (Asset Group)

```
Asset Group: Premium Athletic Wear

Headlines (15-30 characters - Minimum 3, ideally 5+):
- Premium Athletic Wear
- Comfort & Performance
- Train in Style
- Free Shipping Over $199
- Exclusive Fitness Line
- High-Compression Leggings
- Breathable Sports Bras
- New Arrivals!
- Shop Online Now
- First-Order Discount

Long Headlines (30-90 characters - Minimum 1, ideally 3+):
- Premium Athletic Wear for High Performance and Lasting Comfort.
- Elevate Your Workout with Our Exclusive Men's and Women's Fitness Collection.
- Enjoy Free Shipping on Athletic Wear Orders Over $199 Nationwide.

Descriptions (60-90 characters - Minimum 2, ideally 4+):
- Tech fabrics and modern design for your best performance.
- Find the perfect look for your workout with comfort and style.
- Variety of colors and sizes. Shop online and get it fast at your door!
- Comfort and style combined for your workout routine. Guaranteed quality.
- Online fitness apparel store with the best brands and prices.
```

---

## Checklist

- [x] GA4 configured with e-commerce events (PageView, ViewItem, AddToCart, Purchase) and enhanced e-commerce tracking.
- [x] Meta Conversions API implemented and validated for data redundancy and quality.
- [x] Google Merchant Center product feed updated, optimized, and error-free for Google Ads (PMax and Shopping).
- [x] Remarketing audiences (visitors, abandoned cart, viewed product) and Lookalikes (purchasers, added to cart) created and updated in Meta Ads and TikTok Ads.
- [x] PMax campaign with complete asset groups (videos, images, headlines, descriptions) and relevant audience signals.
- [x] Creative A/B tests (videos, images, copy) actively running to identify winners in Meta/TikTok Ads.
- [x] Budget strategically allocated across funnel stages (TOFU/MOFU/BOFU) to maximize overall ROAS.
- [x] Automated optimization rules (pause low-ROAS ads, adjust bids) configured in Meta Ads.
- [x] Metrics dashboard (ROAS, CPA, LTV, CTR, Conversion Rate) monitored daily in Google Analytics and ad platforms.
- [x] Bidding strategy configured to maximize conversion value (e.g.: Target ROAS in Google Ads, Lowest Cost with Minimum ROAS in Meta Ads).

---

## Reference Metrics

| Metric | Benchmark (general e-commerce) | Target (high-performance e-commerce) |
|---------|------------------------------|--------------------------------------|
| ROAS    | 2.5x                         | 3.5x - 5.0x                          |
| CTR (Meta/TikTok) | 1.0%                         | 1.5% - 2.5%                          |
| CTR (Google Search) | 3.0%                         | 5.0% - 8.0%                          |
| CPC (Cost per Click) | $1.50 - $3.00            | $0.80 - $2.00                    |
| CPA (Cost per Acquisition) | $50.00 - $100.00         | $20.00 - $40.00                  |
| Conversion Rate (Ecommerce) | 1.5% - 2.5%                  | 3.0% - 5.0%                          |
| LTV:CAC Ratio | 2:1                          | 3:1 or higher                      |

---

## Common Mistakes

1.  **Not using the Meta Conversions API**: Relying only on the Meta pixel leads to data loss and inaccurate optimization, especially with privacy restrictions (iOS 14+). **How to avoid it**: Implement the Meta Conversions API with server events, prioritizing the quality of the data sent. Example: Configure "Purchase" and "AddToCart" events to be sent directly from the e-commerce server to Meta, complementing pixel data.
2.  **Ignoring Product Feed Optimization on Google Ads**: An outdated product feed with low-quality images, incomplete information, or errors in Google Merchant Center severely limits the performance of Performance Max and Shopping campaigns. **How to avoid it**: Optimize the product feed weekly. Ensure high-resolution images, descriptive titles with relevant keywords, detailed descriptions, correct category attributes, updated prices, and in-stock availability. Example: Add attributes like "color," "size," "brand," "gender," and "material type" for each item.
3.  **Scaling budget abruptly without ROAS validation**: Increasing a campaign's budget by 50% or more at once, without a consistent ROAS track record, can quickly dilute performance and generate unnecessary costs. **How to avoid it**: Scale gradually, increasing the budget by 15-20% every 2-3 days, closely monitoring ROAS and CPA. If ROAS drops significantly, lower the budget and focus on creative and audience optimization. Example: A campaign with a 3.0 ROAS at $200/day can be scaled to $240/day and monitored for 48h before another increase.

---

## Advanced Tips

1.  **LTV (Lifetime Value) Segmentation for Retargeting**: Create custom audiences in Meta Ads based on customer LTV (total amount spent). Prioritize remarketing to high-LTV customers with exclusive offers, loyalty programs, or higher-ticket complementary products. Example: Create a "VIP Customers" audience that spent more than $500 in the last 12 months and target them with premium product pre-launch ads or higher-margin cross-sell items.
2.  **Using Smart Bidding on Google Ads with adjusted conversion values**: Instead of only optimizing for "Purchases" with a fixed value, adjust the value of each conversion in Google Ads to reflect the real profit margin or estimated LTV per product/category. This lets Smart Bidding prioritize more profitable sales. Example:
