---
description: Maps the niche, audience, competitors, pains, objections and angles before any campaign
argument-hint: "[product or niche] [market] — optional, uses the config defaults"
---

Run market research following the `market-research` skill, and use the `keyword-research` skill for real search intent.

## Preparation
1. Read `meta-ads-config.json`. If missing, suggest `/setup` first.
2. Determine the product/niche and market from `$ARGUMENTS`, or ask. Always confirm before continuing.

## Execution
Use web search if it is available. Otherwise use Claude in Chrome if it is available. If neither is available, ask the user to paste what they know about their competitors and customers and say clearly that the result is based only on that.

Cover: real search terms, search intent (informational / commercial / transactional), real pains and objections, 2-3 competitors for positioning reference, and 5-8 Meta interests that exist in the Ads Manager interest selector.

## Output
Save `research-[product].md` in the connected folder with a keyword table by intent, the real pains and objections (raw material for copy), the suggested interests, and a 3-line summary. Present the summary and suggest `/creative [product]`.
