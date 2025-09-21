# سیستم مدیریت فاکتور فروش | Persian Invoicing System

<div align="center">
  
![Persian Invoice](https://img.shields.io/badge/Persian-Invoice-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**نرم‌افزار پیشرفته مدیریت فاکتور فروش با رابط کاربری فارسی**

[ویژگی‌ها](#ویژگی‌ها) •
[نصب](#نصب) •
[استفاده](#استفاده) •
[توسعه](#توسعه) •
[پشتیبانی](#پشتیبانی)

</div>

---

## 📖 معرفی

سیستم مدیریت فاکتور فروش یک نرم‌افزار کامل و پیشرفته برای مدیریت فروش، صدور فاکتور، و کنترل موجودی است که به صورت ویژه برای کسب‌وکارهای ایرانی طراحی شده است.

### 🎯 هدف

این نرم‌افزار با هدف ارائه راه‌حلی ساده، کارآمد و کاملاً فارسی برای مدیریت فروش کسب‌وکارهای کوچک و متوسط طراحی شده است.

---

## ✨ ویژگی‌ها

### 🧾 مدیریت فاکتور
- ✅ صدور فاکتور با امکان انتخاب پس‌زمینه دلخواه
- ✅ افزودن سربرگ سفارشی به فاکتور
- ✅ محاسبه خودکار مبالغ و اعمال تخفیف
- ✅ خروجی فاکتور به صورت PDF و تصویر (PNG/JPG)
- ✅ چاپ مستقیم فاکتور
- ✅ شماره‌گذاری خودکار بر مبنای تاریخ شمسی

### 📦 مدیریت کالاها
- ✅ افزودن، ویرایش و حذف کالاها
- ✅ کنترل موجودی با هشدار کالاهای کم‌موجود
- ✅ کسر خودکار موجودی پس از فروش
- ✅ قیمت‌گذاری خرید و فروش
- ✅ جستجو و فیلتر کالاها

### 👥 مدیریت مشتریان
- ✅ ثبت اطلاعات کامل مشتریان
- ✅ تاریخچه خرید مشتریان
- ✅ گزارش عملکرد مشتریان

### 📊 گزارش‌گیری پیشرفته
- ✅ گزارش فروش روزانه، هفتگی و ماهانه
- ✅ گزارش موجودی کالاها
- ✅ گزارش عملکرد مشتریان
- ✅ خروجی گزارشات به Excel

### 🛡️ امنیت و احراز هویت
- ✅ سیستم ورود با نام کاربری و رمز عبور
- ✅ رمزگذاری رمزهای عبور
- ✅ مدیریت کاربران چندگانه

### 🎨 رابط کاربری
- ✅ طراحی مدرن و زیبا
- ✅ پشتیبانی کامل از زبان فارسی (RTL)
- ✅ فونت فارسی Vazirmatn
- ✅ تم‌های رنگی متنوع
- ✅ رابط کاربری دوستانه و ساده

### 📅 پشتیبانی از تاریخ شمسی
- ✅ نمایش تاریخ شمسی در تمام بخش‌ها
- ✅ تبدیل خودکار تاریخ میلادی به شمسی
- ✅ فیلتر گزارشات بر اساس تاریخ شمسی

### 💾 مدیریت دیتابیس
- ✅ دیتابیس SQLite برای پایداری و سرعت
- ✅ پشتیبان‌گیری خودکار و دستی
- ✅ بهینه‌سازی دیتابیس
- ✅ امکان بازیابی از پشتیبان

---

## 🔧 نصب

### پیش‌نیازها
- Python 3.8 یا بالاتر
- سیستم عامل: Windows, macOS, Linux
- حداقل 500 مگابایت فضای خالی

### نصب خودکار (توصیه شده)

1. **دانلود نرم‌افزار:**
   ```bash
   git clone https://github.com/KimiVerse/PersianInvoicingPYQT.git
   cd PersianInvoicingPYQT
   ```

2. **اجرای نصب خودکار:**
   ```bash
   python quick_install.py
   ```

3. **اجرای نرم‌افزار:**
   ```bash
   # Windows
   run.bat
   
   # Linux/macOS
   ./run.sh
   ```

### نصب دستی

1. **ایجاد محیط مجازی:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

2. **نصب وابستگی‌ها:**
   ```bash
   pip install -r requirements.txt
   ```

3. **اجرای نرم‌افزار:**
   ```bash
   python main.py
   ```

### اطلاعات ورود پیش‌فرض
- **نام کاربری:** `admin`
- **رمز عبور:** `admin123`

> ⚠️ **توجه:** پس از اولین ورود، حتماً رمز عبور را تغییر دهید.

---

## 📱 استفاده

### شروع کار

1. **ورود به سیستم:**
   - نرم‌افزار را اجرا کنید
   - از اطلاعات ورود پیش‌فرض استفاده کنید
   - در صورت اولین اجرا، نام کاربری و رمز عبور جدید ایجاد کنید

2. **تنظیمات اولیه:**
   - از منوی تنظیمات، اطلاعات شرکت را وارد کنید
   - فونت و تم مورد نظر را انتخاب کنید
   - تنظیمات چاپ را پیکربندی کنید

### 📦 مدیریت کالاها

1. **افزودن کالای جدید:**
   - به بخش "مدیریت کالاها" بروید
   - روی "افزودن کالا" کلیک کنید
   - اطلاعات کالا را وارد کنید (نام، قیمت خرید/فروش، موجودی)
   - روی "ذخیره" کلیک کنید

2. **ویرایش کالا:**
   - کالای مورد نظر را از لیست انتخاب کنید
   - روی "ویرایش" کلیک کنید
   - تغییرات را اعمال کنید

3. **کنترل موجودی:**
   - موجودی کالاها به صورت خودکار کنترل می‌شود
   - کالاهای کم‌موجود در داشبورد نمایش داده می‌شوند
   - هشدار موجودی پایین (کمتر از 5 عدد)

### 🧾 صدور فاکتور

1. **فاکتور جدید:**
   - به بخش "صدور فاکتور" بروید
   - اطلاعات مشتری را وارد کنید
   - در صورت نیاز، پس‌زمینه و سربرگ اضافه کنید

2. **افزودن کالا به فاکتور:**
   - کالای مورد نظر را از لیست انتخاب کنید
   - تعداد را مشخص کنید
   - روی "افزودن کالا" کلیک کنید

3. **تکمیل فاکتور:**
   - تخفیف را در صورت نیاز اعمال کنید
   - یادداشت اضافه کنید
   - روی "ثبت فاکتور" کلیک کنید

4. **خروجی فاکتور:**
   - **PDF:** برای ارسال الکترونیکی
   - **تصویر:** برای اشتراک در شبکه‌های اجتماعی
   - **چاپ:** برای چاپ مستقیم

### 📊 گزارش‌گیری

1. **گزارش فروش:**
   - بازه زمانی مورد نظر را انتخاب کنید
   - نوع گزارش (فروش، کالاها، مشتریان) را مشخص کنید
   - روی "تولید گزارش" کلیک کنید

2. **خروجی گزارش:**
   - گزارش را به صورت Excel دانلود کنید
   - اطلاعات خلاصه در پنل جانبی نمایش داده می‌شود

### 🔧 تنظیمات

دسترسی به تنظیمات از طریق منوی اصلی یا آیکون تنظیمات:

- **ظاهر:** تم، فونت، رنگ‌ها
- **دیتابیس:** پشتیبان‌گیری، نگهداری
- **چاپ:** تنظیمات چاپگر، قالب فاکتور
- **امنیت:** تغییر رمز عبور، تنظیمات امنیتی

---

## 🏗️ ساختار پروژه

```
PersianInvoicingPYQT/
├── 📁 assets/              # فایل‌های گرافیکی
├── 📁 backups/             # پشتیبان‌های دیتابیس
├── 📁 database/            # مدل‌های دیتابیس
│   ├── __init__.py
│   └── models.py
├── 📁 exports/             # فایل‌های خروجی
├── 📁 fonts/               # فونت‌های فارسی
│   └── Vazirmatn-Regular.ttf
├── 📁 logs/                # فایل‌های لاگ
├── 📁 services/            # سرویس‌های اصلی
│   ├── __init__.py
│   ├── database_service.py
│   ├── print_service.py
│   └── report_service.py
├── 📁 views/               # رابط کاربری
│   ├── __init__.py
│   ├── dashboard_view.py
│   ├── invoice_view.py
│   ├── products_view.py
│   ├── reports_view.py
│   └── settings_dialog.py
├── 📄 .gitignore
├── 📄 invoicing.db        # دیتابیس اصلی
├── 📄 main_window.py       # پنجره اصلی
├── 📄 main.py              # فایل اجرایی
├── 📄 quick_install.py     # نصب خودکار
├── 📄 README.md            # راهنمای کامل
├── 📄 requirements.txt     # وابستگی‌ها
├── 📄 run.bat              # اجرا در Windows
├── 📄 run.sh               # اجرا در Linux/macOS
└── 📄 test_setup.py        # تست راه‌اندازی
```

---

## ⌨️ کلیدهای میانبر

| کلید | عملکرد |
|------|---------|
| `Ctrl + N` | فاکتور جدید |
| `Ctrl + P` | کالای جدید |
| `Ctrl + Q` | خروج از برنامه |
| `F5` | به‌روزرسانی |
| `Ctrl + S` | ذخیره (در فرم‌ها) |
| `Esc` | انصراف |

---

## 🛠️ توسعه

### راه‌اندازی محیط توسعه

1. **کلون پروژه:**
   ```bash
   git clone https://github.com/KimiVerse/PersianInvoicingPYQT.git
   cd PersianInvoicingPYQT
   ```

2. **ایجاد محیط مجازی:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # یا
   venv\Scripts\activate     # Windows
   ```

3. **نصب وابستگی‌های توسعه:**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8  # ابزارهای توسعه
   ```

### ساختار کد

- **MVC Pattern:** مدل-نما-کنترلر
- **Service Layer:** منطق کسب‌وکار در سرویس‌ها
- **Database ORM:** SQLAlchemy
- **UI Framework:** PyQt6

### راهنمای مشارکت

1. Fork کنید
2. برنچ جدید بسازید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. برنچ را push کنید (`git push origin feature/amazing-feature`)
5. Pull Request بسازید

### استانداردهای کد

- **Python:** PEP 8
- **Docstrings:** Google Style
- **Type Hints:** استفاده شود
- **Comments:** به فارسی و انگلیسی

---

## 🐛 رفع مشکلات

### مشکلات رایج

#### خطای فونت فارسی
**علامت:** اعداد یا متون فارسی به درستی نمایش داده نمی‌شوند

**راه‌حل:**
```bash
# دانلود دستی فونت
wget https://github.com/rastikerdar/vazirmatn/raw/master/fonts/ttf/Vazirmatn-Regular.ttf
# و قرار دادن در پوشه fonts/
```

#### خطای دیتابیس
**علامت:** پیام خطای "Database connection failed"

**راه‌حل:**
1. بررسی مجوزهای فایل `invoicing.db`
2. اجرای `python -c "from services.database_service import DatabaseService; DatabaseService()"`

#### خطای وابستگی‌ها
**علامت:** ModuleNotFoundError

**راه‌حل:**
```bash
pip install --upgrade -r requirements.txt
```

#### مشکل چاپ فاکتور
**علامت:** فاکتور چاپ نمی‌شود یا خروجی ندارد

**راه‌حل:**
1. بررسی درایور چاپگر
2. تست با خروجی PDF
3. بررسی تنظیمات چاپ در سیستم‌عامل

### لاگ‌ها و عیب‌یابی

فایل‌های لاگ در پوشه `logs/` ذخیره می‌شوند:
- `database.log`: عملیات دیتابیس
- `application.log`: عملیات کلی برنامه
- `error.log`: خطاهای سیستم

---

## 📋 TODO

### ویژگی‌های آینده

- [ ] پشتیبانی از چندین انبار
- [ ] اتصال به کدخوان (Barcode Scanner)
- [ ] پنل وب برای دسترسی از راه دور
- [ ] اپلیکیشن موبایل همراه
- [ ] اتصال به سیستم‌های حسابداری
- [ ] پرداخت آنلاین
- [ ] SMS و ایمیل خودکار
- [ ] تحلیل‌های پیشرفته با AI

### بهبودهای فنی

- [ ] بهینه‌سازی عملکرد
- [ ] تست‌های خودکار
- [ ] CI/CD Pipeline
- [ ] Docker Container
- [ ] مستندات API

---

## 🤝 پشتیبانی

### راه‌های ارتباط

- **ایمیل:** support@kimivi.com
- **گیتهاب:** [مسائل و پیشنهادات](https://github.com/KimiVerse/PersianInvoicingPYQT/issues)
- **تلگرام:** @KimiVerse_Support

### مستندات

- [راهنمای کاربر](docs/user-guide.md)
- [راهنمای برنامه‌نویس](docs/developer-guide.md)
- [سوالات متداول](docs/faq.md)

### کمک مالی

اگر این پروژه برای شما مفید بوده، می‌توانید از طریق راه‌های زیر حمایت کنید:

- ⭐ ستاره دادن به پروژه در گیتهاب
- 🐛 گزارش باگ‌ها و مشکلات
- 💡 پیشنهاد ویژگی‌های جدید
- 📝 بهبود مستندات

---

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای جزئیات بیشتر فایل [LICENSE](LICENSE) را مطالعه کنید.

```
MIT License

Copyright (c) 2024 KimiVerse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🏆 تشکر و قدردانی

### کتابخانه‌های استفاده شده

- **PyQt6:** رابط کاربری گرافیکی
- **SQLAlchemy:** ORM دیتابیس
- **jdatetime:** تاریخ شمسی
- **bcrypt:** رمزگذاری
- **Pillow:** پردازش تصویر
- **ReportLab:** تولید PDF

### فونت‌ها

- **Vazirmatn:** فونت فارسی توسط [Saber Rastikerdar](https://github.com/rastikerdar)

### الهام‌گیری

این پروژه با الهام از نیازهای واقعی کسب‌وکارهای ایرانی و با هدف ارائه راه‌حلی متن‌باز و رایگان طراحی شده است.

---

<div align="center">

**ساخته شده با ❤️ برای جامعه توسعه‌دهندگان ایران**

[⬆️ بازگشت به بالا](#سیستم-مدیریت-فاکتور-فروش--persian-invoicing-system)

</div>