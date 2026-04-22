import sqlite3
from contextlib import contextmanager
from datetime import datetime
import os
from typing import Optional, List, Dict, Any

# 数据库文件路径
DB_PATH = os.getenv("DB_PATH", "data/app.db")

# 确保数据目录存在
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

@contextmanager
def get_db():
    """获取数据库连接上下文管理器"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """初始化数据库表"""
    with get_db() as conn:
        # 用户表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)

        # 用户余额表（剩余次数）
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_balance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                remaining_count INTEGER DEFAULT 0,
                total_purchased INTEGER DEFAULT 0,
                total_used INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # 套餐表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                count INTEGER NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 订单表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                package_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                count INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                payment_method TEXT,
                paid_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (package_id) REFERENCES packages (id)
            )
        """)

        # 使用记录表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic TEXT,
                need_images BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # 插入默认套餐（如果不存在）
        cursor = conn.execute("SELECT COUNT(*) FROM packages")
        if cursor.fetchone()[0] == 0:
            conn.executemany("""
                INSERT INTO packages (name, count, price, description, sort_order)
                VALUES (?, ?, ?, ?, ?)
            """, [
                ("体验包", 1, 1.0, "体验一下，1次生成", 1),
                ("10次套餐", 10, 8.0, "超值套餐，平均0.8元/次", 2),
                ("50次套餐", 50, 35.0, "热门套餐，平均0.7元/次", 3),
                ("100次套餐", 100, 60.0, "畅享套餐，平均0.6元/次", 4),
            ])

# ===== 用户操作 =====

def create_user(email: str, password_hash: Optional[str] = None) -> int:
    """创建用户"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )
        user_id = cursor.lastrowid

        # 创建用户余额记录
        conn.execute(
            "INSERT INTO user_balance (user_id, remaining_count) VALUES (?, ?)",
            (user_id, 0)
        )

        return user_id

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """根据邮箱获取用户"""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """根据ID获取用户"""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def update_user_last_login(user_id: int):
    """更新用户最后登录时间"""
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (datetime.now(), user_id)
        )

# ===== 用户余额操作 =====

def get_user_balance(user_id: int) -> Optional[Dict[str, Any]]:
    """获取用户余额"""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM user_balance WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        # 如果没有余额记录，创建一个
        conn.execute(
            "INSERT INTO user_balance (user_id, remaining_count) VALUES (?, ?)",
            (user_id, 0)
        )
        return {"user_id": user_id, "remaining_count": 0, "total_purchased": 0, "total_used": 0}

def add_balance(user_id: int, count: int):
    """增加用户余额（购买套餐后调用）"""
    with get_db() as conn:
        conn.execute("""
            UPDATE user_balance
            SET remaining_count = remaining_count + ?,
                total_purchased = total_purchased + ?,
                updated_at = ?
            WHERE user_id = ?
        """, (count, count, datetime.now(), user_id))

def use_balance(user_id: int) -> bool:
    """使用一次余额（生成文案时调用）"""
    with get_db() as conn:
        # 先检查余额是否足够
        cursor = conn.execute(
            "SELECT remaining_count FROM user_balance WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        if not result or result[0] <= 0:
            return False

        # 扣除余额
        conn.execute("""
            UPDATE user_balance
            SET remaining_count = remaining_count - 1,
                total_used = total_used + 1,
                updated_at = ?
            WHERE user_id = ?
        """, (datetime.now(), user_id))

        return True

# ===== 套餐操作 =====

def get_all_packages() -> List[Dict[str, Any]]:
    """获取所有可用套餐"""
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT * FROM packages WHERE is_active = 1 ORDER BY sort_order"
        )
        return [dict(row) for row in cursor.fetchall()]

def get_package_by_id(package_id: int) -> Optional[Dict[str, Any]]:
    """根据ID获取套餐"""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM packages WHERE id = ?", (package_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

# ===== 订单操作 =====

def create_order(user_id: int, package_id: int) -> Dict[str, Any]:
    """创建订单"""
    package = get_package_by_id(package_id)
    if not package:
        raise ValueError("套餐不存在")

    order_no = f"ORD{int(datetime.now().timestamp())}{user_id}"

    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO orders (order_no, user_id, package_id, amount, count)
            VALUES (?, ?, ?, ?, ?)
        """, (order_no, user_id, package_id, package['price'], package['count']))

        order_id = cursor.lastrowid
        order = get_order_by_id(order_id)

        return order

def get_order_by_id(order_id: int) -> Optional[Dict[str, Any]]:
    """根据ID获取订单"""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def get_order_by_no(order_no: str) -> Optional[Dict[str, Any]]:
    """根据订单号获取订单"""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM orders WHERE order_no = ?", (order_no,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def update_order_status(order_no: str, status: str, payment_method: Optional[str] = None):
    """更新订单状态"""
    with get_db() as conn:
        params = [status, order_no]
        if payment_method:
            conn.execute("""
                UPDATE orders
                SET status = ?, payment_method = ?, paid_at = ?
                WHERE order_no = ?
            """, (status, payment_method, datetime.now(), order_no))
        else:
            conn.execute("UPDATE orders SET status = ? WHERE order_no = ?", params)

def get_user_orders(user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
    """获取用户订单列表"""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM orders
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]

# ===== 使用记录操作 =====

def log_usage(user_id: int, topic: str, need_images: bool):
    """记录使用"""
    with get_db() as conn:
        conn.execute("""
            INSERT INTO usage_logs (user_id, topic, need_images)
            VALUES (?, ?, ?)
        """, (user_id, topic, need_images))

def get_user_usage_logs(user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
    """获取用户使用记录"""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM usage_logs
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]

# 初始化数据库
if __name__ == "__main__":
    init_db()
    print("数据库初始化成功！")
