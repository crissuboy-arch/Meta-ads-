---
name: local-ads-strategy
description: "Local Ads Strategy — Specialized skill for local ads strategy"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Local Ads Strategy

This skill enables you to develop, launch, and optimize highly targeted local ad campaigns on platforms like Meta Ads, Google Ads, and TikTok Ads, maximizing return on investment for brick-and-mortar businesses.

---

## Keywords

Local ads, Local Meta Ads, Google Business Profile Ads, Physical store traffic, Advanced geotargeting, Local reach campaigns, Local CPA optimization, In-store sales ROAS, TikTok Local Ads, Proximity audiences, Google Ads location assets, Local Performance Max.

---

## Quick Start

1.  **GBP Optimization**: Make sure the Google Business Profile is 100% filled out, verified, and stocked with high-quality photos, including business hours and phone number.
2.  **Local Performance Max Campaign**: Launch a Performance Max campaign in Google Ads with the "Store visits and local promotions" goal, linking the GBP and adding location assets.
3.  **Meta Ads Reach Campaign**: Set up a "Store Traffic" campaign in Meta Ads, targeting a 2-5 mile radius around the physical address with offer creatives.
4.  **Basic Tracking**: Enable call and directions request tracking in Google Ads and monitor Cost Per Store Visit (CPSV) in Meta Ads as primary metrics.

---

## Core Workflows

### Workflow 1: Local Customer Acquisition with Meta Ads

This workflow focuses on attracting new customers to a physical establishment through targeted campaigns on Facebook and Instagram.

1.  **Campaign Structure**: Create a new campaign in Meta Ads Manager.
    *   **Objective**: Select "Store Traffic" for multi-location businesses, or "Conversions" if the pixel is configured to record store visits via location data, or if the objective is local booking form submissions.
    *   **Budget**: Start with a daily budget of $50-$100 (example for a small business). Use CBO (Campaign Budget Optimization) so Meta distributes the budget among the best-performing ad sets.
2.  **Ad Set Configuration**:
    *   **Location**: Define the targeting radius. For a restaurant in a busy neighborhood, a 2-3 mile radius is ideal. For a specialized service, expand to 5-6 miles, excluding low-density or irrelevant areas. Example: "5th Avenue, New York" with a 2.5-mile radius.
    *   **Age and Gender**: Adjust to the ideal customer profile. E.g.: Premium beauty salon -> Women, 28-55. Neighborhood gym -> All, 18-45.
    *   **Detailed Targeting**: Add relevant interests that complement the geo targeting without restricting too much. E.g.: For a café, include "Coffee," "Bakery," "Foodie," "Small business." Use custom audiences from Facebook/Instagram page engagement.
    *   **Placements**: Select manual placements, prioritizing Facebook Feed, Instagram Feed, Stories, and Reels. Disable Audience Network and Messenger for quality control.
3.  **Creative Creation**:
    *   **Format**: Short videos (15-30 seconds) showing the space, product, or service in action, or high-quality images with real people interacting.
    *   **Content**: Highlight exclusive offers for local customers (E.g.: "15% off for [Neighborhood] residents!"), special hours, or a differentiator that encourages an immediate visit. Include recognizable visual elements from the area.
    *   **Call-to-Action (CTA)**: "Get Directions," "Book Now," "Call Now," "Learn More" (pointing to a local landing page).
4.  **Monitoring and Optimization**:
    *   Track Cost Per Store Visit (CPSV) if configured, or Cost Per Click on the "Get Directions" CTA.
    *   Run A/B tests with different offers, creatives, or CTAs.
    *   Adjust the targeting radius if frequency is too high or reach too low.

### Workflow 2: Local Visibility Optimization with Google Ads (Performance Max)

This workflow aims to maximize a physical business's presence across Google properties (Search, Maps, YouTube, Display, Discover, Gmail) for users in geographic proximity.

1.  **Initial Setup**:
    *   **Link GBP**: It's essential to link the verified Google Business Profile to the Google Ads account.
    *   **Campaign Objective**: Create a new Performance Max campaign, selecting "Store visits and local promotions" as the main goal.
    *   **Budget**: Set an initial daily budget of $70-$150, depending on local competitiveness.
    *   **Bid Strategy**: Use "Maximize conversion value" or "Maximize conversions," assigning values for calls and store visits.
