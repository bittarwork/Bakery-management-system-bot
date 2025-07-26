#!/bin/bash

# 🍰 Bakery MERN System - Quick Start Script
# This script sets up and runs the complete system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🍰 مرحباً بك في نظام إدارة المخبز - MERN Stack${NC}"
echo -e "${BLUE}================================================${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js غير مثبت. يرجى تثبيت Node.js 18+ أولاً${NC}"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${RED}❌ إصدار Node.js قديم. يرجى التحديث إلى Node.js 18+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js version: $(node --version)${NC}"

# Function to install dependencies
install_deps() {
    local dir=$1
    local name=$2
    
    echo -e "${YELLOW}📦 تثبيت متطلبات $name...${NC}"
    cd "$dir"
    
    if [ -f "package-lock.json" ]; then
        npm ci
    else
        npm install
    fi
    
    cd - > /dev/null
}

# Function to setup environment
setup_env() {
    echo -e "${YELLOW}⚙️  إعداد متغيرات البيئة...${NC}"
    
    if [ ! -f "backend/.env" ]; then
        if [ -f "backend/config/env.example" ]; then
            cp backend/config/env.example backend/.env
            echo -e "${GREEN}✅ تم إنشاء ملف .env من المثال${NC}"
        else
            echo -e "${YELLOW}⚠️  ملف .env غير موجود. سيتم استخدام المتغيرات الافتراضية${NC}"
        fi
    fi
}

# Function to start backend
start_backend() {
    echo -e "${YELLOW}🚀 تشغيل Backend...${NC}"
    cd backend
    npm run dev &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../backend.pid
    cd - > /dev/null
    
    # Wait for backend to start
    sleep 5
    
    # Check if backend is running
    if curl -f -s http://localhost:5000/health > /dev/null; then
        echo -e "${GREEN}✅ Backend يعمل على http://localhost:5000${NC}"
    else
        echo -e "${RED}❌ فشل في تشغيل Backend${NC}"
        exit 1
    fi
}

# Function to start frontend
start_frontend() {
    echo -e "${YELLOW}🎨 تشغيل Frontend...${NC}"
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../frontend.pid
    cd - > /dev/null
    
    echo -e "${GREEN}✅ Frontend يعمل على http://localhost:3000${NC}"
}

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🔄 إيقاف النظام...${NC}"
    
    if [ -f "backend.pid" ]; then
        kill $(cat backend.pid) 2>/dev/null || true
        rm backend.pid
    fi
    
    if [ -f "frontend.pid" ]; then
        kill $(cat frontend.pid) 2>/dev/null || true
        rm frontend.pid
    fi
    
    echo -e "${GREEN}✅ تم إيقاف النظام بنجاح${NC}"
    exit 0
}

# Setup signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo -e "${BLUE}📋 بدء الإعداد...${NC}"
    
    # Install dependencies
    install_deps "backend" "Backend"
    install_deps "frontend" "Frontend"
    
    # Setup environment
    setup_env
    
    # Start services
    start_backend
    start_frontend
    
    echo -e "${GREEN}🎉 النظام يعمل بنجاح!${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo -e "${GREEN}📊 الداشبورد: http://localhost:3000${NC}"
    echo -e "${GREEN}🤖 البوت المدمج: http://localhost:3000/bot${NC}"
    echo -e "${GREEN}⚡ Backend API: http://localhost:5000${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo -e "${YELLOW}💡 للإيقاف: اضغط Ctrl+C${NC}"
    
    # Keep the script running
    while true; do
        sleep 1
    done
}

# Check if running with specific command
case "${1:-}" in
    "backend")
        echo -e "${BLUE}🚀 تشغيل Backend فقط...${NC}"
        install_deps "backend" "Backend"
        setup_env
        cd backend && npm run dev
        ;;
    "frontend")
        echo -e "${BLUE}🎨 تشغيل Frontend فقط...${NC}"
        install_deps "frontend" "Frontend"
        cd frontend && npm run dev
        ;;
    "docker")
        echo -e "${BLUE}🐳 تشغيل باستخدام Docker...${NC}"
        if ! command -v docker &> /dev/null; then
            echo -e "${RED}❌ Docker غير مثبت${NC}"
            exit 1
        fi
        docker-compose up --build
        ;;
    "install")
        echo -e "${BLUE}📦 تثبيت المتطلبات فقط...${NC}"
        install_deps "backend" "Backend"
        install_deps "frontend" "Frontend"
        setup_env
        echo -e "${GREEN}✅ تم تثبيت جميع المتطلبات${NC}"
        ;;
    "help"|"-h"|"--help")
        echo -e "${BLUE}الاستخدام:${NC}"
        echo -e "  ./start.sh           تشغيل النظام كاملاً"
        echo -e "  ./start.sh backend   تشغيل Backend فقط"
        echo -e "  ./start.sh frontend  تشغيل Frontend فقط"
        echo -e "  ./start.sh docker    تشغيل باستخدام Docker"
        echo -e "  ./start.sh install   تثبيت المتطلبات فقط"
        echo -e "  ./start.sh help      عرض هذه المساعدة"
        exit 0
        ;;
    *)
        main
        ;;
esac 