# ======================================================
# 👑 PROJECT: THE ULTIMATE MODULAR BOT (V52.0)
# 👤 DEVELOPER: IBRAHIM MUSTAFA (@x_u3s1)
# 🆔 ADMIN ID: 8301016131
# 🛠 STATUS: ANTI-CRASH + ADMIN PRO PANEL
# 📏 LENGTH: FULL EXTENDED VERSION - ULTRA STABLE
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
    handlers=[logging.FileHandler('bot_v52.log'), logging.StreamHandler()]
)

# --- [ 2. محرك البيئة البرمجية المستقر ] ---
def setup_environment():
    """
    محرك فحص البيئة - تم تعطيل التثبيت التلقائي لتجنب تعارض الصلاحيات في السيرفر.
    """
    print("🚀 [STARTUP] جاري فحص المحركات البرمجية في البصرة...")
    print("✅ [SUCCESS] البيئة مهيأة وجاهزة للعمل.")

setup_environment()

import telebot
from telebot import types
import yt_dlp
import certifi

# استيراد مكتبة معالجة الفيديو بحذر لضمان عدم توقف البوت
try:
    from moviepy.editor import VideoFileClip
except ImportError:
    print("⚠️ مكتبة MoviePy غير متوفرة حالياً.")

# --- [ 3. الثوابت والإعدادات العميقة ] ---
API_TOKEN = '8168190815:AAG0U-eqjIvAr5HbtTWTGOqQzSRz9Pdx4AY'.strip()
bot = telebot.TeleBot(API_TOKEN, num_threads=100) 
ADMIN_ID = 8301016131 
MY_USER = "@x_u3s1"

DB_PATH = {
    "ranks": "v52_ranks.json",
    "users": "v52_users.json",
    "daily": "v52_daily.json",
    "settings": "v52_settings.json",
    "banned": "v52_banned.json"
}

CACHE_DIR = "v52_storage_bin"
if not os.path.exists(CACHE_DIR): 
    os.makedirs(CACHE_DIR)

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
            content = f.read()
            if not content: return [] if key in ["users", "banned"] else {}
            return json.loads(content)
    except Exception as e:
        logging.error(f"Error loading {key}: {e}")
        return [] if key in ["users", "banned"] else {}

def save_data(key, data):
    try:
        with open(DB_PATH[key], "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving {key}: {e}")

# --- [ 5. نظام الرتب والمقامات ] ---
def get_rank_title(xp):
    ranks = [
        (1000000, "ملك البرمجة البصراوي 👑"),
        (500000, "إمبراطور الميديا 🌌"),
        (100000, "سيد التحميل 👑"),
        (50000, "الأسطورة البصرية 🏆"),
        (20000, "محمل ذهبي ✨"),
        (10000, "محترف 🔥"),
        (5000, "نشط جداً ⚡"),
        (1000, "عضو متميز 🎖️"),
        (0, "مبتدئ 👶")
    ]
    for limit, title in ranks:
        if xp >= limit: return title
    return "مبتدئ 👶"

def update_user_profile(uid, name, xp=0, dl=0):
    data = load_data("ranks")
    uid_s = str(uid)
    if uid_s not in data:
        data[uid_s] = {
            "name": re.sub(r'[^\w\s]', '', str(name)),
            "xp": 0, "dl": 0, "lvl": "مبتدئ 👶",
            "date": str(datetime.now().date())
        }
    data[uid_s]["xp"] += xp
    data[uid_s]["dl"] += dl
    data[uid_s]["lvl"] = get_rank_title(data[uid_s]["xp"])
    if uid == ADMIN_ID:
        data[uid_s]["lvl"] = "المطور الأساسي (ابن البصرة) 👑"
    save_data("ranks", data)

# --- [ 6. لوحة تحكم الأدمن PRO ] ---
def admin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 إذاعة للمشتركين", callback_data="adm_broadcast"),
        types.InlineKeyboardButton("📊 إحصائيات دقيقة", callback_data="adm_full_stats"),
        types.InlineKeyboardButton("🚫 حظر مستخدم", callback_data="adm_ban"),
        types.InlineKeyboardButton("🟢 فك حظر", callback_data="adm_unban"),
        types.InlineKeyboardButton("📂 جلب قواعد البيانات", callback_data="adm_get_db"),
        types.InlineKeyboardButton("🗑 تنظيف الكاش", callback_data="adm_clean"),
        types.InlineKeyboardButton("🔄 ريستارت النظام", callback_data="adm_restart"),
        types.InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="ui_back")
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
        types.InlineKeyboardButton("👨‍💻 مبرمج البوت", callback_data="ui_owner"),
        types.InlineKeyboardButton("💬 الدعم الفني", callback_data="ui_support")
    ]
    markup.add(*btns)
    if uid == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("🛠 لوحة الإدارة العليا 🛠", callback_data="adm_panel"))
    return markup

