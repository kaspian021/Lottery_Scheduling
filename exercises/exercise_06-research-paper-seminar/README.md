# تمرین 6 — مقاله و سمینار درباره Lottery Scheduling

**عنوان انگلیسی:** Research Paper and Seminar on Lottery Scheduling  
**الگوریتم محوری:** Lottery Scheduling  
**هدف:** تحلیل مقالهٔ اصلی Waldspurger و Weihl، مزایا، currency، ticket transfer، محدودیت‌ها و ارائهٔ کلاسی.

## راهنمای تصویری

![معماری تمرین](docs/figures/architecture.svg)

![فلوچارت اجرای تمرین](docs/figures/flowchart.svg)

![نمودار نتایج تولیدشده از اجرای کد](docs/figures/results.png)

## اجرا

از ریشهٔ مخزن:

```bash
pip install -r requirements.txt
python exercises/exercise_06-research-paper-seminar/src/run.py
python -m pytest exercises/exercise_06-research-paper-seminar/tests -q
```

خروجی در `outputs/results.json` ذخیره می‌شود. توضیح علمی، سناریو، محدودیت و تفسیر نمودارها در [راهنمای docs](docs/README.md) آمده است.

## ساختار پوشه

```text
exercises/exercise_06-research-paper-seminar/
├── README.md
├── src/run.py
├── tests/test_exercise_06.py
├── docs/README.md
├── docs/figures/ (2 SVG + 1 PNG)
├── docs/reports/report_fa.md
├── docs/reports/report_en.md
└── outputs/results.json
```

## نتیجه و محدودیت

تحلیل مقالهٔ اصلی Waldspurger و Weihl، مزایا، currency، ticket transfer، محدودیت‌ها و ارائهٔ کلاسی. نتیجه‌ها برای سناریو و seed ثبت‌شده معتبرند؛ آن‌ها را به همهٔ بارهای کاری یا به زمان‌بند kernel تعمیم ندهید.
