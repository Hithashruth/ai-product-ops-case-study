"""Deterministic audit summary for the manually adjudicated verification sample."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
sample = json.loads((ROOT / "data" / "verification_sample.json").read_text(encoding="utf-8"))
total = len(sample)
before = sum(x["first_pass_correct"] for x in sample)
after = sum(x["final_correct"] for x in sample)
print(f"Manual sample: {total} apps")
print(f"First-pass field accuracy: {before}/{total} ({before / total:.0%})")
print(f"After evidence loop: {after}/{total} ({after / total:.0%})")
for row in sample:
    if row["correction"]:
        print(f"- {row['app']}: {row['correction']}")