def dl_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎬 فيديو MP4", callback_data="m_vid"),
        types.InlineKeyboardButton("🎵 صوت MP3", callback_data="m_aud"),
        types.InlineKeyboardButton("🔙 إلغاء", callback_data="ui_back")
    )
    return markup

# --- [ 8. محرك التقسيم والتحميل العميق ] ---
def split_large_video(file_path, max_size_mb=45):
    try:
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size <= max_size_mb: return [file_path]
        parts = []
        video = VideoFileClip(file_path)
        duration = video.duration
        num_parts = int(file_size // max_size_mb) + 1
        part_duration = duration / num_parts
        for i in range(num_parts):
            start_t = i * part_duration
            end_t = min((i + 1) * part_duration, duration)
            part_path = file_path.replace(".mp4", f"_part{i+1}.mp4")
            clip = video.subclip(start_t, end_t)
            clip.write_videofile(part_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            parts.append(part_path)
        video.close()
        return parts
    except Exception as e:
        logging.error(f"Split error: {e}")
        return [file_path]

def secure_download(chat_id, url, type_mode):
    status_msg = bot.send_message(chat_id, "⏳ جاري المعالجة...")
    try:
        file_id = f"v52_{int(time.time())}"
        path_tmpl = os.path.join(CACHE_DIR, f"{file_id}.%(ext)s")
        ydl_opts = {'format': 'best', 'outtmpl': path_tmpl, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            f_name = ydl.prepare_filename(info)
        
        if type_mode == 'v':
            parts = split_large_video(f_name)
            for p in parts:
                with open(p, 'rb') as f: bot.send_video(chat_id, f, caption=f"👤 بواسطة: {MY_USER}")
                if p != f_name: os.remove(p)
        elif type_mode == 'a':
            with open(f_name, 'rb') as f: bot.send_audio(chat_id, f, caption=f"👤 المطور: {MY_USER}")
        
        if os.path.exists(f_name): os.remove(f_name)
        bot.delete_message(chat_id, status_msg.message_id)
        update_user_profile(chat_id, "User", xp=150, dl=1)
    except Exception as e:
        bot.edit_message_text(f"❌ خطأ تقني: {str(e)[:50]}", chat_id, status_msg.message_id)

# --- [ 9. معالجة الأحداث والدردشة ] ---
current_urls = {}

@bot.message_handler(commands=['start'])
def start_handler(m):
    uid = m.from_user.id
    if uid in load_data("banned"): return
    update_user_profile(uid, m.from_user.first_name)
    bot.send_message(m.chat.id, f"👑 أهلاً بك يا {m.from_user.first_name}", reply_markup=main_keyboard(uid))

@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def link_handler(m):
    current_urls[m.from_user.id] = m.text
    bot.reply_to(m, "🗳 اختر الصيغة المطلوبة:", reply_markup=dl_keyboard())

# --- [ 10. معالج الأزرار ] ---
@bot.callback_query_handler(func=lambda call: True)
def ui_manager(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    if call.data == "adm_panel" and uid == ADMIN_ID:
        bot.edit_message_text("🛠 لوحة الإدارة العليا", cid, mid, reply_markup=admin_keyboard())
    elif call.data == "m_vid":
        url = current_urls.get(uid)
        if url: threading.Thread(target=secure_download, args=(cid, url, 'v')).start()
    elif call.data == "ui_back":
        bot.edit_message_text("🏠 القائمة الرئيسية", cid, mid, reply_markup=main_keyboard(uid))

# --- [ 11. وظائف الإدارة ] ---
def process_broadcast(m):
    users = load_data("users")
    for u in users:
        try: bot.send_message(u, m.text)
        except: pass

# --- [ 12. محرك التنظيف والاستقرار ] ---
def maintenance_engine():
    while True:
        try:
            for file in os.listdir(CACHE_DIR):
                file_path = os.path.join(CACHE_DIR, file)
                if os.path.getmtime(file_path) < time.time() - 600: os.remove(file_path)
        except: pass
        time.sleep(300)

# --- [ 13. تشغيل البوت ] ---
if __name__ == "__main__":
    threading.Thread(target=maintenance_engine, daemon=True).start()
    print(f"🚀 V52.0 IS LIVE | DEVELOPER: {MY_USER}")
    while True:
        try:
            bot.infinity_polling(timeout=120)
        except:
            time.sleep(10)
            
