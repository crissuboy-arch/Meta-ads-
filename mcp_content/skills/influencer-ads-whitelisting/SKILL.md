---
name: influencer-ads-whitelisting
description: "Influencer Ads Whitelisting — Specialized skill for setting up, optimizing, and managing influencer ads whitelisting campaigns on Meta Ads, Google Ads, and TikTok Ads."
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Influencer Ads Whitelisting

This skill enables you to set up, optimize, and manage Influencer Ads Whitelisting campaigns, using partner access on platforms like Meta Ads, Google Ads, and TikTok Ads to maximize ad performance and scale.

---

## Keywords

Influencer Whitelisting, Meta Partner Access, TikTok Spark Ads, Google Ads Influencer, Collab Ads, Influencer Dark Posts, Whitelisting Optimization, Influencer Scalability, Meta Business Suite Permissions, TikTok Branded Content, Influencer-Identity Ads, Influencer Ad Permission.

---

## Quick Start

1.  **Get the Business Manager (BM) ID** from the influencer for Meta Ads, or the Spark Ads code for TikTok.
2.  **Send a partner access request** (Meta Ads) or import the code (TikTok Ads) into your ad account.
3.  **Create the campaign** in Ads Manager, selecting the influencer's identity at the ad level.
4.  **Publish and monitor** performance metrics (ROAS, CTR, CPA) for continuous optimization.

---

## Core Workflows

### Workflow 1: Whitelisting Setup for Meta Ads (Facebook/Instagram)

This workflow details the process of obtaining permission and creating ad campaigns that will appear with an influencer's identity on Facebook and Instagram, using Meta Business Manager (BM).

1.  **Prerequisite Check with the Influencer:**
    *   Confirm the influencer has an active Meta Business Manager (BM).
    *   Make sure the influencer's Instagram and/or Facebook page is linked to their BM.
    *   Request the influencer's BM ID (e.g.: `ID: 1234567890`).

2.  **Partner Access Request in Your BM:**
    *   In your Meta Business Manager (e.g.: "BM Digital Agency X"), navigate to "Business Settings" > "Partners."
    *   Click "Add" and select "Give a partner access to your assets."
    *   Enter the influencer's BM ID (e.g.: `1234567890`).
    *   On the next screen, select the assets needed for the collaboration:
        *   **Pages:** Select the influencer's Instagram and/or Facebook page (e.g.: "@influencer_top"). Grant the "Ads" and "Content" permissions (essential for creating and running ads with the influencer's identity).
        *   **Ad Accounts:** Usually not necessary for whitelisting, but can be granted if there's a need to directly manage the influencer's ad account.
        *   **Pixels:** If the influencer has their own pixel and you need data or permission to write events, request "Manage Pixel" access.
    *   Click "Save changes." The influencer will receive a notification in their BM to accept the invite.

3.  **Ad Campaign Creation in Your BM's Ads Manager:**
    *   In your BM's Ads Manager, click "Create" to start a new campaign.
    *   **Campaign Objective:** For e-commerce campaigns with whitelisting, select "Sales." For greater reach and awareness, "Awareness" or "Reach."
    *   **Ad Set Setup:**
        *   Define your target audience (e.g.: "Women, 25-45, interests in sustainable fashion, United States").
        *   Budget (e.g.: `$200.00/day`) and schedule.
        *   Placements: "Advantage+ Placements" is recommended for automatic optimization.
    *   **Ad Setup (Ad Level):**
        *   Under "Identity," select the influencer's Instagram/Facebook page (e.g.: "@influencer_top"). This is the crucial step for whitelisting.
        *   **Ad Format:**
            *   **Use Existing Post:** Select an organic post the influencer already published (e.g.: a product review Reels). This capitalizes on existing engagement and social proof.
            *   **Create Ad (Dark Post):** Build an ad from scratch that will run only as an ad, without appearing in the influencer's organic feed. Ideal for A/B testing more commercial creatives.
        *   Add the call to action (CTA, e.g.: "Shop Now") and the final URL of your landing page (with UTM parameters for tracking: `?utm_source=metaads&utm_medium=influencer_top&utm_campaign=product_launch`).
    *   Publish the campaign and start monitoring.

### Workflow 2: Optimization and Scalability of Whitelisted Campaigns on TikTok Ads (Spark Ads)

This workflow focuses on using TikTok Spark Ads to boost influencer content, optimizing and scaling results.

1.  **Authorization Code (Spark Ads) from the Influencer:**
    *   **Prerequisite:** The influencer must have a TikTok Business account and the content (video) already published or ready to publish on their profile.
    *   **Step 1.1:** The influencer publishes the video on TikTok. After publishing, they open the video, tap the three dots (...) and select "Ad settings."
    *   **Step 1.2:** Turn on "Ad authorization" and generate an authorization code (e.g.: `789ABCDEF`). It's essential to set an adequate validity period (e.g.: 60 or 90 days) for the campaign duration.
    *   **Step 1.3:** The influencer shares the authorization code with your agency/brand.

