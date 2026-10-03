---
name: app-install-campaign
description: "App Install Campaign — Specialized skill for app install campaigns"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# App Install Campaign

This skill enables Claude to plan, launch, and optimize app install campaigns across Meta Ads, Google Ads, and TikTok Ads, focused on user acquisition and retention results.

---

## Keywords

App Install Campaign, UAC (Universal App Campaigns), GAC (Google App Campaigns), Meta App Ads, TikTok App Install, Mobile Measurement Partner (MMP), Deep Linking, SKAdNetwork, CPI (Cost Per Install), ROAS, Post-Install Events, Bid Optimization, Mobile Attribution, ASO (App Store Optimization).

---

## Quick Start

1.  **Set up an MMP and SDKs**: Install and configure a Mobile Measurement Partner (MMP) such as AppsFlyer, Adjust, or Branch, making sure the SDK is integrated into the app and sending `App Install` and `App Open` events (minimum) to the ad platforms.
2.  **Create a Meta Ads Campaign**: Launch a campaign in Meta Ads Manager with the `App Installs` objective, using vertical video and image creatives.
3.  **Launch a Google App Campaign (GAC)**: Set up a Google App Campaign focused on `App installs`, providing the maximum number of text, image, and video assets.
4.  **Initial Monitoring**: Track Cost Per Install (CPI) and install volume during the first 48-72 hours post-launch, adjusting budgets if volume is below expectations or CPI is above target.

---

## Core Workflows

### Workflow 1: Launching and Optimizing an App Install Campaign on Meta Ads

This workflow details how to build and optimize a Meta Ads campaign focused on installs and post-install events.

1.  **Verify the Data Source and SDK**:
    *   **Action**: Confirm the Facebook SDK (or MMP integration) is implemented and sending app conversion events to Events Manager.
    *   **Example**: Go to Events Manager > Data Sources > App SDK. Verify that `fb_mobile_activate_app` (install), `fb_mobile_app_open` (first open) and, where applicable, value events like `fb_mobile_purchase` or `fb_mobile_complete_registration` are being received actively.
    *   **Why it matters**: Without accurate data, campaign optimization will be compromised.
2.  **Campaign Structure in Ads Manager**:
    *   **Setup**: Start a new campaign.
    *   **Objective**: Select `App Installs` for the initial acquisition phase, or `App Events` if the primary goal is to optimize for valuable in-app actions (e.g., purchase, registration).
    *   **Budget**: Set a daily or lifetime budget.
        *   **Example**: $350/day budget.
    *   **Ad Set - Delivery Optimization**:
        *   For `App Installs`: Keep optimization set to `App Installs`.
        *   For `App Events`: Choose the highest-value event (e.g., `Complete Registration`, `In-App Purchase`).
    *   **Ad Set - Target Audience**:
        *   **Action**: Build specific audiences to maximize qualified user acquisition.
        *   **Example**:
            *   `1% Lookalike of Recent Buyers (last 30 days)`: Uses a customer list of people who purchased in the app.
            *   `Interests`: Target interests in `[App Category] Apps`, `Direct Competitors`, or `Mobile Technology`.
            *   `Broad Audience`: For apps with large data volume, test an audience with no detailed targeting (age, gender, location) and let Meta's algorithm find the users most likely to install.
    *   **Ad Set - Placements**:
        *   **Recommendation**: Use `Advantage+ Placements` (automatic) to let the algorithm distribute ads where conversion is most likely.
    *   **Ads - Creatives and Call to Action (CTA)**:
        *   **Action**: Develop creatives that clearly demonstrate the app's value.
        *   **Example**: Short videos (15-30 seconds) showing the app interface in use, carousels with the main features, and high-quality static images.
        *   **CTA**: Use `Install Now`, `Download App`, or `Open App` (for re-engagement).
3.  **Ongoing Monitoring and Optimization**:
    *   **Action**: Track key metrics and make adjustments.
    *   **Example**: If CPI is high, test new creatives or refine the audience. If ROAS D7 (7 days post-install) is low, shift optimization to a higher-value event or lower the max bid. Review creative reports to pause underperformers and scale the winners.

