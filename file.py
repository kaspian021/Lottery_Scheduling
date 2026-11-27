"""Interactive launcher for the best-effort Lottery process runner."""
from shared.process_runner import run_commands
import json


def main():
    try:
        count=int(input("Number of programs: "))
        quantum=float(input("Time quantum (seconds): "))
        if count < 1 or quantum <= 0:
            raise ValueError("program count and quantum must be positive")
        entries=[]
        for i in range(count):
            print(f"\nProgram {i+1}")
            command=input("Executable and arguments: ").strip()
            tickets=int(input("Number of tickets: "))
            if tickets <= 0: raise ValueError("tickets must be positive")
            entries.append({"name":f"P{i+1}","command":command,"tickets":tickets})
        result=run_commands(entries,quantum)
        print(json.dumps(result,indent=2))
    except (ValueError, KeyboardInterrupt) as exc:
        raise SystemExit(f"Input error: {exc}")

if __name__ == "__main__": main()