2.  **Asset Group Configuration**:
    *   **Text Assets**:
        *   **Headlines**: Write catchy headlines including the business name, service/product, and location. E.g.: "Artisan Burgers in Brooklyn," "Best Beauty Salon in Manhattan," "Fast Delivery in Queens."
        *   **Descriptions**: Detail local differentiators, promotions, and benefits. E.g.: "Try the best burger with homemade brioche buns. Near Grand Central Station," "Specialized team and exclusive atmosphere. Book your appointment!"
    *   **Image and Video Assets**:
        *   **Images**: Upload 5-10 high-resolution images of the establishment's exterior and interior, products, team, and customers. Images sized 1200x628 and 1200x1200 are crucial.
        *   **Videos**: Include at least one 15-30 second video showing the space, customer testimonials, or a service process.
    *   **Audience Signals**: Provide Google with target audience information to guide the AI.
        *   **Customer Lists**: Upload existing customer lists (emails, phones) so Google can find similar profiles.
        *   **Interests**: Add relevant interests and demographics. E.g.: "Japanese food," "Spa," "Automotive services."
3.  **Ad Assets**:
    *   **Location Assets**: Make sure they're active and linked to the GBP.
    *   **Call Assets**: Let users call the business directly.
    *   **Callout Assets**: Add phrases like "Premium Service," "Free Parking," "Free Wi-Fi."
4.  **Monitoring and Optimization**:
    *   Track metrics like direct calls, directions requests, website clicks, and store visits (if configured).
    *   Analyze Performance Max "Insights" reports to understand which assets and channels generate the best results.
    *   Adjust budget and conversion values based on performance.

---

## Templates

### Meta Ads Template for a Local Offer

```
Headline: [Store Name] - Your Exclusive Offer in [Neighborhood/City]!
Primary Text: Don't miss out! [Product/Service] with [Discount/Benefit] *for local customers only*. Valid until [Date]. Visit us at [Address] or click to learn more!
Link Description: [Brief detail of the offer and location]
Call-to-Action: Get Directions / Book Now / Call Now / Learn More
Destination URL: [Link to Local Landing Page/Google Business Profile]

Filled Example:
Headline: Delight Bakery - Your Fresh Breakfast in Brooklyn!
Primary Text: Fresh out of the oven! Warm cheese bread + drip coffee for $9.90 *exclusive for Brooklyn neighbors*. Valid until 06/30. Come visit us at 1234 Atlantic Avenue!
Link Description: Complete breakfast in Brooklyn!
Call-to-Action: Get Directions
Destination URL: https://g.page/delightbakery?share
```

### Text Assets Template for Google Ads Performance Max (Local Segment)

```
Headlines (Minimum 5, ideal 15):
1. [Service/Product] in [City/Neighborhood]
2. [Your Business] Is [Local Differentiator]
3. Best [Service/Product] Near You
4. Exclusive Offer for [City/Neighborhood]
5. Visit Our [Business Type] at [Short Address]

Descriptions (Minimum 3, ideal 5):
1. [Differentiator 1] + [Differentiator 2]. Come meet us in [Neighborhood/City]!
2. Guaranteed [Adjective] experience. We're waiting for you!
3. Prime location and personalized service.
4. Special discounts for the [Neighborhood/City] community.

Filled Example:
Headlines:
1. Manicure and Pedicure in Brooklyn
2. Lux Salon Brooklyn Is the Nail Reference
3. Best Nail Salon Near You
4. 15% Off for Brooklyn Residents
5. Lux Salon Brooklyn at 2000 Atlantic Avenue

Descriptions:
1. Flawless nails and a relaxing atmosphere. Come visit us in Brooklyn!
2. Guaranteed beauty experience with premium products. We're waiting for you!
3. Prime location next to the Brooklyn Mall and personalized service.
4. Special discounts Tuesday through Thursday for the Brooklyn community.
```

---

## Checklist

