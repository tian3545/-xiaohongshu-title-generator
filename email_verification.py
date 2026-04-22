import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os
from datetime import datetime, timedelta
from typing import Optional

# 邮箱配置（使用免费邮箱）
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.qq.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "your_email@qq.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_smtp_password")

# 验证码存储（生产环境建议用Redis）
verification_codes = {}

def generate_code(length: int = 6) -> str:
    """生成验证码"""
    return ''.join(random.choices(string.digits, k=length))

def send_verification_email(to_email: str, code: str) -> bool:
    """发送验证邮件"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = '【小红书文案生成器】验证码'

        body = f"""
        <html>
        <body>
            <h2>您好！</h2>
            <p>您的验证码是：<strong style="font-size: 24px; color: #ff6b6b;">{code}</strong></p>
            <p>10分钟内有效，请勿泄露给他人。</p>
            <p>如非本人操作，请忽略此邮件。</p>
            <hr>
            <p style="color: #999; font-size: 12px;">小红书文案生成器</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html', 'utf-8'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return False

def send_code(email: str) -> tuple[bool, str]:
    """发送验证码"""
    code = generate_code()
    verification_codes[email] = {
        'code': code,
        'expire_time': datetime.now() + timedelta(minutes=10),
        'created_at': datetime.now()
    }

    success = send_verification_email(email, code)
    if success:
        return True, "验证码已发送到您的邮箱"
    else:
        del verification_codes[email]
        return False, "发送失败，请检查邮箱配置"

def verify_code(email: str, input_code: str) -> bool:
    """验证验证码"""
    if email not in verification_codes:
        return False

    record = verification_codes[email]

    # 检查是否过期
    if datetime.now() > record['expire_time']:
        del verification_codes[email]
        return False

    # 检查验证码是否正确
    if record['code'] == input_code:
        del verification_codes[email]
        return True

    return False

def get_remaining_time(email: str) -> Optional[int]:
    """获取剩余时间（秒）"""
    if email not in verification_codes:
        return None

    record = verification_codes[email]
    remaining = (record['expire_time'] - datetime.now()).total_seconds()
    return int(remaining) if remaining > 0 else 0

def clean_expired_codes():
    """清理过期的验证码"""
    now = datetime.now()
    expired_emails = [
        email for email, record in verification_codes.items()
        if now > record['expire_time']
    ]
    for email in expired_emails:
        del verification_codes[email]
