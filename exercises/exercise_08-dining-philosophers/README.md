# تمرین 8 — فیلسوفان غذاخور: بن‌بست و گرسنگی زیر سیاست Lottery

**عنوان انگلیسی:** Dining Philosophers: Deadlock and Starvation under Lottery  
**الگوریتم محوری:** Lottery Scheduling  
**هدف:** استفاده از بلیت برای انتخاب فیلسوفِ مجاز، جلوگیری از بن‌بست و تحلیل محدودیت گرسنگی.

## راهنمای تصویری

![معماری تمرین](docs/figures/architecture.svg)

![فلوچارت اجرای تمرین](docs/figures/flowchart.svg)

![نمودار نتایج تولیدشده از اجرای کد](docs/figures/results.png)

## اجرا

از ریشهٔ مخزن:

```bash
pip install -r requirements.txt
python exercises/exercise_08-dining-philosophers/src/run.py
python -m pytest exercises/exercise_08-dining-philosophers/tests -q
```

خروجی در `outputs/results.json` ذخیره می‌شود. توضیح علمی، سناریو، محدودیت و تفسیر نمودارها در [راهنمای docs](docs/README.md) آمده است.

## ساختار پوشه

```text
exercises/exercise_08-dining-philosophers/
├── README.md
├── src/run.py
├── tests/test_exercise_08.py
├── docs/README.md
├── docs/figures/ (2 SVG + 1 PNG)
├── docs/reports/report_fa.md
├── docs/reports/report_en.md
└── outputs/results.json
```

## نتیجه و محدودیت

استفاده از بلیت برای انتخاب فیلسوفِ مجاز، جلوگیری از بن‌بست و تحلیل محدودیت گرسنگی. نتیجه‌ها برای سناریو و seed ثبت‌شده معتبرند؛ آن‌ها را به همهٔ بارهای کاری یا به زمان‌بند kernel تعمیم ندهید.
