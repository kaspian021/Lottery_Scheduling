import csv
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from shared.experiments import run_exercise

def main():
    result = run_exercise(3)
    out_dir = ROOT / "exercises/exercise_03-manual-lottery-trace" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out_dir / "manual_draws.csv").open("w", newline="", encoding="utf-8") as stream:
        fields = ["decision", "draw", "total_tickets", "winner", "interval_low", "interval_high"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in result["draws"]:
            writer.writerow({field: row[field] for field in fields})
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
