---
name: budget-allocation
description: "Budget Allocation — Specialized skill for budget allocation"
license: MIT
metadata:
  version: 1.0.0
  author: Cafe Code AI
  category: 04-anuncios-trafego
  updated: 2026-03-01
risk: safe
---

# Budget Allocation

This skill enables Claude to optimize digital ad budget distribution across Meta Ads, Google Ads, and TikTok Ads to maximize return on investment (ROAS) and cost-per-acquisition (CPA) efficiency.

---

## Keywords

Ad Budget Optimization, Digital Budget Allocation, Meta Ads Budget, Google Ads Funding, TikTok Ads Spend, ROAS Maximization, CPA Efficiency, Campaign Budget Optimization (CBO), Google Ads Portfolio Bidding, Multi-Platform Ad Spend, Incrementality Testing, Digital Marketing Budgeting, Performance Marketing Allocation.

---

## Quick Start

1.  **Consolidate Recent Performance Data**: Pull ROAS and CPA for the last 30 days for every active campaign on Meta Ads, Google Ads, and TikTok Ads.
2.  **Identify High-Return Campaigns**: Prioritize campaigns with ROAS above 3.5x and CPA below $50.00 as candidates to receive more budget.
3.  **Reallocate 15% of the Total Budget**: Move 15% of the total monthly budget from underperforming campaigns (ROAS < 2.0x or CPA > $80.00) to the high-return campaigns identified.
4.  **Adjust Daily Budgets**: Implement the new daily budget values on the platforms and schedule a review in 7 days.

---

## Core Workflows

### Workflow 1: Dynamic Budget Allocation Based on Performance and Saturation

This workflow focuses on adjusting budget across campaigns and platforms based on performance metrics and audience saturation signals.

1.  **Performance Data Collection and Consolidation (Weekly)**:
    *   **Meta Ads**: Export `Purchase ROAS`, `Purchase CPA`, `Impression Frequency`, and `Reach` by ad set and campaign for the last 7 days.
    *   **Google Ads**: Export `Conversion ROAS`, `CPA`, and `Lost Impression Share (Budget)` by campaign for the last 7 days.
    *   **TikTok Ads**: Export `ROAS` and `CPA` by campaign and ad group, including `Frequency` and `Reach` for the last 7 days.
    *   **Example**:
        *   Meta Ads - Campaign A (Retargeting): ROAS 5.2x, CPA $25, Frequency 3.8.
        *   Meta Ads - Campaign B (Acquisition): ROAS 2.7x, CPA $60, Frequency 1.2.
        *   Google Ads - Campaign C (Branded Search): ROAS 6.8x, CPA $15.
        *   Google Ads - Campaign D (Shopping): ROAS 3.0x, CPA $48, Lost IS (Budget) 15%.
        *   TikTok Ads - Campaign E (Acquisition): ROAS 2.1x, CPA $75, Frequency 2.5.

2.  **Potential and Saturation Analysis**:
    *   **Identify Winners**: Campaigns with ROAS > 3.5x and CPA < $40.00.
    *   **Identify Losers**: Campaigns with ROAS < 2.0x and CPA > $70.00.
    *   **Assess Saturation**: Frequency > 3.0 on Meta/TikTok Ads (last 7 days) or `Lost Impression Share (Budget)` < 5% on Google Ads for high-ROAS campaigns indicate possible saturation or a spend ceiling.
    *   **Example Analysis**:
        *   Campaign A (Meta Retargeting): Excellent ROAS and CPA, but Frequency 3.8. Possible saturation if the budget is increased too much.
        *   Campaign B (Meta Acquisition): Average performance, low Frequency. Room to increase budget.
        *   Campaign C (Google Branded): Great ROAS/CPA. Probably already maximized, but check `Lost Impression Share`.
        *   Campaign D (Google Shopping): Good ROAS, acceptable CPA, but 15% `Lost IS (Budget)`. Clear signal that more budget can generate more volume.
        *   Campaign E (TikTok Acquisition): ROAS and CPA below target. Candidate for a budget cut or deep optimization.

