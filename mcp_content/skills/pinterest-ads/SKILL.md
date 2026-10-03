---
name: pinterest-ads
description: "Pinterest Ads — Specialized skill for planning, creating, optimizing, and analyzing ad campaigns on Pinterest."
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Pinterest Ads

This skill enables you to plan, create, optimize, and analyze ad campaigns on Pinterest to drive traffic, engagement, and sales, using the platform's specific features.

---

## Keywords

Pinterest Ads Manager, Pinterest Tag, Shopping Ads, Idea Ads, Collection Ads, Bid Optimization, Pinterest Custom Audiences, Pinterest Lookalikes, Interest Targeting, Pinterest Analytics, Pinterest Retargeting, Pinterest Product Catalog.

---

## Quick Start

1.  **Access Pinterest Ads Manager**: Navigate to `ads.pinterest.com` and log in with your Pinterest business account.
2.  **Start a New Campaign**: Click `Ads` in the top menu, then `Create Campaign` and select the `Consideration (Traffic)` objective to drive visits to your site.
3.  **Configure Budget and Schedule**: Set a `Daily Budget` of $75.00 and an immediate `Start Date`, with no end date.
4.  **Install the Pinterest Tag**: In the campaign panel, locate the `Pinterest Tag` section and enter the Tag ID for event tracking on `www.mystore.com`.

---

## Core Workflows

### Workflow 1: Ecommerce Conversion Campaign Creation and Launch

This workflow details setting up a Pinterest Shopping Ads campaign focused on direct sales, using a synced product catalog.

1.  **Access and Objective**:
    *   In Pinterest Ads Manager, click `Create Campaign`.
    *   Select the `Conversions` objective to optimize the campaign for purchases, add-to-carts, or checkouts.
    *   Name the campaign, e.g.: `Summer Sales Campaign 2025 - Home Decor`.
2.  **Budget and Schedule Configuration**:
    *   Choose `Daily Budget` and set $150.00.
    *   Set the `Start Date` to today and leave no `End Date` for continuous monitoring.
3.  **Ad Group Configuration**:
    *   Name the ad group `Ad Group Retargeting Cart Abandoners`.
    *   Under `Bid Strategy`, select `Automatic Bid` so Pinterest optimizes bids for conversions.
    *   **Target Audience**:
        *   Under `Custom Audiences`, select a previously created audience of `Website Visitors Who Added to Cart in the Last 30 Days`.
        *   For expansion, add a `Buyer Lookalike (Top 5%)` audience based on your existing customers.
        *   Under `Detailed Targeting`, add interests like `Interior Decor`, `Furniture Design`, and `Home Organization` to capture new high-intent users.
        *   Exclude audiences like `Repeat Buyers (Last 7 Days)` to avoid wasting impressions on recent buyers.
    *   **Placements**: Leave `All Placements` enabled to maximize reach.
4.  **Ad Selection and Creation**:
    *   Under `Ad Format`, choose `Shopping Ads`.
    *   **Product Catalog**: Verify the `Product Catalog` is synced and active.
    *   Select the products to advertise. For example, filter by products in the `Rustic Decor` or `Outdoor Furniture` category.
    *   Pinterest will automatically create ads from your products. You can customize the `Pin titles and descriptions` to include CTAs like "Shop Now" or "Discover the Collection."
    *   **Destination URL**: Make sure product destination URLs are correct and point to the specific product pages.
5.  **Review and Publish**:
    *   Review all campaign, ad group, and individual ad settings.
    *   Click `Publish` to launch the campaign.

### Workflow 2: Continuous Optimization of a Blog Post Traffic Campaign

This workflow describes the steps to optimize an existing traffic campaign, aiming to increase qualified clicks to a blog article.

1.  **Initial Monitoring and Key Metrics**:
    *   Open the `Campaigns Dashboard` in Pinterest Ads Manager.
    *   Filter by the campaign `Blog Traffic Trends 2024`.
    *   Monitor `CTR (Click-Through Rate)`, `CPC (Cost per Click)`, and `Outbound Clicks` in the first 7 days. A CTR below 0.8% or a CPC above $2.00 for this campaign type indicates a need for optimization.
