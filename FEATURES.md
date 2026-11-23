# The Weekly Funnel Digest: features and how to change them

Every feature below is a few lines in [`PROMPT.md`](PROMPT.md). Change the words and you change the behaviour. Run the task once by hand after any edit.

## Pulls straight from Google Analytics, Instagram, Pinterest and TikTok, no Supermetrics

**What it does.** SETUP c) and d) run [`native_pull.py`](native_pull.py) against the GA4 Data API and the Meta Graph API with your own key and token. SETUP f) reads the platforms you don't have an API for (for example Pinterest and TikTok) from stats you saved in the last 3 days, copied exactly and labelled "(browser read)".

**Why it's there.** It replaces a paid connector and a spreadsheet. No third-party connector sits between you and your numbers.

**How to change it.**
- Add a platform with an API: add a mode to `native_pull.py` and a line to SETUP for it, then add it to STEP 3.
- Move a platform from browser read to native: take it out of the SETUP f) list once you have a pull for it.
- Use a connector instead: replace the SETUP line for that source with the connector, and keep the rule in SETUP e) about never guessing a number.
- Drop a source: remove its line from SETUP and STEP 3, and its box from your page.

## Tells you where the funnel is leaking

**What it does.** STEP 4 writes one plain line per row in the Insight column and names the stage where numbers fall off most from one step of the funnel to the next.

**Why it's there.** Once a number knows its stage, a drop between stages becomes visible, and that drop is the leak. The page points; you choose what to change.

**How to change it.**
- Change the stages: edit the funnel columns in STEP 2 and on your page.
- More than one leak: change "name the stage where numbers fall off most" to "name the two stages".
- Turn insights off: delete the Insight sentence in STEP 4 and the Insight column.

## Refreshes the live dashboard every week

**What it does.** The task runs once a week. STEP 1 reads the current page, STEP 4 edits every number in place and moves the "week of" date range, and STEP 5 saves the same page. It never rebuilds the page or makes a second copy.

**Why it's there.** Saturday morning means the week it reports on is fully over. One page means you stop opening four dashboards to find numbers you will forget by Friday.

**How to change it.**
- Change the day: change the schedule on the task.
- Change the windows: edit the windows in SETUP c) and the columns in STEP 2.
- Get a message every week: change "only if something broke or moved sharply" in STEP 5.
