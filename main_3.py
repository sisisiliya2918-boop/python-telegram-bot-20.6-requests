import requests, urllib3, os, json, re, time, threading
from datetime import datetime
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from google.protobuf import json_format
import Fo_pb2
import telebot
from telebot import types
from xGeTJwT import xGeT

# تعطيل تحذيرات urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============ إعدادات التكوين ============
key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

JWT_UID = "4016344983"
JWT_PW = "D61AF8D47D5A22D322658C6DD4DE33B929A277C915BCF9DDBF7CBD2488769A02"
TELEGRAM_TOKEN = "7784857432:AAE4OaI61C8UlGEU_xKsweqm3PsfZvsnD3Q" 
DEFAULT_OWNERS = [6661768021]  # قائمة المالكين الافتراضية

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode='HTML')

# ============ إدارة الملفات ============
USERS_FILE = 'users.json'
UIDS_FILE = 'uids.json'
GROUPS_FILE = 'groups.json'
LOG_FILE = 'bot_log.txt'
OWNERS_FILE = 'owners.json'

def clean_text(text):
    """تنظيف النص من الأحرف الخاصة"""
    if not text:
        return ""
    return str(text).replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')

def log_action(action, user_id=None, details=""):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {action}"
    if user_id:
        log_entry += f" | User: {user_id}"
    if details:
        log_entry += f" | Details: {clean_text(details)}"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_owners():
    try:
        with open(OWNERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('owners', DEFAULT_OWNERS)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_OWNERS

def save_owners(owners_list):
    with open(OWNERS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'owners': owners_list}, f, indent=4)

# تحميل قائمة المالكين
OWNERS = load_owners()

# ============ دوال الردود JSON ============
def json_response(success, message, data=None, command=None):
    """إنشاء رد بتنسيق JSON"""
    response = {
        "status": "success" if success else "error",
        "message": message,
        "data": data if data else {},
        "command": command,
        "timestamp": datetime.now().isoformat(),
        "bot": "FriendPanelBot",
        "version": "2.1 X"
    }
    return json.dumps(response, ensure_ascii=False, indent=2)

def send_json_response(chat_id, message, success=True, data=None, command=None, reply_to_message_id=None):
    """إرسال رد JSON مع معالجة الأخطاء"""
    try:
        response = json_response(success, message, data, command)
        bot.send_message(chat_id, f"<pre>{response}</pre>", parse_mode='HTML', reply_to_message_id=reply_to_message_id)
    except Exception as e:
        log_action("JSON_RESPONSE_ERROR", details=str(e))
        bot.send_message(chat_id, "❌ حدث خطأ في معالجة طلبك", reply_to_message_id=reply_to_message_id)

# ============ إدارة المستخدمين ============
def add_user(user_id, username, points=3):
    users = load_data(USERS_FILE)
    users[str(user_id)] = {
        "username": clean_text(username),
        "points": points,
        "used": 0,
        "first_seen": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "last_active": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_data(users, USERS_FILE)
    log_action("NEW_USER", user_id, f"Username: {username} | Points: {points}")

def is_owner(user_id):
    """التحقق إذا كان المستخدم من المالكين"""
    return user_id in OWNERS

def is_allowed_user(user_id):
    """التحقق إذا كان المستخدم مسجلاً وله نقاط متبقية"""
    users = load_data(USERS_FILE)
    return str(user_id) in users and get_user_points(user_id) > 0

def update_user_activity(user_id):
    users = load_data(USERS_FILE)
    if str(user_id) in users:
        users[str(user_id)]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_data(users, USERS_FILE)

def use_point(user_id):
    users = load_data(USERS_FILE)
    if str(user_id) in users:
        if users[str(user_id)]['used'] < users[str(user_id)]['points']:
            users[str(user_id)]['used'] += 1
            save_data(users, USERS_FILE)
            log_action("POINT_USED", user_id, f"Remaining: {users[str(user_id)]['points'] - users[str(user_id)]['used']}")
            return True
    return False

def get_user_points(user_id):
    users = load_data(USERS_FILE)
    if str(user_id) in users:
        return users[str(user_id)]['points'] - users[str(user_id)]['used']
    return 0

def get_user_info(user_id):
    return load_data(USERS_FILE).get(str(user_id))

# ============ إدارة المجموعات ============
def add_group(group_id, group_title):
    groups = load_data(GROUPS_FILE)
    groups[str(group_id)] = {
        "title": clean_text(group_title),
        "activated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "active": True
    }
    save_data(groups, GROUPS_FILE)
    log_action("GROUP_ADDED", None, f"Group: {group_title} | ID: {group_id}")

def is_group_allowed(group_id):
    groups = load_data(GROUPS_FILE)
    return str(group_id) in groups and groups[str(group_id)].get('active', True)

# ============ دوال التشفير ============
def EnC_AEs(HeX):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()
    
def EnC_Vr(n):
    e = []
    while n:
        e.append((n & 0x7F) | (0x80 if n > 0x7F else 0))
        n >>= 7
    return bytes(e)
    
def EnC_Uid(n):
    e = []
    while n:
        e.append((n & 0x7F) | (0x80 if n > 0x7F else 0))
        n >>= 7
    return bytes(e).hex()
    
def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))           
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet.hex()

