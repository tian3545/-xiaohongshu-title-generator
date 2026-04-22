# 🌸 小红书文案生成器 - 零成本按次付费方案

完全零成本的小红书爆款文案生成器，采用按次付费模式，无需购买服务器，无需购买域名，立即开始赚钱！

## ✨ 特色功能

- ✅ **完全零成本启动** - 使用Render免费服务器、SQLite数据库、免费邮箱验证
- ✅ **按次付费模式** - 用户购买套餐，灵活计费
- ✅ **邮箱验证登录** - 无需短信成本，免费邮箱验证
- ✅ **自动HTTPS** - 免费SSL证书
- ✅ **精美前端界面** - 响应式设计，支持手机访问
- ✅ **完整的用户系统** - 注册、登录、余额、订单、历史记录

## 📊 成本清单

| 项目 | 成本 | 说明 |
|------|------|------|
| 服务器 | **0元** | Render免费版（512MB，无限带宽） |
| 域名 | **0元** | 使用Render免费域名 |
| SSL证书 | **0元** | Let's Encrypt自动免费 |
| 数据库 | **0元** | SQLite文件数据库 |
| 短信验证 | **0元** | 改为邮箱验证 |
| 支付接口 | **0元** | 微信支付/支付宝（只收0.6%手续费） |
| 云存储 | **0元** | 阿里云OSS 5GB免费额度 |
| **总启动成本** | **0元** | 真正的零成本！ |

## 🚀 快速部署（5分钟）

### 第一步：准备代码

```bash
# 1. 克隆或下载代码到本地

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化数据库
python database.py
```

### 第二步：配置环境变量

创建 `.env` 文件：

```env
# 邮箱配置（使用免费邮箱，如QQ邮箱、163邮箱）
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
SMTP_USER=your_email@qq.com
SMTP_PASSWORD=your_smtp_password  # QQ邮箱需要申请授权码

# JWT配置（修改为随机字符串）
SECRET_KEY=your-secret-key-change-this-in-production

# 微信支付配置（可选，用于正式支付）
WECHAT_APPID=
WECHAT_MCH_ID=
WECHAT_API_KEY=
WECHAT_NOTIFY_URL=

# 支付宝配置（可选）
ALIPAY_APPID=
ALIPAY_PRIVATE_KEY=
ALIPAY_PUBLIC_KEY=
ALIPAY_NOTIFY_URL=
```

**获取QQ邮箱授权码：**
1. 登录QQ邮箱
2. 设置 -> 账户
3. 开启POP3/SMTP服务
4. 获取授权码

### 第三步：提交到GitHub

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 连接GitHub仓库
git remote add origin https://github.com/your-username/your-repo.git

# 推送到GitHub
git push -u origin main
```

### 第四步：部署到Render

1. 访问 https://render.com
2. 用GitHub账号登录（免费）
3. 点击 "New" -> "Web Service"
4. 连接你的GitHub仓库
5. 配置如下：
   - **Name**: xiaohongshu-generator
   - **Environment**: Python 3
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
6. 点击 "Deploy Web Service"
7. 等待2-5分钟，部署完成

### 第五步：配置环境变量

在Render中配置环境变量：

1. 进入你的Web Service
2. 点击 "Environment"
3. 添加环境变量（与第二步相同）
4. 点击 "Save Changes"
5. 点击 "Manual Deploy" -> "Clear build cache & deploy"

### 第六步：访问应用

部署完成后，你会获得一个免费域名：
```
https://your-app-name.onrender.com
```

访问这个域名就可以使用你的小红书文案生成器了！

## 📁 项目结构

```
.
├── api/                    # 后端API
│   ├── main.py            # FastAPI主入口
│   └── routers/           # 路由
│       ├── auth.py        # 认证（登录/注册）
│       ├── content.py     # 内容生成
│       ├── payment.py     # 支付
│       └── user.py        # 用户管理
├── web/                    # 前端
│   ├── index.html         # 主页面
│   └── static/            # 静态文件
│       ├── css/
│       │   └── style.css  # 样式
│       └── js/
│           └── app.js     # 前端逻辑
├── config/                 # 配置
│   └── settings.py        # 配置管理
├── database.py            # 数据库（SQLite）
├── email_verification.py  # 邮箱验证
├── requirements.txt       # Python依赖
├── runtime.txt            # Python版本
├── start.sh               # 启动脚本
└── README.md             # 说明文档
```

## 💰 收费方案

### 套餐配置（可在database.py中修改）

| 套餐名称 | 次数 | 价格 | 平均价格 |
|----------|------|------|----------|
| 体验包 | 1次 | 1元 | 1元/次 |
| 10次套餐 | 10次 | 8元 | 0.8元/次 |
| 50次套餐 | 50次 | 35元 | 0.7元/次 |
| 100次套餐 | 100次 | 60元 | 0.6元/次 |

## 💡 收入估算

假设：
- 日均使用100次
- 平均单价0.7元/次
- 月收入：100 × 30 × 0.7 = 2,100元
- 年收入：2,100 × 12 = 25,200元

**投入成本：0元**
**ROI：∞（无限大）**

## 🔧 本地开发

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库
python database.py

# 3. 启动服务
python -m uvicorn api.main:app --reload

# 4. 访问
http://localhost:8000
```

## 📱 接入真实支付

### 微信支付

1. 注册微信支付商户号：https://pay.weixin.qq.com/
2. 获取appid、mch_id、api_key
3. 配置回调URL
4. 修改代码中的支付逻辑

### 支付宝

1. 注册支付宝开放平台：https://open.alipay.com/
2. 创建应用获取appid
3. 配置公钥私钥
4. 修改代码中的支付逻辑

## ⚠️ 注意事项

### 1. 免费资源限制

**Render免费版：**
- 15分钟无访问会休眠
- 再次访问10秒内唤醒
- 512MB内存

**阿里云OSS免费额度：**
- 5GB存储空间
- 每月5GB流量

**应对策略：**
- 定期清理旧图片
- 压缩图片大小
- 定期备份SQLite数据库

### 2. 邮箱发送限制

免费邮箱可能有发送限制：
- QQ邮箱：每天约50封
- 163邮箱：每天约200封

**应对策略：**
- 使用多个邮箱轮换
- 或者直接让用户设置密码登录
- 或搭建自己的SMTP服务器

### 3. 安全性

生产环境需要：
- 修改SECRET_KEY为强密码
- 启用HTTPS（Render自动支持）
- 限制API请求频率
- 定期备份数据库

## 🎯 后续优化方向

1. **接入真实支付** - 微信支付/支付宝
2. **优化智能体** - 接入你的小红书文案智能体
3. **图片存储** - 使用阿里云OSS存储生成的图片
4. **数据统计** - 添加用户行为分析
5. **推广运营** - 在小红书、知乎、抖音推广
6. **功能增强** - 添加更多模板、风格选择

## 📞 技术支持

如有问题，请：
1. 查看Render日志
2. 检查环境变量配置
3. 查看API文档：http://your-domain.com/docs

## 🎉 开始赚钱

1. ✅ 零成本部署（5分钟）
2. ✅ 分享给朋友使用
3. ✅ 在小红书、知乎、抖音推广
4. ✅ 开始收钱！

**记住：成本是0元，收入是无限的！**

---

**祝你赚大钱！💰🚀**