### Workflow 2: Optimizing Google App Campaigns (GAC) for ROAS and Post-Install Events

This workflow focuses on how to set up and optimize app campaigns in Google Ads to maximize return on ad spend.

1.  **Google Analytics 4 (GA4) Integration and Conversion Events**:
    *   **Action**: Ensure Google Analytics 4 is set up in the app and that relevant conversion events (e.g., `first_open`, `in_app_purchase`, `subscription_start`, `ad_impression`) are being sent to Google Ads.
    *   **Example**: In Google Ads, go to `Tools and Settings` > `Measurement` > `Conversions`. Verify that GA4 events are imported and marked as "Primary" for bidding.
    *   **Why it matters**: GAC depends heavily on this data for machine-learning-based optimization.
2.  **Google App Campaign Structure**:
    *   **Campaign Type**: Select `App`.
    *   **Subtype**:
        *   `App installs`: To maximize install volume.
        *   `App conversion value`: Essential for ROAS optimization, focused on purchase or subscription events.
        *   `App engagement`: To reactivate existing users or drive actions from active users.
    *   **Bidding and Budget**:
        *   **ROAS Optimization**: Set a `Target ROAS` (tROAS).
            *   **Example**: $600/day budget with a 250% tROAS.
        *   **Event Optimization**: If ROAS doesn't have enough data yet, use `Target CPA` (tCPA) for an intermediate value event (e.g., `Registration Complete`).
            *   **Example**: $400/day budget with a $15.00 tCPA for `Complete Registration`.
    *   **Ad Assets**:
        *   **Action**: Provide a wide variety of creative assets for Google to test and optimize.
        *   **Example**:
            *   **Headlines (up to 30)**: "#1 [Category] App", "Exclusive Discounts", "Manage Your Finances the Easy Way".
            *   **Descriptions (up to 20)**: "Thousands of products, fast delivery", "Save time and money on your everyday shopping".
            *   **Images (up to 20)**: Screenshots of the app interface, lifestyle images representing app usage.
            *   **Videos (up to 20)**: Feature demos, testimonials, short animations.
3.  **Performance Analysis and Adjustments**:
    *   **Asset Reports**: Monitor the performance of each asset (headlines, descriptions, images, videos) in the campaign's asset report.
    *   **Action**: Pause assets rated "Low" and replace them with new variations.
    *   **Example**: If a headline like "Download Free!" underperforms, test "Start Saving Today!".
    *   **Bid Adjustments**: If tROAS isn't being hit after a learning period (typically 7-14 days), adjust the tROAS up or down in 10-20% increments.
    *   **Event Monitoring**: Regularly verify that conversion events are being attributed correctly and that post-install event volume is growing.

---

## Templates

### Creative Briefing Template for App Install (Meta/TikTok)

```
Campaign Title: [App Name] App Launch - Summer 2025
Primary Objective: Increase Installs and Activations (First Login)
Platforms: Meta Ads (Facebook/Instagram), TikTok Ads
Target Audience: Smartphone users interested in [App Category, e.g., fitness, casual games, finance], 18-35, United States.
Primary Call-to-Action: Install Now / Download App / Get Started
Key Message: "Transform your routine with [App Name]! [App's Core Benefit] is just one tap away."
Mandatory Visual Elements:
  - App logo always visible (top/bottom corner)
  - Clear demo of the app interface in use (real usage scenarios)
  - On-screen text with the core benefit or an offer
  - Brand colors front and center
Optional Elements:
  - Social proof (e.g., "Over 1 million downloads!")
  - Short user testimonials
  - Urgency elements (if there's a promotion)
Desired Formats:
  - Vertical Video (9:16, 15-30s)
  - Square Video (1:1, 10-20s)
  - Carousel (3-5 images/videos, 1:1)
  - Static Image (1:1, 9:16)
Sample Ad Copy:
  - Headline: "[App Name]: Your Personal Trainer in Your Pocket!"
  - Description/Body: "Hit your fitness goals with personalized workouts and daily tracking. Install now and get 7 days free!"
  - On-screen video text: "Work Out at Home. Real Results."
```

