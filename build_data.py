#!/usr/bin/env python3
"""Pulls all verified FRED series, computes threshold/percentile context, writes dashboard-data.json.
Meant to be re-run on a schedule (weekly) to refresh the live artifact's data."""
import json
import urllib.request
import datetime
import sys
from series_config import SERIES

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
LOOKBACK_YEARS = 20
PCTL_YEARS = 10


def fetch_series(series_id):
    url = FRED_CSV.format(series_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8")
    rows = []
    for line in text.strip().splitlines()[1:]:
        parts = line.split(",")
        if len(parts) != 2:
            continue
        date_str, val_str = parts
        if val_str.strip() in (".", ""):
            continue
        try:
            rows.append((date_str, float(val_str)))
        except ValueError:
            continue
    return rows


def percentile_rank(value, values):
    if not values:
        return None
    below = sum(1 for v in values if v <= value)
    return round(100 * below / len(values), 1)


def month_key(date_str):
    return date_str[:7]  # "YYYY-MM"


def build_cpi_lookup(cpi_rows):
    """month -> CPI value, plus the latest (most recent) CPI value for rebasing."""
    lookup = {}
    for d, v in cpi_rows:
        lookup[month_key(d)] = v
    latest_cpi = cpi_rows[-1][1]
    return lookup, latest_cpi


def nearest_cpi(lookup, mkey, sorted_months):
    if mkey in lookup:
        return lookup[mkey]
    # fall back to the closest earlier month (weekly series like GASREGW can
    # land a few days into a month FRED hasn't posted CPI for yet)
    earlier = [m for m in sorted_months if m <= mkey]
    return lookup[earlier[-1]] if earlier else lookup[sorted_months[0]]


def process_series(meta, cpi_lookup=None, cpi_sorted_months=None, latest_cpi=None):
    sid = meta["id"]
    try:
        rows = fetch_series(sid)
    except Exception as e:
        print(f"  FAILED {sid}: {e}", file=sys.stderr)
        return None
    if not rows:
        print(f"  EMPTY {sid}", file=sys.stderr)
        return None

    last_date = datetime.datetime.strptime(rows[-1][0], "%Y-%m-%d").date()
    cutoff_chart = last_date - datetime.timedelta(days=365 * LOOKBACK_YEARS)
    cutoff_pctl = last_date - datetime.timedelta(days=365 * PCTL_YEARS)

    chart_rows = [(d, v) for d, v in rows if datetime.datetime.strptime(d, "%Y-%m-%d").date() >= cutoff_chart]
    pctl_rows = [v for d, v in rows if datetime.datetime.strptime(d, "%Y-%m-%d").date() >= cutoff_pctl]
    if len(pctl_rows) < 8:
        pctl_rows = [v for _, v in rows]

    latest_date, latest_value = rows[-1]
    ten_yr_min = min(pctl_rows)
    ten_yr_max = max(pctl_rows)
    pctl = percentile_rank(latest_value, pctl_rows)

    result = {
        "id": sid,
        "label": meta["label"],
        "category": meta["category"],
        "unit": meta["unit"],
        "higher_is_worse": meta["higher_is_worse"],
        "threshold": meta["threshold"],
        "latest_value": latest_value,
        "latest_date": latest_date,
        "ten_yr_min": ten_yr_min,
        "ten_yr_max": ten_yr_max,
        "percentile_10yr": pctl,
        "data": [{"d": d, "v": v} for d, v in chart_rows],
    }

    if meta.get("deflate") and cpi_lookup:
        real_rows = []
        for d, v in chart_rows:
            cpi_at_date = nearest_cpi(cpi_lookup, month_key(d), cpi_sorted_months)
            real_rows.append({"d": d, "v": round(v * (latest_cpi / cpi_at_date), 4)})
        result["real_data"] = real_rows
        result["real_latest_value"] = real_rows[-1]["v"]
        cpi_first = nearest_cpi(cpi_lookup, month_key(chart_rows[0][0]), cpi_sorted_months)
        nominal_change_pct = (chart_rows[-1][1] / chart_rows[0][1] - 1) * 100
        inflation_change_pct = (latest_cpi / cpi_first - 1) * 100
        result["above_inflation_pct"] = round(nominal_change_pct - inflation_change_pct, 1)
        result["chart_span_years"] = round((last_date - datetime.datetime.strptime(chart_rows[0][0], "%Y-%m-%d").date()).days / 365, 1)

        # Status/percentile must be scored off the REAL series, not nominal --
        # nominal prices trend up almost monotonically from inflation alone,
        # which would falsely mark nearly every price series "critical" every year.
        real_pctl_rows = [r["v"] for r in real_rows if datetime.datetime.strptime(r["d"], "%Y-%m-%d").date() >= cutoff_pctl]
        if len(real_pctl_rows) < 8:
            real_pctl_rows = [r["v"] for r in real_rows]
        result["ten_yr_min"] = min(real_pctl_rows)
        result["ten_yr_max"] = max(real_pctl_rows)
        result["percentile_10yr"] = percentile_rank(result["real_latest_value"], real_pctl_rows)

    return result


def main():
    out = {"generated_at": datetime.datetime.utcnow().isoformat() + "Z", "series": []}
    failed = []

    print("Fetching CPIAUCNS (inflation deflator)...")
    cpi_rows = fetch_series("CPIAUCNS")
    cpi_lookup, latest_cpi = build_cpi_lookup(cpi_rows)
    cpi_sorted_months = sorted(cpi_lookup.keys())

    for meta in SERIES:
        print(f"Fetching {meta['id']} ({meta['label']})...")
        result = process_series(meta, cpi_lookup, cpi_sorted_months, latest_cpi)
        if result is None:
            failed.append(meta["id"])
            continue
        out["series"].append(result)

    with open("data/dashboard-data.json", "w") as f:
        json.dump(out, f, separators=(",", ":"))

    print(f"\nDone. {len(out['series'])}/{len(SERIES)} series written.")
    if failed:
        print(f"FAILED: {failed}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