# ============ التواصل مع API ============
AUTH_TOKEN = None

def get_jwt_token(uid, pw):
    try:
        log_action("TOKEN_REQUEST")
        jwt_token = xGeT(uid, pw)
        if jwt_token:
            log_action("TOKEN_SUCCESS")
            return jwt_token
        else:
            log_action("TOKEN_FAILED")
            return None
    except Exception as e:
        log_action("TOKEN_ERROR", details=str(e))
        return None

def SEnd(UrL, PyL):
    global AUTH_TOKEN
    
    if not AUTH_TOKEN:
        AUTH_TOKEN = get_jwt_token(JWT_UID, JWT_PW)
        if not AUTH_TOKEN:
            return None, None, None
    
    try:
        H = requests.session().post(UrL, headers={
            "Expect": "100-continue",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB50",
            "Authorization": "Bearer " + AUTH_TOKEN,
            "Host": "loginbp.common.ggbluefox.com"
        }, data=PyL, verify=False)
        
        if H.status_code == 401:
            log_action("TOKEN_REFRESH")
            AUTH_TOKEN = get_jwt_token(JWT_UID, JWT_PW)
            if AUTH_TOKEN:
                H = requests.session().post(UrL, headers={
                    "Expect": "100-continue",
                    "X-Unity-Version": "2018.4.11f1",
                    "X-GA": "v1 1",
                    "ReleaseVersion": "OB50",
                    "Authorization": "Bearer " + AUTH_TOKEN,
                    "Host": "loginbp.common.ggbluefox.com"
                }, data=PyL, verify=False)
        
        log_action("API_REQUEST", details=f"URL: {UrL} | Status: {H.status_code}")
        return H.status_code, H.content, H.text
        
    except Exception as e:
        log_action("API_ERROR", details=str(e))
        return None, None, None

# ============ إدارة الأصدقاء ============
def Add_FrEind(Uid, days=None):
    UrL = 'https://clientbp.ggblueshark.com/RequestAddingFriend'
    PyL = f'08a7c4839f1e10{EnC_Uid(int(Uid))}1801'
    PyL = bytes.fromhex(EnC_AEs(PyL))
    status, _, _ = SEnd(UrL, PyL)
    
    if status == 200 and days:
        expire_time = add_uid_with_expiry(Uid, days)
        return expire_time
    return None
    
def DeLetE_FrEind(Uid):
    UrL = 'https://clientbp.ggblueshark.com/RemoveFriend'
    PyL = f'08a7c4839f1e10{EnC_Uid(int(Uid))}'
    PyL = bytes.fromhex(EnC_AEs(PyL))
    SEnd(UrL, PyL)
    
    uids = load_data(UIDS_FILE)
    if str(Uid) in uids:
        uids[str(Uid)]['status'] = 'removed'
        save_data(uids, UIDS_FILE)
        log_action("FRIEND_REMOVED", details=f"UID: {Uid}")
    
