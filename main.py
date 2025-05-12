# main.py
import sqlite3
from db_setup import setup_db
from datetime import datetime

def view_cases():
    conn = sqlite3.connect("cases.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cases")
    cases = cur.fetchall()
    for case in cases:
        print(case)
    conn.close()

def add_case():
    title = input("Case Title: ")
    desc = input("Description: ")
    user_id = int(input("User ID: "))
    conn = sqlite3.connect("cases.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO cases (user_id, title, description, status) VALUES (?, ?, ?, ?)",
                (user_id, title, desc, 'open'))
    conn.commit()
    conn.close()
    print("✅ Case added.")

def assign_case():
    case_id = int(input("Enter Case ID: "))
    consultant_id = int(input("Enter Consultant ID: "))
    conn = sqlite3.connect("cases.db")
    cur = conn.cursor()
    cur.execute("UPDATE cases SET consultant_id = ?, status = 'in progress' WHERE id = ?",
                (consultant_id, case_id))
    conn.commit()
    conn.close()
    print("✅ Case assigned.")

def send_message():
    sender = int(input("Sender ID: "))
    receiver = int(input("Receiver ID: "))
    msg = input("Message: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("cases.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (sender_id, receiver_id, message, timestamp) VALUES (?, ?, ?, ?)",
                (sender, receiver, msg, timestamp))
    conn.commit()
    conn.close()
    print("✅ Message sent.")

def view_analytics():
    conn = sqlite3.connect("cases.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cases")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM cases WHERE status = 'approved'")
    approved = cur.fetchone()[0]
    approval_rate = (approved / total) * 100 if total else 0
    print(f"📊 Total Cases: {total}, Approved: {approved}, Approval Rate: {approval_rate:.2f}%")
    conn.close()

def menu():
    setup_db()
    while True:
        print("""
        1. View Cases
        2. Add Case
        3. Assign Case
        4. Send Message
        5. View Analytics
        0. Exit
        """)
        choice = input("Enter choice: ")
        if choice == '1':
            view_cases()
        elif choice == '2':
            add_case()
        elif choice == '3':
            assign_case()
        elif choice == '4':
            send_message()
        elif choice == '5':
            view_analytics()
        elif choice == '0':
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu()
