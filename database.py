#!/usr/bin/python
import sqlite3
import os

# Always use the same absolute DB path as this file
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def connect_to_db():
    return sqlite3.connect(DB_PATH)

def create_db_table():
    conn = connect_to_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
              user_id INTEGER PRIMARY KEY AUTOINCREMENT,
              name    TEXT NOT NULL,
              email   TEXT NOT NULL,
              phone   TEXT NOT NULL,
              address TEXT NOT NULL,
              country TEXT NOT NULL
            );
        """)
        conn.commit()
        print("User table ready")
    except Exception as e:
        print("User table creation failed:", e)
    finally:
        conn.close()

def insert_user(user):
    inserted_user = {}
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (user['name'], user['email'], user['phone'], user['address'], user['country'])
        )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        print("insert_user error:", e)
        conn.rollback()          # <-- fixed
    finally:
        conn.close()
    return inserted_user

def get_users():
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    users = []
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for r in rows:
            users.append({
                "user_id": r["user_id"],
                "name": r["name"],
                "email": r["email"],
                "phone": r["phone"],
                "address": r["address"],
                "country": r["country"],
            })
        return users              # <-- ensure return on success
    except Exception as e:
        print("get_users error:", e)
        return []                 # safe fallback
    finally:
        conn.close()

def get_user_by_id(user_id):
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            return {}             # not found
        return {
            "user_id": row["user_id"],
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"],
            "address": row["address"],
            "country": row["country"],
        }
    except Exception as e:
        print("get_user_by_id error:", e)
        return {}
    finally:
        conn.close()

def update_user(user):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
            (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"])
        )
        conn.commit()
        return get_user_by_id(user["user_id"])
    except Exception as e:
        print("update_user error:", e)
        conn.rollback()
        return {}
    finally:
        conn.close()

def delete_user(user_id):
    conn = connect_to_db()
    try:
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        return {"status": "User deleted successfully"}
    except Exception as e:
        print("delete_user error:", e)
        conn.rollback()
        return {"status": "Cannot delete user"}
    finally:
        conn.close()

if __name__ == "__main__":
    create_db_table()
