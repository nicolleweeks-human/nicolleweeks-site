---
title: "Scotiabank's conversational assistant: building a usable AI experience before the LLM era"
pubDate: 2022-01-01
description: "Lead content design on the award-winning Scotiabank assistant — a pre-gen-AI chatbot where every reply in every flow had to be written by hand to earn customer trust."
originalUrl: "https://nicolleweeks6.wixsite.com/mysite-1/portfolio-collections/my-portfolio/project-title-4"
---

This was built before generative AI. No LLM was filling in the blanks. Every reply in every flow — every greeting, every confirmation, every recovery path — had to be written by hand, reviewed, and approved before it ever reached a customer. That constraint shaped everything about how this assistant got designed, and it's the reason the work held up.

## Context

In 2022, chat support was the #1 requested feature by Scotiabank's mobile customers. The business needed an assistant that could reduce contact centre load, speed up resolution, and modernize digital service — without eroding the trust people place in their bank. Most conversational AI at the time felt clunky or gimmicky. The bar was higher than that: it had to feel like service.

The assistant was built on an AIML-based platform, not a large language model. There was no probabilistic generation smoothing over the edges. If a customer asked something we hadn't anticipated, we had to have already written the response — or written a graceful way to recover.

## The problem

Our flows covered the kind of moments where a bad answer is worse than no answer: password resets, credit card disputes, payment issues, profile changes. High-volume, high-sensitivity, high-stakes. We had to:

- Write every line of every conversation by hand, across dozens of intents
- Hold a consistent voice across flows that touched legal, compliance, accessibility, and brand
- Build something rigid enough to be safe and flexible enough to feel human
- Avoid the trap of making the assistant "fun" — customers wanted a working bank, not a personality

## The approach

I was the lead content designer on the assistant, integrated directly with the AIML team and the contact centre. That integration was not a nice-to-have. The AIML team understood what the system could and couldn't reliably classify. The contact centre understood what customers were actually calling about and where conversations went sideways. Designing in isolation from either would have produced a demo, not a service.

We framed the assistant as a service layer, not a character. That meant:

- Predictable, scannable patterns over clever dialogue
- Micro-interactions that clarified next steps and minimized dead ends
- A tone guide that balanced approachability with accountability — especially at the edges
- Accessibility as a design input, not a QA checkbox at the end

## What I did

**Authored 25+ flows** across login issues, payments, card management, and profile updates — each one written, tested, and iterated line by line.

**Built a reusable conversation system** for openings, confirmations, and closings, so new flows could be assembled without reinventing voice every time. This is what eventually let the framework get reused across other internal assistant products.

**Partnered with the AIML and data teams** to test and tune intents inside the AIML logic framework — pairing the writing with the classification work so they actually held together in production.

**Led accessibility reviews with screen reader users**, treating their feedback as design input rather than a final-stage compliance pass.

**Aligned five review groups** — legal, compliance, accessibility, brand, and the contact centre — by prototyping sample flows and running review workshops. The goal was to turn approvals into a partnership instead of a bottleneck. It worked.

**Held the line on voice.** One stakeholder pushed for overly flattering language — the kind of bot-speak that tells the customer they're doing great for clicking a button. I pushed back. Competence builds trust more than praise does, especially in a banking context. The assistant stayed plain, useful, and respectful of the customer's time.

**Documented everything in Confluence** so the patterns, tone rules, and flow logic could be reused by the teams that came after us.

## The results

- **85% of user inquiries resolved without human escalation**
- **30% reduction in contact centre volume**
- **Framework reused** across other assistant products inside the bank
- **Voice, structure, and clarity** consistently praised in internal UX reviews
- **2023 Digital Transformation Award** from IT World Canada, recognizing the work as a modernization of Scotiabank's customer experience

> We didn't try to make the assistant fun. We made it reliable.

That was the call we kept making, in review after review. It's the call that made the rest of the work possible.

## Why this work matters

It's easy now, in the LLM era, to forget what conversational AI used to demand. Without a model generating fluent responses on the fly, every moment of helpfulness had to be earned by writing, by structure, and by decisions about what the assistant would and wouldn't try to do. There was no fallback to "the model will figure it out." We had to figure it out.

What we shipped was a usable AI experience at a time when most weren't — built on tight collaboration with the AIML and contact centre teams, ethical tone decisions held under stakeholder pressure, and a content system rigorous enough that other product teams wanted to reuse it.

The award was a nice signal. The reuse inside the bank was a better one. The 30% drop in contact centre volume was the one that mattered to customers.
