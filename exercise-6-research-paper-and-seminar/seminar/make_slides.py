#!/usr/bin/env python3
"""Build a concise editable seminar deck for the Lottery Scheduling research paper."""
from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "output" / "scheduler_comparison.json"
OUT = ROOT / "docs" / "Lottery_Scheduling_Seminar.pptx"
NAVY = RGBColor(31, 56, 100)
BLUE = RGBColor(47, 84, 150)
GRAY = RGBColor(85, 85, 85)


def add_title(slide, title: str, subtitle: str = "") -> None:
    box = slide.shapes.add_textbox(Inches(0.55), Inches(0.35), Inches(12.2), Inches(0.8))
    p = box.text_frame.paragraphs[0]
    p.text = title
    p.font.name = "Aptos Display"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = NAVY
    if subtitle:
        sub = slide.shapes.add_textbox(Inches(0.6), Inches(1.12), Inches(12), Inches(0.45))
        p2 = sub.text_frame.paragraphs[0]
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = GRAY


def add_bullets(slide, items: list[str], top: float = 1.8) -> None:
    box = slide.shapes.add_textbox(Inches(0.85), Inches(top), Inches(11.7), Inches(5.1))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    for index, item in enumerate(items):
        p = tf.paragraphs[0] if index == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.name = "Aptos"
        p.font.size = Pt(20 if len(items) <= 4 else 17)
        p.font.color.rgb = RGBColor(35, 35, 35)
        p.space_after = Pt(17)


def footer(slide, number: int) -> None:
    box = slide.shapes.add_textbox(Inches(0.55), Inches(7.08), Inches(12.1), Inches(0.22))
    p = box.text_frame.paragraphs[0]
    p.text = f"Operating Systems | Lottery Scheduling | {number}"
    p.font.size = Pt(9)
    p.font.color.rgb = GRAY
    p.alignment = PP_ALIGN.RIGHT


def add_slide(prs: Presentation, title: str, items: list[str], subtitle: str = "") -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, title, subtitle)
    add_bullets(slide, items)
    footer(slide, len(prs.slides))


def main() -> None:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "Lottery Scheduling", "Flexible proportional-share resource management")
    add_bullets(slide, [
        "Research focus: how randomized tickets allocate a contended resource",
        "Seminar: design, probability, implementation, evidence, and limitations",
        "Anchor paper: Waldspurger & Weihl, OSDI 1994",
    ], top=2.15)
    footer(slide, 1)

    add_slide(prs, "Why proportional share?", [
        "Fixed priority is not the same as an explicit resource-share contract.",
        "Lottery scheduling represents a client's entitlement with tickets.",
        "A ticket draw selects one runnable client for the next allocation quantum.",
        "Expected share is proportional to tickets; a finite sample is not exact.",
    ])
    add_slide(prs, "The allocation rule", [
        "Total tickets T = sum(t_i) over currently runnable clients.",
        "Draw one integer uniformly from 1 through T.",
        "The owner of the winning ticket receives the next quantum.",
        "P(client i wins one draw) = t_i / T.",
    ])
    add_slide(prs, "A small worked example", [
        "P1 owns 5 tickets, P2 owns 3, and P3 owns 2.",
        "Total = 10; expected shares are 50%, 30%, and 20%.",
        "A draw of 7 selects P2 because its ticket interval is 6–8.",
        "The schedule is probabilistic: short windows can deviate from target.",
    ])
    add_slide(prs, "Resource-management extensions", [
        "Ticket transfer: temporarily lend rights to a dependency or server.",
        "Ticket currencies: let modules allocate shares internally.",
        "Compensation tickets: compensate a client that blocks early.",
        "The original paper also discusses locks and resources beyond CPU time.",
    ])
    add_slide(prs, "Experimental method", [
        f"Ticket vector: {results['workload']['tickets']}",
        f"Lottery runs: {results['workload']['seeds']} independent seeds",
        f"Decisions per run: {results['workload']['decisions_per_run']:,}",
        "Metric: maximum absolute deviation from each target share.",
        "Model: one CPU, equal quanta, all processes continuously runnable.",
    ])
    add_slide(prs, "Measured comparison", [
        f"Lottery mean worst-share error: {results['lottery']['mean_max_absolute_share_error']:.4f}",
        f"Lottery worst seed error: {results['lottery']['worst_max_absolute_share_error']:.4f}",
        f"Stride observed shares: {results['stride']['observed_shares']}",
        f"Stride maximum error: {results['stride']['max_absolute_share_error']:.4f}",
        "Stride is deterministic in this model; its result depends on tie-breaking and quantum count.",
    ])
    add_slide(prs, "Lottery and stride are not identical", [
        "Lottery: randomized, responsive to ticket changes, statistical short-term variation.",
        "Stride: deterministic virtual-time accounting, typically lower allocation variance.",
        "Neither result alone measures latency, context-switch overhead, or multicore behavior.",
        "A fair comparison must state the workload and metric.",
    ])
    add_slide(prs, "Synchronization connection", [
        "The OSDI paper generalizes lottery rights to mutex/lock acquisition.",
        "This repository's Exercise 5 demonstrates a weighted lottery lock.",
        "The lock still needs a correct queue, ownership invariant, and wake-up protocol.",
        "Ticket weights do not automatically imply FIFO or a hard starvation bound.",
    ])
    add_slide(prs, "Limitations and conclusions", [
        "Lottery scheduling provides probabilistic proportional fairness, not hard deadlines.",
        "A fixed seed makes experiments repeatable; it does not make the algorithm deterministic in deployment.",
        "Use EDF/RM for real-time deadline analysis; use lottery for proportional allocation.",
        "Report expected shares, observed error, workload assumptions, and run-to-run variation.",
    ])
    add_slide(prs, "References", [
        "Waldspurger & Weihl (1994), Lottery Scheduling, OSDI '94.",
        "Waldspurger (1995), Lottery and Stride Scheduling, MIT-LCS-TR-667.",
        "Waldspurger & Weihl (1995), Stride Scheduling, MIT-LCS-TM-528.",
        "Downey, The Little Book of Semaphores, readers-writers and dining philosophers.",
    ])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
