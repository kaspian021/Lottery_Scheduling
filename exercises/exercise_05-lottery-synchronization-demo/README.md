# تمرین 5 — نمایش اجرای Lottery با Semaphore و Monitor

**عنوان انگلیسی:** Lottery Synchronization Demonstration  
**الگوریتم محوری:** Lottery Scheduling  
**هدف:** ساخت trace و تصویر مرحله‌ای از انتخاب بلیت و حفاظت هم‌زمانی با Semaphore/Monitor.

## راهنمای تصویری

![معماری تمرین](docs/figures/architecture.svg)

![فلوچارت اجرای تمرین](docs/figures/flowchart.svg)

![نمودار نتایج تولیدشده از اجرای کد](docs/figures/results.png)

## اجرا

از ریشهٔ مخزن:

```bash
pip install -r requirements.txt
python exercises/exercise_05-lottery-synchronization-demo/src/run.py
python -m pytest exercises/exercise_05-lottery-synchronization-demo/tests -q
```

خروجی در `outputs/results.json` ذخیره می‌شود. توضیح علمی، سناریو، محدودیت و تفسیر نمودارها در [راهنمای docs](docs/README.md) آمده است.

## ساختار پوشه

```text
exercises/exercise_05-lottery-synchronization-demo/
├── README.md
├── src/run.py
├── tests/test_exercise_05.py
├── docs/README.md
├── docs/figures/ (2 SVG + 1 PNG)
├── docs/reports/report_fa.md
├── docs/reports/report_en.md
└── outputs/results.json
```

## نتیجه و محدودیت

ساخت trace و تصویر مرحله‌ای از انتخاب بلیت و حفاظت هم‌زمانی با Semaphore/Monitor. نتیجه‌ها برای سناریو و seed ثبت‌شده معتبرند؛ آن‌ها را به همهٔ بارهای کاری یا به زمان‌بند kernel تعمیم ندهید.
