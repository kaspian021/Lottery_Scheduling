# راهنمای مستندات تمرین 4

## موضوع و منطق علمی

بررسی race condition روی مولد تصادفی و شمارنده‌ها و مقایسهٔ Semaphore و Monitor.

در Lottery Scheduling، مجموع بلیت‌های پردازه‌های آماده در هر تصمیم محاسبه می‌شود. یک بلیت برنده به‌طور یکنواخت از بازهٔ `1..T` انتخاب می‌شود و پردازه‌ای که بازهٔ تجمعی آن شامل بلیت برنده است، سهم بعدی CPU را دریافت می‌کند. احتمال انتخاب در یک قرعه برابر نسبت بلیت آن پردازه به مجموع بلیت‌های آماده است.

## اجزای پیاده‌سازی

- `src/run.py`: اجرای سناریوی اختصاصی تمرین و ذخیرهٔ JSON.
- `shared/lottery_scheduler.py`: هستهٔ مشترک و قابل‌آزمون زمان‌بند.
- `shared/experiments.py`: تعریف workload و تولید دادهٔ آزمایش.
- `tests/test_exercise_04.py`: کنترل invariantهای اختصاصی تمرین.
- `outputs/results.json`: خروجی واقعی اجرای همین سناریو.

## سناریو و تحلیل خروجی

برای بازتولید:

```bash
python exercises/exercise_04-synchronization-primitives/src/run.py
```

فایل JSON را از نظر seed، تعداد عملیات، ترتیب رویدادها و metricها بررسی کنید. نمودار `results.png` از همان JSON تولید شده است؛ شکل‌های SVG معماری و مسیر تصمیم‌گیری را توضیح می‌دهند و نمودار تزئینی نیستند.

## مزایا، معایب و فرض‌ها

مزیت Lottery، کنترل سادهٔ سهم نسبی با تغییر ticket count است. عیب اصلی، نوسان تصادفی در بازهٔ کوتاه و نبود تضمین ذاتی deadline یا bounded waiting است. نتایج به seed، تعداد drawها، مجموعهٔ پردازه‌های آماده و طول quantum وابسته‌اند.

## شکل‌ها

- `figures/architecture.svg`: اجزای مدل و ارتباط آن‌ها را نشان می‌دهد.
- `figures/flowchart.svg`: ترتیب تصمیم‌گیری از تشکیل مجموعهٔ آماده تا اجرای برنده را نشان می‌دهد.
- `figures/results.png`: نمودار دادهٔ آزمایش که از `outputs/results.json` ساخته شده است.

## گزارش‌ها

- [گزارش فارسی](reports/report_fa.md)
- [English report](reports/report_en.md)

## راهنمای اجرای مجدد و تست

```bash
python exercises/exercise_04-synchronization-primitives/src/run.py
python -m pytest exercises/exercise_04-synchronization-primitives/tests -q
python tools/generate_figures.py
```

**محدودیت:** این پروژه مدل آموزشی user-space است. زمان‌های شبیه‌ساز گسسته‌اند و هزینهٔ واقعی تعویض زمینه، رفتار kernel، وقفه‌ها و پردازه‌های فرزند را مدل نمی‌کنند.
