# 📁 دليل رفع المشروع على PythonAnywhere - خطوة بخطوة

## 🎯 **الحل الأسرع: رفع الملفات يدوياً**

### 📋 **الخطوة 1: تحضير الملفات**

✅ **تم إنشاء ملف ZIP تلقائياً:** `bakery-management-system.zip`

**الملفات المطلوبة:**

- `main.py` - نقطة البداية
- `wsgi.py` - إعداد الخادم
- `web_server.py` - خادم الويب
- `config.py` - الإعدادات
- `env_config.py` - متغيرات البيئة
- `requirements.txt` - المتطلبات
- مجلد `api/` - جميع ملفات API
- مجلد `ai/` - خدمات الذكاء الاصطناعي
- مجلد `database/` - قاعدة البيانات
- مجلد `templates/` - القوالب
- مجلد `static/` - الملفات الثابتة
- مجلد `seeders/` - بيانات العينة
- `sample_data.sql` - بيانات قاعدة البيانات

### 🚀 **الخطوة 2: رفع الملفات إلى PythonAnywhere**

#### **الطريقة الأولى: رفع ملف ZIP (الأسرع)**

1. **اذهب إلى Files tab في PythonAnywhere**
2. **تأكد أنك في المجلد الرئيسي:** `/home/yourusername/`
3. **اضغط على "Upload a file"**
4. **ارفع الملف:** `bakery-management-system.zip`
5. **انتظر حتى يكتمل الرفع**

#### **استخراج الملفات:**

```bash
# في Console PythonAnywhere
cd ~
unzip bakery-management-system.zip
# أو
python3.8 -m zipfile -e bakery-management-system.zip .
```

#### **الطريقة الثانية: رفع المجلدات منفصلة**

1. **إنشاء مجلد المشروع:**

```bash
# في Console PythonAnywhere
cd ~
mkdir bakery-management-system
cd bakery-management-system
```

2. **رفع الملفات الرئيسية:**

   - `main.py`
   - `wsgi.py`
   - `web_server.py`
   - `config.py`
   - `env_config.py`
   - `requirements.txt`
   - `sample_data.sql`

3. **إنشاء المجلدات:**

```bash
# في Console PythonAnywhere
mkdir api ai database templates static seeders
mkdir static/css static/js static/images
```

4. **رفع ملفات كل مجلد:**
   - `api/` → رفع جميع ملفات Python
   - `ai/` → رفع ملفات الذكاء الاصطناعي
   - `database/` → رفع ملفات قاعدة البيانات
   - `templates/` → رفع `index.html`
   - `static/css/` → رفع `style.css`
   - `static/js/` → رفع `app.js`
   - `seeders/` → رفع جميع ملفات SQL

### 🔧 **الخطوة 3: تثبيت المتطلبات**

```bash
# في Console PythonAnywhere
cd ~/bakery-management-system
pip3.8 install --user -r requirements.txt
```

**المتطلبات المطلوبة:**

```
Flask==2.3.3
Flask-CORS==4.0.0
PyMySQL==1.1.0
google-generativeai==0.1.0
requests==2.31.0
pydantic==2.5.0
```

### 🗄️ **الخطوة 4: إعداد قاعدة البيانات**

#### **إنشاء قاعدة البيانات:**

1. **اذهب إلى Databases tab**
2. **اختر MySQL**
3. **أنشئ قاعدة بيانات جديدة:** `bakery_db`

#### **رفع البيانات:**

```bash
# في Console PythonAnywhere
cd ~/bakery-management-system
mysql -u yourusername -p -h yourusername.mysql.pythonanywhere-services.com yourusername\$bakery_db < sample_data.sql
```

### ⚙️ **الخطوة 5: تحديث الإعدادات**

#### **تحديث `env_config.py`:**

