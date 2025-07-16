# ===== BAKERY MANAGEMENT SYSTEM PRO - CONFIGURATION =====
# Premium Google Cloud AI Configuration

import os

# AI Provider Configuration
os.environ["AI_PROVIDER"] = "gemini"
os.environ["BOT_NAME"] = "BakeryBot Pro"

# Google Cloud AI Configuration (Premium)
os.environ["GEMINI_API_KEY"] = "AIzaSyD813Gu6WszqsjbEq-5MvO5GYlxj5By8fE"
os.environ["GEMINI_MODEL"] = "gemini-1.5-pro-latest"

# Advanced AI Parameters
os.environ["MAX_TOKENS"] = "2048"
os.environ["TEMPERATURE"] = "0.4"
os.environ["TOP_P"] = "0.95"
os.environ["TOP_K"] = "40"

# Premium Features Configuration
os.environ["ENABLE_ADVANCED_ANALYTICS"] = "true"
os.environ["ENABLE_SMART_CACHING"] = "true"
os.environ["ENABLE_MULTI_LANGUAGE"] = "true"
os.environ["ENABLE_VOICE_RESPONSES"] = "false"

# Database Configuration
os.environ["DATABASE_URL"] = "mysql://root:ZEsGFfzwlnsvgvcUiNsvGraAKFnuVZRA@shinkansen.proxy.rlwy.net:24785/railway"
os.environ["DATABASE_TYPE"] = "mysql"

# Server Configuration
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = "8000"

# Optional: OpenAI Backup Configuration
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_MODEL"] = "gpt-3.5-turbo"

# ===== SYSTEM OPTIMIZATION SETTINGS =====
# These settings optimize performance for premium usage

# Cache Settings
os.environ["CACHE_ENABLED"] = "true"
os.environ["CACHE_TTL"] = "3600"

# Rate Limiting (Premium API has higher limits)
os.environ["RATE_LIMIT_REQUESTS"] = "100"
os.environ["RATE_LIMIT_WINDOW"] = "60"

# Logging Configuration
os.environ["LOG_LEVEL"] = "INFO"
os.environ["LOG_FILE"] = "bakery_bot.log"

# ===== BUSINESS CONFIGURATION =====
# Customize these for your bakery

# Currency and Localization
os.environ["DEFAULT_CURRENCY"] = "EUR"
os.environ["SECONDARY_CURRENCY"] = "SYP"
os.environ["DATE_FORMAT"] = "YYYY-MM-DD"
os.environ["TIMEZONE"] = "Europe/Berlin"

# Business Rules
os.environ["MIN_ORDER_VALUE"] = "5.00"
os.environ["MAX_ORDER_VALUE"] = "1000.00"
os.environ["DEFAULT_TAX_RATE"] = "0.19"

# Notification Settings
os.environ["ENABLE_NOTIFICATIONS"] = "true"
os.environ["NOTIFICATION_CHANNELS"] = "email,sms"

print("🚀 BakeryBot Pro Configuration Loaded Successfully!")
print("✅ Premium Google Cloud AI Features Enabled")
print("🔧 Advanced Analytics and Caching Activated")
print("🌍 Multi-language Support Ready")
print("📊 Enhanced Performance Settings Applied") 