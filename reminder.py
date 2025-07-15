import smtplib
import sqlite3
import os
from datetime import datetime
from ai_helper import is_urgent
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# Load credentials from .env file
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_email(subject, body):
    # Encode subject and body using UTF-8 to support emojis
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = formataddr(('🧠 Deadline Agent', EMAIL_SENDER))
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"📧 Email sent: {subject}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def check_tasks():
    print("🔎 Checking tasks...")
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status='Pending'")
    tasks = cur.fetchall()
    for task in tasks:
        task_id, name, deadline, priority, status = task
        if is_urgent(deadline):
            print(f"📨 Sending reminder for task: {name}")
            send_email(
                f"⏰ Urgent: {name} Due Soon",
                f"Hey there!\n\nYour task '{name}' is due at {deadline}.\nPriority: {priority}\n\n- Deadline Agent 🤖"
            )
    conn.close()

# Run the reminder agent
check_tasks()