2.  **Creative Optimization (Pins)**:
    *   Navigate to the `Ads` tab within the ad group.
    *   Identify the pins with the lowest `CTR`.
    *   Pause the worst 20% of pins.
    *   Create 3-5 new pins with variations in image (e.g.: lifestyle vs. isolated product), text (e.g.: "5 Essential Tips" vs. "Complete Guide"), and call to action (e.g.: "Read More" vs. "Read the Article").
    *   Use vertical images (2:3 ratio, 1000x1500px) with clear overlay text.
3.  **Targeting Refinement**:
    *   Open the `Ad Group` settings.
    *   Under `Detailed Targeting`, analyze the `Interests` and `Keywords` generating clicks but low post-click engagement (high bounce rate in Google Analytics).
    *   Remove interests like `General Decor` and add more specific terms like `Sustainable Decor`, `Home DIY`, or `Interior Architecture` if the article is about more specific niches.
    *   Use the `Search Terms Report` to identify irrelevant keywords and add them as `Negative Keywords`. Example: if the article is about "interior decor," add `party decorations` as a negative.
4.  **Bid and Budget Adjustment**:
    *   If `CPC` is high and `CTR` low, consider lowering the `Maximum Bid` if manual, or adjusting the `Bid Strategy` to `Automatic Bid` with a `Cost per Click` target (if available for the objective).
    *   If the campaign is performing well (high CTR, low CPC), increase the `Daily Budget` by 10-20% every 2-3 days to scale results without destabilizing campaign learning.
5.  **Landing Page A/B Test**:
    *   Create a variation of the blog post's destination page with a different headline or a mobile-optimized layout.
    *   Duplicate the ad group and point the new group to the Landing Page variation.
    *   Monitor `Time on Page` and `Bounce Rate` metrics in Google Analytics to determine which Landing Page version generates more engagement.

---

## Templates

### Pinterest Ads Campaign Structure (Conversion)

```
Campaign: Winter Sales - Women's Fashion (Objective: Conversions)
  Ad Group 1: Cart Abandoner Retargeting (Audience: Visitors Who Added to Cart 30D)
    Ad 1.1: Summer Collection - Floral Dress (Pin ID: 123456789)
    Ad 1.2: Summer Collection - Midi Skirt (Pin ID: 987654321)
  Ad Group 2: Buyer Lookalike - Casual Clothing (Audience: 1% Buyer Lookalike)
    Ad 2.1: Jeans Promotion - New Collection (Pin ID: 112233445)
    Ad 2.2: Women's Blouses - Latest Trends (Pin ID: 554433221)
```

### Pinterest Ad Copy (Shopping Ad - Example)

```
Pin Title: Floral Midi Dress - Perfect for Summer!
Pin Description: Dazzle with the lightness and elegance of our Floral Midi Dress. Made with premium fabric, ideal for any occasion. Click and get yours! #FloralDress #SummerFashion #FeminineStyle #ShopNow
Destination URL: https://www.mystore.com/floral-midi-dress
```

---

## Checklist

- [x] Pinterest Tag installed and verified with conversion events (PageView, AddToCart, Checkout)?
- [x] Product catalog synced, up to date, and error-free in Pinterest Merchant Center?
- [x] Custom audiences (website visitors, pin engagers) created and up to date?
- [x] Lookalike audiences configured for scale (buyers, add-to-cart)?
- [x] Creatives (pins) in vertical format (2:3 or 1000x1500px) at high resolution?
- [x] Pin texts clear, concise, with relevant keywords and an explicit CTA?
- [x] Destination URLs for all ads correct, working, and pointing to optimized pages?
- [x] Daily/total budget aligned with the campaign objective and the product's sales cycle?
- [x] Interest, keyword, and demographic targeting refined for the ideal audience?
- [x] Irrelevant audience exclusion (e.g.: recent repeat customers, internal IPs) applied?
- [x] Campaign metrics monitoring (CTR, CPC, CPA, ROAS) scheduled for regular analysis?
- [x] A/B tests for creatives, audiences, or bids planned for continuous optimization?

