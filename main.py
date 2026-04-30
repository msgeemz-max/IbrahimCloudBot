# ======================================================
# 👑 PROJECT: THE ULTIMATE MODULAR BOT (V50.0)
# 👤 DEVELOPER: IBRAHIM MUSTAFA (@x_u3s1)
# 🆔 ADMIN ID: 8301016131
# 🛠 STATUS: ADMIN PANEL + AUTO-SPLIT ENABLED
# 📏 LENGTH: FULL EXTENDED VERSION - NO DELETIONS
# 📍 LOCATION: BASRA, IRAQ 🇮🇶
# ======================================================

import os
import threading
import time
import json
import re
import random
import subprocess
import sys
import requests
import shutil
import logging
from datetime import datetime, timedelta

# --- [ 1. إعدادات السجلات والحماية ] ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot_v50.log'), logging.StreamHandler()]
)

# --- [ 2. محرك البيئة البرمجية المستقر ] ---
def setup_environment():
    print("🚀 [STARTUP] جاري فحص المحركات البرمجية في البصرة...")
    required_libs = ["yt-dlp", "pyTelegramBotAPI", "requests", "certifi", "moviepy"]
    for lib in required_libs:
        try:
            __import__(lib.replace('-', '_'))
        except ImportError:
            subprocess.call([sys.executable, "-m", "pip", "install", lib, "--quiet"])
    print("✅ [SUCCESS] جميع المحركات جاهزة.")

setup_environment()

import telebot
from telebot import types
import yt_dlp
import certifi
from moviepy.editor import VideoFileClip

# --- [ 3. الثوابت والإعدادات العميقة ] ---
API_TOKEN = '8168190815:AAG0U-eqjIvAr5HbtTWTGOqQzSRz9Pdx4AY'.strip()
bot = telebot.TeleBot(API_TOKEN, num_threads=30) 
ADMIN_ID = 8301016131 
MY_USER = "@x_u3s1"

DB_PATH = {
    "ranks": "v50_ranks.json",
    "users": "v50_users.json",
    "daily": "v50_daily.json",
    "settings": "v50_settings.json",
    "banned": "v50_banned.json"
}
CACHE_DIR = "v50_storage_bin"
if not os.path.exists(CACHE_DIR): os.makedirs(CACHE_DIR)

# --- [ 4. محرك إدارة البيانات ] ---
def load_data(key):
    path = DB_PATH.get(key)
    try:
        if not os.path.exists(path):
            initial = [] if key in ["users", "banned"] else {}
            with open(path, "w", encoding='utf-8') as f:
                json.dump(initial, f, indent=4)
            return initial
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return [] if key in ["users", "banned"] else {}

def save_data(key, data):
    try:
        with open(DB_PATH[key], "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving {key}: {e}")

# --- [ 5. نظام الرتب والمقامات ] ---
def get_rank_title(xp):
    ranks = [(100000, "إمبراطور الميديا 🌌"), (50000, "سيد التحميل 👑"), (20000, "الأسطورة البصرية 🏆"), (10000, "محمل ذهبي ✨"), (5000, "محترف 🔥"), (1000, "نشط جداً ⚡"), (0, "مبتدئ 👶")]
    for limit, title in ranks:
        if xp >= limit: return title

def update_user_profile(uid, name, xp=0, dl=0):
    data = load_data("ranks")
    uid_s = str(uid)
    if uid_s not in data:
        data[uid_s] = {"name": re.sub(r'[^\w\s]', '', str(name)), "xp": 0, "dl": 0, "lvl": "مبتدئ 👶", "date": str(datetime.now().date())}
    data[uid_s]["xp"] += xp
    data[uid_s]["dl"] += dl
    data[uid_s]["lvl"] = get_rank_title(data[uid_s]["xp"])
    if uid == ADMIN_ID: data[uid_s]["lvl"] = "المطور الأساسي (ابن البصرة) 👑"
    save_data("ranks", data)

# --- [ 6. لوحة تحكم الأدمن (الجديدة كلياً) ] ---
def admin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 إذاعة", callback_data="adm_broadcast"),
        types.InlineKeyboardButton("📊 الإحصائيات", callback_data="adm_full_stats"),
        types.InlineKeyboardButton("🚫 حظر مستخدم", callback_data="adm_ban"),
        types.InlineKeyboardButton("🟢 فك حظر", callback_data="adm_unban"),
        types.InlineKeyboardButton("📥 سحب قاعدة البيانات", callback_data="adm_get_db"),
        types.InlineKeyboardButton("🔄 ريستارت البوت", callback_data="adm_restart"),
        types.InlineKeyboardButton("🔴 إيقاف البوت", callback_data="adm_stop"),
        types.InlineKeyboardButton("🏠 قائمة المستخدمين", callback_data="ui_back")
    )
    return markup

