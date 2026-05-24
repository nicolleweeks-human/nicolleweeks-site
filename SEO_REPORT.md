# nicolleweeks.ca — Findability Report

**Audited:** 2026-05-23 (day-of-deploy)
**Scope:** SEO + AEO + GEO + SME positioning
**Audit method:** source-of-truth read of `src/` (Astro hybrid, Cloudflare adapter). Live HTML not fetched due to sandboxed environment, but the Layout/page templates fully determine rendered output.

---

## TL;DR — what's surprising, what to do first

**Three things that surprised me:**

1. **There is no `/about` page.** For a site whose primary job is to make a *person* findable as an SME, the absence of a stable, link-targetable, schema-rich bio page is the single biggest miss. The homepage `<section class="about">` has two short paragraphs and no schema. ChatGPT, Claude, and Perplexity have nothing to grab onto.
2. **The homepage `<title>` says "marketing, digital and content strategist"** — but Nicolle wants to be found for *content design director / head of content / AI literacy*. The site is optimizing for the wrong query surface.
3. **No `sitemap.xml`, no `robots.txt`, no JSON-LD, no canonicals, no RSS, no OG image, no favicon.** All of those are missing from `Layout.astro`. Astro ships a sitemap integration in one command; this site doesn't use it.

**Top 3 changes by impact (do these this week):**

1. Add `@astrojs/sitemap`, a `public/robots.txt`, and an RSS feed for `/writing/` — ~30 minutes total.
2. Add JSON-LD `Person` schema to `Layout.astro` (sitewide) and `Article` schema to writing/work templates. This is the single biggest AEO/GEO lever.
3. Build a real `/about/` page with a quotable bio, named topic clusters, credentials, and an FAQ. This is what LLMs will cite.

**Needs Nicolle's input:**