### Tracking URL Template (Deep Link) for App Install Campaigns

```
Objective: Track installs accurately and send users to a specific screen inside the app after install.

Deep Link Construction Example (Using an MMP like AppsFlyer/Adjust):

1.  **MMP Base Link (Universal Link/OneLink)**:
    *   URL: https://[your-mmp-subdomain].onelink.me/[MMP_TEMPLATE_ID]
    *   Example: https://myapp.onelink.me/abc12345

2.  **Attribution Parameters (Essential for the MMP to identify the source)**:
    *   `pid`: Media source (e.g., `facebook_int`, `googleadwords_int`, `tiktok_int`)
    *   `c`: Campaign name (e.g., `bf_app_install_campaign_us`)
    *   `af_adset`: Ad set name (e.g., `lookalike_buyers_audience`)
    *   `af_ad`: Ad/creative name (e.g., `main_offer_video_bf`)
    *   `af_channel`: Media channel (e.g., `facebook`, `instagram`, `tiktok`)
    *   `af_siteid`: Placement (e.g., `facebook_mobile_feed`, `tiktok_for_you`)
    *   `af_c_id`: Campaign ID (Meta Ads: `{{campaign.id}}`)
    *   `af_adset_id`: Ad set ID (Meta Ads: `{{adset.id}}`)
    *   `af_ad_id`: Ad ID (Meta Ads: `{{ad.id}}`)

3.  **Deep Linking Parameters (To route the user inside the app)**:
    *   `af_dp`: Your app's URI scheme and desired route (e.g., `myapp://home?tab=bf_offers`)
    *   `af_web_dp`: Web fallback URL in case the app isn't installed or the deep link fails (e.g., `https://www.myapp.com/bf-promo`)
    *   `deep_link_value`: Custom parameter for the app to process (e.g., `black_friday_promo_2024`)

**Final Built URL (Example for Meta Ads with AppsFlyer):**
```
https://myapp.onelink.me/abc12345?pid=facebook_int&c={{campaign.name}}&af_adset={{adset.name}}&af_ad={{ad.name}}&af_channel={{publisher_platform}}&af_siteid={{site_source_name}}&af_dp=myapp://home?tab=bf_offers&af_web_dp=https://www.myapp.com/bf-promo&deep_link_value=black_friday_promo_2024
```
*Note: Meta Ads replaces `{{campaign.name}}`, etc., with the actual campaign values at click time.*
```

---

## Checklist

- [x] MMP (Mobile Measurement Partner) configured and SDKs integrated (e.g., Adjust, AppsFlyer, Branch).
- [x] Post-install events (App Open, Registration, Purchase) mapped and sent correctly to the ad platforms.
- [x] Deep Links configured and tested to ensure correct post-install routing for new and existing users.
- [x] Creatives (videos, images, carousels) optimized for mobile (primarily vertical) with a clear, visible CTA.
- [x] Daily or lifetime budget set based on target CPI, desired volume, and projected LTV.
- [x] Meta Ads campaign configured with the "App Installs" or "App Events" objective (if there's enough data).
- [x] Google App Campaign (GAC) with at least 5 headlines, 5 descriptions, 5 images, and 5 videos uploaded to maximize performance.
- [x] TikTok App Campaign configured with the "App Installs" objective and VCP (Value Cost Per Install) or CPI optimization.
- [x] Daily monitoring of CPI, CVR (Install Conversion Rate), and post-install ROAS (D7, D30).
- [x] Existing-user audience exclusion (where applicable) for new-user acquisition campaigns.
- [x] SKAdNetwork compatibility verified for iOS 14.5+ campaigns and "conversion values" mapped.
- [x] Lookalike audiences built from high-value in-app events.

---

## Reference Metrics

| Metric               | Benchmark (US - Varies by Category) | Target (Example) |
|-----------------------|------------------------------------------|----------------|
| CPI (Android)         | $2.50 - $9.0