3.  **Budget Re-Allocation Proposal (Daily/Weekly)**:
    *   **Increase (Scale)**:
        *   Campaigns with ROAS > 3.5x and Frequency < 2.5 (Meta/TikTok) or `Lost Impression Share (Budget)` > 10% (Google): Increase budget by 10-20%.
        *   **Example**: Campaign D (Google Shopping) with 15% `Lost IS`. Raise the daily budget from $300 to $360.
    *   **Maintain (Optimize)**:
        *   Campaigns with ROAS between 2.5x and 3.5x and Frequency between 2.5 and 3.5 (Meta/TikTok) or `Lost Impression Share (Budget)` between 5-10% (Google): Hold budget, focus on creative or targeting optimizations.
        *   **Example**: Campaign B (Meta Acquisition). Keep $400/day, test new lookalike audiences.
    *   **Reduce (Cut)**:
        *   Campaigns with ROAS < 2.0x, CPA > $70.00 and Frequency > 3.0 or `Lost Impression Share (Budget)` < 5%: Reduce budget by 10-20% or pause.
        *   **Example**: Campaign E (TikTok Acquisition). Cut the daily budget from $200 to $160.
    *   **Rebalance Toward Retargeting**: Keep 20-30% of the total budget on retargeting campaigns, which generally deliver higher ROAS.

4.  **Implementation and Ongoing Monitoring**:
    *   Apply the budget adjustments on the platforms.
    *   Monitor key metrics daily. If a campaign's ROAS climbs significantly after an increase, consider another incremental adjustment.

### Workflow 2: Budget Optimization with CBO and Portfolio Bidding Strategies

This workflow details how to use the platforms' automatic allocation tools to optimize spend.

1.  **Structuring Campaigns for CBO (Meta Ads / TikTok Ads)**:
    *   **Logical Grouping**: Create campaigns with clear objectives (e.g., Acquisition - Prospecting, Acquisition - Lookalike, Retargeting - Cart Abandoners).
    *   **Multiple Ad Sets**: Inside each CBO campaign, include 3 to 5 ad sets with distinct audiences (e.g., 1% Lookalike, 1-3% Lookalike, Broad interests, 30-day Retargeting).
    *   **Campaign Budget Definition**: Allocate a daily or lifetime budget to the campaign, letting the platform distribute it across ad sets.
    *   **Example**:
        *   **Meta Ads Campaign**: `Purchases - Acquisition - CBO`
            *   Daily Budget: $800.00
            *   Ad Set 1: 1% Lookalike Audience (Buyer-based)
            *   Ad Set 2: Interest Audience (e.g., "Sustainable Fashion," "Natural Beauty")
            *   Ad Set 3: Broad Audience (no targeting, just age/gender)
            *   Setup: "Lowest Cost" or "Cost Per Result Goal" bidding ($55.00).

2.  **Setting Up Portfolio Bidding Strategies (Google Ads)**:
    *   **Campaign Grouping**: Group campaigns with similar objectives (e.g., all Shopping campaigns, or all non-branded Search campaigns) into a portfolio.
    *   **Centralized Bidding Strategy**: Apply a portfolio bidding strategy (e.g., "Maximize conversion value with target ROAS" or "Maximize conversions with target CPA") to that campaign group.
    *   **Target Definition**: Set a target ROAS (e.g., 350%) or target CPA (e.g., $45.00) that applies across the campaign set.
    *   **Example**:
        *   **Google Ads Portfolio**: `ecommerce - Max Value ROAS Target`
            *   Campaign 1: Shopping - All Products
            *   Campaign 2: Search - Generic (e.g., "buy sneakers," "clothing store")
            *   Campaign 3: Display - Remarketing
            *   Bidding Strategy: `Maximize conversion value with target ROAS` (Target ROAS: 350%)
            *   Total Daily Budget for the portfolio: $1,200.00

3.  **Spend Caps and ROI Adjustments (TikTok Ads)**:
    *   **Campaign and Ad Group Budgets**: On TikTok Ads, you can set budgets at both the campaign and ad group level. For CBO, set the budget at the campaign level.
    *   **Bid Optimization**: Use bidding strategies like "Lowest Cost" or "Cost Cap" (for CPA) or "Highest ROAS" (for value).
    *   **CPA/ROAS Caps**: If using "Lowest Cost," add a `Cost Cap` (Max CPA) to avoid overspending on expensive results.
    *   **Example**:
        *   **TikTok Ads Campaign**: `Sales - CBO - Summer Collection`
            *   Daily Budget: $600.00
            *   Ad Group 1: Custom Audience (Fashion interest)
            *   Ad Group 2: 1% Lookalike Audience (Video engagement)
            *   Bidding Strategy: `Lowest Cost` with `Cost Cap`: $70.00 (maximum acceptable CPA).

4.  **Monitoring and Iteration**:
    *   Monitor budget distribution across platforms and the performance of the ad sets/campaigns inside the portfolio/CBO strategies.
    *   Adjust campaign budgets and bidding targets (ROAS/CPA) as needed to optimize overall performance.

