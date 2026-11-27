from pathlib import Path
import json, sys, csv
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared.experiments import RUNNERS
SLUGS={1:"01-introduction",2:"02-lottery-vs-edf-rm",3:"03-manual-lottery-trace",4:"04-synchronization-primitives",5:"05-lottery-synchronization-demo",6:"06-research-paper-seminar",7:"07-readers-writers",8:"08-dining-philosophers"}
for number, runner in RUNNERS.items():
    result=runner()
    folder=next((ROOT/"exercises").glob(f"exercise_{number:02d}-*"))
    out=folder/"outputs"/"results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    if number == 3:
        csv_path = folder / "outputs" / "manual_draws.csv"
        fields = ["decision", "draw", "total_tickets", "winner", "interval_low", "interval_high"]
        with csv_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows({field: row[field] for field in fields} for row in result["draws"])
        print(f"Exercise 3: wrote {csv_path.relative_to(ROOT)}")
    print(f"Exercise {number}: wrote {out.relative_to(ROOT)}")