2.  **Campaign Creation in Your Brand's TikTok Ads Manager:**
    *   In your agency/brand's TikTok Ads Manager account, create a new campaign.
    *   **Campaign Objective:** For conversions, select "Sales" or "Lead Generation."
    *   **Ad Set Setup:**
        *   Define your target audience (e.g.: "Men and women, 18-34, interest in gaming, United States").
        *   Budget (e.g.: `$150.00/day`) and schedule.
    *   **Ad Setup (Ad Level):**
        *   Under "Ad Details," select "Use TikTok post."
        *   Click "Enter authorization code" and paste the code provided by the influencer (e.g.: `789ABCDEF`).
        *   The influencer's video will be imported and will appear with their profile as the ad identity.
        *   Add the CTA (e.g.: "Shop Now," "Learn More") and the destination URL (with UTMs: `?utm_source=tiktokads&utm_medium=influencer_gamertop&utm_campaign=headset_promo`).
    *   Publish the campaign.

3.  **Optimization and Scalability Strategies:**
    *   **Daily Performance Analysis:** Monitor metrics like CPM, CPC, CTR, CVR, and ROAS. Videos with CTR above 1.8% and ROAS > 2.5x are excellent candidates for scaling.
    *   **Audience A/B Tests:** Create duplicated ad sets for the same whitelisted content, testing distinct audiences. E.g.: a 1% purchaser lookalike audience vs. a broad interests audience related to the influencer's niche.
    *   **Gradual Budget Increases:** For high-performance campaigns, increase the budget by 15-25% every 2-3 days, avoiding shocks to the algorithm that can destabilize delivery.
    *   **Multi-Influencer Whitelisting:** Collaborate with 3-5 influencers simultaneously to test different content styles and audience profiles. Invest more in those generating the best ROAS and lowest CPA.

---

## Templates

### Template 1: Meta Business Suite Partner Access Request (Email)

```
Subject: BM Partner Access Request for Collab Ads - [Brand Name] x [Influencer Name]

Dear [Influencer/Manager Name],

We hope this email finds you well.

On behalf of [Brand Name], we're very excited about our partnership and the potential of our upcoming joint ads. So we can run optimized ads using your identity on Facebook and Instagram (the well-known "Influencer Ads Whitelisting"), we need partner access to your Meta Business Manager (BM).

This access is secure and lets us create campaigns in [Brand Name]'s Ads Manager that will appear as if published directly from your page, but with the ability to be boosted with paid budget and precise targeting.

Please follow the steps below to grant us access:
1. Open your Meta Business Manager (business.facebook.com/overview).
2. Go to "Business Settings" > "Requests" > "Received."
3. You should find a partnership request from our BM, "BM Alpha Marketing Agency" (ID: 1234567890).
4. Accept the request.
5. Confirm that our BM has access to your Instagram/Facebook Page ([Link to your Page, e.g.: instagram.com/influencer_top_beauty]) with "Ads" and "Content" permissions.

If you have any questions or need help with the steps, please don't hesitate to contact us at [Your Phone/WhatsApp].

Thank you so much for your collaboration!

Best regards,

[Your Name/Agency Name]
[Your Role]
[Your Contact]
```

### Template 2: Summary Performance Report (Influencer Whitelisting)

```
Performance Report - Whitelisting [Influencer Name] - [Period: 03/01 - 03/07/2024]

Campaign: Winter 2024 Launch - @FashionStyle_Influencer
Platform: TikTok Ads
Objective: Sales

----------------------------------------------------
Key Metrics:
----------------------------------------------------
Total Spend: $4,800.00
Revenue Generated: $19,200.00
ROAS (Return on Ad Spend): 4.0x
CPA (Cost per Acquisition): $48.00

Impressions: 400,000
Reach: 210,000
Link Clicks: 8,000
CTR (Link Click-Through Rate): 2.0%
CPC (Cost per Link Click): $0.60

Add to Cart: 320
Purchases: 100
Conversion Rate (Purchases/Clicks): 1.25%

----------------------------------------------------
Quick Analysis:
----------------------------------------------------
The campaign with @FashionStyle_Influencer's content on TikTok posted a 4.0x ROAS, beating our 3.0x target. The 2.0% CTR indicates strong appeal of the creative and the engaged audience. The $48.00 CPA is highly competitive for the fashion industry. The "Winter Look of the Day" video generated the best results.

----------------------------------------------------
Next Steps:
----------------------------------------------------
1. Increase the campaign budget by +20% ($960/week) for next week.
2. Create a new ad set with a 1% Purchaser Lookalike from the brand's pixel on TikTok.
3. Request a new Spark Ads code from the influencer for the "Winter Unboxing" video for A/B testing.
4. Test a different CTA ("Get Your Look") on the best-performing video.
```

---

## Checklist

- [x] Does the influencer have a Meta Business Manager (BM) configured and active?
- [x] Is the influencer's Instagram/Facebook page linked to their BM?
- [x] Was the influencer's BM ID collected correctly and saved for future reference?
- [x] Was the partner access request to the influencer's BM sent with "Ads" and "Content" permissions for the page?
- [x] Did the influencer accept the partnership request in their BM and confirm the permissions?
- [x] For TikTok: Did the influencer enable "Ad authorization" and generate the Spark Ads code with adequate validity?
- [x] TikTok Spark Ads code imported and validated
