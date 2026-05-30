import sqlite3
from datetime import datetime, timedelta

DB_NAME = "shop_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            balance INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Новичок',
            purchases_count INTEGER DEFAULT 0,
            total_spent INTEGER DEFAULT 0
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price INTEGER,
            stock INTEGER,
            category TEXT,
            description TEXT,
            photo_id TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            price INTEGER,
            booked_at TEXT,
            expires_at TEXT,
            status TEXT DEFAULT 'active'
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            price INTEGER,
            purchased_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    populate_sample_products()

def populate_sample_products():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        sample = [
            (1, "Корм ProBalance 2кг", 890, 7, "Корм", "Полнорационный сухой корм для кошек.", ""),
            (2, "Шампунь гипоаллергенный", 450, 12, "Гигиена", "Деликатный шампунь 300мл.", ""),
            (3, "Игрушка-мышка с мятой", 180, 23, "Игрушки", "Кошачья игрушка с кошачьей мятой.", ""),
        ]
        cur.executemany("INSERT INTO products (id, name, price, stock, category, description, photo_id) VALUES (?,?,?,?,?,?,?)", sample)
        conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def create_user(user_id, username, full_name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?,?,?)", (user_id, username, full_name))
    conn.commit()
    conn.close()

def update_user_purchase(user_id, amount):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT purchases_count, total_spent, balance FROM users WHERE user_id = ?", (user_id,))
    count, spent, bal = cur.fetchone()
    new_count = count + 1
    new_spent = spent + amount
    new_bal = bal + int(amount * 0.1)
    if new_count >= 10:
        status = "Постоянный"
    elif new_count >= 5:
        status = "Покупатель"
    else:
        status = "Новичок"
    cur.execute("UPDATE users SET purchases_count = ?, total_spent = ?, balance = ?, status = ? WHERE user_id = ?",
                (new_count, new_spent, new_bal, status, user_id))
    conn.commit()
    conn.close()
    return new_bal

def get_products_by_category(category):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if category:
        cur.execute("SELECT id, name, price, stock, photo_id FROM products WHERE category = ?", (category,))
    else:
        cur.execute("SELECT id, name, price, stock, photo_id FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_product(product_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, stock, description, photo_id FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row

def create_booking(user_id, product_id, product_name, price):
    expires = datetime.now() + timedelta(hours=24)
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO bookings (user_id, product_id, product_name, price, booked_at, expires_at)
        VALUES (?,?,?,?,?,?)
    ''', (user_id, product_id, product_name, price, datetime.now().isoformat(), expires.isoformat()))
    cur.execute("UPDATE products SET stock = stock - 1 WHERE id = ?", (product_id,))
    conn.commit()
    booking_id = cur.lastrowid
    conn.close()
    return booking_id, expires

def get_active_booking(user_id, product_id=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if product_id:
        cur.execute("SELECT * FROM bookings WHERE user_id = ? AND product_id = ? AND status = 'active'", (user_id, product_id))
    else:
        cur.execute("SELECT * FROM bookings WHERE user_id = ? AND status = 'active' ORDER BY expires_at", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row

def cancel_booking(booking_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE bookings SET status = 'cancelled' WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

def complete_booking(booking_id, product_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE bookings SET status = 'completed' WHERE id = ?", (booking_id,))
    cur.execute("INSERT INTO purchases (user_id, product_id, product_name, price, purchased_at) SELECT user_id, product_id, product_name, price, ? FROM bookings WHERE id = ?",
                (datetime.now().isoformat(), booking_id))
    conn.commit()
    conn.close()

def get_expiring_bookings(minutes=60):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    expire_limit = (datetime.now() + timedelta(minutes=minutes)).isoformat()
    cur.execute("SELECT id, user_id, product_name, expires_at FROM bookings WHERE status = 'active' AND expires_at <= ?", (expire_limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
