"""Best-effort OS-process Lottery runner using psutil suspend/resume.

This controls user processes from Python; it is not a kernel CPU scheduler.
On platforms where process suspension is unavailable, use the discrete-event
simulator in shared/lottery_scheduler.py instead.
"""
from __future__ import annotations
import random, shlex, subprocess, time
import psutil


def run_commands(entries, quantum: float, seed: int | None = None):
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    if not entries:
        raise ValueError("at least one command is required")
    jobs=[]
    for i, entry in enumerate(entries, 1):
        command = entry.get("command")
        tickets = entry.get("tickets")
        if not isinstance(command, str) or not command.strip():
            raise ValueError("command must be a non-empty string")
        if isinstance(tickets, bool) or not isinstance(tickets, int) or tickets <= 0:
            raise ValueError("tickets must be positive integers")
        argv=shlex.split(command)
        jobs.append({"name":entry.get("name",f"P{i}"),"argv":argv,"tickets":tickets,
                     "process":None,"monitor":None,"cpu_time":0.0,"started":None,
                     "wall_runtime":0.0,"return_code":None,"finished":False,"error":None})
    rng=random.Random(seed)
    start_all=time.perf_counter()
    try:
        for job in jobs:
            job["process"]=subprocess.Popen(job["argv"])
            job["monitor"]=psutil.Process(job["process"].pid)
            # Best-effort initial suspension; a very short program may exit first.
            try: job["monitor"].suspend()
            except (psutil.NoSuchProcess, psutil.AccessDenied): pass
            job["started"]=time.perf_counter()
        while any(not j["finished"] for j in jobs):
            active=[j for j in jobs if not j["finished"]]
            winner=rng.choices(active,weights=[j["tickets"] for j in active],k=1)[0]
            p, mon=winner["process"],winner["monitor"]
            if p.poll() is not None:
                winner["finished"]=True; winner["return_code"]=p.returncode
                winner["wall_runtime"]=time.perf_counter()-winner["started"]
                continue
            try:
                before=mon.cpu_times()
                mon.resume()
                try:
                    p.wait(timeout=quantum)
                    winner["finished"]=True
                except subprocess.TimeoutExpired:
                    mon.suspend()
                after=mon.cpu_times() if mon.is_running() else before
                winner["cpu_time"] += max(0.0,(after.user+after.system)-(before.user+before.system))
                if winner["finished"]:
                    winner["return_code"]=p.returncode
                    winner["wall_runtime"]=time.perf_counter()-winner["started"]
            except psutil.NoSuchProcess:
                winner["finished"]=True; winner["return_code"]=p.poll()
                winner["wall_runtime"]=time.perf_counter()-winner["started"]
            except psutil.AccessDenied as exc:
                winner["error"]=str(exc)
                try: p.terminate(); p.wait(timeout=1)
                except Exception: p.kill(); p.wait()
                winner["finished"]=True; winner["return_code"]=p.returncode
                winner["wall_runtime"]=time.perf_counter()-winner["started"]
    finally:
        for job in jobs:
            p,mon=job["process"],job["monitor"]
            if p is not None and p.poll() is None:
                try:
                    if mon is not None and mon.is_running(): mon.resume()
                    p.terminate(); p.wait(timeout=2)
                except (psutil.NoSuchProcess, psutil.AccessDenied, subprocess.TimeoutExpired):
                    p.kill(); p.wait()
                job["finished"]=True; job["return_code"]=p.returncode
    return {"quantum_seconds":quantum,"seed":seed,"elapsed_wall_seconds":time.perf_counter()-start_all,
            "scope_warning":"user-space suspend/resume demonstration; not a kernel scheduler; child-process trees and short-start races may affect precision",
            "jobs":[{k:v for k,v in j.items() if k not in {"process","monitor","argv"}}|{"command":" ".join(j["argv"])} for j in jobs]}
