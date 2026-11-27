# گزارش فارسی — تمرین 6: مقاله و سمینار درباره Lottery Scheduling

## چکیده

تحلیل مقالهٔ اصلی Waldspurger و Weihl، مزایا، currency، ticket transfer، محدودیت‌ها و ارائهٔ کلاسی. این گزارش منطق الگوریتم، فرض‌های مدل و شواهد حاصل از اجرای کد را از ادعاهای عمومی جدا می‌کند.

## مسئله و هدف

این تمرین یک مرور پژوهشی بر مقالهٔ اصلی Lottery Scheduling نوشتهٔ Carl A. Waldspurger و William E. Weihl در OSDI 1994 است. مقاله Lottery را سازوکاری تصادفی برای مدیریت proportional-share معرفی می‌کند و علاوه بر تخصیص CPU، ایده‌هایی مانند currency abstraction و تعمیم به منابعی مانند I/O، حافظه و دسترسی به lock را مطرح می‌کند.

در گزارش، ایدهٔ اصلی با مدل بلیت و احتمال انتخاب توضیح داده می‌شود؛ سپس ticket transfer، ticket currency و compensation tickets به‌عنوان extensions پژوهشی از implementation پایه جدا می‌شوند. نسخهٔ این مخزن فقط قرعهٔ وزنی ساده را پیاده می‌کند و نباید به‌عنوان پیاده‌سازی کامل همهٔ extensionها معرفی شود.

نتیجهٔ پژوهش باید تفاوت proportional fairness و hard real-time deadline guarantee را روشن کند. ارائهٔ همراه نیز خلاصهٔ مسئله، مدل، شبه‌کد، نتایج آزمایش قابل‌بازتولید و محدودیت‌ها را نشان می‌دهد. منبع اصلی در انتهای گزارش لینک شده است.

## مدل و روش اجرا

سناریوی این تمرین در `shared/experiments.py` تعریف شده و با تابع `run_exercise(6)` اجرا می‌شود. منبع دادهٔ گزارش، فایل `outputs/results.json` است. برای تکرار نتیجه، نسخهٔ کد و seed ثبت‌شده باید ثابت باشد.

## شبه‌کد Lottery

```text
while unfinished jobs exist:
    ready = jobs with arrival <= now and remaining > 0
    if ready is empty:
        advance time to next arrival
        continue
    T = sum(ticket[p] for p in ready)
    r = uniform_integer(1, T)
    winner = first job whose cumulative ticket interval contains r
    run winner for min(quantum, remaining[winner])
    update remaining time, first response and completion
```

## شکل‌ها و تفسیر

`figures/architecture.svg` معماری و رابطهٔ مولد قرعه با مجموعهٔ آماده را نشان می‌دهد. `figures/flowchart.svg` مسیر تصمیم را مرحله‌به‌مرحله نمایش می‌دهد. `figures/results.png` از دادهٔ واقعی خروجی برنامه رسم شده است؛ عنوان، محور و سناریوی شکل باید همراه فایل JSON خوانده شوند.

## معیارهای ارزیابی

صحت ورودی‌ها، یکتایی شناسه‌ها، مثبت‌بودن ticket و burst، تکمیل همهٔ عملیات، سازگاری شمارنده‌ها، تکرارپذیری seed و صحت metricها بررسی می‌شود. زمان انتظار، پاسخ و turnaround از trace استخراج می‌شوند، نه از عددگذاری دستی.

## محدودیت‌ها

این تمرین یک مرور پژوهشی بر مقالهٔ اصلی Lottery Scheduling نوشتهٔ Carl A. Waldspurger و William E. Weihl در OSDI 1994 است. مقاله Lottery را سازوکاری تصادفی برای مدیریت proportional-share معرفی می‌کند و علاوه بر تخصیص CPU، ایده‌هایی مانند currency abstraction و تعمیم به منابعی مانند I/O، حافظه و دسترسی به lock را مطرح می‌کند.

در گزارش، ایدهٔ اصلی با مدل بلیت و احتمال انتخاب توضیح داده می‌شود؛ سپس ticket transfer، ticket currency و compensation tickets به‌عنوان extensions پژوهشی از implementation پایه جدا می‌شوند. نسخهٔ این مخزن فقط قرعهٔ وزنی ساده را پیاده می‌کند و نباید به‌عنوان پیاده‌سازی کامل همهٔ extensionها معرفی شود.

نتیجهٔ پژوهش باید تفاوت proportional fairness و hard real-time deadline guarantee را روشن کند. ارائهٔ همراه نیز خلاصهٔ مسئله، مدل، شبه‌کد، نتایج آزمایش قابل‌بازتولید و محدودیت‌ها را نشان می‌دهد. منبع اصلی در انتهای گزارش لینک شده است.

مدل حاضر یک شبیه‌ساز آموزشی است؛ نتایج آزمایش محدود جای اثبات عمومی یا benchmark kernel را نمی‌گیرند.

## منابع

Waldspurger, C. A., & Weihl, W. E. (1994). *Lottery Scheduling: Flexible Proportional-Share Resource Management*. OSDI '94. https://www.usenix.org/conference/osdi-94/lottery-scheduling-flexible-proportional-share-resource-management
