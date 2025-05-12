# backend.py
import sqlite3
from datetime import datetime

DB = "cases.db"

def add_case(user_id, title, desc):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO cases (user_id, title, description, status) VALUES (?, ?, ?, 'open')",
                (user_id, title, desc))
    conn.commit()
    conn.close()

def get_cases():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, title, status FROM cases")
    cases = cur.fetchall()
    conn.close()
    return cases

def assign_case(case_id, consultant_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE cases SET consultant_id = ?, status = 'in progress' WHERE id = ?",
                (consultant_id, case_id))
    conn.commit()
    conn.close()

def get_analytics():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cases")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM cases WHERE status = 'approved'")
    approved = cur.fetchone()[0]
    conn.close()
    rate = (approved / total) * 100 if total else 0
    return total, approved, round(rate, 2)
