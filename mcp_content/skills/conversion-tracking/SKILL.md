---
name: conversion-tracking
description: "Conversion Tracking — Specialized skill for setting up, validating, and optimizing conversion tracking on ad platforms like Meta Ads, Google Ads, and TikTok Ads."
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Conversion Tracking

This skill enables you to set up, validate, and troubleshoot conversion tracking on Meta Ads, Google Ads, and TikTok Ads to optimize performance campaigns and maximize return on ad spend.

---

## Keywords

Meta Pixel, Google Ads Tag, Conversions API, GTM Server-Side, Custom Events, Google Analytics 4, Google Ads Goals, TikTok Pixel, Event Deduplication, Conversion Attribution, ROAS, Cost Per Acquisition (CPA), Standard Events, Enhanced Conversions.

---

## Quick Start

1.  **Install Google Tag Manager (GTM)**: Add the GTM snippets to the `<head>` and `<body>` of every page of the site, right after the opening tags.
2.  **Set Up Base Pixels/Tags**: Add the Meta Ads Pixel and the Google Ads Tag (GA4 config ID or Google tag) in GTM with an `All Pages` trigger.
3.  **Implement Essential Conversion Events**: Set up events like `Purchase`, `Lead`, or `AddToCart` in GTM, using Data Layer variables to capture dynamic values like `value` and `currency`.
4.  **Test and Validate Events**: Use the Meta Pixel Helper, Google Tag Assistant, and the "Test Events" tool in Facebook Events Manager to verify correct firing and data reception.
5.  **Enable the Meta Ads Conversions API (CAPI)**: Integrate CAPI via GTM Server-Side or directly in the backend, ensuring event deduplication with the same `event_id` as the browser Pixel.

---

## Core Workflows

### Workflow 1: Implementing and Validating a Purchase Event for E-commerce (Meta Ads & Google Ads via GTM)

This workflow details a robust purchase event setup, essential for e-commerce, using Google Tag Manager for Meta Ads and Google Ads.

1.  **Prepare Google Tag Manager (GTM)**:
    *   Make sure the GTM snippet is installed correctly in the `head` and `body` of *every* page of the site.
    *   Verify the Data Layer is active and ready to receive e-commerce data on the purchase confirmation page.

2.  **Set Up the Meta Ads Base Pixel in GTM**:
    *   In GTM, create a new Tag of type `Meta Pixel`.
    *   Enter your Meta Pixel ID (E.g.: `123456789012345`).
    *   Set the Standard Event to `PageView`.
    *   Set the Trigger: `Initialization - All Pages` or `Consent Initialization - All Pages` (if using consent management).

3.  **Set Up the Base Google Ads Tag (or GA4) in GTM**:
    *   In GTM, create a new Tag of type `Google Tag` (GA4 config ID or Google Ads).
    *   Enter your Google Tag ID (E.g.: `G-ABCDEFG123` for GA4 or `AW-123456789` for Google Ads).
    *   Set the Trigger: `Initialization - All Pages`.

4.  **Set Up the Purchase Event (`Purchase`) for Meta Ads via GTM**:
    *   In GTM, create a new Tag of type `Meta Pixel`.
    *   Enter the same Meta Pixel ID (`123456789012345`).
    *   Set the Standard Event: `Purchase`.
    *   **Set Custom Parameters:**
        *   `value`: Create a Data Layer variable (E.g.: `ecommerce.purchase.value`) that captures the total purchase value.
        *   `currency`: Create a Data Layer variable (E.g.: `ecommerce.purchase.currency`) that captures the transaction currency (E.g.: `USD`).
        *   `content_ids`: Data Layer variable for product IDs (E.g.: `ecommerce.purchase.items.map(item => item.item_id)`).
        *   `content_type`: `product`.
    *   **Set the Trigger:** Create a `Custom Event` trigger with Event Name `purchase` (this event must be pushed to the Data Layer on the purchase confirmation page, E.g.: `dataLayer.push({event: 'purchase', ...})`).

