"""Generate per-exercise architecture, flowchart, and data-backed PNG figures."""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "exercises"

TITLES = {
    1: "Lottery ticket pool and proportional share",
    2: "Lottery / EDF / RM decision paths",
    3: "Manual ticket interval mapping",
    4: "Synchronization around shared draw state",
    5: "Semaphore and monitor execution demonstration",
    6: "Research evidence to seminar synthesis",
    7: "Readers-writers phase arbitration",
    8: "Dining philosophers with eligible-resource lottery",
}
ARCHITECTURE = {
    1: ["Task definitions: PID, tickets, burst and arrival", "Ready queue excludes jobs not yet arrived", "Ticket table creates disjoint cumulative intervals", "Uniform draw selects one interval owner", "Selected task receives one quantum; metrics update"],
    2: ["One common workload with arrival, burst, deadline and period", "Lottery branch uses ticket counts and seeded draws", "EDF branch orders ready jobs by absolute deadline", "RM branch orders ready jobs by fixed period priority", "Common trace metrics expose share and deadline trade-offs"],
    3: ["Ticket pool: P1=5, P2=3, P3=2", "Cumulative intervals: 1-5, 6-8 and 9-10", "Seeded random ticket is drawn from 1 through 10", "The interval containing the draw identifies the winner", "Fifteen decisions are written as a paper-checkable table"],
    4: ["Worker threads request access to shared lottery state", "Semaphore or Condition/Monitor protects the critical section", "One protected draw reads the random generator", "Winner counter and trace are updated atomically", "The invariant checks total recorded draws against completed work"],
    5: ["Concurrent workers submit draw requests", "Semaphore and Monitor provide two protection variants", "The lottery maps each random ticket to a process interval", "Trace records the winner and updated count", "A GIF visualizes the first 24 events of the recorded trace"],
    6: ["Primary OSDI 1994 paper supplies the research claims", "Base weighted-lottery mechanism is separated from extensions", "A seeded 5,000-draw experiment produces share estimates", "Limitations distinguish proportional share from hard deadlines", "The evidence is summarized in a 12-slide seminar deck"],
    7: ["Reader and writer requests wait with individual tickets", "Aggregate ticket counts determine reader- or writer-phase odds", "Reader phase admits the waiting reader cohort", "Writer phase admits one writer exclusively", "The trace compares preference policies and lottery phases"],
    8: ["Philosophers request a meal and own a base ticket weight", "Admission gate allows at most N-1 philosophers in the room", "Eligible set requires both adjacent forks to be free", "Lottery plus wait-aging chooses among eligible philosophers", "Fork pair is reserved atomically; meal ends and resources release"],
}
FLOW = {
    1: ["Validate positive ticket counts and a non-empty task set", "Build the ready set and compute total tickets T", "Draw an unbiased integer r in [1, T]", "Walk cumulative intervals until r is covered", "Run winner, update remaining burst and repeat"],
    2: ["Freeze one task set and its scheduling parameters", "Run Lottery with fixed seed and quantum", "Run preemptive EDF using earliest absolute deadline", "Run fixed-priority RM using shortest period", "Compare waiting, response, turnaround and deadline misses"],
    3: ["Write each process ticket count on paper", "Construct cumulative ticket intervals", "Read the seeded draw number for a decision", "Mark the interval containing that number", "Record winner and update the final win-frequency table"],
    4: ["Start worker threads and initialize shared counters", "Enter the critical section through Semaphore or Monitor", "Draw ticket and locate its interval owner", "Update winner counter and append trace event", "Release / notify; verify that all 2,000 draws were recorded"],
    5: ["Start the synchronized demonstration workers", "Acquire semaphore permit or enter the monitor", "Execute weighted ticket selection", "Record the winning resource and update counters", "Release protection and render the event trace as an animation"],
    6: ["Read the original Lottery Scheduling research paper", "Extract model, proportional-share claim and extensions", "Run the reproducible local ticket-share experiment", "Contrast evidence with EDF/RM and state limits", "Build the seminar narrative and cite the primary source"],
    7: ["Collect pending reader and writer requests", "Sum the tickets waiting in each request class", "Apply reader preference, writer preference or lottery phase choice", "Admit a reader cohort or one exclusive writer", "Record service order and inspect safety / starvation caveats"],
    8: ["Mark philosophers hungry and update waiting ages", "Reject philosophers whose adjacent forks are occupied", "Check room capacity N-1 and form eligible lottery pool", "Select by effective tickets and reserve both forks atomically", "Eat for finite time, release forks, then repeat until all meals finish"],
}


