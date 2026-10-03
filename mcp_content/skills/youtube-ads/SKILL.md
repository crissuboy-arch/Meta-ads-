---
name: youtube-ads
description: "YouTube Ads — Specialized skill for youtube ads"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# YouTube Ads

This skill enables you to plan, execute, and optimize advertising campaigns on YouTube, covering everything from objective selection and audience targeting to metrics analysis and implementation of advanced performance tactics.

---

## Keywords

TrueView In-Stream, TrueView Discovery, Bumper Ads, Outstream Ads, CPV, VRC (View Rate), YouTube ROAS, Video Remarketing, Custom Segment, Competitor Channels, Placement Exclusions, Bid Optimization.

---

## Quick Start

1.  **Set Up Conversion Tracking in Google Ads:** Link your YouTube account to Google Ads and make sure conversion actions (e.g., "Purchase," "Form Submission") are correctly configured and tested via Google Tag Manager or gtag.js.
2.  **Select a Performance Campaign Objective:** Create a new campaign in Google Ads, choosing "Sales" or "Leads" as the objective, then select "Video" as the campaign type.
3.  **Define Bid Strategy and Budget:** For performance campaigns, use "Maximize Conversions" or "Target ROAS." Set a minimum daily budget of $50-100 to allow algorithm learning.
4.  **Create Custom Audience Segments:** Develop segments with competitor URLs (e.g., `youtube.com/channel/UC...`), relevant search terms (e.g., "best CRM software," "digital marketing course"), and custom intent.
5.  **Develop 2-3 Diverse Video Ads:** Produce videos made specifically for YouTube, 15-30 seconds for In-Stream and longer formats for Discovery, focusing on a "hook" in the first 5 seconds and a clear call to action.

---

## Core Workflows

### Workflow 1: YouTube Lead Generation Campaign Creation with Lead Forms

This workflow details building a YouTube Ads campaign focused on capturing qualified leads directly through native Google Ads forms, minimizing user friction.

**Detailed Steps:**

1.  **Campaign Start and Objective:**
    *   In Google Ads, click `Campaigns` > `+ New Campaign` > `+ New Campaign`.
    *   Select the `Leads` objective.
    *   Choose the `Video` campaign type.
    *   Select the subtype `Generate leads with lead form` and click `Continue`.
    *   Name the campaign, e.g.: `YT_Leads_LeadForm_CRMSoftware`.

2.  **Budget and Bid Definition:**
    *   **Bid Strategy:** Select `Maximize conversions`. For lead campaigns, the focus is lead quantity, and this strategy optimizes for that.
    *   **Budget:** Set a `Daily Budget` of, for example, `$80.00`. This allows the system to collect enough data for initial optimization.

3.  **Target Audience Segmentation:**
    *   **Location and Language:** Target `United States` and `English`.
    *   **Audience Segments:**
        *   **Custom Segments:** Create a new segment with "People who searched for any of these terms on Google" and include terms like "CRM software for small businesses," "customer management tool," "CRM comparison." Create another with "People who browsed any of these types of websites" and add direct competitor URLs (e.g., `pipedrive.com`, `hubspot.com`).
        *   **Custom Intent Audiences:** Create an audience with buying-intent keywords like "buy CRM software," "CRM pricing online."
        *   **Demographics:** Adjust age and household income if your product/service has a specific demographic profile (e.g., `25-54`, `Top 10% Household Income`).
        *   **Exclusions:** Exclude remarketing audiences that already converted (e.g., "Purchasing Customers") to avoid spending budget on existing customers.

4.  **Placements and Exclusions:**
    *   **Placements (Optional):** For granular control, you can target specific channels (e.g., tech review channels, business channels). However, for lead gen it's common to leave this open for Google to find the best placements.
    *   **Content Exclusions:** It's CRITICAL to exclude `Sensitive content`, `Live streaming`, `Embedded videos`, `Gaming channels`, `Made for kids`. This prevents impressions in low-quality or irrelevant places. Also exclude `Topics` like "News and Politics" or "Games" if not relevant.

5.  **Video Ad Creation:**
    *   **YouTube Video:** Paste your video URL (e.g., `https://www.youtube.com/watch?v=ABCDEF123`).
    *   **Formats:** Use `Skippable in-stream ad` to maximize video views and lead form interaction.
    *   **Final URL:** The destination page URL for when the user clicks your ad (e.g., `https://yoursite.com/crm-software`).
    *   **Call to Action (CTA):** `Download Now`, `Learn More`, `Free Trial`.
    *   **Headline:** `Essential CRM Software` (90 characters).
    *   **Lead Form (New):**
        *   **Form Headline:** `Request Your Free CRM Trial`
        *   **Business Name:** `My SaaS Company`
        *   **Description:** `Discover how our CRM optimizes your sales and support. Fill it out and start today!`
        *   **Questions:** `Full Name`, `Email`, `Phone`, `Company Name`. Add a custom question like `How many employees does your company have?` (Multiple choice: `1-5`, `6-20`, `21-100`, `100+`).
        *   **Privacy Policy URL:** `https://yoursite.com/privacy-policy`
        *   **Submission Message:**
            *   **Headline:** `Thanks for your interest!`
            *   **Description:** `We'll be in touch soon to schedule your demo.`
            *   **Call to Action:** `Visit website` or `Download e-book`.