5.  **Set Up the Purchase Event for Google Ads via GTM (Specific Conversion)**:
    *   In GTM, create a new Tag of type `Google Ads Conversion Tracking`.
    *   Enter the Google Ads Conversion ID (E.g.: `AW-123456789`).
    *   Enter the Google Ads Conversion Label (E.g.: `AbCdEfGhIjkLmnOpQrStUv`).
    *   **Set Conversion Value**:
        *   Select `Use a different value for each conversion`.
        *   `Value` field: Use the same Data Layer variable `ecommerce.purchase.value`.
        *   `Currency` field: Use the same Data Layer variable `ecommerce.purchase.currency`.
    *   **Set the Trigger:** Use the same `Custom Event` `purchase` trigger created earlier.

6.  **Publish the Changes in GTM**: Submit the GTM container changes to the production environment.

7.  **Test and Validate the Events**:
    *   Open the site in GTM's `Preview` mode.
    *   Simulate a complete purchase.
    *   Check in the GTM debug console whether the `Meta Pixel - Purchase` and `Google Ads Conversion Tracking` Tags fired on the `purchase` event with the correct parameters.
    *   Use the **Meta Pixel Helper** (Chrome extension) to verify Meta Ads events.
    *   Use the **Google Tag Assistant** (Chrome extension) to verify Google Ads events.
    *   In **Facebook Events Manager**, open the "Test Events" section and verify receipt of the `Purchase` event.
    *   In **Google Ads**, check the "Tag Diagnostics" or "Conversion Summary" section to confirm receipt.

### Workflow 2: Implementing the Meta Conversions API (CAPI) for Deduplication and Resilience

This workflow focuses on implementing the Meta Conversions API (CAPI) to ensure more accurate and resilient tracking, complementing the browser Pixel and preventing data loss.

1.  **Understand CAPI and Deduplication**:
    *   CAPI lets you send conversion events directly from the server to Meta, bypassing ad blockers and browser loading issues.
    *   To avoid double counting, it's crucial to send an *identical* `event_id` for the same conversion event, from both the browser Pixel and CAPI. Meta Ads Manager will deduplicate automatically based on this ID.

2.  **Choose the Implementation Method**:
    *   **GTM Server-Side**: Recommended for most cases, since it centralizes control and lets you transform data before sending it.
    *   **Direct Backend Integration**: Requires development and maintenance by an engineering team.

3.  **Setup via GTM Server-Side (Purchase Event Example)**:
    *   **Create a Server-Side Container in GTM**: In the GTM interface, create a new container of type `Server`.
    *   **Provision a Tag Server**: Set up a tag server (E.g.: Google Cloud Run, App Engine) and link it to the GTM Server-Side container.
    *   **Send Browser Data to the Server-Side Container**:
        *   Modify the Google Ads Tag (or GA4) in Client-Side GTM to send data to your new tag server. In the `Google Tag` (GA4 config tag), add the `server_container_url` parameter with your tag server URL (E.g.: `https://gtm.yoursite.com`).
        *   For Meta Pixel events, you can use a Custom HTML Tag in Client-Side GTM to send the data to the tag server via a custom endpoint, or rely on the Google Tag already sending the necessary data that will be intercepted on the server.
    *   **In the GTM Server-Side Container**:
        *   **Client**: Set up a `Client` (E.g.: `GA4` or `Universal Analytics`) to receive the data sent from the browser.
        *   **Facebook Conversions API Tag**:
            *   Create a new Tag of type `Facebook Conversions API` (available in the Community Template Gallery).
            *   Enter your Meta Pixel ID (`123456789012345`) and the Conversions API Access Token (generated in Facebook Events Manager > Settings > Conversions API).
            *   **Map Event Parameters**:
                *   `Event Name`: Map to the received event name (E.g.: `{{Event Name}}` from the GA4 client).
                *   `Event Time`: `{{Event Time}}`.
                *   `Event ID`: **CRUCIAL for deduplication**. This must be the same `event_id` generated and sent by the browser Pixel. Typically, you'll need to capture the browser's `_fbc` and `_fbp` and use a variable to generate a consistent `event_id`, or pass it explicitly via the Data Layer. A common approach is an `event_id` that combines the `transaction_id` with a timestamp or a GUID generated in the browser and passed to the server.
                *   `User Data`: Map user data (SHA256-hashed email, phone, `fbp`, `fbc`). E.g.: `user_data.em` (hashed email), `user_data.ph` (hashed phone), `user_data.fbp` (`_fbp` cookie variable from the browser), `user_data.fbc` (`_fbc` cookie variable from the browser).
                *   `Custom Data`: Map `value` and `currency` of the purchase event (E.g.: `custom_data.value`, `custom_data.currency`).

    *   **Set the Trigger Server-Side**: Create a trigger for the CAPI Tag that reacts to the events you want to send (E.g.: `Custom Event` with `event_name` `purchase`).

