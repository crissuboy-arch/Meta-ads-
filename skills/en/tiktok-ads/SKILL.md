---
name: tiktok-ads
description: "TikTok Ads — Specialized skill for tiktok ads"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# TikTok Ads

This skill enables you to create, optimize, and analyze TikTok Ads campaigns, focusing on performance and real results for ecommerce and lead generation.

---

## Keywords

TikTok Ads campaigns, ROAS optimization, TikTok conversions, TikTok Pixel, Spark Ads, TikTok video ads, TikTok custom audiences, TikTok product launch, TikTok lead generation, TikTok metrics analysis, TikTok bid strategies, TikTok viral creatives.

---

## Quick Start

1.  **TikTok Pixel Installation**: Implement the base pixel and conversion events (ViewContent, AddToCart, InitiateCheckout, CompletePayment) on your site via GTM or directly in the code.
2.  **First Conversion Campaign Creation**: Set up a campaign with the "Website Conversions" objective targeting a "CompletePayment" event for ecommerce or "Lead" for lead gen.
3.  **Ad Group Configuration**: Choose automatic placements, a daily budget of $50-$100, and broad interest targeting (e.g.: "Fashion and Accessories," "Beauty and Personal Care") or use custom audiences of website visitors from the last 30 days.
4.  **Native Creative Upload**: Add 3-5 short videos (15-60s) in vertical format (9:16) with clear captions and a direct call to action, using trending TikTok music.
5.  **Initial Monitoring and Bid Adjustment**: Monitor CPC and CPA in the first 24-48h; if CPA is too high, review the creatives or adjust the bid to "Cost Cap" with a value 10-20% below your maximum acceptable CPA.

---

## Core Workflows

### Workflow 1: High-Performance Ecommerce Conversion Campaign Creation

This workflow details building a campaign focused on direct sales for an ecommerce product, aiming to maximize Return on Ad Spend (ROAS).

1.  **Campaign Structure**:
    *   **Campaign Level**:
        *   **Objective**: Select "Website Conversions."
        *   **Campaign Name**: `PRODUCT_NAME_SALE_CONVERSION_MMDD` (e.g.: `URBAN_SNEAKERS_SALE_CONVERSION_0825`).
        *   **Campaign Budget Optimization (CBO)**: Turn off initially for granular control in the ad groups.
    *   **Ad Group Level**: Create 2-3 distinct ad groups to test audiences.
        *   **Ad Group Name**: `PRODUCT_NAME_AUDIENCE_TYPE` (e.g.: `URBAN_SNEAKERS_BROAD_INTERESTS`, `URBAN_SNEAKERS_BUYER_LOOKALIKE`).
        *   **Promotion Type**: `Website`.
        *   **TikTok Pixel**: Select the configured pixel.
        *   **Optimization Event**: `Complete Payment` (or `Purchase`).
        *   **Placements**: `Automatic` (lets TikTok optimize for the best results, including the Pangle Network).
        *   **Creative Types**: `Dynamic Creative` (so TikTok automatically tests creative combinations).
        *   **Targeting (Audience)**:
            *   **Ad Group 1 (Broad Interests)**:
                *   **Location**: `United States`.
                *   **Gender**: `All`.
                *   **Age**: `18-55+`.
                *   **Interests**: Add 3-5 broad interests related to the product (e.g.: "Fashion and Style," "Sports," "Online Shopping").
                *   **Behavior**: `Video interaction` (last 7 days) in relevant categories (e.g.: "Fashion," "Beauty").
            *   **Ad Group 2 (Buyer Lookalike)**:
                *   **Location**: `United States`.
                *   **Gender**: `All`.
                *   **Age**: `18-55+`.
                *   **Custom Audience**: Exclude "Buyers in the last 30 days" to avoid hitting those who already converted.
                *   **Lookalike Audience**: Create a `1%` audience similar to `Complete Payment` from the last `90 days`.
        *   **Budget and Schedule**:
            *   **Daily Budget**: $70-$100 per Ad Group.
            *   **Schedule**: `Run Continuously`.
        *   **Bid and Optimization Strategy**:
            *   **Optimization Goal**: `Conversion`.
            *   **Bid Strategy**: `Lowest Cost`. Start with this option to collect data. After 3-5 days and more than 20 conversions, consider switching to `Cost Cap` with a value 10-20% above your ideal CPA.
    *   **Ad Level**: Create 3-5 ads per Ad Group.
        *   **Format**: `Single Video`.
        *   **Creative**:
            *   **Videos**: 15-60 seconds, vertical format (9:16), high resolution, with captions. Use UGC-style videos (User-Generated Content) or quick product demos. E.g.: "Before and after" video of sneakers being cleaned or styled.
            *   **Music**: Use popular TikTok music that fits the niche.
            *   **Primary Text (Ad Text)**: `Discover the Urban Sneakers [Product Name]! Style and comfort for your everyday. Free shipping for a limited time! 👟✨`
            *   **Call to Action (CTA)**: `Shop Now`, `Learn More`.
        *   **Destination URL**: The specific product page on your ecommerce store.