def Show_FrEinds():
    UrL = 'https://clientbp.ggblueshark.com/GetFriend'
    PyL = {1: 1, 2: 1, 7: 1}
    PyL = bytes.fromhex(EnC_AEs(CrEaTe_ProTo(PyL)))
    S, H, A = SEnd(UrL, PyL)
    if H is None:
        return []
    
    try:
        f = Fo_pb2.Friends()
        f.ParseFromString(H)
        P = json.loads(json_format.MessageToJson(f).encode('utf-8').decode('unicode_escape'))
        
        friends_list = []
        for entry in P.get("field1", []):
            friend_id = entry.get("ID", "غير معروف")
            friend_name = "غير معروف"
            for key, value in entry.items():
                if isinstance(value, str) and key != "ID":
                    friend_name = clean_text(value)
                    break
            friends_list.append((str(friend_id), friend_name))
        
        log_action("FRIENDS_LISTED", details=f"Count: {len(friends_list)}")
        return friends_list
    except Exception as e:
        log_action("FRIENDS_PARSE_ERROR", details=str(e))
        return []

def ChanGe_Bio(Bio):
    UrL = 'https://clientbp.ggblueshark.com/UpdateSocialBasicInfo'
    PyL = {2: 9, 8: f"{Bio}", 9: 1}
    PyL = bytes.fromhex(EnC_AEs(CrEaTe_ProTo(PyL)))
    SEnd(UrL, PyL)
    log_action("BIO_UPDATED", details=f"New bio: {Bio[:20]}...")

# ============ المهام الخلفية ============
def auto_remove_expired():
    while True:
        try:
            expired_uids = check_expired_uids()
            for uid in expired_uids:
                DeLetE_FrEind(uid)
                log_action("AUTO_REMOVAL", details=f"UID: {uid}")
        except Exception as e:
            log_action("AUTO_REMOVAL_ERROR", details=str(e))
        time.sleep(60 * 60)

def check_expired_uids():
    uids = load_data(UIDS_FILE)
    current_time = int(time.time())
    expired = []
    
    for uid, data in uids.items():
        if data.get('status') == 'active' and data.get('expire', 0) < current_time:
            expired.append(uid)
    
    return expired

def add_uid_with_expiry(uid, days):
    uids = load_data(UIDS_FILE)
    expire_time = int(time.time()) + (days * 24 * 60 * 60)
    uids[uid] = {
        "status": "active",
        "expire": expire_time,
        "added_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "added_by": "user"  # سيتم تحديثها لاحقاً
    }
    save_data(uids, UIDS_FILE)
    log_action("FRIEND_ADDED", details=f"UID: {uid} | Days: {days}")
    return expire_time

# ============ معالجة الأوامر ============
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private' and not is_owner(message.from_user.id):
        return
        
    # تسجيل المستخدم الجديد إذا لم يكن مسجلاً
    if not get_user_info(message.from_user.id):
        username = message.from_user.username or message.from_user.first_name
        initial_points = 3 if not is_owner(message.from_user.id) else 999
        add_user(message.from_user.id, username, initial_points)
        
    update_user_activity(message.from_user.id)
    user_info = get_user_info(message.from_user.id)
    
    response_data = {
        "user_id": message.from_user.id,
        "username": user_info.get('username'),
        "points": {
            "total": user_info.get('points', 0),
            "used": user_info.get('used', 0),
            "remaining": get_user_points(message.from_user.id)
        },
        "first_seen": user_info.get('first_seen'),
        "last_active": user_info.get('last_active'),
        "is_owner": is_owner(message.from_user.id)
    }
    send_json_response(message.chat.id, "مرحباً بك في البوت", True, response_data, "start", message.message_id)
    log_action("WELCOME_MESSAGE", message.from_user.id)

@bot.message_handler(commands=['help'])
def show_help(message):
    if message.chat.type == 'private' and not is_owner(message.from_user.id):
        return
        
    update_user_activity(message.from_user.id)
    help_text = """
<b>أوامر المستخدمين:</b>
/add &lt;ID&gt; &lt;أيام&gt; - إضافة صديق مع مدة محددة
/rm &lt;ID&gt; - حذف صديق
/show - عرض الأصدقاء
/points - عرض النقاط المتبقية
/bio &lt;نص&gt; - تغيير البايو
/stats - إحصائيات البوت
"""
    response_data = {"commands": help_text}
    send_json_response(message.chat.id, "قائمة الأوامر", True, response_data, "help", message.message_id)
    log_action("HELP_REQUESTED", message.from_user.id)

