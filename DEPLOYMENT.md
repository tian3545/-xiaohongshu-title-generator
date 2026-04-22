# 部署指南 - 零成本小红书文案生成器

## 📋 部署前准备

### 1. 准备GitHub账号
- 访问 https://github.com
- 注册账号（如果还没有）

### 2. 准备QQ邮箱
- ✅ 已获取QQ邮箱授权码：`bgqikwhmuitfdejb`
- ⚠️ 请将 `.env` 文件中的邮箱地址改成你的实际QQ邮箱

## 🚀 部署步骤（10分钟）

### 步骤1：创建GitHub仓库

1. 登录GitHub
2. 点击右上角 `+` → `New repository`
3. 填写信息：
   - Repository name: `xiaohongshu-generator`（或自定义）
   - Description: `零成本按次付费小红书文案生成器`
   - Public ✅
4. 点击 `Create repository`

### 步骤2：推送代码到GitHub

在你的本地终端执行：

```bash
# 添加远程仓库（替换成你的GitHub用户名）
git remote add origin https://github.com/你的用户名/xiaohongshu-generator.git

# 推送代码
git push -u origin main
```

**示例：**
```bash
git remote add origin https://github.com/zhangsan/xiaohongshu-generator.git
git push -u origin main
```

### 步骤3：注册Render账号

1. 访问 https://render.com
2. 点击 `Sign Up`
3. 选择 `Sign up with GitHub`（免费）
4. 授权GitHub登录

### 步骤4：部署到Render

1. 在Render首页，点击 `New` → `Web Service`

2. 连接GitHub仓库：
   - 找到 `xiaohongshu-generator` 仓库
   - 点击 `Connect`

3. 配置服务：

   **基本信息：**
   - Name: `xiaohongshu-generator`（会自动成为域名的一部分）
   - Region: `Singapore`（推荐，或选择离你最近的）
   - Branch: `main`

   **环境配置：**
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `bash start.sh`

4. **添加环境变量（重要！）**

   点击 `Advanced` → `Environment Variables` → `Add`

   添加以下环境变量：

   | 变量名 | 值 | 说明 |
   |--------|-----|------|
   | `SECRET_KEY` | `your-random-secret-key-123456` | 随机密钥（建议修改） |
   | `SMTP_SERVER` | `smtp.qq.com` | SMTP服务器 |
   | `SMTP_PORT` | `587` | SMTP端口 |
   | `SMTP_USER` | `你的QQ邮箱@qq.com` | ⚠️ 请改成你的实际邮箱 |
   | `SMTP_PASSWORD` | `bgqikwhmuitfdejb` | QQ邮箱授权码 |
   | `SMTP_FROM` | `小红书文案生成器 <你的QQ邮箱@qq.com>` | 发件人信息 |
   | `DOMAIN` | `your-app-name.onrender.com` | 你的Render域名（部署后自动填充） |

5. 创建服务
   - 点击 `Create Web Service`
   - 等待2-5分钟部署完成

6. 获取访问地址
   - 部署成功后，会显示：
   ```
   https://your-app-name.onrender.com
   ```

### 步骤5：测试访问

访问你的Render地址：
```
https://your-app-name.onrender.com
```

**测试流程：**
1. 输入你的QQ邮箱
2. 点击"发送验证码"
3. 查看邮箱，输入验证码
4. 登录成功，查看余额（默认免费次数）
5. 购买套餐（模拟支付）
6. 生成文案
7. 查看结果

## 🔧 常见问题

### Q1: 部署失败怎么办？

**检查日志：**
1. 在Render Dashboard找到你的服务
2. 点击 `Logs` 标签
3. 查看错误信息

**常见错误：**
- `Module not found`: 检查 `requirements.txt`
- `Port already in use`: 修改 `start.sh` 中的端口
- `Permission denied`: 确保 `start.sh` 有执行权限

### Q2: 邮箱发送失败？

**检查配置：**
1. 确认QQ邮箱授权码正确
2. 确认SMTP配置正确
3. 检查Render环境变量是否正确配置

**获取QQ邮箱授权码：**
1. 登录QQ邮箱
2. 设置 → 账户
3. 开启POP3/SMTP服务
4. 生成授权码（16位字符）

### Q3: 服务访问慢？

**原因：**
- Render免费版有休眠机制
- 15分钟无访问会自动休眠
- 再次访问需要10秒左右唤醒

**解决方案：**
- 这是正常现象，免费版限制
- 如果需要持续在线，考虑升级付费版

### Q4: 如何查看API文档？

访问：`https://your-app-name.onrender.com/docs`

可以看到所有API接口和测试工具。

## 📊 部署后管理

### 查看服务状态

1. 登录Render Dashboard
2. 找到你的服务
3. 查看 `Events` 和 `Logs`

### 更新代码

修改本地代码后：

```bash
git add .
git commit -m "描述你的修改"
git push
```

Render会自动检测到更新并重新部署。

### 查看使用情况

1. 登录Render Dashboard
2. 找到你的服务
3. 点击 `Metrics` 查看流量、CPU、内存等

## 💰 推广赚钱

### 1. 分享链接

你的访问地址：
```
https://your-app-name.onrender.com
```

### 2. 推广渠道

**小红书：**
- 发布"我用AI生成小红书爆款文案的体验"
- 展示生成的效果
- 放上你的链接

**知乎：**
- 回答"如何快速写出小红书爆款文案"
- 提供你的工具链接

**朋友圈：**
- 分享给朋友使用
- 邀请测试

### 3. 定价建议

| 套餐 | 次数 | 价格 | 平均 |
|------|------|------|------|
| 体验包 | 1次 | 1元 | 1元/次 |
| 10次套餐 | 10次 | 8元 | 0.8元/次 |
| 50次套餐 | 50次 | 35元 | 0.7元/次 |
| 100次套餐 | 100次 | 60元 | 0.6元/次 |

### 4. 收入估算

假设日均100次使用：
- **日收入：** 100 × 0.7 = 70元
- **月收入：** 70 × 30 = 2,100元
- **年收入：** 2,100 × 12 = 25,200元

**投入：0元 | ROI：∞**

## 🎯 下一步优化

### 1. 对接真实支付

当前是模拟支付，对接真实支付：

**微信支付：**
1. 注册微信支付商户号
2. 获取AppID、MCH_ID、API_KEY
3. 更新环境变量
4. 修改 `api/routers/payment.py`

**支付宝：**
1. 注册支付宝开放平台
2. 创建应用
3. 获取AppID、应用私钥
4. 更新代码

### 2. 添加更多功能

- 批量生成
- 历史记录导出
- 模板收藏
- 用户反馈系统

### 3. 优化用户体验

- 加载动画
- 错误提示优化
- 移动端适配优化
- 暗色模式

## 📞 需要帮助？

**查看文档：**
- README.md - 详细说明
- DEPLOYMENT.md - 本部署指南

**查看API文档：**
- 访问 `/docs` 查看所有接口

**查看日志：**
- 在Render Dashboard查看实时日志

## 🎉 恭喜！

你已经成功部署了零成本小红书文案生成器！

**现在：**
1. 访问你的地址测试功能
2. 分享给朋友使用
3. 开始推广赚钱

**记住：**
- 总成本：0元
- 收入潜力：月入2000-30000元
- 投资回报率：∞

**开始赚钱吧！💰🚀**
