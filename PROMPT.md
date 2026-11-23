# The Weekly Funnel Digest: scheduled task prompt

Paste this as the prompt of a Claude Code scheduled task (step 4 of the guide) with every `[bracket]` filled: where your three files live, your GA4 property ID, your Instagram account ID, where the page lives, and your Slack DM channel for the rare alert. Set it for Saturday morning in your timezone. Same prompt as on the guide page: https://www.theoptimized.ceo/guides/funnel-digest

```
You are refreshing a live marketing dashboard called "[YOUR DASHBOARD NAME]" for [YOUR NAME] ([YOUR BUSINESS], [YOUR WEBSITE]). This is a fresh session with no memory of prior runs.

GOAL: Re-pull last week's numbers from the sources below, then update the SAME dashboard page in place at [WHERE YOUR DASHBOARD PAGE LIVES]. Read the current page first and edit it. Never rebuild it from scratch, never create a second copy.

SETUP (native pulls, no third-party connector):
a) bash: pip install --break-system-packages -q google-auth requests
b) Fetch three private files from [WHERE YOU KEEP THEM]: native_pull.py, ga4_key.json (your GA4 service-account key) and meta_token.txt (your Meta reporting token). Write each straight to a scratch file and chmod 600 the two secrets. Never print, log, message, publish or store their contents.
c) bash: python3 native_pull.py ga4 ga4_key.json [YOUR GA4 PROPERTY ID] > ga4.json. Windows: last 7 days, previous 7, last 30, last 90 and total, plus top pages for the week.
d) bash: python3 native_pull.py ig meta_token.txt [YOUR INSTAGRAM USER ID] 30 > ig.json. Followers, reach, accounts engaged and interactions for the last 7 and 30 days (Meta caps these windows at 30 days).
e) If a pull prints {"error": ...}, keep that source's previous numbers, mark them "stale since <date>: <short error>" on the page, and tell me (step 5). Never guess a number.
f) [PLATFORMS WITHOUT AN API YOU CAN USE, e.g. LinkedIn, TikTok, Pinterest, Substack]: read the latest saved stats from [WHERE YOU SAVE THEM], only if saved within the last 3 days. For each platform marked "ok", show its 2-3 most useful metrics with the platform's own labels and period, labelled "(browser read)". Otherwise keep the previous state and add one honest status line. Copy values exactly; never compute a trend from them.

STEP 1: read the current page before editing anything.

STEP 2: keep the structure. Funnel columns (Attract, Capture, Nurture, Convert, Keep and Refer) and a KPI table with columns KPI | This week | This month | This quarter | Total | Insight. Do not add or remove boxes. Label every source by where the number came from, e.g. "GA4 (native)", "Instagram (native)".

STEP 3: data to refresh (pull live, never reuse old numbers):
1. Email platform: total and active subscribers; sends, open rate, unsubscribe rate and bounce rate; subscribers added in the last 7 days.
2. Instagram (ig.json): followers, reach and accounts engaged for 7 and 30 days.
3. GA4 (ga4.json): sessions, users and views for 7, 30 and 90 days and total. Say plainly if these are still identical because the property is new. Refresh the top pages list and the stats for [YOUR KEY LANDING PAGE].
4. Paid ads, if any: spend, impressions, clicks and CTR for the last 7 days for [YOUR CAMPAIGN NAME] only. If the connector needs reconnecting, say so on the page rather than guessing.
5. Other platforms per setup step f.

STEP 4: apply the numbers everywhere they appear: funnel boxes, every column of the KPI table, and the notes in prose. Update the "week of" date range. Where windows are identical, say so and why; never fabricate variation. Instagram quarter and total cells show "n/a (Meta caps at 30 days)" unless you have a real figure. In the Insight column write one plain line per row, and name the stage where numbers fall off most from one step of the funnel to the next.

STEP 5: save the edited page in place. Never put any token or key into the page. Message me (Slack DM, channel_id [YOUR SLACK DM CHANNEL ID]) only if something broke or moved sharply. A routine refresh needs no message.

STEP 6: write one log entry: date, status ok | warning | failed, one line on what was refreshed, and anything stale or broken.
```