4.  **Test and Validate Deduplication**:
    *   After publishing the changes in both Client-Side and Server-Side GTM, simulate a purchase.
    *   In **Facebook Events Manager**, go to the "Test Events" section.
    *   You should see the `Purchase` events arriving twice (one from the browser and one from the Conversions API), but the status should show "Deduplicated" for one of them. This confirms CAPI is working and the `event_id` is correct.

---

## Templates

### Purchase Event Data Layer (E-commerce Example)

This is an example of how the `dataLayer.push` should be formatted on the purchase confirmation page to send detailed transaction data, which will be captured by GTM.

```javascript
window.dataLayer = window.dataLayer || [];
dataLayer.push({
  event: "purchase",
  ecommerce: {
    transaction_id: "ORDER-123456789", // Unique transaction ID
    value: 149.90, // Total purchase value
    currency: "USD", // Transaction currency
    shipping: 15.00, // Shipping cost
    tax: 0.00, // Taxes
    coupon: "DISCOUNT10", // Coupon code, if any
    items: [
      {
        item_id: "PROD-SKU001",
        item_name: "Premium Cotton T-Shirt",
        item_category: "Apparel",
        item_variant: "Navy Blue - L",
        price: 99.90,
        quantity: 1
      },
      {
        item_id: "PROD-SKU002",
        item_name: "Adjustable Sports Cap",
        item_category: "Accessories",
        item_variant: "Black",
        price: 50.00,
        quantity: 1
      }
    ]
  },
  // Optional: User data for Enhanced Conversions (Google Ads) or CAPI (Meta Ads)
  user_data: {
    email: "user@email.com", // Send SHA256-hashed email in production
    phone_number: "+12125551234" // Send SHA256-hashed phone in production
  }
});
```

### Google Ads Conversion Setup (Interface)

This template reflects the typical settings when creating a new conversion action manually in the Google Ads interface for a `Lead` or `Purchase` event.

```
Conversion Name: Lead - Commercial Contact
Category: Lead
Value: Use the same value for each conversion ($50.00)
Count: One (recommended for leads)
Click Conversion Window: 30 days
Engaged-View Conversion Window: 3 days
View-Through Conversion Window: 1 day
Attribution Model: Data-driven (recommended)
Include in "Conversions": Yes
```

---

## Checklist

-   [x] Meta Ads Pixel (Base `PageView`) installed via GTM on all pages.
-   [x] Google Ads Tag (Base `config` or GA4) installed via GTM on all pages.
-   [x] Primary conversion events (E.g.: `Purchase`, `Lead`, `CompleteRegistration`) set up in GTM with dynamic parameters (`value`, `currency`, `content_ids`).
-   [x] Meta standard events and Google Ads goals created and mapped to GTM events.
-   [x] Meta Ads Conversions API (CAPI) implemented (GTM Server-Side or backend) for deduplication.
-   [x] `event_id` configured and validated to ensure correct deduplication between Pixel and CAPI.
-   [x] Google Analytics 4 set up to receive e-commerce and lead events for analysis.
-   [x] Full event testing performed with the Meta Pixel Helper, Google Tag Assistant, and the Events Manager "Test Events" tool.
-   [x] Tag/pixel diagnostics free of critical errors or warnings on the ad platforms.
-   [x] Attribution window settings reviewed and aligned with the sales cycle (e.g.: 7-day click, 1-day view).
-   [x] Enhanced Conversions (Google Ads) implemented to improve tracking accuracy.
-   [x] TikTok Ads event prioritization configured for campaign optimization.

---

