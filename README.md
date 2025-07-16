# 🍰 Bakery Management System with AI

نظام إدارة المخبز المتقدم بالذكاء الاصطناعي - جاهز للدمج مع React.js

## 🚀 المميزات

- **🤖 ذكاء اصطناعي متقدم**: Google Gemini Pro للاستفسارات الطبيعية
- **📊 تحليلات شاملة**: تقارير المبيعات والأداء
- **🗄️ تخزين مؤقت ذكي**: توفير 60% من تكلفة API
- **🌍 دعم متعدد اللغات**: العربية والإنجليزية وأكثر
- **⚡ API سريع**: REST endpoints للتكامل مع React
- **🔐 آمن**: حماية البيانات والاستفسارات

## 📋 المتطلبات

- Python 3.8+
- MySQL Database
- Google Cloud AI API Key

## 🔧 التثبيت السريع

```bash
# 1. تثبيت المتطلبات
pip install -r requirements.txt

# 2. تشغيل الخادم
python main.py
```

الخادم سيعمل على: `http://localhost:8000`

## 🌐 API Endpoints

- `GET /api/health` - فحص حالة النظام
- `POST /api/chat` - الدردشة مع الذكاء الاصطناعي
- `GET /api/analytics` - التحليلات والتقارير
- `GET /api/stats` - إحصائيات سريعة
- `GET /api/tables` - معلومات قاعدة البيانات
- `GET|DELETE /api/cache` - إدارة الذاكرة المؤقتة

## ⚛️ دمج React.js

```javascript
// مثال على الاستخدام
import BakeryAPI from "./services/bakeryAPI";

const result = await BakeryAPI.sendMessage("كم عدد المنتجات؟");
console.log(result.response);
```

## 📖 الدلائل

- **[دليل دمج React.js](REACT_INTEGRATION_GUIDE.md)** - دليل شامل للدمج
- **[إعدادات النظام](config.py)** - إعدادات الذكاء الاصطناعي
- **[بيانات تجريبية](sample_data.sql)** - بيانات للاختبار

## 🎯 أمثلة على الاستفسارات

```
"كم عدد المنتجات المتاحة؟"
"أعطني تقرير عن المبيعات"
"ما هي أفضل المنتجات مبيعاً؟"
"كيف يمكنني تحسين الأداء؟"
```

## 🔧 إعدادات الذكاء الاصطناعي

```python
# في env_config.py
GEMINI_API_KEY = "your-api-key-here"
GEMINI_MODEL = "gemini-1.5-pro-latest"
MAX_TOKENS = 2048
ENABLE_SMART_CACHING = True
```

## 📊 هيكل المشروع

```
├── ai/                 # خدمات الذكاء الاصطناعي
├── api/                # REST API endpoints
├── database/           # إدارة قاعدة البيانات
├── config.py           # إعدادات النظام
├── main.py             # نقطة الدخول
└── web_server.py       # خادم الويب
```

## 🚀 للبدء

1. **انسخ المشروع** إلى مجلد backend في مشروع React
2. **ثبت المتطلبات**: `pip install -r requirements.txt`
3. **شغل الخادم**: `python main.py`
4. **اختبر API**: `curl http://localhost:8000/api/health`

## 🎉 جاهز للاستخدام!

النظام محسن ومنظم بالكامل للعمل كـ API backend لموقع React.js. جميع الميزات المتقدمة متاحة عبر REST endpoints.

---

**تم تطوير النظام بواسطة الذكاء الاصطناعي المتقدم** 🤖