---

## Templates

### Consolidated Monthly Budget Allocation Spreadsheet

```
| Platform | Campaign/Type | Current Budget ($) | Avg. ROAS (30d) | Avg. CPA (30d) | % ROAS vs. Target | % CPA vs. Target | Suggested New Budget ($) | Adjustment (%) | Rationale |
|------------|---------------|----------------------|------------------|-----------------|-----------------|----------------|-----------------------------|------------|---------------|
| Meta Ads   | Acquisition - CBO    | 5,000                | 2.8x             | 55.00           | -20%            | +10%           | 4,500                       | -10%       | ROAS below target, high CPA. Reduce and optimize creatives. |
| Meta Ads   | Retargeting - DPA  | 3,000                | 6.5x             | 18.00           | +30%            | -20%           | 3,500                       | +17%       | Excellent ROAS/CPA. Increase to capture more bottom-funnel conversions. |
| Google Ads | Search - Branded   | 2,000                | 7.2x             | 12.00           | +40%            | -30%           | 2,000                       | 0%         | Solid performance, already maximized for search volume. |
| Google Ads | Shopping - Smart   | 4,000                | 3.1x             | 45.00           | +5%            | +5%            | 4,800                       | +20%       | Good ROAS, CPA ok. Google Ads signals scale potential via "Lost Impression Share". |
| TikTok Ads | Acquisition - Video  | 2,500                | 1.9x             | 85.00           | -35%            | +70%           | 1,500                       | -40%       | ROAS and CPA way off target. Reduce and test new creatives/audiences. |
| **TOTAL**  |               | **16,500**           |                  |                 |                 |                | **16,300**                  |            |               |
```

### Post-Allocation Performance Report (Weekly)

```
| Platform | Campaign/Type | Allocated Budget ($) | Spent Budget ($) | Achieved ROAS | Achieved CPA | % ROAS Variance vs. Target | % CPA Variance vs. Target | Notes |
|------------|---------------|------------------------|----------------------|----------------|---------------|------------------------|-----------------------|-------------|
| Meta Ads   | Acquisition - CBO    | 4,500                  | 4,480                | 2.9x           | 52.00         | +3%                    | -5%                   | Slight improvement, still room for creative optimization. |
| Meta Ads   | Retargeting - DPA  | 3,500                  | 3,500                | 6.8x           | 17.50         | +5%                    | -3%                   | Maintaining excellent performance. |
| Google Ads | Search - Branded   | 2,000                  | 1,990                | 7.0x           | 12.50         | -3%                    | +4%                   | Stable, as expected. |
| Google Ads | Shopping - Smart   | 4,800                  | 4,790                | 3.3x           | 43.00         | +6%                    | -4%                   | ROAS up and CPA down after the budget increase. |
| TikTok Ads | Acquisition - Video  | 1,500                  | 1,490                | 2.2x           | 78.00         | +16%                   | -8%                   | Slight improvement, but CPA still high. Needs an audience/offer review. |
```

---

## Checklist

