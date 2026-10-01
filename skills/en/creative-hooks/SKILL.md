---
name: creative-hooks
description: Use this skill to generate hooks (opening lines) for Feed, Stories, Reels, UGC, Carousels, and short-form video. Trigger when the user says "create hooks," "opening hook," "first line of the video," or runs /hooks.
---

# Hooks by Format

The hook is what decides whether someone keeps watching/reading in the first 1-3 seconds (video) or the first visible line (feed/carousel). Always anchor to real pains/desires/objections — from `market-[product].md` or `research-[product].md` if they exist; never invent a generic niche pain.

## Hook patterns (use as raw material, blended with the product's real pain)

- **Direct question**: "Have you also tried [common solution] and it didn't work?"
- **Shock/contrast statement**: "Nobody tells you this about [topic]."
- **Immediate identification**: "If you're [specific avatar situation], this is for you."
- **Common mistake**: "The mistake 9 out of 10 [avatar] make with [topic]."
- **Result as the opener**: show the result/proof before explaining how you got there.
- **Personal confession (for UGC)**: "I didn't want to admit this, but..."

## By format

- **Feed (static image)**: the hook is the first line of text + the visual headline on the image — both must tell the same story, not compete.
- **Stories**: the hook must land in 1-2 seconds, usually with big on-screen text + voice/audio reinforcing the same hook.
- **Reels/short-form video**: the hook in the first 3 seconds must be spoken AND shown as on-screen text (caption) — people watching on mute need to get it too.
- **UGC**: the hook must sound like a real person talking, not an ad — avoid salesy language right up front (the `ugc-script` skill goes deeper on this).
- **Carousel**: the hook is the first slide — it needs to create enough curiosity to swipe to the next one, without giving everything away on slide 1.

## Output

For each requested format, deliver 3-5 different hooks, each testing a different pattern from the list above (never 5 variations of the same pattern). Note which real pain/desire/objection each hook came from, for traceability and to make later A/B testing easier (`/ab-test`).