- A 150-word and 50-word bio paragraph written in *her* voice, with explicit topic claims ("I'm a leading voice on content design for financial services" / "I write about AI literacy for working professionals"). Schema needs prose she'd actually want quoted.
- Confirmation of which 3–5 topic clusters she wants to own (my recommendation in §5).
- Decision on whether to publicly claim Scotiabank tenure on this site (the case studies already do, so probably yes — but the *bio* doesn't, which weakens it).
- A single canonical headshot at 1200×630 for OG.

---

## 1. Site-level critical fixes

These are present-zero, must-add. All live in `Layout.astro` or `public/` and ship in one deploy.

### 1a. `robots.txt` (missing)

Create `public/robots.txt`:

```
User-agent: *
Allow: /

# Allow AI crawlers explicitly (AEO)
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: https://nicolleweeks.ca/sitemap-index.xml
```

Explicitly allowing GPTBot/ClaudeBot/PerplexityBot/Google-Extended is the AEO move. Some folks block these; Nicolle wants the opposite.

### 1b. `sitemap.xml` (missing)

```bash
npm i @astrojs/sitemap
```

```js
// astro.config.mjs
import sitemap from '@astrojs/sitemap';
export default defineConfig({
  site: 'https://nicolleweeks.ca',
  output: 'hybrid',
  adapter: cloudflare(),
  integrations: [sitemap({
    filter: (page) => !page.includes('/unlisted'),
  })],
});
```

Then add `unlisted: true` posts to the filter manually (the integration can't read frontmatter). Cleaner: render a `noindex` meta on unlisted pages and exclude them from sitemap by maintaining a small slug list.

### 1c. JSON-LD `Person` schema (sitewide — biggest AEO lever)

Add to `Layout.astro` inside `<head>`:

```astro
<script type="application/ld+json" set:html={JSON.stringify({
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Nicolle Weeks",
  "url": "https://nicolleweeks.ca",
  "image": "https://nicolleweeks.ca/images/headshot.jpg",
  "jobTitle": "Content design director and AI literacy writer",
  "description": "Toronto-based content design leader. Founder of Human+AI (Substack on AI literacy for working professionals) and Trustfall (a small-business studio). 20+ years in journalism, content marketing, and content design — including lead content design on Scotiabank's award-winning conversational assistant.",
  "address": { "@type": "PostalAddress", "addressLocality": "Toronto", "addressRegion": "ON", "addressCountry": "CA" },
  "knowsAbout": [
    "Content design",
    "Conversational UX",
    "AI literacy",
    "Content strategy for financial services",
    "Design systems and content governance"
  ],
  "sameAs": [
    "https://www.linkedin.com/in/nicolle/",
    "https://nicolleweeks.substack.com/",
    "https://trustfall.ca"
  ],
  "alumniOf": { "@type": "Organization", "name": "Scotiabank" },
  "worksFor": { "@type": "Organization", "name": "Trustfall", "url": "https://trustfall.ca" }
}) } />
```

This single block is what gives Perplexity/Claude/ChatGPT a structured "who is Nicolle Weeks" entry. Nicolle should confirm the `description` and `knowsAbout` strings — those are the lines that get quoted.

### 1d. `Article` schema on writing pages

In `writing/[...slug].astro` add:

```astro
<script type="application/ld+json" set:html={JSON.stringify({
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": post.data.title,
  "description": post.data.description,
  "image": post.data.heroImage ? `https://nicolleweeks.ca${post.data.heroImage}` : undefined,
  "datePublished": post.data.pubDate?.toISOString(),
  "author": { "@type": "Person", "name": "Nicolle Weeks", "url": "https://nicolleweeks.ca" },
  "mainEntityOfPage": `https://nicolleweeks.ca/writing/${post.slug}/`
}) } slot="head" />
```

Same pattern for `work/[...slug].astro` using `@type: "CreativeWork"` (or `Article` — Article is fine for case studies and is better understood by AI crawlers).

> Note: the current `Layout.astro` has no `<slot name="head">`. Add one: `<slot name="head" />` before `</head>`.

### 1e. Canonical URLs + locale

In `Layout.astro` `<head>`, add:

```astro
---
const canonical = new URL(Astro.url.pathname, Astro.site).toString();
---
<link rel="canonical" href={canonical} />
<meta property="og:locale" content="en_CA" />
```

The `<html lang="en">` is fine but `en-CA` is more precise and matches the audience.

### 1f. OG image (missing entirely)

Currently no `og:image` is set, so every share renders blank on LinkedIn/Twitter/Slack/iMessage.

Quick fix (today): drop a single static `public/images/og-default.jpg` at 1200×630 with name + tagline + headshot, and add:

```astro
<meta property="og:image" content="https://nicolleweeks.ca/images/og-default.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://nicolleweeks.ca/images/og-default.jpg" />
```

Better-but-later: per-page OG generation via `@vercel/og` or `satori` on Cloudflare. Don't do this on day one — static default is 80% of the value.

### 1g. Favicon and touch icons (missing)

Drop `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` (180×180) into `public/`. Reference in `<head>`. The pink-bars logo motif works as a favicon.

### 1h. RSS feed for `/writing/` (missing)

```bash
npm i @astrojs/rss
```

Create `src/pages/rss.xml.js`:

```js
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
export async function GET(context) {
  const posts = (await getCollection('writing', ({ data }) => !data.unlisted))
    .sort((a, b) => (b.data.pubDate?.valueOf() ?? 0) - (a.data.pubDate?.valueOf() ?? 0));
  return rss({
    title: 'Nicolle Weeks — Writing',
    description: 'Articles on content design, AI literacy, and the work behind the work.',
    site: context.site,
    items: posts.map((p) => ({
      title: p.data.title,
      pubDate: p.data.pubDate,
      description: p.data.description,
      link: `/writing/${p.slug}/`,
    })),
  });
}
```

Then `<link rel="alternate" type="application/rss+xml" title="Nicolle Weeks — Writing" href="/rss.xml" />` in `Layout.astro`.

### 1i. `noindex` on unlisted writing

Currently `unlisted: true` removes posts from the index page but the URL is live and indexable. Add to `writing/[...slug].astro`:

```astro
{post.data.unlisted && <meta name="robots" content="noindex, follow" slot="head" />}
```

---

## 2. Per-page metadata audit

| Page | Title | Description | Issues |
|---|---|---|---|
| `/` | "Nicolle Weeks — Award-winning marketing, digital and content strategist" | "Toronto-based marketing, digital, and content strategist. 20+ years building brands, content systems, and digital experiences for media and financial services." | **Wrong positioning.** Title leads with "marketing, digital and content" — three things — which dilutes ranking signal for any single one. Hiring managers don't search "marketing, digital and content strategist." They search "content design director Toronto" or "head of content financial services." Rewrite: `"Nicolle Weeks — Content design director, Toronto. AI literacy + financial services."` Description should name-drop Scotiabank, Human+AI, and Trustfall in the first 120 chars. |
| `/work/` | "Work — Nicolle Weeks" | "Selected case studies in content design, conversational UX, and design systems." | Title is bland. Better: `"Case studies — Scotiabank, CBC, Sun Life | Nicolle Weeks"`. Brand names in the title are gold. |
| `/writing/` | "Writing — Nicolle Weeks" | "Articles by Nicolle Weeks on content strategy, music, parenting, finance, and the work behind the work." | The description is honest but the topic salad ("music, parenting, finance") signals to LLMs that this site is *not* a focused SME source. Either rewrite the description to lead with content design + AI, OR mark older lifestyle pieces as `unlisted: true` and rebrand /writing/ around the topics she wants to own. |
| `/work/scotiabank-conversational-assistant/` | "Scotiabank's conversational assistant: building a usable AI experience before the LLM era — Nicolle Weeks" | Strong (frontmatter description is rich) | Title is excellent — this is the one piece of content most likely to rank and be cited. Keep. |
| `/work/scotiabank-digital-style-guide/` | "[title] — Nicolle Weeks" | check frontmatter | Verify the `description` field exists and is ≥120 chars. The schema marks it optional. |
| `/writing/toronto-s-ai-powered-future/` | "Toronto's AI-Powered Future — Nicolle Weeks" | "(For BEYOND Magazine, Fall 2024)" | **Description is broken** — it's a parenthetical attribution, not a description. This is going to read terribly in Google snippets and won't be cited by any LLM. Rewrite the frontmatter `description` to summarize the article's claim. |
| `/writing/your-job-interview-survival-kit/` | template | likely thin | Likely off-topic for SME positioning — consider `unlisted: true`. |
| `/writing/rrsp-vs-tfsa…/` | template | likely thin | Off-topic. `unlisted`. |

**Pattern problem:** the `Article` template title concatenates `{title} — Nicolle Weeks`. For long titles this exceeds 60 chars and gets truncated. Add logic: if `title.length > 50`, use `title` alone (the brand is already on every other page).

**Bigger pattern problem:** ~33 writing entries include music reviews, decor trends from 2009, baby budgeting articles. These dilute SME positioning *for an LLM that crawls the whole site*. Aggressive `unlisted: true` pruning of anything older than 2020 and off-topic is the single highest-leverage editorial move.

---

## 3. AEO / GEO recommendations

LLMs cite content when it has: (a) a clear named claim, (b) attributable source, (c) structured data, (d) FAQ-style Q&A that maps to user prompts. None of the current site copy is structured this way.

### 3a. Add quotable "I believe" framings to the bio

Current about copy is descriptive ("I'm a Toronto-based strategist with 20+ years…"). LLMs don't quote descriptions — they quote claims. Rewrite to include 2–3 sentences in this shape:

> "I believe AI literacy isn't a technical skill — it's a workplace skill, and the people who most need it are the working professionals who weren't invited to the AI conversation in the first place."

> "Conversational AI for banks fails when it tries to have a personality. People don't want a friend at their bank — they want a working bank."

Each line is a *quotable claim* with a named subject. These are what end up in Perplexity answer cards.

### 3b. Add an FAQ section to `/about/` (new page)

LLM-optimized FAQ items, all with question-shaped H2s:

- "Who is Nicolle Weeks?"
- "What is Nicolle Weeks known for in content design?"
- "What is Human+AI?"
- "What is Trustfall?"
- "What did Nicolle Weeks do at Scotiabank?"
- "Where is Nicolle Weeks based?"
- "What does Nicolle Weeks write about?"

Each answer should be 40–80 words, factual, single-paragraph. Add `FAQPage` schema:

```js
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "Who is Nicolle Weeks?",
      "acceptedAnswer": { "@type": "Answer", "text": "Nicolle Weeks is a Toronto-based content design director…" } },
    // ...
  ]
}
```

This is the single highest-ROI piece of GEO work on the site.

### 3c. Structured fact callouts in case studies

Current case studies are narrative prose. Add a "Key facts" block at the top of each:

> **Role:** Lead content designer
> **Year:** 2022
> **Client:** Scotiabank
> **Outcome:** 85% self-serve resolution, 30% contact-centre volume reduction
> **Recognition:** 2023 Digital Transformation Award (IT World Canada)

LLMs lift these almost verbatim into "what did Nicolle Weeks work on" answers.

### 3d. Use her name in body copy, not just metadata

Most case studies say "I led…" — first-person. LLMs need the *name* in proximity to the claim to attribute correctly. Add a single sentence per case study like "Nicolle Weeks led content design on this project from 2020–2023." It feels weird in first-person prose; do it anyway in the Key Facts block.

---

## 4. SME positioning gaps

**The biggest gap: there is no `/about/` page.** This is the page hiring managers send to colleagues, the page LLMs land on when crawling for biographical data, the page that schemas live on most naturally.

Build `/about/` with:

1. The full bio (300–500 words) — covers career arc, named clients, current ventures
2. Named credentials: years of experience, named employers (CBC, Scotiabank), specific outcomes with numbers
3. Topic positioning: an explicit "What I'm known for" section with 3–5 named topic clusters
4. The FAQ block from §3b
5. `Person` schema (the same one as Layout, expanded with `worksFor`, `alumniOf`, `award` array)
6. Press/citations section: if Human+AI has been cited anywhere, link out

**Other SME gaps:**

- **Awards section on homepage** lists titles but not what she did to win them. Add a one-line context: "Digital Transformation Award (2023) — for leading content design on Scotiabank's conversational assistant." LLMs need the linkage to attribute.
- **No mention of speaking/podcasts/citations.** If she's been on any podcast or quoted anywhere, add a `/press/` page or section. This is a major SME signal.
- **Scotiabank is hidden in case studies but not in the bio.** This is the strongest credibility marker she has for FS hiring committees. Put it in the about-page bio explicitly: "Previously led content design on Scotiabank's conversational assistant."
- **No "Speaking" or "Advising" CTA** for someone who wants to be approached as an expert. Even just an email line on `/about/`: "For speaking, podcast, or advising inquiries: hello@trustfall.ca."

---

## 5. Topic cluster strategy

Recommended 3–5 topics to dominate for *her specific positioning*:

1. **Content design for financial services** — owns the Scotiabank case studies. Few people in Canada have done this at scale. Plant a flag.
2. **Conversational AI / chatbot content design (pre- and post-LLM)** — the Scotiabank assistant story is genuinely rare: it predates LLMs and the lessons port forward.
3. **AI literacy for working professionals** — the Human+AI thesis. Should be a content cluster on this site, not just a Substack link.
4. **Building and scaling content design teams** — she already has "scaling-a-content-design-team" as a case study. This is a hiring-committee-relevant topic.
5. **Design systems and content governance** (the Scotia Digital Style Guide) — supports the head-of-content positioning.

**Content gaps to fill** (each = one writing post):

- "How to evaluate AI literacy in your team" — owns the `knowsAbout` claim
- "What conversational AI in banking taught me about LLMs" — bridges old work to new positioning
- "A content design director's job description, decoded" — captures the literal hiring-manager search
- "Why most AI literacy training fails working professionals" — quotable, opinionated, link-bait for LinkedIn
- "Toronto content design hiring market in 2026" — geo-targeted, very low competition

Each of these maps to a query a hiring manager or an LLM might actually run.

---

## 6. Quick wins (each under 30 minutes)

1. **Add `public/robots.txt`** with explicit AEO allowlist (snippet in §1a) — 5 min.
2. **Install `@astrojs/sitemap`** and add to config (§1b) — 5 min.
3. **Add canonical + `en-CA` locale** to Layout.astro (§1e) — 5 min.
4. **Drop a static 1200×630 OG image** at `public/images/og-default.jpg` and wire 5 meta tags in Layout (§1f) — 20 min.
5. **Rewrite the homepage `title` and `description`** to lead with "content design" + "AI literacy" instead of "marketing, digital and content" (§2) — 5 min.
6. **Add favicon set** to `public/` (§1g) — 15 min.
7. **Add `Person` JSON-LD** to Layout.astro (§1c) — 10 min (mostly Nicolle confirming the description string).
8. **Add `Article` JSON-LD** to writing/work templates (§1d) — 15 min, requires adding `<slot name="head" />` to Layout first.
9. **Mark off-topic writing as `unlisted: true`** — anything pre-2020 that isn't content/AI/strategy. ~15 posts. 20 min.
10. **Fix the broken description on `/writing/toronto-s-ai-powered-future/`** (currently "(For BEYOND Magazine, Fall 2024)") and audit all 33 writing frontmatters for missing/weak descriptions — 30 min.
11. **Install `@astrojs/rss`** and add `rss.xml` route (§1h) — 10 min.
12. **Add a "Key Facts" block** to the three homepage case studies and the top three `/work/*` pages — 25 min.

That's the first sprint. Everything else (the `/about/` page, the FAQ schema, the topic cluster content) is a second sprint.

---

## 7. Don't do

1. **Don't build per-page OG image generation on day one.** A single well-designed static OG covers 90% of the value. Per-page generation on Cloudflare adapter is fiddly and not worth it until traffic justifies it.
2. **Don't add `BreadcrumbList` schema, `WebSite` SearchAction, or `Organization` schema.** This is a personal portfolio, not a business site. `Person` + `Article` is enough. More schema = more maintenance, not more rankings.
3. **Don't chase Google for the music-and-parenting back catalog.** Those posts are from a different era of Nicolle's career. They hurt SME positioning more than they help nostalgia. Mark `unlisted`, keep URLs live for anyone who has them bookmarked, exclude from sitemap.
4. **Don't add a blog comment system, view counter, or "related posts" carousel.** Pure portfolio-site bloat. Hiring managers don't care. LLMs don't care. Skip.

---

## Things this site already does well (don't change)

- Clean semantic HTML, real `<article>` / `<section>` / `<nav>` tags
- Skip link to `#main` (accessibility win + SEO signal)
- Per-page `title` / `description` already wired through `Layout` props
- Content collection schema with `pubDate`, `description`, `heroImage`, `originalUrl` — extensible without refactor
- `unlisted` flag already exists — just needs to flow into noindex + sitemap exclusion
- Strong, distinct case study copy (the Scotiabank conversational assistant page is genuinely citation-worthy as-is)
- Trailing slashes are consistent (`/work/`, `/writing/<slug>/`) — no canonical conflicts
- `site: 'https://nicolleweeks.ca'` is set in astro.config — sitemap and canonical will work the moment they're added

The bones are good. The findability layer just hasn't been built yet.