### Workflow 2: Optimization of Active Campaigns with Low ROAS (Below 1.5x)

This workflow details the steps to improve the performance of campaigns that are spending budget but delivering unsatisfactory ROAS.

1.  **Initial Data Analysis (24-48h)**:
    *   **Reports**: Open TikTok Ads Manager, select the campaign, and analyze metrics by `Ad` (creative), `Ad Group` (audience), and `Campaign`.
    *   **Key Metrics**: Watch `CPM` (Cost Per 1,000 Impressions), `CTR` (Click-Through Rate), `CPC` (Cost Per Click), `CPA` (Cost Per Acquisition), and `ROAS`.
    *   **Bottleneck Identification**:
        *   `High CPM, low CTR`: Creative or audience relevance problem. The audience isn't engaging with the ad.
        *   `Good CTR, high CPA`: The click is cheap, but conversion is expensive. Problem with the landing page, offer, or audience qualification.
        *   `Low ROAS in a specific Ad Group`: Indicates that audience isn't profitable.
2.  **Optimization Actions at the Ad Level (Creative)**:
    *   **Pause Low-Performing Creatives**: Identify ads with `CTR below 0.6%` and `ROAS below 1.0x` after accumulating at least 5,000 impressions. Pause them.
    *   **Upload New Creatives (Refresh)**: Create 2-3 new videos with different approaches (e.g.: customer testimonial, humor, focus on a specific benefit). Test new hooks in the first 3 seconds and calls to action.
    *   **Spark Ads Testing**: If you have content creators or influencers, use the Spark Ads feature to boost their videos directly from their accounts, increasing authenticity and engagement.
