"""Build the Persian Exercise 6 seminar deck from repository experiment data."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
EX6 = ROOT / "exercises" / "exercise_06-research-paper-seminar"
OUT = EX6 / "docs" / "presentation" / "seminar_fa.pptx"
DATA = EX6 / "outputs" / "results.json"
CHART = EX6 / "docs" / "figures" / "results.png"

NAVY = RGBColor(24, 48, 78)
BLUE = RGBColor(43, 94, 145)
INK = RGBColor(38, 53, 70)
MUTED = RGBColor(86, 105, 126)
PALE = RGBColor(246, 249, 253)
WHITE = RGBColor(255, 255, 255)
FONT = "Arial"


def set_rtl(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    rtl = OxmlElement("a:rtl")
    rtl.set("val", "1")
    p_pr.append(rtl)
    paragraph.alignment = PP_ALIGN.RIGHT


def add_text(slide, text, x, y, w, h, size=20, bold=False, color=INK, align=PP_ALIGN.RIGHT, rtl=True):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    if rtl:
        set_rtl(p)
    for run in p.runs:
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return shape


def add_base(prs, number, total, section="تمرین ۶ | Lottery Scheduling"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = PALE
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(.26))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    add_text(slide, section, .55, .32, 8.8, .35, size=10, color=MUTED, rtl=True)
    add_text(slide, f"{number} / {total}", 11.6, 7.05, 1.1, .25, size=9, color=MUTED, align=PP_ALIGN.RIGHT, rtl=False)
    return slide


def add_bullet_list(slide, items, x=.85, y=2.0, w=11.6, h=4.3, size=19):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.clear(); tf.word_wrap = True
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = "•  " + item
        p.space_after = Pt(18)
        set_rtl(p)
        for run in p.runs:
            run.font.name = FONT
            run.font.size = Pt(size)
            run.font.color.rgb = INK
    return shape


def build():
    data = __import__("json").loads(DATA.read_text(encoding="utf-8"))
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    total = 12

    # 1 cover
    slide = add_base(prs, 1, total, "سمینار زمان‌بندی سیستم‌عامل")
    add_text(slide, "Lottery Scheduling", .9, 1.45, 11.5, .9, size=34, bold=True, color=NAVY, align=PP_ALIGN.CENTER, rtl=False)
    add_text(slide, "مدیریت سهم CPU با قرعه‌کشی وزنی", 1.0, 2.65, 11.3, .8, size=27, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    add_text(slide, "مروری بر مدل بلیت، پیاده‌سازی آزمایشی، نتایج و محدودیت‌ها", 1.2, 3.75, 10.9, .8, size=18, color=MUTED, align=PP_ALIGN.CENTER)
    add_text(slide, "تمرین ۶ — نسخهٔ آموزشی مبتنی بر کد و آزمایش بازتولیدپذیر", 1.0, 5.3, 11.3, .5, size=14, color=INK, align=PP_ALIGN.CENTER)

    slides = [
        ("مسئله و هدف", [
            "چند پردازهٔ آماده برای استفاده از CPU رقابت می‌کنند.",
            "اولویت ثابت ممکن است انعطاف لازم برای تنظیم سهم نسبی را ندهد.",
            "Lottery با تعداد بلیت‌ها، سهم مورد انتظار هر پردازه را تنظیم می‌کند.",
            "این سیاست برای proportional share است، نه تضمین deadline سخت."
        ]),
        ("مدل بلیت", [
            "هر پردازهٔ آماده i تعداد tᵢ بلیت در اختیار دارد.",
            "T برابر مجموع بلیت‌های پردازه‌های آماده در همان لحظه است.",
            "در هر تصمیم، یک عدد صحیح یکنواخت از ۱ تا T انتخاب می‌شود.",
            "احتمال برد یک قرعه برای پردازهٔ i برابر tᵢ / T است."
        ]),
        ("تعیین برنده", [
            "۱) مجموعهٔ ready را با توجه به زمان ورود و پایان burst بساز.",
            "۲) مجموع بلیت‌ها را محاسبه کن.",
            "۳) عدد برنده را تولید کن و بازه‌های تجمعی را بررسی کن.",
            "۴) پردازهٔ برنده یک quantum یا باقیماندهٔ burst را اجرا می‌کند.",
            "۵) وضعیت پردازه‌ها و metricها به‌روزرسانی می‌شود."
        ]),
        ("مثال دستی: ۵ / ۳ / ۲", [
            "P1 پنج بلیت دارد: بازهٔ ۱ تا ۵.",
            "P2 سه بلیت دارد: بازهٔ ۶ تا ۸.",
            "P3 دو بلیت دارد: بازهٔ ۹ تا ۱۰.",
            "سهم نظری: P1=50٪، P2=30٪، P3=20٪.",
            "این نسبت، احتمال هر قرعه است و تضمین دقیق در ده draw نیست."
        ]),
        ("معماری آزمایش این مخزن", [
            "هستهٔ shared/lottery_scheduler.py قرعه و زمان‌بندی گسسته را اجرا می‌کند.",
            "seed ثابت، دنبالهٔ قرعه را برای بازتولیدپذیری مشخص می‌کند.",
            "هر رویداد زمان شروع/پایان، عدد قرعه و بازهٔ برنده را ثبت می‌کند.",
            "خروجی JSON مبنای نمودار و گزارش است؛ اعداد دستی وارد نشده‌اند."
        ]),
        ("پژوهش اصلی", [
            "Waldspurger و Weihl، مقالهٔ Lottery Scheduling در OSDI 1994.",
            "هدف مقاله: مدیریت انعطاف‌پذیر منابع به روش proportional-share.",
            "مقاله امکان تعمیم تخصیص بلیت به منابعی مانند I/O، حافظه و lock را توضیح می‌دهد.",
            "مرجع اصلی در اسلاید پایانی و گزارش docs/references.md آمده است."
        ]),
        ("Extensions در پژوهش", [
            "Ticket currency برای نام‌گذاری و جداسازی حقوق منابع.",
            "Ticket transfer برای انتقال موقت حق تخصیص در وابستگی‌های سرویس.",
            "Compensation tickets برای جبران زمانی که کار نتوانسته سهم تخصیص‌یافته را مصرف کند.",
            "این موارد ایده‌های پژوهش‌اند؛ کد این مخزن فقط lottery وزنی پایه را پیاده می‌کند."
        ]),
        ("اعتبارسنجی و معیارهای اندازه‌گیری", [
            "seed ثابت، آزمایش را از نظر تصادفی بازتولیدپذیر می‌کند.",
            "تعداد قرعه، سهم نظری و سهم مشاهده‌شده در JSON ثبت می‌شوند.",
            "خطای قدرمطلق سهم، برای توصیف تفاوت نمونه با انتظار گزارش می‌شود.",
            "آزمون‌های واحد، ورودی نامعتبر، تکمیل کار و محاسبات metric را کنترل می‌کنند.",
            "تست موفق جای اثبات رسمی یا آزمایش روی kernel را نمی‌گیرد."
        ]),
    ]
    for idx, (title, items) in enumerate(slides, start=2):
        slide = add_base(prs, idx, total)
        add_text(slide, title, .75, .85, 11.8, .72, size=27, bold=True, color=NAVY)
        add_bullet_list(slide, items, y=1.85, size=18)

    # 10 measured experiment chart
    slide = add_base(prs, 10, total)
    add_text(slide, "نتیجهٔ آزمایش ۵٬۰۰۰ قرعه", .75, .78, 11.8, .65, size=26, bold=True, color=NAVY)
    if CHART.exists():
        slide.shapes.add_picture(str(CHART), Inches(2.0), Inches(1.6), width=Inches(9.2))
    add_text(slide, f"تعداد تصمیم‌ها: {data['decisions']}  |  seed: 2026  |  سهم‌های مشاهده‌شده در outputs/results.json ثبت شده‌اند.", .8, 6.35, 11.8, .45, size=13, color=MUTED)

    # 11 comparison
    slide = add_base(prs, 11, total)
    add_text(slide, "تفاوت هدف Lottery با EDF و RM", .75, .82, 11.8, .7, size=26, bold=True, color=NAVY)
    add_bullet_list(slide, [
        "Lottery: سهم نسبی منابع از طریق وزن بلیت‌ها و قرعهٔ تصادفی.",
        "EDF: اولویت به کار آماده با نزدیک‌ترین deadline مطلق.",
        "RM: اولویت ثابت بر اساس دورهٔ تناوب؛ دورهٔ کوتاه‌تر اولویت بالاتر.",
        "معیار مقایسه باید هدف الگوریتم، workload و محدودیت مدل را مشخص کند."
    ], y=1.9, size=19)

    # 12 limitations and source
    slide = add_base(prs, 12, total)
    add_text(slide, "جمع‌بندی، محدودیت و منبع", .75, .78, 11.8, .7, size=26, bold=True, color=NAVY)
    add_bullet_list(slide, [
        "سهم بلیت، امید ریاضی تخصیص را کنترل می‌کند؛ اجرای کوتاه‌مدت نوسان دارد.",
        "Lottery به‌تنهایی نه deadline را تضمین می‌کند و نه bounded waiting قطعی می‌دهد.",
        "شبیه‌ساز این مخزن مدل آموزشی user-space است و جای زمان‌بند kernel نیست.",
        "Waldspurger & Weihl (1994), OSDI 94 — USENIX: https://www.usenix.org/conference/osdi-94/lottery-scheduling-flexible-proportional-share-resource-management"
    ], y=1.8, size=16)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Built {len(prs.slides)} slides: {OUT}")


if __name__ == "__main__":
    build()
