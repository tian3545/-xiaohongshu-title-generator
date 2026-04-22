# 🚀 快速开始指南

## 一键部署到GitHub（2分钟）

### 运行自动化脚本

```bash
bash push-to-github.sh
```

按照提示输入：
1. GitHub用户名（例如：`zhangsan`）
2. 仓库名称（默认：`xiaohongshu-generator`）
3. 确认信息

### 推送成功后

GitHub仓库地址：`https://github.com/你的用户名/xiaohongshu-generator`

---

## 部署到Render（5分钟）

### 1. 访问Render
👉 https://render.com
- 用GitHub账号登录（免费）

### 2. 创建新服务
- 点击 **New** → **Web Service**

### 3. 连接仓库
- 选择你的GitHub仓库：`xiaohongshu-generator`
- 点击 **Connect**

### 4. 配置部署

**基础配置：**
- Name: `xiaohongshu-generator`
- Region: `Singapore`（或离你最近的）
- Branch: `main`
- Runtime: `Python 3`

**构建配置：**
- Build Command: `pip install -r requirements.txt`
- Start Command: `bash start.sh`

### 5. 添加环境变量

点击 **Advanced** → **Environment Variables**，添加以下变量：

```env
SECRET_KEY=your-random-secret-key-123456
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
SMTP_USER=2991375770@qq.com
SMTP_PASSWORD=bgqikwhmuitfdejb
SMTP_FROM=小红书文案生成器 <2991375770@qq.com>
DOMAIN=xiaohongshu-generator.onrender.com
```

### 6. 创建服务
- 点击 **Create Web Service**
- 等待2-5分钟部署完成

### 7. 访问应用

部署成功后，访问：
```
https://xiaohongshu-generator.onrender.com
```

---

## 测试功能

### 1. 发送验证码
- 输入邮箱：`2991375770@qq.com`
- 点击"发送验证码"
- 查看邮箱收到的验证码

### 2. 登录
- 输入收到的验证码
- 点击"登录"

### 3. 查看余额
- 登录后显示免费次数
- 可以购买套餐

### 4. 生成文案
- 输入主题（例如：春季穿搭）
- 选择是否生成配图
- 点击"开始生成"
- 等待生成结果

### 5. 查看结果
- 查看生成的文案
- 查看生成的图片
- 可以复制文案

---

## 💰 收费方案

| 套餐 | 次数 | 价格 | 平均 |
|------|------|------|------|
| 体验包 | 1次 | 1元 | 1元/次 |
| 10次套餐 | 10次 | 8元 | 0.8元/次 |
| 50次套餐 | 50次 | 35元 | 0.7元/次 |
| 100次套餐 | 100次 | 60元 | 0.6元/次 |

---

## 📊 收入预估

假设日均100次使用：
- 日收入：70元
- 月收入：2,100元
- 年收入：25,200元

**零成本投入，无限收益可能！💰**

---

## 常见问题

### Q: 推送代码时需要密码怎么办？
**A:** 使用GitHub Personal Access Token
1. 访问：https://github.com/settings/tokens
2. 点击"Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制Token
5. 推送时用Token代替密码

### Q: 部署后无法访问怎么办？
**A:**
1. 检查Render日志
2. 确认环境变量配置正确
3. 等待部署完成（可能需要几分钟）

### Q: 收不到验证码怎么办？
**A:**
1. 检查邮箱垃圾箱
2. 确认SMTP配置正确
3. 查看Render日志

### Q: 如何对接真实支付？
**A:**
1. 注册微信支付/支付宝
2. 获取商户ID和密钥
3. 修改 `api/routers/payment.py`
4. 更新环境变量

---

## 📚 详细文档

- `README.md` - 完整功能介绍
- `DEPLOYMENT.md` - 详细部署说明
- `NEXT_STEPS.md` - 操作步骤

---

## 🎉 开始赚钱吧！

部署成功后，立即开始推广：
- 分享给朋友
- 小红书推广
- 知乎回答
- 抖音短视频

**零成本投入，无限可能！💪**