@bot.message_handler(commands=['owner'])
def owner_commands(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="owner", reply_to_message_id=message.message_id)
        return
    response_data = {
        "commands": [
            {"command": "/addowner [user_id]", "description": "إضافة مالك جديد"},
            {"command": "/removeowner [user_id]", "description": "إزالة مالك"},
            {"command": "/listowners", "description": "عرض قائمة المالكين"},
            {"command": "/adduser [user_id] [points]", "description": "إضافة مستخدم جديد"},
            {"command": "/allow [group_id]", "description": "تفعيل البوت في مجموعة"},
            {"command": "/delete_all", "description": "حذف جميع الأصدقاء"},
            {"command": "/bio [نص]", "description": "تغيير البايو"},
            {"command": "/stats", "description": "عرض إحصائيات البوت"}
        ]
    }
    
    try:
        send_json_response(message.chat.id, "أوامر المالكين", True, response_data, "owner", message.message_id)
    except Exception as e:
        log_action("OWNER_COMMANDS_ERROR", message.from_user.id, str(e))
        send_json_response(message.chat.id, "أوامر المالكين", True, response_data, "owner", message.message_id)
    
    log_action("OWNER_COMMANDS_VIEWED", message.from_user.id)

@bot.message_handler(commands=['allow'])
def allow_group(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="allow", reply_to_message_id=message.message_id)
        return
        
    try:
        group_id = message.text.split()[1]
        group_title = message.chat.title if message.chat.title else "Unknown Group"
        add_group(group_id, group_title)
        response_data = {
            "group_id": group_id,
            "group_title": group_title
        }
        send_json_response(message.chat.id, f"تم تفعيل البوت في المجموعة {clean_text(group_title)}", True, response_data, "allow", message.message_id)
    except:
        send_json_response(message.chat.id, "خطأ في الصيغة. استخدم: /allow <group_id>", False, command="allow", reply_to_message_id=message.message_id)

@bot.message_handler(commands=['adduser'])
def add_user_command(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="adduser", reply_to_message_id=message.message_id)
        return
        
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        points = int(parts[2])
        
        # الحصول على معلومات المستخدم من التلغرام
        user_info = bot.get_chat(user_id)
        username = user_info.username or user_info.first_name
        
        add_user(user_id, username, points)
        response_data = {
            "user_id": user_id,
            "username": username,
            "points": points
        }
        send_json_response(message.chat.id, "تمت إضافة المستخدم بنجاح", True, response_data, "adduser", message.message_id)
    except Exception as e:
        send_json_response(message.chat.id, f"خطأ: {str(e)}\nاستخدم: /adduser <user_id> <points>", False, command="adduser", reply_to_message_id=message.message_id)
        log_action("ADD_USER_ERROR", message.from_user.id, str(e))

@bot.message_handler(commands=['add'])
def add_friend(message):
    if message.chat.type == 'private' and not is_owner(message.from_user.id):
        return
        
    if message.chat.type in ['group', 'supergroup'] and not is_group_allowed(message.chat.id):
        return
        
    if not is_allowed_user(message.from_user.id) and not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="add", reply_to_message_id=message.message_id)
        return
        
    try:
        parts = message.text.split()
        if len(parts) < 2:
            send_json_response(message.chat.id, "خطأ في الصيغة. استخدم: /add <ID> <أيام>", False, command="add", reply_to_message_id=message.message_id)
            return
            
        uid = parts[1]
        days = int(parts[2]) if len(parts) > 2 else None
        
        if not uid.isdigit():
            send_json_response(message.chat.id, "يجب أن يكون ID رقمًا صحيحًا!", False, command="add", reply_to_message_id=message.message_id)
            return
            
        if not is_owner(message.from_user.id) and not use_point(message.from_user.id):
            send_json_response(message.chat.id, "ليس لديك نقاط كافية لإضافة أصدقاء!", False, command="add", reply_to_message_id=message.message_id)
            return
            
        if days:
            expire_time = Add_FrEind(uid, days)
            if expire_time:
                expire_date = datetime.fromtimestamp(expire_time).strftime('%Y-%m-%d %H:%M:%S')
                response_data = {
                    "uid": uid,
                    "expire_time": expire_time,
                    "expire_date": expire_date,
                    "remaining_points": get_user_points(message.from_user.id)
                }
                send_json_response(message.chat.id, "تم إرسال طلب إضافة الصديق بنجاح", True, response_data, "add", message.message_id)
            else:
                send_json_response(message.chat.id, "فشل في إضافة الصديق", False, command="add", reply_to_message_id=message.message_id)
        else:
            Add_FrEind(uid)
            response_data = {
                "uid": uid,
                "remaining_points": get_user_points(message.from_user.id)
            }
            send_json_response(message.chat.id, "تم إرسال طلب إضافة الصديق بنجاح", True, response_data, "add", message.message_id)
            
        update_user_activity(message.from_user.id)
    except Exception as e:
        send_json_response(message.chat.id, f"حدث خطأ: {str(e)}", False, command="add", reply_to_message_id=message.message_id)
        log_action("ADD_FRIEND_ERROR", message.from_user.id, str(e))

