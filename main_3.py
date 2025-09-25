import telebot
import requests
import json
import os
import time
import threading
from datetime import datetime, timedelta

# ================== الإعدادات ==================
TOKEN = "7784857432:AAE4OaI61C8UlGEU_xKsweqm3PsfZvsnD3Q"
bot = telebot.TeleBot(TOKEN)

USERS_FILE = "users.json"
UIDS_FILE = "uids.json"
GROUPS_FILE = "groups.json"
LOG_FILE = "log.txt"
OWNERS_FILE = "owners.json"

OWNERS = [123456789]  # ضع هنا الآي دي الخاص بك (المالكين)

# ================== دوال مساعدة ==================
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_data(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def log_action(action):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {action}\n")

def save_owners(owners):
    with open(OWNERS_FILE, "w") as f:
        json.dump(owners, f, indent=4)

def load_owners():
    if os.path.exists(OWNERS_FILE):
        with open(OWNERS_FILE, "r") as f:
            return json.load(f)
    return OWNERS

# ================== إدارة المستخدمين ==================
def add_user(user_id, username, rank):
    users = load_data(USERS_FILE)
    users[str(user_id)] = {"username": username, "rank": rank}
    save_data(users, USERS_FILE)
    log_action(f"إضافة مستخدم: {username} (ID: {user_id}, Rank: {rank})")

def remove_user(user_id):
    users = load_data(USERS_FILE)
    if str(user_id) in users:
        username = users[str(user_id)]["username"]
        del users[str(user_id)]
        save_data(users, USERS_FILE)
        log_action(f"حذف مستخدم: {username} (ID: {user_id})")

def get_user_rank(user_id):
    users = load_data(USERS_FILE)
    return users.get(str(user_id), {}).get("rank", 0)

# ================== إدارة المجموعات ==================
def add_group(group_id, name):
    groups = load_data(GROUPS_FILE)
    groups[str(group_id)] = {"name": name}
    save_data(groups, GROUPS_FILE)
    log_action(f"إضافة مجموعة: {name} (ID: {group_id})")

def remove_group(group_id):
    groups = load_data(GROUPS_FILE)
    if str(group_id) in groups:
        name = groups[str(group_id)]["name"]
        del groups[str(group_id)]
        save_data(groups, GROUPS_FILE)
        log_action(f"حذف مجموعة: {name} (ID: {group_id})")

# ================== أوامر البوت ==================
@bot.message_handler(commands=["start"])
def start_command(message):
    bot.reply_to(message, "✅ البوت شغال، أرسل /help لعرض الأوامر")

@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = """
🛠 أوامر البوت:
- /start : تشغيل البوت
- /help : عرض الأوامر
"""
    bot.reply_to(message, help_text)

# ================== مهمة الحذف التلقائي ==================
def auto_remove_expired():
    while True:
        # هنا من المفترض تتحقق من الاشتراكات المنتهية وتحذفها
        time.sleep(3600)  # كل ساعة

# ================== التشغيل ==================
if __name__ == "__main__":
    # إنشاء الملفات إذا لم تكن موجودة
    for filename in [USERS_FILE, UIDS_FILE, GROUPS_FILE, LOG_FILE, OWNERS_FILE]:
        if not os.path.exists(filename):
            if filename == OWNERS_FILE:
                save_owners(OWNERS)
            elif filename != LOG_FILE:
                save_data({}, filename)
            else:
                open(filename, 'w').close()

    # إضافة المالكين الافتراضيين
    users = load_data(USERS_FILE)
    for owner_id in OWNERS:
        if str(owner_id) not in users:
            try:
                user_info = bot.get_chat(owner_id)
                username = user_info.username or user_info.first_name
                add_user(owner_id, username, 999)
            except:
                add_user(owner_id, f"owner_{owner_id}", 999)

    # تشغيل مهمة الحذف التلقائي بالخلفية
    threading.Thread(target=auto_remove_expired, daemon=True).start()

    # تشغيل البوت
    print("✅ البوت شغال الآن...")
    bot.infinity_polling(skip_pending=True)
