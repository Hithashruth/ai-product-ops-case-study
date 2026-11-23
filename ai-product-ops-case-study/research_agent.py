"""Evidence-first research harness for the 100-app landscape.

Usage: python research_agent.py --check-links
No API key is needed for link checking. The seeded record is the reviewed, human-readable
research output; a production enrichment worker belongs between fetch and validate.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "apps.json"
OUT = ROOT / "output"


def load_records():
    records = json.loads(DATA.read_text(encoding="utf-8"))
    required = {"name", "category", "auth", "access", "surface", "mcp", "verdict", "blocker", "evidence"}
    for row in records:
        missing = required - row.keys()
        if missing:
            raise ValueError(f"{row.get('name', 'unnamed')}: missing {sorted(missing)}")
        if not row["evidence"].startswith("https://"):
            raise ValueError(f"{row['name']}: evidence must be an HTTPS official URL")
    return records


def check(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (research-evidence-check/1.0)"}, method="HEAD")
    try:
        with urlopen(request, timeout=15) as response:
            return {"ok": 200 <= response.status < 400, "status": response.status}
    except HTTPError as exc:
        # Some developer portals reject HEAD despite serving GET; retain the status for review.
        return {"ok": False, "status": exc.code, "note": "manual review / retry with browser"}
    except (URLError, TimeoutError) as exc:
        return {"ok": False, "status": None, "note": str(exc.reason) if hasattr(exc, "reason") else type(exc).__name__}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-links", action="store_true", help="HEAD-check every evidence URL")
    args = parser.parse_args()
    rows = load_records()
    print(f"Validated schema: {len(rows)} records")
    if not args.check_links:
        return
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "records": []}
    for i, row in enumerate(rows, 1):
        result = check(row["evidence"])
        report["records"].append({"id": row["id"], "name": row["name"], "url": row["evidence"], **result})
        print(f"[{i:03}/100] {row['name']}: {result.get('status') or 'unreachable'}")
    OUT.mkdir(exist_ok=True)
    target = OUT / "evidence_status.json"
    target.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