@bot.message_handler(commands=['points'])
def show_points(message):
    if message.chat.type == 'private' and not is_owner(message.from_user.id):
        return
        
    if message.chat.type in ['group', 'supergroup'] and not is_group_allowed(message.chat.id):
        return
        
    points = get_user_points(message.from_user.id)
    user_info = get_user_info(message.from_user.id)
    response_data = {
        "user_id": message.from_user.id,
        "points": {
            "total": user_info.get('points', 0),
            "used": user_info.get('used', 0),
            "remaining": points
        }
    }
    send_json_response(message.chat.id, "نقاطك الحالية", True, response_data, "points", message.message_id)
    update_user_activity(message.from_user.id)

@bot.message_handler(commands=['show'])
def show_friends(message):
    if message.chat.type == 'private' and not is_owner(message.from_user.id):
        return
        
    if message.chat.type in ['group', 'supergroup'] and not is_group_allowed(message.chat.id):
        return
        
    friends_list = Show_FrEinds()
    if not friends_list:
        send_json_response(message.chat.id, "لا يوجد أصدقاء لعرضهم حالياً", False, command="show", reply_to_message_id=message.message_id)
        return
        
    try:
        response_data = {
            "count": len(friends_list),
            "friends": [{"id": fid, "name": fname} for fid, fname in friends_list]
        }
        send_json_response(message.chat.id, f"تم العثور على {len(friends_list)} صديق", True, response_data, "show", message.message_id)
    except Exception as e:
        send_json_response(message.chat.id, f"حدث خطأ في عرض القائمة: {str(e)}", False, command="show", reply_to_message_id=message.message_id)
        log_action("SHOW_FRIENDS_ERROR", message.from_user.id, str(e))
    
    update_user_activity(message.from_user.id)

@bot.message_handler(commands=['rm'])
def remove_friend(message):
    if message.chat.type == 'private' and not is_owner(message.from_user.id):
        return
        
    if message.chat.type in ['group', 'supergroup'] and not is_group_allowed(message.chat.id):
        return
        
    try:
        command, uid = message.text.split(maxsplit=1)
        if not uid.isdigit():
            send_json_response(message.chat.id, "يجب أن يكون ID رقمًا صحيحًا!", False, command="rm", reply_to_message_id=message.message_id)
            return
            
        DeLetE_FrEind(uid)
        response_data = {"uid": uid}
        send_json_response(message.chat.id, "تم حذف الصديق بنجاح", True, response_data, "rm", message.message_id)
        update_user_activity(message.from_user.id)
    except:
        send_json_response(message.chat.id, "خطأ في الصيغة. استخدم: /rm <ID>", False, command="rm", reply_to_message_id=message.message_id)

@bot.message_handler(commands=['delete_all'])
def delete_all_friends(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="delete_all", reply_to_message_id=message.message_id)
        return
        
    friends_list = Show_FrEinds()
    if not friends_list:
        send_json_response(message.chat.id, "لا يوجد أصدقاء لحذفهم حالياً", False, command="delete_all", reply_to_message_id=message.message_id)
        return
        
    bot.send_message(message.chat.id, "⏳ <b>جاري حذف جميع الأصدقاء...</b>", reply_to_message_id=message.message_id)
    for fid, fname in friends_list:
        DeLetE_FrEind(fid)
        
    response_data = {"deleted_count": len(friends_list)}
    send_json_response(message.chat.id, f"تم الانتهاء من حذف {len(friends_list)} صديق", True, response_data, "delete_all", message.message_id)
    update_user_activity(message.from_user.id)

