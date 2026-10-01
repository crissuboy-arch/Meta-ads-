---
name: brand-awareness-campaign
description: "Brand Awareness Campaign — Specialized skill for brand awareness campaigns"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Brand Awareness Campaign

This skill enables Claude to architect and execute high-impact Brand Awareness campaigns across Meta Ads, Google Ads, and TikTok Ads, focused on reach, frequency, and brand recall.

---

## Keywords

*   Potential Reach
*   Exposure Frequency
*   Ad Recall
*   Viewable CPM (Cost per 1,000 Viewable Impressions)
*   Meta Brand Awareness
*   Google Display Network
*   TikTok Reach & Frequency
*   Lookalike Audiences
*   Brand Storytelling
*   Brand Lift Study
*   Organic Video Views
*   Creative Engagement

---

## Quick Start

1.  Set up an "Awareness" campaign in Meta Ads, selecting the "Reach" awareness type and targeting 1% Lookalikes of video engagers.
2.  Launch a "Reach" campaign on TikTok Ads, using the "Reach & Frequency" strategy to guarantee high exposure to a broad audience (18-34, major metro areas).
3.  Create ad groups on the Google Display Network focused on "Viewable Impressions," targeting topics like "Beauty & Personal Care" and specific niche influencer channels.
4.  Set a frequency cap of 3-5 impressions per person every 7 days on all platforms to optimize recall without causing fatigue.
5.  Prioritize 15-30 second video creatives that tell a brand story or show the lifestyle associated with the product, instead of direct-response ads.

---

## Core Workflows

### Workflow 1: Structuring and Optimizing a Reach Campaign on Meta Ads and Google Ads

This workflow details the setup and optimization of Brand Awareness campaigns on Meta Ads and Google Ads, focused on maximizing reach and frequency efficiently.

1.  **Meta Ads Campaign Setup (Objective: Awareness)**:
    *   Open Facebook Ads Manager, create a new campaign, and select the "Awareness" objective.
    *   Name the campaign descriptively, e.g., `AW_MyBrand_US_Q4_2024_Awareness`.
    *   At the ad set level, set the awareness type to "Reach" and configure a $180.00/day budget.
    *   **Audiences**: Exclude remarketing audiences (e.g., "Purchases in the last 30 days," "Website visitors in the last 7 days") to ensure the campaign reaches new users. Include a 1% Lookalike based on website visitors from the last 90 days and a detailed interest audience, e.g., "Fitness and wellness," "Healthy eating," and "Adventure travel."
    *   **Placements**: Select "Manual Placements" and uncheck Audience Network to prioritize Facebook/Instagram news feeds and stories, which have greater visibility for the reach objective.
    *   **Optimization and Delivery**: Keep "Reach" as the optimization and set a frequency control of "1 impression every 7 days" per person at the ad set level to maximize breadth without saturating.
    *   **Creatives**: Use 3-5 variations of short videos (15-30 seconds) and high-quality static images that convey the brand's visual identity. Focus on visual storytelling around the brand universe, showing the lifestyle and values. Add clear captions and a soft call to action like "Learn More" or "Visit Our Website" for anyone interested.

2.  **Google Ads Campaign Setup (Display Network - Brand Awareness)**:
    *   Create a new campaign in Google Ads with the "Brand awareness and reach" goal.
    *   Select the "Display Network" campaign type.
    *   **Bidding Strategy**: Choose "Viewable CPM" to pay only for impressions that can actually be seen. Set a viewable CPM bid of $5.00.
    *   **Budget**: Set a $120.00/day budget.
    *   **Targeting**:
        *   **Audiences**: Exclude remarketing audiences. Include "Custom Audiences" segments with direct competitor URLs (e.g., `competitorA.com`, `competitorblog.net`) and broad category search terms (e.g., "best project management software," "sustainable fashion trends"). Add "Affinity Audiences" like "Luxury Shoppers," "Tech Enthusiasts," or "Travel Lovers."
        *   **Content**: Target relevant "Topics" (e.g., "Beauty & personal care," "Technology & electronics," "Travel") and specific "Placements" (e.g., YouTube channels of niche influencers, high-traffic fashion blogs).
    *   **Frequency Caps**: Apply a cap of 4 impressions per user per day to avoid saturation and optimize recall.
    *   **Creatives**: Prepare responsive display ads with multiple images (landscape, square, portrait), logos, and short copy that reinforces the brand message. Make sure the images convey the brand's visual identity consistently and professionally.

### Workflow 2: Content Strategy and Audience Expansion on TikTok Ads

This workflow focuses on creating authentic content and using TikTok Ads' reach tools to build Brand Awareness, leveraging the platform's viral nature.

