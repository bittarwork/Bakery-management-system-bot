# 🚀 دليل النشر على PythonAnywhere

## 📋 الخطوات المطلوبة

### 1. إنشاء حساب PythonAnywhere

- اذهب إلى [PythonAnywhere](https://www.pythonanywhere.com)
- أنشئ حساب مجاني أو مدفوع
- اختر Python 3.8 أو أحدث

### 2. رفع الملفات

```bash
# رفع جميع ملفات المشروع عبر Files tab أو Git
git clone https://github.com/yourusername/bakery-management-system.git
```

### 3. إعداد قاعدة البيانات

```bash
# تحديث معلومات قاعدة البيانات في env_config.py
DATABASE_URL = "mysql://username:password@hostname:port/database_name"
```

### 4. تثبيت المتطلبات

```bash
# في console PythonAnywhere
pip3.8 install --user -r requirements.txt
```

### 5. إعداد Web App

1. اذهب إلى Web tab
2. اضغط "Add a new web app"
3. اختر "Manual configuration"
4. اختر Python 3.8
5. حدد مجلد المشروع: `/home/yourusername/bakery-management-system`

### 6. إعداد WSGI

1. في Web tab، اضغط على WSGI configuration file
2. استبدل المحتوى بما يلي:

```python
import sys
import os

# Add your project directory to sys.path
project_home = '/home/yourusername/bakery-management-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from wsgi import application
```

### 7. إعداد Static Files

في Web tab، إضافة:

- URL: `/static/`
- Directory: `/home/yourusername/bakery-management-system/static`

### 8. إعداد متغيرات البيئة

في Files tab، حرر `env_config.py`:

```python
import os

# Database Configuration
DATABASE_URL = "mysql://username:password@hostname:port/database_name"

# AI Configuration
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_MODEL = "gemini-1.5-pro-latest"

# App Configuration
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False
```

### 9. اختبار النشر

1. اضغط "Reload" في Web tab
2. اذهب إلى `https://yourusername.pythonanywhere.com`
3. تأكد من أن الموقع يعمل بشكل صحيح

## 🔧 إعدادات خاصة بـ PythonAnywhere

### إعداد قاعدة البيانات MySQL

```sql
-- في MySQL console
CREATE DATABASE bakery_db;
USE bakery_db;

-- تشغيل ملفات البيانات
SOURCE /home/yourusername/bakery-management-system/sample_data.sql;
```

### إعداد المهام المجدولة (Tasks)

```bash
# تشغيل تحديثات دورية
0 */6 * * * /usr/local/bin/python3.8 /home/yourusername/bakery-management-system/maintenance.py
```

### إعداد الأمان

```python
# في config.py
SECRET_KEY = 'your-secret-key-here'
CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

## 📱 الوصول للموقع

بعد النشر الناجح، يمكنك الوصول للموقع عبر:

- `https://yourusername.pythonanywhere.com`
- `https://yourusername.pythonanywhere.com/api/health` (للتحقق من API)

## 🎯 المميزات المتاحة

### 🏠 الصفحة الرئيسية

- إحصائيات شاملة
- نظرة عامة على النشاط
- واجهة مستخدم جميلة

### 📦 إدارة المنتجات

- عرض جميع المنتجات
- تفاصيل المنتجات
- حالة المخزون

### 🛒 إدارة الطلبات

- عرض الطلبات الحالية
- تتبع حالة الطلبات
- تفاصيل العملاء

### 📊 التحليلات

- تقارير مفصلة
- إحصائيات الأداء
- تحليل المبيعات

### 🤖 المساعد الذكي

- دردشة مع AI
- استفسارات طبيعية
- تحليل البيانات

## 🔍 استكشاف الأخطاء

### خطأ في قاعدة البيانات

```bash
# تحقق من الاتصال
python3.8 -c "from database.connection import db_manager; print(db_manager.test_connection())"
```

### خطأ في AI

```bash
# تحقق من API key
python3.8 -c "from ai.gemini_service import gemini_service; print(gemini_service.test_connection())"
```

### خطأ في Static Files

- تأكد من مسار `/static/` في Web tab
- تحقق من أن الملفات موجودة في المجلد الصحيح

## 📞 الدعم الفني

إذا واجهت أي مشاكل:

1. تحقق من Error log في Web tab
2. راجع Console للأخطاء
3. تأكد من جميع المتطلبات مثبتة

## 🎉 تهانينا!

موقع إدارة المخبز جاهز للاستخدام على PythonAnywhere!

---

**تطوير:** نظام إدارة المخبز بالذكاء الاصطناعي
**الإصدار:** 1.0.0
**التاريخ:** 2025
