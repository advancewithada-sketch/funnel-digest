# Sources and the one page they feed (example)

Step 1 of the guide: write down each place your audience comes from, which funnel stage it belongs to, and how the agent gets its number. Then one page where every number lands. Not four pages. One.

Two kinds of source:

- **Native**: has an API you can use yourself. Pulled live by `native_pull.py` (GA4, Instagram through Meta) or a connector (most email software, ads accounts). Labelled e.g. "GA4 (native)", "Instagram (native)".
- **Browser read**: easier to read from the platform's own analytics page (Pinterest, TikTok, LinkedIn, Substack). Copied exactly, with the platform's own labels and period, labelled "(browser read)". Never turned into a trend.

| Stage | Source | How the number arrives | Label on the page |
| --- | --- | --- | --- |
| Attract | Website | `native_pull.py ga4` | GA4 (native) |
| Attract | Instagram | `native_pull.py ig` | Instagram (native) |
| Attract | Pinterest | saved stats, read within the last 3 days | (browser read) |
| Attract | TikTok | saved stats, read within the last 3 days | (browser read) |
| Attract | Paid ads, [YOUR CAMPAIGN NAME] only | ads connector | [your ads platform] |
| Capture | [free call / masterclass / pricing guide] | email platform connector | [your email platform] |
| Nurture | [your email automations] | email platform connector | [your email platform] |
| Convert | [calls booked / sales] | [where you count them] | [source] |
| Keep and Refer | [no referral automation yet] | GAP, say so in a box | n/a |

## The one page

- Name: [YOUR DASHBOARD NAME]
- Lives at: [WHERE YOUR DASHBOARD PAGE LIVES]
- Title block carries a "week of" date range that the agent moves every Saturday.
- Funnel columns across the top: Attract, Capture, Nurture, Convert, Keep and Refer. One box per source or offer inside each column.
- KPI table underneath with six columns: KPI | This week | This month | This quarter | Total | Insight.
- Boxes do not come and go. Known gaps get a box that says so.

## The private folder (step 2)

Three files, in one private folder the agent can fetch from and nowhere else:

- `native_pull.py` (this repo)
- `ga4_key.json`: Google service-account key, read access to your GA4 property only
- `meta_token.txt`: Meta system-user token, read access to your Instagram insights only

IDs to have ready: [YOUR GA4 PROPERTY ID], [YOUR INSTAGRAM USER ID], [YOUR SLACK DM CHANNEL ID].