---

## Reference Metrics

| Metric               | Benchmark          | Target               |
|-----------------------|--------------------|--------------------|
| CTR (Click-Through Rate) | 0.8% - 1.5%        | > 1.2%             |
| CPC (Cost per Click)  | $0.70 - $2.50  | < $1.80          |
| ROAS (Return on Ad Spend) | 2.0x - 3.5x        | > 2.8x             |
| CPA (Cost per Acquisition)| $30 - $120     | < $80            |
| Conversion Rate      | 1.0% - 2.5%        | > 2.0%             |
| Cost per Mille (CPM) | $15 - $40      | < $30            |

---

## Common Mistakes

1.  **Not Verifying the Pinterest Tag**: Launching conversion campaigns without the tag correctly installed and events verified results in total loss of conversion data and makes effective optimization impossible. **How to avoid it**: After installation, use the `Pinterest Tag Helper` (Chrome extension) and the `Pinterest Ads Manager` itself (in the Tags section) to verify that `PageView`, `AddToCart`, and `Checkout` events are firing correctly on your site before activating the campaign.
2.  **Using Creatives Not Optimized for Pinterest**: Publishing pins with incorrect ratios (e.g.: horizontal 16:9), low resolution, or no clear text overlay. Pinterest is visual; pins that don't stand out in the user feed have very low CTRs. **How to avoid it**: Always use the 2:3 vertical ratio (1000x1500px is ideal) for images and videos. Include concise, legible text over the image with a clear call to action. Test different angles and visual styles that resonate with Pinterest aesthetics (inspiration, DIY, aspiration).
3.  **Targeting Too Broad for Lower-Funnel Objectives**: A conversion campaign targeting only "Broad interests" with no custom audiences or lookalikes, resulting in expensive clicks and low conversion rates. **How to avoid it**: For conversion campaigns (sales), prioritize retargeting audiences (visitors, add-to-cart), lookalikes of existing customers, or keyword targeting with high buying intent. Use broad interests in moderation and only for upper-funnel objectives (awareness, traffic).

---

## Advanced Tips

1.  **Optimization by Product Catalog Attributes**: On Pinterest, you can create ad groups based on specific attributes of your catalog (price, brand, category, stock). **Example**: Create an ad group focused only on products with `Price > $300` and `Category = Premium Footwear`, with a more aggressive bid, since these items usually have a higher profit margin.
2.  **Leverage Idea Pins for Awareness and Qualified Traffic**: Idea Pins (multi-page storytelling format) can be promoted as ads. They're excellent for educating or inspiring. **Example**: Create an Idea Pin promoting "5 Quick Vegan Recipes for Everyday Life" and add an outbound link (deep link) to your full blog post or ingredient product page. Monitor `Engagement` and `Outbound Clicks` to optimize.
3.  **A/B Testing with Pinterest-Specific Landing Pages**: Don't send all traffic to the homepage. Create landing pages optimized specifically for the Pinterest audience, with a more visual design, less text, and a more direct user journey. **Example**: For a "Boho Chic Decor" ad, create an LP with a product carousel in that style, customer testimonials, and a prominent "Shop the Collection" button, instead of a generic category page.
4.  **Specific Pin Engagement Audiences for Retargeting**: Beyond website visitors, create custom audiences of users who saved, commented on, or clicked *specific* pins from your account. **Example**: If you have a viral pin about "Vertical Gardening Ideas," create a `Pin X Engagers` audience and target ads for vertical gardening-related products to them, with a highly relevant message.
5.  **Pinterest Trends Analysis for Content Creation and Targeting**: Use the `Pinterest Trends` tool (trends.pinterest.com) to identify rising search terms. **Example**: If "Japandi Minimalist Decor" is on the rise, create new pins and ads with that theme, using those keywords in the description and targeting. This ensures your content is aligned with what users are already actively searching for on the platform.