### Workflow 2: YouTube Ads Optimization for Ecommerce with ROAS

This workflow focuses on refining YouTube Ads campaigns for ecommerce, aiming to maximize Return on Ad Spend (ROAS) through bid, targeting, and creative adjustments.

**Detailed Steps:**

1.  **Initial Performance Analysis (7-14 days after launch):**
    *   **Primary Metrics:** Watch `ROAS`, `Cost per Conversion (CPA)`, `Conversion Rate (CVR)`, `View Rate (VTR)`, and `Cost per View (CPV)`.
    *   **Segmentation Reports:** Go to `Campaigns` > `Ad groups` > `Segments`. Analyze performance by `Device type`, `Time of day`, `Location`, and `Age/Gender`. Identify segments with ROAS below target.
    *   **Placements Report:** Under `Content` > `Placements`, check the channels and videos where your ads were shown. Identify placements with low ROAS, high CPV, and low CVR.

2.  **Bid and Strategy Adjustments:**
    *   **Target ROAS:** If the campaign is on `Maximize conversion value` or `Target ROAS`, adjust the `Target ROAS` gradually. If ROAS is below target (e.g., target 300% and it's at 200%), raise the target to 320-350% to force the system to seek higher-value conversions. If ROAS is very good but volume is low, reduce the target to 280% to try to scale.
    *   **Device Bid Adjustments:** If mobile devices have much lower ROAS (e.g., 150% vs. desktop 400%), apply a negative bid adjustment (e.g., `-20%` or `-30%`) for mobile devices.
    *   **Demographic/Location Bid Adjustments:** If a specific age range or region underperforms, apply negative bid adjustments or exclude those segments.

3.  **Audience Refinement:**
    *   **Audience Exclusions:**
        *   **Low Performance:** Exclude `demographic segments` or `interests` that consistently show negative or very low ROAS.
        *   **Audiences That Already Purchased:** Use remarketing lists of customers who already made a purchase to exclude them from acquisition campaigns, focusing the budget on new customers.
    *   **Adding New Audiences:**
        *   **Custom Segments:** Create new intent segments based on specific product search terms or product review URLs.
        *   **Similar Audiences (Lookalikes):** Create similar audiences from your `buyers`, `cart abandoners`, or `product page visitors` lists.

4.  **Creative and Placement Optimization:**
    *   **Video A/B Testing:** Test video ad variations (different "hooks" in the first 5 seconds, CTAs, offers). Create new ads focused on customer reviews, product demos, or seasonal promotions.
    *   **Low-Quality Channel/Video Exclusion:**
        *   In the `Placements` report, select channels/videos with low ROAS, high CPV, and/or low-quality views (e.g., kids' channels, generic content aggregators, off-niche videos).
        *   Click `Exclude` > `Exclude from ad group` or `Exclude from campaign` to remove these placements.
    *   **Format Testing:** Experiment with `Bumper Ads` (6s, non-skippable) to reinforce branding and complement performance campaigns, especially for impulse products.

5.  **Budget Adjustments:**
    *   **Scale Successful Campaigns:** If a campaign or ad group is delivering excellent ROAS, consider increasing the budget by `10-20%` every 3-5 days to avoid destabilizing the algorithm's learning.
    *   **Reduce Budget/Pause Weak Campaigns:** If a campaign doesn't hit the target ROAS after optimizations and an adequate learning period, reduce the budget or pause it to reallocate resources.

---

## Templates

### TrueView In-Stream Video Ad Script (Performance)

```
[0-5 seconds] HOOK: close-up of a person frustrated with the computer, scene of a slow ecommerce store.
NARRATOR (VO): "Tired of losing sales to a sluggish online store?"

[5-15 seconds] PROBLEM/SOLUTION: Quick transition to animated graphics showing the problem (slowness, bugs) and the solution ("FastShop" platform).
NARRATOR (VO): "With FastShop, your site loads 3x faster, ensuring your customers complete their purchase without friction."

[15-25 seconds] BENEFIT/SOCIAL PROOF: Quick testimonial from a satisfied customer or conversion increase numbers.
CUSTOMER (on screen): "After FastShop, my online sales exploded! Incredible!"
ON-SCREEN TEXT: "+35% CONVERSIONS IN 30 DAYS!"

[25-30 seconds] CALL TO ACTION (CTA): Final screen with logo, website URL, and a clear button.
NARRATOR (VO): "Don't waste any more time and sales! Click NOW for a free trial and transform your store!"
ON-SCREEN TEXT: "FREE TRIAL AT FASTSHOP.COM - CLICK AND SELL MORE!"
BUTTON: "FREE TRIAL"
```

### Custom Segment Structure for YouTube Ads

```
Segment Name: "Interest in B2B Productivity Tools"

Segment Type: People who searched for any of these terms on Google
Search Terms:
- "best project management software"
- "online collaboration tools"
- "marketing automation for small businesses"
- "CRM for sales"
- "cloud ERP system"

Segment Type: People who visited any of these types of websites
Website URLs:
- "asana.com"
- "monday.com"
- "hubspot.com"
- "salesforce.com"
- "trello.com"
- "clickup.com"

Notes: This segment combines active search intent with demonstrated interest from visiting competitor or industry-leader websites, creating a highly qualified audience for B2B SaaS campaigns.
```

---

## Checklist

- [x] Link YouTube account to Google Ads.
- [x] Configure conversion tracking with specific values for ecommerce (e.g., `purchase value`).
- [x] Create at least 2 custom audience segments (search intent and competitor URLs).
- [x] Exclude low-quality channels, irrelevant topics, and live streams.
- [x] Develop 3-5 video ad variations with clear CTAs and "hooks" in the first 5 seconds.
- [x] Implement a performance-based bid strategy (Maximize conversions or Target ROAS).
- [x] Run A/B tests of video thumbnails.
- [x] Configure audience and placement reports for post-launch analysis.
- [x] Schedule remarketing list exclusions of existing customers for acquisition campaigns.
- [x] Analyze VTR (View Rate) and CPV (Cost per View) for creative and targeting optimization.

---

## Reference Metrics

| Metric | Benchmark (Performance) | Target (Ecommerce/Leads) |
|---------|-------------------------|-------------------------|
| VTR (View Rate) | 20% - 40% (In-Stream) | > 35%                   |
| CPV (Cost per View) | $0.05 - $0.20       | < $0.10               |
| CTR (Click-Through Rate) | 0.5% - 2.0%             | > 1.0%                  |
| CVR (Conversion Rate) | 1.0% - 5.0%             | > 2.5%                  |
| ROAS (Return on Ad Spend) | 150% - 300%             | > 250%                  |
| CPA (Cost per Acquisition) | $20.00 - $100.00 (Lead) | < $50.00              |

---

## Common Mistakes

1.  **Not Excluding Irrelevant Channels and Topics**: Ads appearing on kids' videos, gaming channels, or news unrelated to the product, generating irrelevant impressions and clicks.
    *   **How to avoid it**: Always use `Content exclusions` (channels, topics, content types) at the campaign level. For example, exclude `Games`, `Embedded content`, `Live streaming`, and create specific channel exclusion lists (e.g., cartoon channels).
2.  **Generic Creatives Not Optimized for YouTube**: Using long institutional videos or adapted TV ads, with no strong "hook" in the first seconds or clear CTA. This results in low VTR and early abandonment.
    *   **How to avoid it**: Develop short videos (15-30s for In-Stream), dynamic, that capture attention in the first 5 seconds. Include the value proposition and an explicit CTA. Test different "hooks" and offers.
3.  **Budget Too Low for Performance Campaigns**: Setting a negligible daily budget (e.g., $10-20) for "Maximize conversions" or "Target ROAS" campaigns. This prevents the algorithm from collecting enough data for optimization.
    *   **How to avoid it**: Start with a daily budget of at least $50-$100 for performance campaigns. Monitor cost per conversion and gradually increase the budget by 10-20% every 3-5 days if ROAS is positive.

---

## Advanced Tips

1.  **Remarketing Based on Channel Video Engagement**: Create remarketing lists in Google Ads with users who watched 25%, 50%, 75%, or 100% of your YouTube channel videos in the last 30-90 days. Target bottom-of-funnel ads to those who showed high interest.
2.  **Competitor Channel or Niche Influencer Targeting**: Use the `Placements` feature and add URLs of direct competitor YouTube channels or influencers your target audience follows. Your ads will be shown before or during those channels' videos, capturing an already-qualified audience's attention.
3.  **Video Ad Sequencing**: Create a sequence of video ads to guide the user through a journey. For example, first a 6-second Bumper Ad for branding, then a 30-second TrueView In-Stream with the value proposition, and, for those who watched the second, a 15-second In-Stream with a conversion offer.
4.  **Excluding Audiences That Already Converted (Customer Lists)**: Upload an email list of your existing customers to Google Ads and use it as an `exclusion list` in acquisition campaigns. This ensures your budget is spent only on potential new customers.
5.  **YouTube Search Terms Report Analysis**: Although not as robust as in Google Search, YouTube offers insights into the search terms that led users to see your ads (especially in Discovery Ads). Use these terms to refine custom segments and better understand audience intent.