# --- [ 7. واجهات المستخدم ] ---
def main_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("📥 بدء التحميل", callback_data="ui_download"),
        types.InlineKeyboardButton("👤 الملف الشخصي", callback_data="ui_me"),
        types.InlineKeyboardButton("🏆 المتصدرين", callback_data="ui_top"),
        types.InlineKeyboardButton("🎁 هدية البصرة", callback_data="ui_gift"),
        types.InlineKeyboardButton("⚙️ الإحصائيات", callback_data="ui_stats"),
        types.InlineKeyboardButton("👨‍💻 مبرمج البوت", callback_data="ui_owner")
    ]
    markup.add(*btns)
    if uid == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("🛠 لوحة الإدارة (إبراهيم)", callback_data="adm_panel"))
    return markup

def dl_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🎬 فيديو MP4", callback_data="m_vid"), types.InlineKeyboardButton("🎵 صوت MP3", callback_data="m_aud"), types.InlineKeyboardButton("🔙 رجوع", callback_data="ui_back"))
    return markup

# --- [ 8. محرك التقسيم والتحميل ] ---
def split_large_video(file_path, max_size_mb=48):
    file_size = os.path.getsize(file_path) / (1024 * 1024)
    if file_size <= max_size_mb: return [file_path]
    parts = []
    try:
        video = VideoFileClip(file_path)
        num_parts = int(file_size // max_size_mb) + 1
        part_dur = video.duration / num_parts
        for i in range(num_parts):
            p_path = file_path.replace(".mp4", f"_part{i+1}.mp4")
            video.subclip(i*part_dur, min((i+1)*part_dur, video.duration)).write_videofile(p_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            parts.append(p_path)
        video.close()
        return parts
    except: return [file_path]

def secure_download(chat_id, url, type_mode):
    msg = bot.send_message(chat_id, "⏳ جاري التحميل ومعالجة الحجم...")
    try:
        file_id = f"f_{int(time.time())}"
        path_tmpl = os.path.join(CACHE_DIR, f"{file_id}.%(ext)s")
        with yt_dlp.YoutubeDL({'format': 'best', 'outtmpl': path_tmpl, 'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=True)
            f_name = ydl.prepare_filename(info)
        
        if type_mode == 'v':
            video_parts = split_large_video(f_name)
            for i, p in enumerate(video_parts):
                with open(p, 'rb') as f:
                    bot.send_video(chat_id, f, caption=f"✅ جزء {i+1}/{len(video_parts)}" if len(video_parts)>1 else "✅ تم التحميل")
                if p != f_name: os.remove(p)
        else:
            with open(f_name, 'rb') as f: bot.send_audio(chat_id, f)
            
        if os.path.exists(f_name): os.remove(f_name)
        bot.delete_message(chat_id, msg.message_id)
        update_user_profile(chat_id, "User", xp=100, dl=1)
    except Exception as e:
        bot.edit_message_text(f"❌ فشل: {str(e)[:50]}", chat_id, msg.message_id)

# --- [ 9. معالجة الأحداث والدردشة ] ---
current_urls = {}

@bot.message_handler(commands=['start'])
def start_handler(m):
    if m.from_user.id in load_data("banned"):
        return bot.reply_to(m, "🚫 أنت محظور من استخدام البوت.")
    users = load_data("users")
    if m.from_user.id not in users:
        users.append(m.from_user.id)
        save_data("users", users)
    update_user_profile(m.from_user.id, m.from_user.first_name)
    bot.send_message(m.chat.id, f"👑 أهلاً يا {m.from_user.first_name} في بوت إبراهيم مصطفى.\nأرسل أي رابط للتحميل.", reply_markup=main_keyboard(m.from_user.id))

@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def link_handler(m):
    if m.from_user.id in load_data("banned"): return
    current_urls[m.from_user.id] = m.text
    bot.reply_to(m, "🗳 تم استلام الرابط، اختر الصيغة:", reply_markup=dl_keyboard())

# --- [ 10. معالج أزرار التحكم والإدارة ] ---
@bot.callback_query_handler(func=lambda call: True)
def ui_manager(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    
    # قسم الأدمن فقط
    if "adm_" in call.data and uid != ADMIN_ID:
        return bot.answer_callback_query(call.id, "❌ هذا الأمر خاص بإبراهيم مصطفى فقط!")

    if call.data == "adm_panel":
        bot.edit_message_text("🛠 لوحة تحكم المطور إبراهيم مصطفى:", cid, mid, reply_markup=admin_keyboard())

    elif call.data == "adm_full_stats":
        total = len(load_data("users"))
        banned = len(load_data("banned"))
        bot.answer_callback_query(call.id, f"👥 مستخدمين: {total}\n🚫 محظورين: {banned}", show_alert=True)

    elif call.data == "adm_broadcast":
        msg = bot.send_message(cid, "📝 أرسل الرسالة التي تريد إذاعتها الآن (نص فقط):")
        bot.register_next_step_handler(msg, process_broadcast)

    elif call.data == "adm_get_db":
        bot.send_document(cid, open(DB_PATH["users"], 'rb'))
        bot.send_document(cid, open(DB_PATH["ranks"], 'rb'))

    elif call.data == "adm_restart":
        bot.edit_message_text("🔄 جاري إعادة التشغيل في سيرفر Railway...", cid, mid)
        os.execv(sys.executable, ['python'] + sys.argv)

    elif call.data == "adm_stop":
        bot.edit_message_text("🔴 تم إيقاف البوت نهائياً.", cid, mid)
        os._exit(0)

    elif call.data == "adm_ban":
        msg = bot.send_message(cid, "🆔 أرسل الـ ID الخاص بالمستخدم لحظره:")
        bot.register_next_step_handler(msg, process_ban)

    elif call.data == "adm_unban":
        msg = bot.send_message(cid, "🆔 أرسل الـ ID لفك الحظر:")
        bot.register_next_step_handler(msg, process_unban)

    # قسم المستخدمين
    elif call.data == "ui_back":
        bot.edit_message_text("🏠 القائمة الرئيسية", cid, mid, reply_markup=main_keyboard(uid))
    elif call.data == "m_vid":
        url = current_urls.get(uid)
        if url: 
            bot.delete_message(cid, mid)
            threading.Thread(target=secure_download, args=(cid, url, 'v')).start()
    elif call.data == "ui_me":
        u = load_data("ranks").get(str(uid), {"name":"User", "xp":0, "dl":0, "lvl":"مبتدئ"})
        bot.edit_message_text(f"👤 بطاقتك:\n🎖 الرتبة: {u['lvl']}\n⭐ نقاطك: {u['xp']}\n📍 الموقع: البصرة", cid, mid, reply_markup=main_keyboard(uid))
    elif call.data == "ui_top":
        top = sorted(load_data("ranks").items(), key=lambda x: x[1]['xp'], reverse=True)[:10]
        txt = "🏆 قائمة العمالقة:\n" + "\n".join([f"{i+1} | {v['name']} -> {v['xp']}" for i, (k,v) in enumerate(top)])
        bot.edit_message_text(txt, cid, mid, reply_markup=main_keyboard(uid))
    elif call.data == "ui_gift":
        daily = load_data("daily")
        today = datetime.now().strftime("%Y-%m-%d")
        if daily.get(str(uid)) == today: bot.answer_callback_query(call.id, "❌ استلمت جائزتك!")
        else:
            daily[str(uid)] = today
            save_data("daily", daily)
            update_user_profile(uid, call.from_user.first_name, xp=500)
            bot.answer_callback_query(call.id, "🎁 +500 نقطة من ابن البصرة!", show_alert=True)

# --- [ 11. وظائف الأدمن الإضافية ] ---
def process_broadcast(m):
    users = load_data("users")
    count = 0
    for u in users:
        try:
            bot.send_message(u, f"📢 رسالة من الإدارة:\n\n{m.text}")
            count += 1
        except: pass
    bot.send_message(m.chat.id, f"✅ تمت الإذاعة لـ {count} مستخدم.")

def process_ban(m):
    try:
        banned = load_data("banned")
        if int(m.text) not in banned:
            banned.append(int(m.text))
            save_data("banned", banned)
            bot.send_message(m.chat.id, f"✅ تم حظر {m.text}")
    except: bot.send_message(m.chat.id, "❌ خطأ في الـ ID")

def process_unban(m):
    try:
        banned = load_data("banned")
        if int(m.text) in banned:
            banned.remove(int(m.text))
            save_data("banned", banned)
            bot.send_message(m.chat.id, f"✅ تم فك حظر {m.text}")
    except: bot.send_message(m.chat.id, "❌ خطأ في الـ ID")

# --- [ 12. نظام التنظيف والاستدامة ] ---
def cleaner_engine():
    while True:
        try:
            if os.path.exists(CACHE_DIR):
                for f in os.listdir(CACHE_DIR):
                    if os.path.getmtime(os.path.join(CACHE_DIR, f)) < time.time() - 600:
                        os.remove(os.path.join(CACHE_DIR, f))
        except: pass
        time.sleep(600)

if __name__ == "__main__":
    print(f"✅ [V50.0] LIVE. ADMIN PANEL READY FOR IBRAHIM.")
    threading.Thread(target=cleaner_engine, daemon=True).start()
    while True:
        try: bot.infinity_polling(timeout=120)
        except: time.sleep(10)
            