## Reference Metrics

| Metric               | Benchmark (E-commerce) | Benchmark (Lead Gen) |
|-----------------------|------------------------|------------------------------|
| ROAS (Return on Ad Spend) | 3.0x - 5.0x            | N/A                          |
| CPA (Cost per Acquisition) | $30 - $150         | $15 - $50                |
| Conversion Rate (CR) | 1.0% - 3.0%            | 5.0% - 15.0%                 |
| CTR (Click-Through Rate) | 1.5% - 3.5%            | 0.8% - 2.0%                  |
| CPC (Cost per Click) | $0.80 - $2.50      | $1.50 - $4.00            |
| Frequency (Meta Ads) | 1.8 - 3.5              | 1.5 - 2.5                    |

---

## Common Mistakes

1.  **Failed Deduplication in the Conversions API**: The `event_id` sent via CAPI doesn't match the `event_id` generated by the browser Pixel for the same event. This results in duplicate conversions in Events Manager.
    *   **How to avoid it**: Make sure the `event_id` is generated consistently and uniquely for each conversion event and that *exactly* the same ID is passed to both the browser Pixel (via Data Layer or a GTM variable) and the CAPI call (whether via GTM Server-Side or direct integration). E.g.: Instead of generating a new GUID on the server, use the `_fbc` or the `transaction_id` with a timestamp as the basis for a consistent `event_id`.

2.  **Events Missing Essential Dynamic Parameters**: `Purchase` or `Lead` events fire, but crucial parameters like `value`, `currency`, or `content_ids` are missing. This prevents value-based optimization and dynamic audience creation.
    *   **How to avoid it**: Always configure conversion events in GTM to capture and send all relevant Data Layer parameters. For `Purchase`, `value` and `currency` are required. For `Lead`, even if it's a fixed value, assign one to enable value-based optimization. E.g.: A `Lead` event can have `value: 25.00, currency: "USD"`.

3.  **Pixel/Tag Conflicts or Incorrect Firing**: Multiple pixels or conversion tags of the same type fire on the same page, or an event fires in the wrong place (E.g.: `Purchase` firing on `AddToCart`). This causes inflated data and erroneous optimization.
    *   **How to avoid it**: Use GTM to centralize and control tag firing. Create highly specific triggers for each event. Review trigger conditions (`Page Path`, `Event Name`, `URL`) to ensure each tag fires only when and where it should. E.g.: The `Purchase` trigger should be `Page Path` contains `/order-confirmation` AND `Event` is `purchase`.

---

## Advanced Tips

1.  **Conversion Value Optimization (CVO)**: For e-commerce, set campaigns to optimize for conversion value (ROAS). Make sure your `Purchase` events send the correct `value` and `currency`. This lets ad platforms target users with a higher propensity to spend more, not just to convert. E.g.: In Meta Ads, select "Value" as your optimization goal for sales campaigns.

2.  **Cross-Domain/Subdomain Tracking with GTM and GA4**: If your conversion funnel spans multiple domains (E.g.: store.com and checkout.paymentprovider.com) or subdomains (E.g.: blog.site.com and store.site.com), configure GTM to let the same pixel/tag track the user continuously. For GA4, set `cookie_domain: auto` and `linker.domains: ['store.com', 'checkout.paymentprovider.com']` in your `Google Tag`.

3.  **User-Provided Data (UPD) / Enhanced Conversions Implementation (Google Ads)**: To improve conversion tracking accuracy, send hashed customer data (email, phone, name) to Google Ads. This helps match conversions even in cookie-restricted scenarios. Set it up in GTM to collect this data from the Data Layer or form fields at the moment of conversion and send it along with the event.

4.  **Custom Events and Micro-Conversions (Meta Ads)**: Beyond standard events, create custom events for key interactions that indicate high interest but aren't a final conversion. E.g.: `DeepScroll` (for users who scroll 75% of the product page), `ProductVideoView` (for users who watch 75% of a video). Use these events to build highly qualified remarketing audiences or to optimize top-of-funnel campaigns.

5.  **A/B Testing Attribution Settings**: Experiment with different attribution windows (e.g.: 7-day click vs. 1-day click)
