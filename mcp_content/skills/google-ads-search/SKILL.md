---
name: google-ads-search
description: "Google Ads Search — Specialized skill for Google Ads Search"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Google Ads Search

Enables you to plan, implement, and optimize Google Ads Search campaigns focused on performance, return on investment, and growth strategies.

---

## Keywords

Google Ads Search, Search Campaign, Bid Optimization, Keyword Strategy, Responsive Search Ads, Google Ads ROAS, Google Ads CPC, Campaign Structure, Google Ads Negatives, Ad Extensions, Google Ads Experiments, Google Ads Automation, Quality Score, Target CPA.

---

## Quick Start

1.  **Campaign Creation with a Clear Objective**: Start a new Search campaign, selecting "Sales" or "Leads" as the main objective. Set geo-targeting to "United States" and languages to "English" and "Spanish."
2.  **Initial Bidding Strategy**: Choose the "Maximize Conversions" bidding strategy for campaigns with conversion history, or "Maximize Clicks" with a $3.00 manual CPC cap for new campaigns aiming at traffic volume.
3.  **Ad Group Structure**: Create at least 3 ad groups, each focused on a highly specific keyword theme. Example: "Men's Running Shoes Nike," "Men's Running Shoes Adidas," "Women's Running Shoes Asics."
4.  **Responsive Search Ad (RSA) Development**: For each ad group, write 2-3 Responsive Search Ads (RSA) with 10-15 headlines and 3-4 descriptions, making sure the headlines include the group's keywords and clear calls to action (CTAs) like "Buy Now" or "Request a Quote."
5.  **Essential Ad Extension Implementation**: Add sitelink extensions (minimum 4), callout extensions (minimum 4), and structured snippets (minimum 2 types) to enrich the ad and increase visibility.

---

## Core Workflows

### Workflow 1: High-Performance Campaign Structure for E-commerce

This workflow details creating a search campaign focused on maximizing sales for a specific product in an e-commerce store, using best practices for Quality Score and relevance.

1.  **Objective and Budget Definition**:
    *   **Action**: In Google Ads, create a "New Campaign" > "Sales" > "Search." Uncheck "Display Network" and "Search Partners" initially to keep control.
    *   **Example**: Daily budget set at $250.00. "Maximize Conversions" bidding strategy with a $40.00 target CPA, assuming an average conversion value of $200.00. Geo-targeting for the "United States" and languages "English," "Spanish."
2.  **Strategic Keyword Research and Grouping**:
    *   **Action**: Use Google Ads Keyword Planner to identify long-tail and high-volume search terms. Group keywords around very specific themes, preferably following the STAGs concept (Single Theme Ad Groups).
    *   **Example**: For an electronics e-commerce store, an ad group might be "Samsung 55 Inch Smart TV." Keywords: `[samsung 55 inch smart tv]` (exact), `"55 inch samsung smart tv"` (phrase). Add the keywords with bids at $3.50 for exact and $2.80 for phrase.
3.  **High-Relevance Responsive Search Ad (RSA) Creation**:
    *   **Action**: Develop 3 RSAs per ad group. Prioritize headlines (at least 3 pinned in positions 1, 2, or 3) and descriptions containing the group's main keyword, clear product benefits, and strong CTAs.
    *   **Example**: For the "Samsung 55 Inch Smart TV" group:
        *   **Pinned Headlines**: "Samsung 55'' Smart TV" (Position 1), "Buy Now | Fast Shipping" (Position 2).
        *   **Other Headlines**: "Samsung Crystal UHD 4K," "Best Price Guaranteed," "2024 Models," "Watch Your Favorite Movies."
        *   **Descriptions**: "Find the ideal 55-inch Samsung Smart TV. 4K quality and the best apps. Pay in up to 12 installments," "Experience total immersion with Samsung Crystal UHD. Exclusive deals and free shipping nationwide."
