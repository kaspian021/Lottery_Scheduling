# گزارش فارسی — تمرین 2: مقایسه Lottery با EDF و RM

## چکیده

مقایسهٔ هدف، قاعدهٔ انتخاب، سهم CPU و deadline miss روی یک workload مشترک. این گزارش منطق الگوریتم، فرض‌های مدل و شواهد حاصل از اجرای کد را از ادعاهای عمومی جدا می‌کند.

## مسئله و هدف

این تمرین سه سیاست زمان‌بندی را روی یک مجموعهٔ کار مشترک مقایسه می‌کند. Lottery با وزن بلیت‌ها پردازه را انتخاب می‌کند؛ EDF پردازهٔ آماده با نزدیک‌ترین deadline مطلق را انتخاب می‌کند؛ RM اولویت ثابت را بر اساس دورهٔ تناوب می‌دهد و دورهٔ کوتاه‌تر اولویت بالاتری دارد.

سناریوی این مخزن شامل سه job تک‌بار با زمان ورود، burst، تعداد بلیت، deadline و period مشخص است. برای Lottery، قرعه با seed ثابت انجام می‌شود. برای EDF و RM مدل مرجع یک‌تیکی و preemptive است. خروجی شامل گانت، زمان انتظار، turnaround، response و deadline_missed است. همهٔ اعداد از کد تولید می‌شوند و نباید از یک workload محدود نتیجهٔ برتری جهانی گرفت.

Lottery برای کنترل سهم نسبی CPU مناسب است، نه تضمین مهلت. EDF/RM برای مدل‌های بلادرنگ طراحی شده‌اند و تضمین‌هایشان به فرض‌های زمان‌بندی، مدل پردازه و امکان‌پذیری بار وابسته است. در نتیجه مقایسه باید چندمعیاره باشد و تفاوت هدف الگوریتم‌ها را حفظ کند.

## مدل و روش اجرا

سناریوی این تمرین در `shared/experiments.py` تعریف شده و با تابع `run_exercise(2)` اجرا می‌شود. منبع دادهٔ گزارش، فایل `outputs/results.json` است. برای تکرار نتیجه، نسخهٔ کد و seed ثبت‌شده باید ثابت باشد.

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

این تمرین سه سیاست زمان‌بندی را روی یک مجموعهٔ کار مشترک مقایسه می‌کند. Lottery با وزن بلیت‌ها پردازه را انتخاب می‌کند؛ EDF پردازهٔ آماده با نزدیک‌ترین deadline مطلق را انتخاب می‌کند؛ RM اولویت ثابت را بر اساس دورهٔ تناوب می‌دهد و دورهٔ کوتاه‌تر اولویت بالاتری دارد.

سناریوی این مخزن شامل سه job تک‌بار با زمان ورود، burst، تعداد بلیت، deadline و period مشخص است. برای Lottery، قرعه با seed ثابت انجام می‌شود. برای EDF و RM مدل مرجع یک‌تیکی و preemptive است. خروجی شامل گانت، زمان انتظار، turnaround، response و deadline_missed است. همهٔ اعداد از کد تولید می‌شوند و نباید از یک workload محدود نتیجهٔ برتری جهانی گرفت.

Lottery برای کنترل سهم نسبی CPU مناسب است، نه تضمین مهلت. EDF/RM برای مدل‌های بلادرنگ طراحی شده‌اند و تضمین‌هایشان به فرض‌های زمان‌بندی، مدل پردازه و امکان‌پذیری بار وابسته است. در نتیجه مقایسه باید چندمعیاره باشد و تفاوت هدف الگوریتم‌ها را حفظ کند.

مدل حاضر یک شبیه‌ساز آموزشی است؛ نتایج آزمایش محدود جای اثبات عمومی یا benchmark kernel را نمی‌گیرند.

## منابع

Waldspurger, C. A., & Weihl, W. E. (1994). *Lottery Scheduling: Flexible Proportional-Share Resource Management*. OSDI '94. https://www.usenix.org/conference/osdi-94/lottery-scheduling-flexible-proportional-share-resource-management