3.  **Optimization Actions at the Ad Group Level (Audience and Offer)**:
    *   **Targeting Review**:
        *   **Unqualified Audience Exclusion**: If `CPA` is high in an interest Ad Group, add exclusions for audiences that already converted or showed low value (e.g.: blog visitors who didn't interact with products).
        *   **Interest/Behavior Refinement**: Test more niche interests or combine interests with specific video behaviors (e.g.: "watched fashion videos to the end").
        *   **Different Lookalike Testing**: Experiment with 1% and 3% lookalikes of `AddToCart` or `InitiateCheckout` events — warmer audiences than site visitors alone.
    *   **Budget and Bid Adjustment**:
        *   **Budget Redistribution**: Pause Ad Groups with `ROAS below 1.0x` or `CPA far above target` and reallocate the budget to well-performing Ad Groups (e.g.: `ROAS above 2.0x`).
        *   **Bid Strategy (if you have data)**: If the campaign has at least 20 conversions and `CPA` is consistent, test the `Cost Cap` strategy. Set the cost cap 10-15% above your `target CPA` to give the system room to optimize.
4.  **Landing Page Optimization**:
    *   **Load Speed**: Check the load time of the product/offer page. Slow pages increase bounce rate.
    *   **Offer Clarity**: Make sure the value proposition, price, and CTA are extremely clear and visible on mobile devices.
    *   **Social Proof**: Add customer reviews, security badges, and a guarantee.

---

## Templates

### TikTok Ads Campaign Brief for a Product Launch

```
**CAMPAIGN NAME:** Summer 2024 Capsule Collection Launch - [Brand Name]
**CAMPAIGN OBJECTIVE:** Website Conversions (Sales)
**PRODUCT/SERVICE PROMOTED:** Capsule Collection of Light Dresses and Beach Accessories
**TARGET AUDIENCE:**
  - **Demographics:** Women, 20-45, United States
  - **Interests:** Fashion and Style, Travel, Beach, Summer, Online Shopping, Beauty and Personal Care
  - **Behaviors:** Video interaction (last 7 days) in "Fashion" and "Travel"
  - **Custom Audiences:** 1% Lookalike of Buyers from the last 90 days; Exclusion of Buyers from the last 7 days.
**DAILY BUDGET:** $150 (Total $4,500 for 30 days)
**CAMPAIGN DURATION:** 10/01/2024 - 10/31/2024
**SUCCESS METRICS:**
  - ROAS: Above 2.5x
  - CPA (Cost per Acquisition): Maximum $30
  - CTR: Above 0.8%
**KEY MESSAGE:** Wear the lightness and style of summer. Exclusive collection for you to shine!
**CALL TO ACTION (CTA):** Shop Now / Learn More
**DESTINATION URL:** [collection_link_on_site.com]
**CREATIVE IDEAS (Videos):**
  1.  **UGC (User-Generated Content):** Influencer showing off the dresses in a beach/pool setting, highlighting details and fabric lightness.
  2.  **Quick Demo:** Fast look transitions with different collection pieces, with a summer soundtrack and on-screen text with benefits (e.g.: "Breathable fabric," "Perfect for everyday").
  3.  **"Get Ready With Me":** Video showing the process of choosing a collection look for a summer event, with accessories.
**NOTES:** Prioritize videos with trending TikTok music and captions for accessibility.
```

### Short TikTok Video Ad Script (UGC Format)

```
**PRODUCT:** Anti-Acne Skincare Kit "Renewed Skin"
**TARGET DURATION:** 25-30 seconds
**OBJECTIVE:** Generate interest and clicks to the product page.
**AUDIO:** Popular TikTok music with an upbeat beat, then fade to narrator voice.
**SCENE 1 (0-3s): Hook - Common Problem**
  - **Visual:** Person (acting) looking in the mirror with a frustrated expression, close-up on a pimple. On-screen text: "Tired of pimples?"
  - **Voiceover:** "Do you also struggle with acne that just won't go away?"
**SCENE 2 (3-10s): Solution Presentation - Product Highlight**
  - **Visual:** Quick transition to hands holding the "Renewed Skin" Kit attractively, showing the bottles.
  - **Voiceover:** "Meet the Renewed Skin Kit! The complete solution for acne-free, radiant skin."
**SCENE 3 (10-20s): Demo and Benefits**
  - **Visual:** Person applying the kit products to their skin (washing face, applying serum, cream), with close-ups on texture and absorption. Quick "before and after" transitions of improved skin.
  - **Voiceover:** "With natural ingredients and advanced technology, our kit deep-cleans, reduces inflammation, and prevents new pimples. See the difference!"
**SCENE 4 (20-25s): Social Proof / Call to Action**
  - **Visual:** Small clip of a customer testimonial (on-screen text or short audio) or a shot of 5-star reviews. Person smiling with clear skin.
  - **Voiceover:** "Thousands of people have already transformed their skin. Don't waste time!"
**SCENE 5 (25-30s): Final CTA**
  - **Visual:** Final screen with the kit, brand logo, and BIG text: "Renewed Skin. Click 'Shop Now'!" Animated CTA button.
  - **Voiceover:** "Click 'Shop Now' and achieve the skin of your dreams!"
**AD PRIMARY TEXT:** "Say goodbye to acne! ✨ The Renewed Skin Kit is your ally for flawless skin. Visible results in just a few weeks! #RenewedSkin #Skincare #AntiAcne #TikTokBeauty"
**DESTINATION URL:** [product_page_link.com]
```

---

## Checklist

- [x] TikTok base pixel and conversion events (ViewContent, AddToCart, CompletePayment) installed and verified.
- [x] Campaign with "Website Conversions" or "Lead Generation" objective configured.
- [x] Optimization event selected (e.g.: "Complete Payment," "Lead").
- [x] Daily budget defined (minimum $50 per Ad Group to start).
- [x] Target audience targeting configured (interests, lookalikes, exclusions).
- [x] Minimum of 3-5 video creatives (9:16) per Ad Group, with clear captions and CTA.
- [x] "Automatic" placements test enabled to explore Pangle and others.
- [x] Initial "Lowest Cost" bid strategy selected for learning.
- [x] Daily monitoring of CPM, CTR, CPC, CPA, and ROAS started.
- [x] Destination URL checked for fast loading and mobile optimization.
- [x] Recent buyer audience exclusion (last 7-30 days) for acquisition campaigns.
- [x] Dynamic Creative setup enabled to let TikTok test ad copy and creative variations.

---

## Reference Metrics

| Metric | Benchmark (Ecommerce) | Target (Optimized) |
|---------|-------------------------------|------------------|
| CTR     | 0.6% - 1.0%                   | 1.2% - 2.5%      |
| CPC     | $0.80 - $1.50             | $0.50 - $1.00|
| CPM     | $12.00 - $25.00           | $8.00 - $18.00|
| CPA     | $40.00 - $100.00          | $20.00 - $50.00|
| ROAS    | 1.5x - 2.5x                   | 3.0x - 5.0x      |
| Conversion Rate | 0.8% - 1.5%           | 1.8% - 3.0%      |

---

## Common Mistakes

1.  **Not Using the TikTok Pixel Correctly**: Often the pixel is installed, but conversion events aren't configured or are misconfigured (e.g.: "CompletePayment" firing on the cart).
    *   **How to avoid it**: Use the "TikTok Pixel Helper" tool (Chrome extension) to verify all conversion events are firing correctly at each step of your site's funnel. Test each event manually (add to cart, start checkout, complete purchase).
2.  **Creatives Not Native to TikTok**: Ads that look like traditional commercials or don't follow the platform's short, authentic video style (no captions, horizontal format, slow editing).
    *   **How to avoid it**: Create videos with dynamic editing, hooks in the first 3 seconds, clear captions, trending soundtracks, and vertical format (9:16). Think of content that blends organically with the user feed, like UGC videos, quick tutorials, or challenges. E.g.: A clothing ad showing "5 ways to wear this piece" instead of a static model.
3.  **Targeting Too Narrow or Too Broad**: Very small audiences limit reach and raise CPM, while overly broad audiences spend money on unqualified people.
    *   **How to avoid it**: Start with broad interest targeting combined with video behaviors and location. After collecting data (at least 50 conversions), create 1-3% Lookalike audiences of your best customers or of AddToCart/InitiateCheckout events. Exclude irrelevant or already-converted audiences to avoid budget waste.

---

## Advanced Tips

1.  **Multiple Video Hook Testing**: Create 3-5 variations of the same ad, changing only the first 3-5 seconds (the "hook"). A strong hook is crucial to hold attention on TikTok. E.g.: For a beauty product, test hooks like "My secret to perfect skin," "Stop wasting money!" and "You'll never suffer from... again."
2.  **Use Spark Ads for Authenticity**: Collaborate with content creators and use the Spark Ads feature to boost their videos directly from their accounts. This increases social proof, authenticity, and often engagement and conversion rate, as users trust creator content more.
3.  **User-Generated Content (UGC) Optimization**: Encourage or create campaigns with videos that simulate user-generated content. TikTok values spontaneity. Use testimonials, "unboxing" product reviews, or videos of people using the product in real situations, with informal, genuine language.
4.  **Dynamic Retargeting Strategy with Catalog**: Set up a product catalog in TikTok Ads Manager and use dynamic retargeting campaigns to show personalized ads for products users viewed, added to cart, or started checkout for on your site but didn't convert. This generally has very high ROAS.
5.  **"Cost Cap" Bid Strategy Testing**: After the campaign accumulates significant conversion volume (over 50), switch the bid strategy from "Lowest Cost" to "Cost Cap." Set the cost cap 10-20% above your target CPA. This lets you control cost per acquisition while the algorithm still optimizes, without being as restrictive as a "Bid Cap."
