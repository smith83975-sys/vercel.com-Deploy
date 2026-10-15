# VaultPulse

A simple, agent-maintainable site tracking COMEX registered vs eligible inventory and physical silver/gold premiums.

**Live prototype:** Open `index.html` in a browser.

## What it solves

People who follow silver/gold want one place for:
- Current COMEX registered (deliverable) vs eligible stocks
- Recent changes
- A simple "physical tightness" score
- Snapshot of retail premiums over spot

## Deploy

### Option A: Vercel (recommended, matches Alex Finn's setup)
1. Push this folder to a GitHub repo.
2. Import the repo at vercel.com → Deploy.
3. It will serve `index.html` as the root.

### Option B: GitHub Pages
1. Push to a repo.
2. Settings → Pages → Deploy from branch → `/` or `/docs`.

### Option C: Any static host
Upload the folder. The site is pure static HTML/CSS.

## Connectors for full autonomy

1. **Hosting**: Vercel (or Netlify, Cloudflare Pages)
2. **Payments / Sponsors**: Stripe Payment Links or a simple "Sponsor us" page that points to a Stripe checkout
3. **Newsletter**: Buttondown, ConvertKit, Beehiiv, or Substack. Replace the form action.
4. **X / Research**: Give the agent access to search X and official CME reports for daily updates.

## Agent maintenance prompt (paste into Grok Bot / Cursor agent)

```
You are the CEO of VaultPulse (vaultpulse site). Your job is to autonomously maintain it:

- Update the COMEX registered/eligible numbers daily from official CME warehouse reports or reliable aggregators.
- Recalculate the tightness scores (simple formula: registered inventory percentile vs recent history + total vault / open interest coverage; registered-only coverage shown as secondary).
- Refresh the premium snapshot from major dealer sites when notable moves occur.
- Optimize page titles, meta description, and headings for SEO and AI chatbots.
- Start and maintain a short daily email newsletter with the numbers.
- Watch X for feedback on physical metals / COMEX and note relevant comments.
- Fix any bugs or broken links.
- When appropriate, add or update sponsor placements and keep sponsors happy.
- Post a short weekly update on progress (numbers, traffic, newsletter growth).

Prefer small, accurate updates over flashy claims. Always cite the data date and source. Never give financial advice.
```

## Next steps to monetize

1. Add a real newsletter provider and collect emails.
2. Create a Stripe Payment Link for sponsorships ($300–$1,000/month typical for niche finance sites).
3. Put the sponsor logo/link in the sponsor bar.
4. Share the site on X and metals communities.

This follows the same loop as agentusecases.ai: useful directory/signal site → traffic → sponsors + newsletter.

## Deliveries & notable moves (merged from VaultFlow)
`flow.html` (linked from the nav and a homepage section) is a plain-English feed of notable COMEX silver/gold delivery notices, issues/stops and big registered/eligible shifts (`data/entries.json`, auto-archived after `archive_after_days`), "gas tank" gauges of registered stock vs. month-to-date deliveries (`data/tank.json`), and a short force majeure explainer. Every entry cites its data date and source. Not financial advice, no price predictions. The old vaultflow-rho.vercel.app address redirects here.

## Paper vs metal (single source of truth)
Every paper-to-metal figure (open-interest ratio, coverage, M2/M1 implied prices) is computed by
`scripts/compute_paper_to_metal.py` into `data/latest.json -> paper_to_metal`. Pages read only that block;
no ratio is hardcoded in HTML/JS. Silver is measured against TOTAL COMEX vault silver (registered + eligible);
registered-only values are labelled secondary.

Weekday refresh routine:
1. Update `comex` (CME warehouse stocks via thevaultreport.com, cross-check metalcharts.org).
2. Open interest: download CME Daily Bulletin Section 02B and run `python3 scripts/parse_cme_oi.py <file.pdf>`
   (or `--fetch`). It sets contracts, `fetched_at` and `trade_date` (when the header shows one). If CME blocks
   the download, leave `open_interest` as is: the old `fetched_at` keeps the site honest about the date.
3. `python3 scripts/build_seo_pages.py` (runs compute_paper_to_metal.py first), then commit and deploy.