```python
import os

# Database Configuration
DATABASE_URL = "mysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere-services.com/yourusername$bakery_db"

# AI Configuration
GEMINI_API_KEY = "AIzaSyD813Gu6WszqsjbEq-5MvO5GYlxj5By8fE"
GEMINI_MODEL = "gemini-1.5-pro-latest"
MAX_TOKENS = 2048

# Server Configuration
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False

# Security
SECRET_KEY = 'your-secret-key-here'
ENABLE_CORS = True
```

#### **تحديث `wsgi.py`:**

```python
import sys
import os

# Add your project directory to sys.path
project_home = '/home/yourusername/bakery-management-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask application
from api.web_routes import app as application

# Configure logging for production
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 🌐 **الخطوة 6: إعداد Web App**

#### **إنشاء Web App:**

1. **اذهب إلى Web tab**
2. **اضغط "Add a new web app"**
3. **اختر "Manual configuration"**
4. **اختر Python 3.8**

#### **إعداد WSGI:**

```python
import sys
import os

# Add your project directory to sys.path
project_home = '/home/yourusername/bakery-management-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from wsgi import application
```

#### **إعداد Static Files:**

```
URL: /static/
Directory: /home/yourusername/bakery-management-system/static
```

### 🚀 **الخطوة 7: تشغيل الموقع**

```bash
# اختبار الموقع محلياً
cd ~/bakery-management-system
python3.8 main.py
```

**في Web tab:**

1. **اضغط "Reload"**
2. **انتظر حتى يظهر "Reloaded"**
3. **اذهب إلى موقعك:** `https://yourusername.pythonanywhere.com`

### 🔍 **الخطوة 8: اختبار الموقع**

#### **اختبار الصفحة الرئيسية:**

```
https://yourusername.pythonanywhere.com/
```

#### **اختبار API:**

```
https://yourusername.pythonanywhere.com/api/health
```

#### **اختبار قاعدة البيانات:**

```bash
# في Console PythonAnywhere
cd ~/bakery-management-system
python3.8 test_website.py
```

### 🛠️ **الخطوة 9: حل المشاكل**

#### **إذا ظهر خطأ 404:**

- تأكد من أن WSGI يشير للمسار الصحيح
- تأكد من أن `wsgi.py` في المجلد الصحيح

#### **إذا ظهر خطأ 500:**

- راجع Error log في Web tab
- تأكد من تثبيت جميع المتطلبات

#### **إذا لم تعمل قاعدة البيانات:**

- تأكد من صحة DATABASE_URL
- تأكد من رفع sample_data.sql

#### **إذا لم تعمل الملفات الثابتة:**

- تأكد من إعداد Static Files في Web tab
- تأكد من وجود الملفات في static/

### 📊 **الخطوة 10: مراقبة الأداء**

#### **في Web tab:**

- **Traffic:** عدد الزيارات
- **CPU:** استخدام المعالج
- **Error log:** الأخطاء
- **Access log:** سجل الوصول

#### **في Console:**

```bash
# مراقبة الملفات
ls -la ~/bakery-management-system/
# مراقبة العمليات
ps aux | grep python
# مراقبة المساحة
df -h
```

### 🎯 **النتيجة النهائية**

بعد اتباع جميع الخطوات، ستحصل على:

- ✅ موقع يعمل: `https://yourusername.pythonanywhere.com`
- ✅ API يعمل: `https://yourusername.pythonanywhere.com/api/health`
- ✅ قاعدة بيانات متصلة
- ✅ ذكاء اصطناعي يعمل
- ✅ واجهة مستخدم جميلة

### 🔗 **الروابط المفيدة:**

- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **Flask على PythonAnywhere:** https://help.pythonanywhere.com/pages/Flask/
- **MySQL على PythonAnywhere:** https://help.pythonanywhere.com/pages/MySQLdb/

---

## 🎉 **مبروك! موقعك جاهز للاستخدام!**

**استبدل `yourusername` باسم المستخدم الخاص بك في جميع الأوامر**
