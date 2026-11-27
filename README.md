# The Weekly Funnel Digest

## Make it yours

This is a starting point, not a finished product. It was built for one person's work, and every rule in it is meant to be changed to fit yours. Nothing in here is precious.

- Fill in the `[BRACKETED]` placeholders in [`PROMPT.md`](PROMPT.md) with your own details.
- Read [`FEATURES.md`](FEATURES.md). It explains each feature, why it's there, and which part of the prompt to edit to turn it off, loosen it or swap it.
- Edit the prompt in plain words. If a rule doesn't fit how you work, rewrite it or delete it.
- Run it once by hand after every change and read what comes back.

An agent that pulls last week's numbers straight from the native APIs (Google Analytics, Meta and Instagram, plus the platforms you read by hand), writes them into one living dashboard page every Saturday morning, and says where the funnel is leaking. No connector subscription, no four tabs open on a Friday.

This repo walks the same five steps as the guide, with the prompt in [`PROMPT.md`](PROMPT.md) and the pull script in [`native_pull.py`](native_pull.py).

## Features

- Pulls Google Analytics and Instagram from their own APIs and reads Pinterest and TikTok, no Supermetrics
- Tells you where the funnel is leaking
- Refreshes the live dashboard every week

**Who it's for:** small businesses paying for an analytics tool they open once a month.

**What it replaces:** a $100-a-month connector and a spreadsheet.

## You need

- A paid Claude plan with scheduled tasks, a Google Analytics 4 property, a Meta Business account with your Instagram connected, and somewhere private to keep two small key files.
- A couple of hours the first time. Creating the API access (a GA4 service account and a Meta reporting token) is the real work. The agent itself takes twenty minutes.
- Your GA4 property ID, your Instagram account ID, and a plain list of what each stage of your funnel is supposed to do.

## What it does

Every Saturday morning:

1. Fetches three private files (the script and two read-only credentials) into a scratch location, locks the secrets to owner-only, and never prints, logs, messages, publishes or stores their contents.
2. Runs `native_pull.py` against the GA4 Data API (last 7 days, previous 7, last 30, last 90 and total, plus top pages for the week) and the Meta Graph API (followers, reach, accounts engaged and interactions for the last 7 and 30 days).
3. Pulls your email platform and, if you run one, your ads account through their connectors. Reads the platforms without an API from the stats you saved in the last 3 days, copied exactly with their own labels and period, marked "(browser read)".
4. Reads your dashboard page first, then edits the numbers in place: funnel boxes, every column of the KPI table, the notes, and the "week of" date range. Every source is labelled by where its number came from.
5. In the Insight column writes one plain line per row and names the stage where numbers fall off most from one step of the funnel to the next.
6. Messages you only if something broke or moved sharply, and writes one log entry per run: date, status, what was refreshed, anything stale or broken.

## What stays yours

- What to change because of the numbers. The agent reports the drop-off; you decide the fix.
- Which stage to work on this week. The page shows every stage; you pick one.
- The shape of the dashboard. The agent edits numbers in place; it never adds, removes or redesigns a box.

## What it will never do

- Guess a number. If a pull fails, it keeps last week's figure, marks it "stale since <date>: <short error>", and tells you.
- Fabricate variation. Where windows are identical because a property is new, it says so and why. Instagram quarter and total cells read "n/a (Meta caps at 30 days)".
- Compute a trend from a browser-read figure. Those are copied exactly.
- Rebuild the page from scratch or create a second copy.
- Put a token or key into the page, a log or a message.

## Set it up (five steps)

### 1. Name the sources and the one page they feed

The reason you open four dashboards and forget the numbers by Friday is that nothing joins them. So start with the join. Write down each place your audience comes from, and then one page where every number will land. Split your sources into two kinds: those with an API you can use yourself (Google Analytics 4, Instagram through Meta, most email software) and those easier to read from their own analytics page (Pinterest, TikTok, LinkedIn, Substack). A funnel has stages (attract, capture, nurture, convert, keep and refer), and each source belongs to a stage. Once a number knows its stage, a drop between stages becomes visible, and that drop is the leak. [`sources.example.md`](sources.example.md) shows the shape.

### 2. Create the API access and keep it private

This is the real work, and it is a one-time job. You need two small credentials: a Google service-account key with read access to your GA4 property, and a Meta system-user token with read access to your Instagram insights. Both are created in the platforms' own admin consoles (Google Cloud for the key, Meta Business settings for the token) and both are files you download once.

Then the script, [`native_pull.py`](native_pull.py). In `ga4` mode it takes the key file, your property ID and a window of days and prints the numbers as JSON: sessions, users, new users, page views, engaged sessions, key events, plus channels, sources, landing pages and top pages. In `ig` mode it does the same for Instagram: followers, reach, accounts engaged, interactions, saves, shares and views.

```
pip install google-auth requests
python3 native_pull.py ga4 ga4_key.json [YOUR GA4 PROPERTY ID] > ga4.json
python3 native_pull.py ig meta_token.txt [YOUR INSTAGRAM USER ID] 30 > ig.json
```

Put the script and both secrets in one private folder the agent can fetch from (a private drive folder works) and nowhere else. The agent downloads them into a scratch file at run time, locks the two secrets to owner-only, and never prints, logs, messages, publishes or stores their contents. Not in the prompt, not on the page, not in a message to you. Do not commit the key or the token to any repo, including a fork of this one.

### 3. Build the dashboard page once

The agent updates a page; it does not design one. So design it first, by hand, with the numbers you have today. Five funnel columns across the top (attract, capture, nurture, convert, keep and refer), one box per source or offer inside each column, and under it a KPI table with six columns: KPI, this week, this month, this quarter, total, insight. Build it in whatever you can edit as HTML and the agent can read and republish in place: a Claude artifact, a page in your site, a file in a folder. Boxes do not come and go. Each source is labelled by where its number came from. Known gaps get a box that says so. Give the page a "week of" date range in the title block; the agent moves that range every Saturday.

### 4. Create the Saturday agent

In Claude Code, open Scheduled tasks and create a new one. Paste the prompt from [`PROMPT.md`](PROMPT.md) with every bracket filled: where your three files live, your GA4 property ID, your Instagram account ID, where the page lives, and your Slack DM channel for the rare alert. Set it for Saturday morning in your timezone, so the week it reports on is fully over. Connect the connectors it needs: your file storage, your email platform, your ads account if you run one, and Slack. The GA4 and Instagram pulls need no connector at all; the script does those itself. The prompt is long on purpose: a scheduled task starts with no memory, so everything it must know has to be in the prompt every single time.

### 5. Read the leak, then decide what to change

Run it once now rather than waiting for Saturday. The first refresh is a test of your access, not your marketing: it tells you whether the key works, whether the token works, and which boxes you built that no source can fill. Fix those in the folder or on the page, not in the prompt, and run it again. From the second run on, read the page top to bottom once a week, starting with the insight column, because that is where the agent names the stage where numbers fall off most. The page points; you choose. What you do about it is yours, and the agent will show you next Saturday whether it worked.

## Files

| File | What it is |
| --- | --- |
| `FEATURES.md` | Each feature, why it's there, and which part of the prompt to edit to change it |
| `PROMPT.md` | The scheduled task prompt, with `[bracket]` placeholders for your details |
| `native_pull.py` | The pull script: `ga4` mode for the GA4 Data API, `ig` mode for the Meta Graph API, plain JSON out |
| `sources.example.md` | The shape of your sources list, stage by stage, and the one page they feed |

## Shared as-is

This is the digest exactly as it runs for one Fractional COO, with names and IDs taken out. No support, no roadmap. Fork it and make it yours.
