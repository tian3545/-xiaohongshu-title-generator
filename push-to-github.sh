#!/bin/bash

set -e

echo "🚀 小红书文案生成器 - GitHub部署脚本"
echo "=================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取GitHub用户名
echo -e "${BLUE}请输入你的GitHub用户名:${NC}"
read github_username

if [ -z "$github_username" ]; then
    echo -e "${YELLOW}错误: 用户名不能为空${NC}"
    exit 1
fi

# 获取仓库名称
echo -e "${BLUE}请输入仓库名称 (默认: xiaohongshu-generator):${NC}"
read repo_name
repo_name=${repo_name:-xiaohongshu-generator}

echo ""
echo -e "${GREEN}配置信息:${NC}"
echo "  GitHub用户名: $github_username"
echo "  仓库名称: $repo_name"
echo ""

# 确认
echo -e "${BLUE}确认无误吗? (y/n)${NC}"
read confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "已取消"
    exit 0
fi

# 检查是否已配置远程仓库
if git remote get-url origin >/dev/null 2>&1; then
    echo -e "${YELLOW}远程仓库已存在，正在更新...${NC}"
    git remote set-url origin "https://github.com/$github_username/$repo_name.git"
else
    echo -e "${GREEN}添加远程仓库...${NC}"
    git remote add origin "https://github.com/$github_username/$repo_name.git"
fi

echo -e "${GREEN}推送代码到GitHub...${NC}"
echo ""
echo -e "${YELLOW}⚠️  如果提示输入用户名和密码:${NC}"
echo "  用户名: $github_username"
echo "  密码: 请使用GitHub Personal Access Token (不是登录密码)"
echo "  获取Token: https://github.com/settings/tokens"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ 代码推送成功！${NC}"
    echo ""
    echo -e "${BLUE}📍 GitHub仓库地址:${NC}"
    echo "   https://github.com/$github_username/$repo_name"
    echo ""
    echo -e "${BLUE}📋 下一步操作:${NC}"
    echo "   1. 访问 https://render.com"
    echo "   2. 用GitHub账号登录"
    echo "   3. 点击 New → Web Service"
    echo "   4. 连接仓库: $github_username/$repo_name"
    echo "   5. 添加环境变量（见下方）"
    echo "   6. 点击 Create Web Service"
    echo ""
    echo -e "${BLUE}🔑 Render环境变量:${NC}"
    echo "   SECRET_KEY=your-random-secret-key-123456"
    echo "   SMTP_SERVER=smtp.qq.com"
    echo "   SMTP_PORT=587"
    echo "   SMTP_USER=2991375770@qq.com"
    echo "   SMTP_PASSWORD=bgqikwhmuitfdejb"
    echo "   SMTP_FROM=小红书文案生成器 <2991375770@qq.com>"
    echo "   DOMAIN=$repo_name.onrender.com"
    echo ""
else
    echo ""
    echo -e "${YELLOW}❌ 推送失败，请检查:${NC}"
    echo "  1. GitHub用户名是否正确"
    echo "  2. 网络连接是否正常"
    echo "  3. 是否需要使用GitHub Personal Access Token"
    echo ""
    echo -e "${BLUE}获取GitHub Token:${NC}"
    echo "  1. 访问 https://github.com/settings/tokens"
    echo "  2. 点击 Generate new token (classic)"
    echo "  3. 勾选 repo 权限"
    echo "  4. 生成并复制Token"
    echo ""
fi