-   [ ] Google Business Profile (GBP) fully filled out and verified.
-   [ ] Location and affiliate location assets active in Google Ads, linked to the GBP.
-   [ ] Geolocation radius set for maximum relevance (2-5 miles), with irrelevant areas excluded.
-   [ ] Ad creatives containing visual elements of the location and exclusive regional offers.
-   [ ] Call and directions request tracking configured as primary conversions in Google Ads.
-   [ ] Meta Ads campaigns configured with "Store Traffic" or "Conversions" objective (with in-store visit pixel).
-   [ ] A/B test of different offers, CTAs, and creative formats with local appeal.
-   [ ] Use of custom audiences (existing customers, page engagement) or Lookalike Audiences in Meta Ads.
-   [ ] Facebook pixel and Google Ads conversion tag integration on the website or landing page (if applicable).
-   [ ] Landing page load speed review for mobile devices.

---

## Reference Metrics

| Metric                 | Benchmark (Local Businesses) | Target (Example) |
| :---------------------- | :-------------------------- | :------------- |
| CTR (Google Search Ads) | 3.5% - 7%                   | > 5.5%         |
| Average CPC (Google Ads)  | $2.80 - $7.50             | < $4.50       |
| Cost per Call       | $18 - $45           | < $30      |
| Cost per Store Visit | $25 - $70           | < $40      |
| ROAS (Offline Sales)   | 2.5:1 - 6:1                 | > 3.5:1        |
| Conversion Rate (Call) | 6% - 18%                    | > 10%          |

---

## Common Mistakes

1.  **Geotargeting too broad or too restrictive**: Targeting an entire city for a neighborhood business dilutes the budget and impact. Targeting only half a mile for a specialized service can unnecessarily limit reach.
    *   **How to avoid it**: Start with a 2-3 mile radius for retail businesses or everyday services, gradually adjusting based on reach, impressions, and click data. Use location exclusion options to remove irrelevant or low-density areas inside the radius. Example: For a pet shop in Brooklyn, start with 2.5 miles and exclude commercial areas that aren't residential.

2.  **Generic creatives with no local appeal**: Using stock images or videos that don't reflect the business's storefront, interior, or community. This fails to create a connection with the local audience.
    *   **How to avoid it**: Produce ads with real photos and videos of the establishment, team, and local customers interacting. Include mentions of nearby landmarks, neighborhood names, or local events in the copy and captions. Example: Instead of "Best Coffee," use "Try the best coffee on Atlantic Avenue, near Prospect Park!"

3.  **Not linking the Google Business Profile (GBP) in Google Ads**: This is a critical error that prevents location assets from showing and store visit data from being used for bid optimization.
    *   **How to avoid it**: Always verify and connect the verified GBP profile to the Google Ads account before creating any local campaign, especially Performance Max campaigns and search campaigns focused on physical store traffic. This ensures address, phone, and hours are displayed correctly and store visits are measured.

---

## Advanced Tips

1.  **Localized Ad Scheduling Optimization**: Analyze demand peaks for your business type in the local context (e.g.: restaurants before lunch/dinner, gyms in the early morning/late afternoon) and adjust ad schedules to concentrate the budget in those periods. E.g.: A pizzeria can disable ads from 12 a.m. to 5 p.m., activating them only for the dinner peak.

2.  **Proximity Retargeting Campaigns**: Create custom audiences in Meta Ads based on people who were physically near your establishment in the last 30-90 days (using app location data, if available and consented, or through data partners). Target these audiences with return offers or reminders.

3.  **First-Party Data Leverage**: Import email and phone lists of existing local customers into the ad platforms (Meta Ads, Google Ads). Use these lists to create Lookalike Audiences highly targeted within your geographic area, expanding reach to profiles with a high conversion probability.

4.  **Community and Seasonal Event Integration**: Develop specific local ad campaigns to coincide with community events, local holidays, or seasonal promotions. Use creatives that directly mention the event or season, creating a sense of opportunity and belonging. E.g.: "Special discount for neighborhood day in [Neighborhood Name]!" or "Easter promotion, come get your artisanal chocolate!"

5.  **A/B Testing Local Scarcity and Urgency Triggers**: Experiment with creatives incorporating scarcity or urgency triggers with a local touch. Phrases like "Last spots for [Neighborhood] residents!", "Offer valid this week only for our community!", or "Few units left at the [Address] store" can significantly increase click and conversion rates for physical businesses.