@bot.message_handler(commands=['bio'])
def change_bio(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="bio", reply_to_message_id=message.message_id)
        return
        
    try:
        command, bio_text = message.text.split(maxsplit=1)
        ChanGe_Bio(bio_text)
        response_data = {"bio": bio_text[:100] + "..." if len(bio_text) > 100 else bio_text}
        send_json_response(message.chat.id, "تم تغيير البايو بنجاح", True, response_data, "bio", message.message_id)
        update_user_activity(message.from_user.id)
    except:
        send_json_response(message.chat.id, "خطأ في الصيغة. استخدم: /bio <نص>", False, command="bio", reply_to_message_id=message.message_id)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="stats", reply_to_message_id=message.message_id)
        return
        
    users = load_data(USERS_FILE)
    groups = load_data(GROUPS_FILE)
    uids = load_data(UIDS_FILE)
    
    active_users = sum(1 for user in users.values() if user['points'] > user['used'])
    active_friends = sum(1 for uid in uids.values() if uid.get('status') == 'active')
    
    stats_data = {
        "users": {
            "total": len(users),
            "active": active_users
        },
        "groups": {
            "total": len(groups)
        },
        "friends": {
            "total": len(uids),
            "active": active_friends
        }
    }
    send_json_response(message.chat.id, "إحصائيات البوت", True, stats_data, "stats", message.message_id)
    log_action("STATS_VIEWED", message.from_user.id)

@bot.message_handler(commands=['addowner'])
def add_owner_command(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="addowner", reply_to_message_id=message.message_id)
        return
        
    try:
        new_owner_id = int(message.text.split()[1])
        if new_owner_id in OWNERS:
            send_json_response(message.chat.id, f"المستخدم ({new_owner_id}) موجود بالفعل في قائمة المالكين", True, {"owner_id": new_owner_id}, "addowner", message.message_id)
            return
            
        OWNERS.append(new_owner_id)
        save_owners(OWNERS)
        
        # إضافة المستخدم كمالك مع نقاط غير محدودة
        if not get_user_info(new_owner_id):
            try:
                user_info = bot.get_chat(new_owner_id)
                username = user_info.username or user_info.first_name
                add_user(new_owner_id, username, 999)
            except Exception as e:
                log_action("ADD_OWNER_ERROR", message.from_user.id, str(e))
        
        response_data = {
            "new_owner_id": new_owner_id,
            "total_owners": len(OWNERS),
            "action": "owner_added"
        }
        send_json_response(message.chat.id, f"تمت إضافة المالك الجديد بنجاح", True, response_data, "addowner", message.message_id)
        log_action("OWNER_ADDED", message.from_user.id, f"New owner: {new_owner_id}")
        
    except (IndexError, ValueError):
        send_json_response(message.chat.id, "خطأ في الصيغة. استخدم: /addowner <user_id>", False, command="addowner", reply_to_message_id=message.message_id)
    except Exception as e:
        send_json_response(message.chat.id, f"حدث خطأ: {str(e)}", False, command="addowner", reply_to_message_id=message.message_id)
        log_action("ADD_OWNER_ERROR", message.from_user.id, str(e))

@bot.message_handler(commands=['removeowner'])
def remove_owner_command(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="removeowner", reply_to_message_id=message.message_id)
        return
        
    try:
        owner_id = int(message.text.split()[1])
        if owner_id not in OWNERS:
            send_json_response(message.chat.id, f"المستخدم ({owner_id}) غير موجود في قائمة المالكين", False, {"owner_id": owner_id}, "removeowner", message.message_id)
            return
            
        OWNERS.remove(owner_id)
        save_owners(OWNERS)
        
        response_data = {
            "removed_owner_id": owner_id,
            "total_owners": len(OWNERS),
            "action": "owner_removed"
        }
        send_json_response(message.chat.id, f"تمت إزالة المالك بنجاح", True, response_data, "removeowner", message.message_id)
        log_action("OWNER_REMOVED", message.from_user.id, f"Removed owner: {owner_id}")
        
    except (IndexError, ValueError):
        send_json_response(message.chat.id, "خطأ في الصيغة. استخدم: /removeowner <user_id>", False, command="removeowner", reply_to_message_id=message.message_id)
    except Exception as e:
        send_json_response(message.chat.id, f"حدث خطأ: {str(e)}", False, command="removeowner", reply_to_message_id=message.message_id)
        log_action("REMOVE_OWNER_ERROR", message.from_user.id, str(e))