4.  **Comprehensive Ad Extension Implementation**:
    *   **Action**: Add relevant ad extensions to increase the space the ad occupies and provide additional information.
    *   **Example**:
        *   **Sitelinks**: "Smart TVs on Sale," "65 Inch Models," "Tech Support," "In-Store Pickup."
        *   **Callouts**: "Fast Shipping," "Up to 12 Interest-Free Installments," "Samsung Warranty," "Best Online Price."
        *   **Structured Snippets**: Types: "Models," Values: "AU8000, BU8000, QN90B."
        *   **Image Extension**: Add high-quality product images.
5.  **Strategic Negative Keyword Addition**:
    *   **Action**: Create a master negative keyword list at campaign level for irrelevant generic terms. Also add specific negatives at ad group level.
    *   **Example**: Campaign-level negatives: "free," "used," "repair," "defect," "jobs," "craigslist." Specific negative for "Samsung 55 Inch Smart TV": "review," "manual," "problems," "repair."

### Workflow 2: Continuous Bid and Budget Optimization in Existing Campaigns

This workflow focuses on refining the performance of active campaigns, adjusting bids and budget based on data to maximize ROAS (Return on Ad Spend) and CPA (Cost per Acquisition).

1.  **Detailed Weekly Performance Analysis**:
    *   **Action**: Open the "Campaigns," "Ad Groups," and "Keywords" reports in Google Ads. Filter by last week's period and compare with the previous week or month. Focus on CTR, CPC, Conversion Rate, Cost/Conv., and Conv. Value/Cost (ROAS).
    *   **Example**: Identify that the "Sport Shoes" campaign had a 15% drop in conversion rate and a 20% increase in CPA, while the "Workout Clothing" campaign maintained a 4.0x ROAS.
2.  **Bid Adjustments by Device, Location, and Time**:
    *   **Action**: In the "Devices," "Locations," and "Ad Schedule" reports, check CPA and ROAS performance. Apply positive or negative bid adjustments.
    *   **Example**: If "Mobile Phones" has a 30% higher CPA than "Computers," apply a -20% bid adjustment for mobile. If "New York" has a ROAS 20% above average, raise the bid by +10% for that location. If conversions between 12am-6am are zero, set a -100% adjustment.
3.  **Smart Budget Allocation**:
    *   **Action**: Based on ROAS and CPA analysis, redirect budget from low-performing campaigns or ad groups to those generating higher return.
    *   **Example**: Lower the "Sport Shoes" campaign's daily budget by $50.00 and increase the "Workout Clothing" campaign's by $50.00, capitalizing on the latter's better performance.
4.  **Keyword and Negative Review and Expansion**:
    *   **Action**: Analyze the "Search Terms" report weekly. Add new relevant terms as keywords (especially long-tail) and irrelevant terms as negative keywords.
    *   **Example**: In the report, the term "running shoes sale free" appeared with 100 clicks and 0 conversions. Add "free" as a campaign-level negative. The term "women's running shoes asics gel-kayano" generated 5 conversions and wasn't an explicit keyword; add it as `[women's running shoes asics gel-kayano]` in a new ad group.
5.  **Strategy A/B Tests (Experiments)**:
    *   **Action**: Use the Google Ads "Experiments" feature to test significant changes without impacting the whole campaign. Test different bidding strategies, new RSAs, or targeting adjustments.
    *   **Example**: Create an experiment to test a $35.00 "Target CPA" against the current "Maximize Conversions" strategy without a target CPA. Split traffic 50/50 and run for 4-6 weeks to gather statistically significant data.

---

## Templates

### Ad Group Structure for a Specific Product (E-commerce)

```
Ad Group Name: Dell G15 Gaming Laptop RTX 3050
Default Final URL: https://www.yoursite.com/dell-g15-gaming-laptop-rtx-3050

Keywords (Exact and Phrase match for more control):
- [dell g15 gaming laptop rtx 3050]
- "dell g15 gaming laptop"
- "dell g15 rtx 3050"
- [dell g15 rtx 3050]