1.  **Planning Viral-Worthy TikTok Content**:
    *   **Trend Spotting**: Monitor TikTok's "For You" feed and tools like the "TikTok Creative Center" to identify trending songs, audio, and video formats. Example: Popular dance challenges (e.g., "Zoom In/Out Challenge"), quick tutorials (e.g., "30-second recipe"), "day in the life" videos with the brand's product or service integrated.
    *   **Creating Authentic, Native Content**: Produce short videos (10-30 seconds) that feel native to the platform, with humor and authenticity, showing the lifestyle associated with the brand. Avoid overly polished videos that look like traditional commercials. Example: Users demonstrating the product in a fun context, using a popular transition with the brand slogan, or a creative "unboxing."
    *   **Creator Collaborations**: Identify micro and macro influencers whose audience aligns with the brand's target and who already have organic engagement. Negotiate partnerships to co-create content that presents the brand organically. Example: Beauty influencer @BeautyWithJess using the brand's new liquid lipstick in her "Get Ready With Me" tutorial, or gamer @ProPlayerX integrating a new headset into his stream.

2.  **Launching a Reach & Frequency Campaign on TikTok Ads**:
    *   In TikTok Ads Manager, create a new campaign and select the "Reach" objective.
    *   **Buying Type**: Choose "Reach & Frequency" to control how many people are reached and how often ads are shown — ideal for predictability and impact.
    *   **Budget**: Set a total campaign budget, e.g., $7,000.00 over a 10-day period.
    *   **Target Audience**:
        *   **Demographics**: Age (18-34), Gender (All), Location (Major US metros: New York, Los Angeles, Chicago, Houston, Miami).
        *   **Interests**: Select broad categories like "Fashion," "Beauty," "Technology," "Travel," "Food & Beverage" that align with the brand.
        *   **Custom/Lookalike Audiences**: Upload a (hashed) customer email list or create a 1% "Lookalike" audience based on video engagers of the brand's TikTok page.
    *   **Frequency**: Set a frequency cap of "3 impressions per person every 7 days" to optimize recall without causing fatigue.
    *   **Creatives**: Upload 3-4 different videos planned to be native to TikTok, with trending soundtracks and clear captions. Add a simple CTA like "Learn More" or "Visit" that leads to the brand's profile page or a content landing page.

---

## Templates

### Meta Ads Campaign Structure for Brand Awareness

```json
{
  "campaign_name": "AW_MyBrand_US_Q4_2024_Awareness_Videos",
  "objective": "RECOGNITION",
  "buying_type": "AUCTION",
  "daily_budget": 180.00,
  "ad_sets": [
    {
      "ad_set_name": "AW_Lookalike1%_VideoEngagers_ExclPurchases_LifestyleInterest",
      "optimization_goal": "REACH",
      "frequency_cap": {
        "impressions": 1,
        "time_unit": "DAY",
        "time_value": 7
      },
      "targeting": {
        "geo_locations": ["United States"],
        "age_min": 18,
        "age_max": 45,
        "custom_audiences_include": ["LOOKALIKE_VIDEO_ENGAGERS_1PCT_LAST_90_DAYS"],
        "custom_audiences_exclude": ["PURCHASES_LAST_30_DAYS", "WEBSITE_VISITORS_LAST_7_DAYS"],
        "detailed_targeting_interests": ["Sustainable Living", "Outdoor Activities", "Healthy Eating"]
      },
      "placements": ["FACEBOOK_FEED", "INSTAGRAM_FEED", "INSTAGRAM_STORY", "FACEBOOK_STORY"],
      "ads": [
        {
          "ad_name": "AW_Video_Storytelling_MyBrand",
          "creative_type": "VIDEO",
          "media_url": "https://mybrand.com/videos/brandstory_30s.mp4",
          "primary_text": "Discover the #MyBrand universe. Passion and quality in every detail. 🌿",
          "call_to_action": "LEARN_MORE",
          "destination_url": "https://mybrand.com/our-story"
        },
        {
          "ad_name": "AW_Image_BrandValue_Sustainability",
          "creative_type": "IMAGE",
          "media_url": "https://mybrand.com/images/sustainability_square.jpg",
          "primary_text": "Your life, your style, our commitment. MyBrand is synonymous with the future. #MadeForYou",
          "call_to_action": "VISIT_PROFILE",
          "destination_url": "https://instagram.com/mybrand"
        }
      ]
    }
  ]
}
```

### Google Ads Performance Max Asset Group for Brand Awareness

```json
{
  "asset_group_name": "AW_ProductivitySoftware_Q4_2024