def svg_box(title, subtitle, steps, path):
    width, height = 920, 610
    x, box_w, box_h, gap, y = 70, 780, 58, 15, 120
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#31445f"/></marker></defs>',
        '<rect width="100%" height="100%" fill="#f7f9fc"/>',
        f'<text x="460" y="48" text-anchor="middle" font-family="Arial" font-size="25" font-weight="bold" fill="#14213d">{escape(title)}</text>',
        f'<text x="460" y="82" text-anchor="middle" font-family="Arial" font-size="14" fill="#49566a">{escape(subtitle)}</text>',
    ]
    for i, label in enumerate(steps):
        yy = y + i * (box_h + gap)
        fill = ["#dceeff", "#e5f3ed", "#fff0d8", "#f0e8ff", "#e7edf4"][i % 5]
        parts.append(f'<rect x="{x}" y="{yy}" width="{box_w}" height="{box_h}" rx="12" fill="{fill}" stroke="#59718f" stroke-width="1.5"/>')
        parts.append(f'<text x="460" y="{yy+36}" text-anchor="middle" font-family="Arial" font-size="16" fill="#152238">{escape(label)}</text>')
        if i < len(steps) - 1:
            parts.append(f'<path d="M460 {yy+box_h} L460 {yy+box_h+gap-2}" stroke="#31445f" stroke-width="2" fill="none" marker-end="url(#arrow)"/>')
    parts.append('</svg>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts), encoding="utf-8")


def draw_results(number, result, path):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    if number in (1, 6):
        data = result.get("shares", {})
        names = list(data)
        expected = [100 * data[n]["expected_share"] for n in names]
        observed = [100 * data[n]["observed_share"] for n in names]
        x = range(len(names))
        ax.bar([i - .18 for i in x], expected, width=.36, label="Expected share")
        ax.bar([i + .18 for i in x], observed, width=.36, label="Observed share")
        ax.set_xticks(list(x), names)
        ax.set_ylabel("Share (%)")
        ax.legend()
    elif number == 2:
        policies = list(result["results"])
        waits = [sum(m["waiting"] for m in result["results"][p]["metrics"].values()) / len(result["results"][p]["metrics"]) for p in policies]
        misses = [sum(bool(m["deadline_missed"]) for m in result["results"][p]["metrics"].values()) for p in policies]
        bars = ax.bar(policies, waits)
        ax.set_ylabel("Mean waiting time (ticks)")
        for bar, count in zip(bars, misses):
            ax.annotate(f"deadline misses: {count}", (bar.get_x() + bar.get_width()/2, bar.get_height()),
                        xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8)
    elif number == 3:
        rows = result["draws"][:15]
        ax.bar(range(1, len(rows) + 1), [r["draw"] for r in rows])
        ax.set_xlabel("Draw number")
        ax.set_ylabel("Winning ticket number (1–10)")
        ax.set_xticks(range(1, len(rows)+1))
    elif number in (4, 5):
        vals = result.get("runs", {}) if number == 4 else {"semaphore": result["semaphore"], "monitor": result["monitor"]}
        modes = list(vals)
        names = list(next(iter(vals.values()))["counts"])
        x = range(len(names))
        width = .8 / len(modes)
        for i, mode in enumerate(modes):
            ax.bar([q - width * len(modes)/2 + i*width + width/2 for q in x],
                   [vals[mode]["counts"][n] for n in names], width=width, label=mode)
        ax.set_xticks(list(x), names)
        ax.set_ylabel("Completed draws")
        ax.legend()
    elif number == 7:
        offsets = {"reader_preference": 0, "writer_preference": 1, "lottery": 2}
        labels = {"reader_preference": "Reader preference", "writer_preference": "Writer preference", "lottery": "Lottery phase"}
        for policy, offset in offsets.items():
            trace = result["runs"][policy]["trace"]
            ax.scatter([t["phase"] for t in trace], [offset] * len(trace), s=42, label=labels[policy])
            for event in trace:
                ax.annotate(event["request"], (event["phase"], offset), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=7)
        ax.set_yticks([0, 1, 2], ["Reader preference", "Writer preference", "Lottery phase"])
        ax.set_xlabel("Service phase")
    elif number == 8:
        starts = [e for e in result["trace"] if e["action"] == "eat_start"]
        for event in starts:
            ax.barh(event["philosopher"], 2, left=event["time"], height=.55)
        ax.set_yticks(range(5), [f"P{i}" for i in range(5)])
        ax.set_xlabel("Simulation time (ticks)")
        ax.set_ylabel("Philosopher")
    ax.set_title(f"Exercise {number} — generated experiment output")
    ax.grid(axis="y", alpha=.22)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=170)
    plt.close(fig)


def generate():
    folders = sorted(EX.glob("exercise_*"))
    for folder in folders:
        number = int(folder.name.split("_")[1].split("-")[0])
        result = json.loads((folder / "outputs" / "results.json").read_text(encoding="utf-8"))
        figdir = folder / "docs" / "figures"
        svg_box(f"Exercise {number} — {TITLES[number]}", "Lottery Scheduling • exercise-specific architecture",
                ARCHITECTURE[number], figdir / "architecture.svg")
        svg_box(f"Exercise {number} — execution flow", "Exercise-specific control flow",
                FLOW[number], figdir / "flowchart.svg")
        draw_results(number, result, figdir / "results.png")


if __name__ == "__main__":
    generate()
