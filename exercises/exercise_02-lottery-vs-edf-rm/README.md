# تمرین 2 — مقایسه Lottery با EDF و RM

**عنوان انگلیسی:** Lottery vs EDF and RM  
**الگوریتم محوری:** Lottery Scheduling  
**هدف:** مقایسهٔ هدف، قاعدهٔ انتخاب، سهم CPU و deadline miss روی یک workload مشترک.

## راهنمای تصویری

![معماری تمرین](docs/figures/architecture.svg)

![فلوچارت اجرای تمرین](docs/figures/flowchart.svg)

![نمودار نتایج تولیدشده از اجرای کد](docs/figures/results.png)

## اجرا

از ریشهٔ مخزن:

```bash
pip install -r requirements.txt
python exercises/exercise_02-lottery-vs-edf-rm/src/run.py
python -m pytest exercises/exercise_02-lottery-vs-edf-rm/tests -q
```

خروجی در `outputs/results.json` ذخیره می‌شود. توضیح علمی، سناریو، محدودیت و تفسیر نمودارها در [راهنمای docs](docs/README.md) آمده است.

## ساختار پوشه

```text
exercises/exercise_02-lottery-vs-edf-rm/
├── README.md
├── src/run.py
├── tests/test_exercise_02.py
├── docs/README.md
├── docs/figures/ (2 SVG + 1 PNG)
├── docs/reports/report_fa.md
├── docs/reports/report_en.md
└── outputs/results.json
```

## نتیجه و محدودیت

مقایسهٔ هدف، قاعدهٔ انتخاب، سهم CPU و deadline miss روی یک workload مشترک. نتیجه‌ها برای سناریو و seed ثبت‌شده معتبرند؛ آن‌ها را به همهٔ بارهای کاری یا به زمان‌بند kernel تعمیم ندهید.
