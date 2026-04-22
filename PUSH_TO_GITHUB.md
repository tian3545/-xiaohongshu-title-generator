# 推送代码到GitHub

## 🔑 获取GitHub Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 点击底部的 "Generate token"
5. **复制Token（只显示一次，立即复制！）**

## 📤 推送代码

### 方法1：使用Token推送（推荐）

```bash
git push -u origin main
```

当提示输入密码时，粘贴你的Token（不是GitHub登录密码）

### 方法2：配置凭证（只需配置一次）

```bash
# 配置凭证存储
git config --global credential.helper store

# 再次推送
git push -u origin main
```

输入用户名：`tian3545`
输入密码：粘贴你的Token

## ✅ 推送成功后

你的代码会在：https://github.com/tian3545/xiaohongshu-generator

然后就可以部署到Render了！