- [x] Consolidate ROAS, CPA, and conversion volume data by campaign/platform.
- [x] Analyze impression frequency and reach on Meta/TikTok Ads to detect saturation.
- [x] Check `Lost Impression Share (Budget)` on Google Ads.
- [x] Identify campaigns with ROAS consistently above target (e.g., 3.5x).
- [x] Identify campaigns with CPA consistently below target (e.g., $40.00).
- [x] Prioritize budgets for retargeting campaigns (highest expected ROAS).
- [x] Allocate 20-30% of the total budget to retargeting campaigns.
- [x] Factor in seasonality and promotional events (Black Friday, Mother's Day) in the allocation.
- [x] Run A/B budget tests to validate significant changes.
- [x] Use CBO (Campaign Budget Optimization) on Meta Ads and TikTok Ads for automatic distribution.
- [x] Apply Google Ads portfolio bidding strategies to manage multiple budgets.
- [x] Schedule weekly performance reviews and budget adjustments.

---

## Reference Metrics

| Metric                      | Benchmark (e-commerce) | Target (Example) |
|------------------------------|------------------------|----------------|
| ROAS (Return on Ad Spend)    | 3.0x - 5.0x            | 3.5x           |
| CPA (Cost per Acquisition)    | $30.00 - $80.00      | $45.00        |
| CTR (Click-Through Rate) Meta Ads | 1.5% - 3.0%            | 2.2%           |
| CPC (Cost per Click) Google Search | $1.50 - $5.00        | $2.80         |
| CPM (Cost per 1,000 Impressions) TikTok Ads | $15.00 - $35.00      | $25.00        |
| Frequency (Meta/TikTok - 7d) | 2.5 - 3.5              | 3.0            |

---

## Common Mistakes

1.  **Allocating budget based only on raw ROAS without considering volume**: A campaign can have a 10.0x ROAS with only 5 conversions, while another at 3.0x ROAS generates 200 conversions. The mistake is fixating on the high ROAS and ignoring scale potential.
    *   **How to avoid it**: Prioritize total profit generated and conversion volume. Use a metric like "Gross Ad Profit" (Revenue - Ad Cost - Product Cost) or "Volume-Weighted ROAS" to make allocation decisions. E.g., If the 3.0x ROAS campaign generates $15,000 in sales and the 10.0x one generates $1,000, scaling the first is more profitable.

2.  **Ignoring audience saturation and continuing to pour in money**: Holding or increasing budget on audiences that have already seen the ads multiple times drives CPM and CPA up and ROAS down.
    *   **How to avoid it**: Monitor `Impression Frequency` (especially on Meta Ads and TikTok Ads) and `Reach` weekly. If average frequency is above 3.5-4.0 over the last 7-14 days, the audience may be saturated. Cut budget for that audience and invest in prospecting new audiences or testing new creatives. E.g., A Meta Ads acquisition campaign at 4.8 frequency over the last 7 days should have its budget cut by 15-20%, with the surplus reallocated to a different 1-3% lookalike audience.

3.  **Not differentiating budgets for top, mid, and bottom funnel campaigns**: Treating every campaign with the same ROAS and CPA expectations, without recognizing that acquisition campaigns (top of funnel) will have lower ROAS but higher volume, while retargeting (bottom of funnel) will have higher ROAS but lower volume.
    *   **How to avoid it**: Set differentiated ROAS and CPA targets for each funnel stage. Allocate a larger share of the budget (70-80%) to acquisition and brand awareness campaigns, and a smaller share (20-30%) to high-intent retargeting campaigns. E.g., On a $10,000 total budget, allocate $7,500 to prospecting on Meta Ads and Google Search, and $2,500 to retargeting on Meta Ads DPA and Google Display.

---

## Advanced Tips

1.  **Custom Attribution Modeling**: Go beyond default models ("last click," "linear") and build a data-driven attribution model in Google Analytics 4 or use external attribution tools to understand the true impact of each touchpoint. This lets you allocate budget to channels that contribute to the journey but don't get the final credit. E.g., An initial display ad click may not be the "last click," but it's crucial to starting the journey. A custom model will assign it part of the credit.

2.  **Geographic Incrementality Tests (Geo-Lift Tests)**: Instead of just comparing ROAS, run controlled tests to measure the *incremental* impact of a budget increase. Select two similar geographic regions and apply the budget increase to one (test group) while keeping the other (control group) unchanged. Compare sales and profitability lift between groups to validate the real effectiveness of the additional investment. E.g., Increase the Meta Ads budget by 20% in Texas and compare sales performance against Florida, which kept its budget unchanged.

3.  **Budget Rule Automation with Scripts**: Use custom scripts (Google Ads Scripts, Meta Automated Rules) to automate budget adjustments based on real-time performance. Set rules to increase budgets on campaigns that beat the target ROAS by 20% for 3 consecutive days, or reduce budgets on campaigns running 30% above target CPA. E.g., A Google Ads script that raises the daily budget by 10% for campaigns with ROAS > 4.0x the previous day, capped at a maximum 20% weekly increase.

4.  **Gross Margin Analysis by Product/Campaign**: Allocate budget not just on generic ROAS or CPA, but considering the gross margin of the products being promoted. Prioritize campaigns selling higher-margin products, even if absolute ROAS is slightly lower than low-margin products, because the bottom-line profit will be greater. E.g., A product with 3.0x ROAS and 60% margin is more profitable than one with 4.0x ROAS and 20% margin, at the same sales volume.

5.  **Budget Forecasting with Seasonal and External Trends**: Use historical seasonality data (holidays, sales periods) and external factors (product launches, market trends) to forecast future performance and pre-allocate budgets. BI tools or Machine Learning models can help build optimized allocation scenarios for demand peaks and valleys. E.g., Increase the Google Shopping budget by 40% three weeks before Black Friday, based on ROAS and conversion volume analysis from the last 3 years for that period.
