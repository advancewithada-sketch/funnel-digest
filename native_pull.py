#!/usr/bin/env python3
"""native_pull.py: pull last week's numbers straight from the GA4 Data API or the
Meta Graph API and print them as JSON. No third-party connector.

Usage:
  python3 native_pull.py ga4 ga4_key.json PROPERTY_ID [DAYS] > ga4.json
  python3 native_pull.py ig  meta_token.txt IG_USER_ID [DAYS] > ig.json

ga4 mode: DAYS defaults to 7 and sets the primary window. Output always holds the
fixed windows last_7, previous_7, last_30, last_90 and total, plus channels,
sources, landing pages and top pages for the primary window.

ig mode: DAYS defaults to 30 and is capped at 30 (Meta caps account insights at
30 days). Output holds followers plus reach, accounts engaged, interactions,
saves, shares and views for the last 7 days and for DAYS.

On any failure this prints {"error": "..."} to stdout and exits 1, so the agent
keeps last week's figure and marks it stale instead of guessing.

Requires: pip install google-auth requests
The key file and the token are read from disk and used for the request only.
They are never printed or written anywhere by this script.
"""
import datetime as dt
import json
import sys

try:
    import requests
except ImportError:
    print(json.dumps({"error": "missing dependency: pip install google-auth requests"}))
    sys.exit(1)

GA4_METRICS = ["sessions", "totalUsers", "newUsers", "screenPageViews", "engagedSessions", "keyEvents"]
GA4_EPOCH = "2015-08-14"  # earliest date the GA4 Data API accepts
IG_METRICS = ["reach", "accounts_engaged", "total_interactions", "saves", "shares", "views"]
GRAPH = "https://graph.facebook.com/v21.0"


def fail(msg):
    print(json.dumps({"error": str(msg)}))
    sys.exit(1)


def iso(d):
    return d.strftime("%Y-%m-%d")


# ---------------------------------------------------------------- GA4 ------


def ga4_token(key_path):
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request

    creds = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    creds.refresh(Request())
    return creds.token


def ga4_report(token, prop, start, end, dimensions=None, limit=None):
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "metrics": [{"name": m} for m in GA4_METRICS],
    }
    if dimensions:
        body["dimensions"] = [{"name": d} for d in dimensions]
        body["orderBys"] = [{"metric": {"metricName": "sessions"}, "desc": True}]
    if limit:
        body["limit"] = limit
    r = requests.post(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport",
        headers={"Authorization": f"Bearer {token}"},
        json=body,
        timeout=60,
    )
    if r.status_code != 200:
        raise RuntimeError(f"GA4 {r.status_code}: {r.text[:200]}")
    return r.json()


def ga4_totals(rep):
    rows = rep.get("rows") or []
    if not rows:
        return {m: 0 for m in GA4_METRICS}
    vals = rows[0]["metricValues"]
    return {m: _num(v["value"]) for m, v in zip(GA4_METRICS, vals)}


def ga4_rows(rep, dim):
    out = []
    for row in rep.get("rows") or []:
        item = {dim: row["dimensionValues"][0]["value"]}
        item.update({m: _num(v["value"]) for m, v in zip(GA4_METRICS, row["metricValues"])})
        out.append(item)
    return out


def _num(s):
    try:
        f = float(s)
        return int(f) if f.is_integer() else f
    except ValueError:
        return s


def run_ga4(key_path, prop, days):
    token = ga4_token(key_path)
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=1)

    def window(n, end=yesterday):
        return iso(end - dt.timedelta(days=n - 1)), iso(end)

    p_start, p_end = window(days)
    prev_end = yesterday - dt.timedelta(days=days)
    windows = {
        f"last_{days}": (p_start, p_end),
        f"previous_{days}": window(days, prev_end),
        "last_7": window(7),
        "previous_7": window(7, yesterday - dt.timedelta(days=7)),
        "last_30": window(30),
        "last_90": window(90),
        "total": (GA4_EPOCH, iso(yesterday)),
    }
    out = {"source": "GA4 (native)", "property": str(prop), "pulled": iso(today), "windows": {}}
    for name, (s, e) in windows.items():
        out["windows"][name] = {"start": s, "end": e, **ga4_totals(ga4_report(token, prop, s, e))}
    breakdowns = {
        "channels": "sessionDefaultChannelGroup",
        "sources": "sessionSource",
        "landing_pages": "landingPage",
        "top_pages": "pagePath",
    }
    out["week"] = {"start": p_start, "end": p_end}
    for key, dim in breakdowns.items():
        out["week"][key] = ga4_rows(ga4_report(token, prop, p_start, p_end, [dim], 15), dim)
    return out


# ---------------------------------------------------------------- IG -------


def ig_get(path, token, **params):
    params["access_token"] = token
    r = requests.get(f"{GRAPH}/{path}", params=params, timeout=60)
    data = r.json()
    if r.status_code != 200 or "error" in data:
        err = data.get("error", {})
        raise RuntimeError(f"Meta {r.status_code}: {err.get('message', r.text[:200])}")
    return data


def ig_window(token, user_id, days):
    until = dt.datetime.combine(dt.date.today(), dt.time.min)
    since = until - dt.timedelta(days=days)
    out = {"days": days, "start": iso(since.date()), "end": iso((until - dt.timedelta(days=1)).date())}
    data = ig_get(
        f"{user_id}/insights",
        token,
        metric=",".join(IG_METRICS),
        period="day",
        metric_type="total_value",
        since=int(since.timestamp()),
        until=int(until.timestamp()),
    )
    for item in data.get("data", []):
        out[item["name"]] = item.get("total_value", {}).get("value")
    return out


def run_ig(token_path, user_id, days):
    with open(token_path) as f:
        token = f.read().strip()
    if not token:
        raise RuntimeError("token file is empty")
    days = max(1, min(int(days), 30))
    acct = ig_get(user_id, token, fields="username,followers_count,media_count")
    out = {
        "source": "Instagram (native)",
        "pulled": iso(dt.date.today()),
        "followers": acct.get("followers_count"),
        "posts": acct.get("media_count"),
        "note": "Meta caps account insights at 30 days; quarter and total are n/a",
        "last_7": ig_window(token, user_id, 7),
    }
    if days != 7:
        out[f"last_{days}"] = ig_window(token, user_id, days)
    return out


# ---------------------------------------------------------------- main -----


def main(argv):
    if len(argv) < 4 or argv[1] not in ("ga4", "ig"):
        fail("usage: native_pull.py ga4 KEY.json PROPERTY_ID [DAYS] | ig TOKEN.txt IG_USER_ID [DAYS]")
    mode, cred, ident = argv[1], argv[2], argv[3]
    days = argv[4] if len(argv) > 4 else ("7" if mode == "ga4" else "30")
    try:
        days = int(days)
        result = run_ga4(cred, ident, days) if mode == "ga4" else run_ig(cred, ident, days)
    except Exception as e:  # noqa: BLE001
        fail(e)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main(sys.argv)