Responsive Search Ads (RSA):
Headline 1: Dell G15 Gaming Laptop (Pinned Position 1)
Headline 2: RTX 3050 | High Performance (Pinned Position 2)
Headline 3: Buy Now | Free Shipping
Headline 4: Dell G15 | Best Prices
Headline 5: Unbeatable Gaming Performance
Headline 6: 2024 Models | Latest Generations
Headline 7: Up to 12 Interest-Free Installments
Headline 8: Full HD 120Hz Screen
Headline 9: Official Dell Warranty
Headline 10: Exclusive Online Deals

Description 1: Get your Dell G15 Gaming Laptop with RTX 3050. Superior performance for your favorite games.
Description 2: Find the Dell G15 with the best configurations and price. Take advantage of our deals and fast shipping.
Description 3: Play smoothly with incredible graphics on the Dell G15. Cutting-edge technology within your reach.

Ad Extensions:
Sitelinks:
- Dell Laptops on Sale
- Gaming Accessories
- Dell Tech Support
- Easy Financing
Callouts:
- Fast US Shipping
- Secure Payment
- Limited Stock
- Exclusive Models
Structured Snippets:
- Types: Processors, Values: Intel Core i5, Intel Core i7
- Types: RAM, Values: 8GB, 16GB
```

### Weekly Google Ads Search Performance Report (Summary)

```
Google Ads Search Performance Report - Week: 07/22/2024 - 07/28/2024
Campaign: E-commerce Women's Fitness Fashion
Total Clicks: 3,120 (+8% vs. previous week)
Impressions: 58,900 (+5% vs. previous week)
CTR: 5.29% (+3% vs. previous week)
Average CPC: $1.98 (-2% vs. previous week)
Total Cost: $6,177.60 (+6% vs. previous week)
Conversions (Purchases): 125 (+15% vs. previous week)
Conversion Rate: 4.01% (+7% vs. previous week)
Average CPA: $49.42 (-8% vs. previous week)
Total Conversion Value: $24,500.00 (+12% vs. previous week)
ROAS: 3.97 (+5% vs. previous week)

Key Insights:
- Overall campaign performance improved significantly, with increased conversions and ROAS, and reduced CPA.
- The "High-Waist Fitness Leggings" ad group posted a 4.5x ROAS and $40.00 CPA, beating the campaign average.
- The search terms report identified "cheap gym clothes" with high click volume but 0 conversions. The term "women's fitness set" generated 10 conversions with good ROAS and wasn't an exact-match keyword.
- Mobile devices contribute 70% of conversions, with a CPA 10% lower than desktop.

Recommended Next Actions:
1.  Increase the "E-commerce Women's Fitness Fashion" campaign budget by 10% ($25/day) to capitalize on the strong performance.
2.  Add "cheap" as a negative keyword at campaign level.
3.  Add `[women's fitness set]` as an exact keyword in the "Fitness Sets" ad group.
4.  Review and test new headlines in the RSAs of the "High-Support Fitness Tops" group to improve CTR, which is slightly below average.
5.  Consider a +5% positive bid adjustment for mobile devices, given the superior performance.
```

---

## Checklist

- [X] Conversion tracking setup validated and working.
- [X] Minimum of 3 Responsive Search Ads (RSA) per ad group, with an Ad Strength of "Good" or "Excellent."
- [X] At least 4 ad extensions (sitelinks, callouts, snippets, calls) configured and approved.
- [X] Robust negative keyword list implemented at campaign and ad group level.
- [X] Search terms report analyzed weekly for new keywords and negatives.
- [X] Bid adjustments by device, location, and time of day applied based on performance data.
- [X] Budget allocated according to the performance and ROAS/CPA of the most effective campaigns.
- [X] Final and tracking URLs working correctly with no 404 errors.
- [X] A/B test (experiment) of bids or creatives running or planned.
- [X] Content exclusion setup in "Settings" > "Content exclusions" to avoid irrelevant impressions (if the Display Network isn't disabled).

---

## Reference Metrics

| Metric            | Benchmark (US E-commerce) | Target (Example) |
|--------------------|-------------------------------|----------------|
| CTR (Search Ads)   | 4.5% - 8.0%                   | > 6.0
