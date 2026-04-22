# 🎯 接下来你需要做的（5步搞定）

## 📋 操作清单

### 第1步：配置邮箱地址（2分钟）

打开 `.env` 文件，找到这两行：
```
SMTP_USER=请改成你的QQ邮箱@qq.com
SMTP_FROM=小红书文案生成器 <请改成你的QQ邮箱@qq.com>
```

改成你的实际QQ邮箱，例如：
```
SMTP_USER=123456@qq.com
SMTP_FROM=小红书文案生成器 <123456@qq.com>
```

---

### 第2步：创建GitHub仓库（3分钟）

1. 访问：https://github.com
2. 点击右上角 `+` → `New repository`
3. 填写：
   - Repository name: `xiaohongshu-generator`
   - Public ✅
4. 点击 `Create repository`

---

### 第3步：推送代码到GitHub（2分钟）

执行以下命令（**替换成你的GitHub用户名**）：

```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/xiaohongshu-generator.git

# 推送代码
git push -u origin main
```

**或者直接运行部署脚本：**
```bash
bash deploy.sh
```

---

### 第4步：部署到Render（5分钟）

1. **注册Render**
   - 访问：https://render.com
   - 点击 `Sign Up`
   - 用GitHub账号登录（免费）

2. **创建服务**
   - 点击 `New` → `Web Service`
   - 找到 `xiaohongshu-generator` 仓库
   - 点击 `Connect`

3. **配置服务**

   **Name:** `xiaohongshu-generator`

   **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```

   **Start Command:**
   ```bash
   bash start.sh
   ```

4. **添加环境变量（重要！）**

   点击 `Advanced` → `Environment Variables` → `Add`

   添加这些环境变量：

   ```env
   SECRET_KEY=your-random-secret-key-123456
   SMTP_SERVER=smtp.qq.com
   SMTP_PORT=587
   SMTP_USER=你的QQ邮箱@qq.com
   SMTP_PASSWORD=bgqikwhmuitfdejb
   SMTP_FROM=小红书文案生成器 <你的QQ邮箱@qq.com>
   DOMAIN=你的应用名.onrender.com
   ```

5. **点击 `Create Web Service`**

6. **等待2-5分钟部署完成**

---

### 第5步：测试访问（1分钟）

部署成功后，你会看到一个地址，类似：
```
https://xiaohongshu-generator-xxxx.onrender.com
```

**访问测试：**
1. 输入你的QQ邮箱
2. 点击"发送验证码"
3. 查看邮箱，输入验证码
4. 登录成功
5. 购买套餐（模拟支付）
6. 生成文案

---

## ✅ 完成后你就拥有：

- ✅ 在线可用的文案生成器
- ✅ 按次付费功能
- ✅ 零成本运营
- ✅ 完整的后台系统

---

## 💰 开始赚钱

**你的访问地址：**
```
https://你的应用名.onrender.com
```

**推广方式：**
1. 分享到朋友圈
2. 发到微信群
3. 在小红书发布体验分享
4. 在知乎回答相关问题

**定价建议：**
- 体验包：1元/次
- 10次：8元
- 50次：35元
- 100次：60元

---

## 📚 帮助文档

- `README.md` - 完整说明文档
- `DEPLOYMENT.md` - 详细部署指南
- `NEXT_STEPS.md` - 本文件

---

## 🎉 现在开始行动吧！

按照上面的步骤，大约 **10-15分钟** 就能完成部署！

**记住：零成本投入，无限收入可能！💰🚀**