@bot.message_handler(commands=['listowners'])
def list_owners_command(message):
    if not is_owner(message.from_user.id):
        send_json_response(message.chat.id, "ليس لديك صلاحية استخدام هذا الأمر", False, command="listowners", reply_to_message_id=message.message_id)
        return
        
    owners_info = []
    for owner_id in OWNERS:
        try:
            user_info = bot.get_chat(owner_id)
            owners_info.append({
                "id": owner_id,
                "username": user_info.username,
                "first_name": user_info.first_name,
                "last_name": user_info.last_name
            })
        except Exception as e:
            owners_info.append({
                "id": owner_id,
                "error": "Unable to fetch info"
            })
            log_action("FETCH_OWNER_INFO_ERROR", message.from_user.id, f"Owner: {owner_id} | Error: {str(e)}")
    
    response_data = {
        "count": len(OWNERS),
        "owners": owners_info
    }
    send_json_response(message.chat.id, "قائمة المالكين", True, response_data, "listowners", message.message_id)
    log_action("OWNERS_LISTED", message.from_user.id)

@bot.callback_query_handler(func=lambda call: call.data == 'delete_all')
def delete_all_callback(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "ليس لديك صلاحية لهذا الإجراء!")
        return
        
    friends_list = Show_FrEinds()
    if not friends_list:
        bot.answer_callback_query(call.id, "لا يوجد أصدقاء لحذفهم!")
        return
        
    bot.answer_callback_query(call.id, "جاري حذف جميع الأصدقاء...")
    for fid, fname in friends_list:
        DeLetE_FrEind(fid)
        
    response_data = {"deleted_count": len(friends_list)}
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ <b>تم حذف {len(friends_list)} صديق بنجاح!</b>",
        reply_markup=None
    )
    # يمكن إضافة رد JSON هنا إذا رغبت
    update_user_activity(call.from_user.id)

# ============ بدء التشغيل ============
if __name__ == "__main__":
    # إنشاء ملفات البيانات إذا لم تكن موجودة
    for filename in [USERS_FILE, UIDS_FILE, GROUPS_FILE, LOG_FILE, OWNERS_FILE]:
        if not os.path.exists(filename):
            if filename == OWNERS_FILE:
                save_owners(OWNERS)
            elif filename != LOG_FILE:
                save_data({}, filename)
            else:
                open(filename, 'w').close()
    
    # إضافة المالكين الافتراضيين إذا لم يكونوا مسجلين
    users = load_data(USERS_FILE)
    for owner_id in OWNERS:
        if str(owner_id) not in users:
            try:
                user_info = bot.get_chat(owner_id)
                username = user_info.username or user_info.first_name
                add_user(owner_id, username, 999)
                log_action("OWNER_ADDED", owner_id)
            except Exception as e:
                log_action("INIT_OWNER_ADD_ERROR", owner_id, str(e))
    
    # الحصول على التوكن الأولي
    AUTH_TOKEN = get_jwt_token(JWT_UID, JWT_PW)
    if not AUTH_TOKEN:
        print(json_response(False, "فشل في الحصول على التوكن، الخروج من البرنامج"))
        exit(1)
    
    # بدء الخيط للحذف التلقائي
    threading.Thread(target=auto_remove_expired, daemon=True).start()
    
    # رسالة بدء التشغيل
    startup_data = {
        "status": "running",
        "start_time": datetime.now().isoformat(),
        "owners_count": len(OWNERS),
        "bot_username": bot.get_me().username,
        "bot_id": bot.get_me().id
    }
    print(json_response(True, "تم بدء تشغيل البوت بنجاح", startup_data))
    
    bot.polling()
