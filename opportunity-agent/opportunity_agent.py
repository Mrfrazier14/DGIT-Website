"""Read-only DGIT contract/job discovery using official public APIs."""
import datetime as dt
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
TODAY = dt.datetime.now(dt.timezone.utc).date()


def get_json(url, headers=None):
    request = urllib.request.Request(url, headers=headers or {"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def search_sam():
    key = os.environ.get("SAM_API_KEY")
    if not key:
        return [], "SAM_API_KEY is missing"
    start = TODAY - dt.timedelta(days=14)
    params = {
        "api_key": key,
        "postedFrom": start.strftime("%m/%d/%Y"),
        "postedTo": TODAY.strftime("%m/%d/%Y"),
        "limit": "100",
        "offset": "0",
    }
    url = "https://api.sam.gov/opportunities/v2/search?" + urllib.parse.urlencode(params)
    try:
        data = get_json(url)
    except Exception as exc:
        return [], f"SAM request failed: {type(exc).__name__}. Check the API key and service status."
    matches = []
    for item in data.get("opportunitiesData", []):
        notice_id = item.get("noticeId", "")
        link = item.get("uiLink") or ("https://sam.gov/opp/" + notice_id if notice_id else "")
        matches.append({
            "kind": "Contract", "title": item.get("title", "Untitled"),
            "link": link, "deadline": item.get("responseDeadLine", ""),
            "details": " ".join(str(item.get(k, "")) for k in ("description", "naicsCode", "type")),
        })
    return matches, ""


def search_usajobs():
    key = os.environ.get("USAJOBS_API_KEY")
    email = os.environ.get("USAJOBS_API_EMAIL")
    if not key or not email:
        return [], "USAJOBS_API_KEY or USAJOBS_API_EMAIL is missing"
    params = {"JobCategoryCode": "2210", "RemoteIndicator": "True", "ResultsPerPage": "100"}
    url = "https://data.usajobs.gov/api/search?" + urllib.parse.urlencode(params)
    headers = {"Host": "data.usajobs.gov", "User-Agent": email, "Authorization-Key": key}
    try:
        data = get_json(url, headers)
    except Exception as exc:
        return [], f"USAJOBS request failed: {type(exc).__name__}. Check the API credentials and service status."
    matches = []
    for item in data.get("SearchResult", {}).get("SearchResultItems", []):
        job = item.get("MatchedObjectDescriptor", {})
        matches.append({
            "kind": "Job", "title": job.get("PositionTitle", "Untitled"),
            "link": job.get("PositionURI", ""),
            "deadline": job.get("ApplicationCloseDate", ""),
            "details": job.get("QualificationSummary", ""),
        })
    return matches, ""


def rank(item):
    haystack = (item["title"] + " " + item["details"]).lower()
    matched = [word for word in CONFIG["keywords"] if word.lower() in haystack]
    item["score"] = len(matched)
    item["matched"] = matched
    return item


def main():
    contracts, sam_note = search_sam()
    jobs, jobs_note = search_usajobs()
    results = [rank(item) for item in contracts + jobs]
    results = [item for item in results if item["score"] >= CONFIG["minimum_score"]]
    results.sort(key=lambda item: (-item["score"], item["deadline"] or "~"))
    lines = [f"# DGIT opportunities — {TODAY.isoformat()}", "", CONFIG["focus"], ""]
    if CONFIG["website_url"]:
        lines += [f"Website: {CONFIG['website_url']}", ""]
    for note in (sam_note, jobs_note):
        if note:
            lines += [f"Source status: {note}", ""]
    if not results:
        lines += ["No matches reached the configured score. Check credentials, source status, and filters.", ""]
    for item in results:
        lines += [f"## {item['kind']}: {item['title']}", "",
                  f"Source: {item['link']}", f"Deadline: {item['deadline'] or 'Check source'}",
                  f"Match score: {item['score']} ({', '.join(item['matched'])})", "",
                  "Review: eligibility, location/remote terms, requirements, submission method, and deadline.", ""]
    report = ROOT / "opportunities.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    (ROOT / "opportunities.json").write_text(json.dumps({
        "generated_at": TODAY.isoformat(), "focus": CONFIG["focus"],
        "website_url": CONFIG["website_url"], "source_status": [x for x in (sam_note, jobs_note) if x],
        "opportunities": results,
    }, indent=2), encoding="utf-8")
    print(f"Wrote {len(results)} matches to {report}")


if __name__ == "__main__":
    main()

