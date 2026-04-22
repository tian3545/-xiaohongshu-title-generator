#!/bin/bash

# 零成本小红书文案生成器 - 快速部署脚本

echo "========================================="
echo "  零成本小红书文案生成器 - 部署向导"
echo "========================================="
echo ""

# 检查是否已配置GitHub远程仓库
if ! git remote get-url origin &> /dev/null; then
    echo "❌ 未检测到GitHub远程仓库"
    echo ""
    echo "请先执行以下步骤："
    echo "1. 访问 https://github.com"
    echo "2. 创建新仓库（名称：xiaohongshu-generator）"
    echo "3. 执行以下命令连接仓库："
    echo ""
    echo "   git remote add origin https://github.com/你的用户名/xiaohongshu-generator.git"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

echo "✅ 检测到远程仓库："
git remote get-url origin
echo ""

# 检查邮箱配置
echo "📧 检查邮箱配置..."
if grep -q "请改成你的QQ邮箱" .env; then
    echo "⚠️  请先配置 .env 文件中的邮箱地址"
    echo ""
    echo "打开 .env 文件，找到这两行："
    echo "  SMTP_USER=请改成你的QQ邮箱@qq.com"
    echo "  SMTP_FROM=小红书文案生成器 <请改成你的QQ邮箱@qq.com>"
    echo ""
    echo "改成你的实际QQ邮箱，例如："
    echo "  SMTP_USER=123456@qq.com"
    echo "  SMTP_FROM=小红书文案生成器 <123456@qq.com>"
    echo ""
    read -p "配置完成后按回车继续..."
fi

# 显示环境变量清单
echo ""
echo "========================================="
echo "  Render 环境变量配置清单"
echo "========================================="
echo ""
echo "在Render部署时，请添加以下环境变量："
echo ""
echo "SECRET_KEY=your-random-secret-key-123456"
echo "SMTP_SERVER=smtp.qq.com"
echo "SMTP_PORT=587"
echo "SMTP_USER=你的QQ邮箱@qq.com"
echo "SMTP_PASSWORD=bgqikwhmuitfdejb"
echo "SMTP_FROM=小红书文案生成器 <你的QQ邮箱@qq.com>"
echo "DOMAIN=your-app-name.onrender.com"
echo ""
echo "========================================="
echo ""

# 询问是否推送到GitHub
read -p "是否现在推送到GitHub？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 正在推送到GitHub..."
    git push -u origin main
    echo ""
    echo "✅ 代码已成功推送到GitHub！"
    echo ""
else
    echo "❌ 已取消推送"
    echo "   你可以稍后手动执行：git push -u origin main"
    echo ""
fi

# 下一步指导
echo "========================================="
echo "  下一步操作"
echo "========================================="
echo ""
echo "1. 访问 https://render.com"
echo "2. 用GitHub账号登录（免费）"
echo "3. 点击 New → Web Service"
echo "4. 连接你的GitHub仓库"
echo "5. 配置环境变量（见上方清单）"
echo "6. 等待2-5分钟部署完成"
echo "7. 访问你的地址开始使用！"
echo ""
echo "详细部署步骤请查看：DEPLOYMENT.md"
echo ""
echo "🚀 开始赚钱吧！"
echo ""
