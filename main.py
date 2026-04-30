# ======================================================
# 👑 PROJECT: THE ULTIMATE MODULAR BOT (V52.0)
# 👤 DEVELOPER: IBRAHIM MUSTAFA (@x_u3s1)
# 🆔 ADMIN ID: 8301016131
# 🛠 STATUS: ANTI-CRASH + ADMIN PRO PANEL (BROADCAST ONLY)
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
bot = telebot.TeleBot(API_TOKEN, num_threads=50) 
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
if not os.path.exists(CACHE_DIR): os.makedirs(CACHE_DIR)

# --- [ 4. محرك إدارة البيانات ] ---
def load_data(key):
    path = DB_PATH.get(key)
    try:
        if not os.path.exists(path) or os.stat(path).st_size == 0:
            initial = [] if key in ["users", "banned"] else {}
            with open(path, "w", encoding='utf-8') as f:
                json.dump(initial, f, indent=4)
            return initial
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception:
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

# --- [ 6. لوحة تحكم الأدمن (إذاعة فقط) ] ---
def admin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📢 إذاعة للمشتركين", callback_data="adm_broadcast"),
        types.InlineKeyboardButton("🔙 رجوع", callback_data="ui_back")
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
        markup.add(types.InlineKeyboardButton("🛠 لوحة الإذاعة 🛠", callback_data="adm_panel"))
    return markup

def dl_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🎬 فيديو MP4", callback_data="m_vid"), types.InlineKeyboardButton("🎵 صوت MP3", callback_data="m_aud"), types.InlineKeyboardButton("🔙 رجوع", callback_data="ui_back"))
    return markup

# --- [ 8. محرك التقسيم والتحميل ] ---
def split_large_video(file_path, max_size_mb=48):
    if not file_path.endswith(".mp4"): return [file_path]
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
    except Exception: return [file_path]

def secure_download(chat_id, url, type_mode):
    msg = bot.send_message(chat_id, "⏳ جاري المعالجة والتحميل...")
    try:
        file_id = f"f_{int(time.time())}"
        path_tmpl = os.path.join(CACHE_DIR, f"{file_id}.%(ext)s")
        ydl_opts = {'format': 'best', 'outtmpl': path_tmpl, 'quiet': True, 'no_warnings': True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            f_name = ydl.prepare_filename(info)
        
        if type_mode == 'v':
            video_parts = split_large_video(f_name)
            for i, p in enumerate(video_parts):
                with open(p, 'rb') as f:
                    cap = f"✅ الجزء {i+1} من {len(video_parts)}" if len(video_parts) > 1 else "✅ تم التحميل بنجاح"
                    bot.send_video(chat_id, f, caption=cap)
                if p != f_name and os.path.exists(p): os.remove(p)
        else:
            with open(f_name, 'rb') as f: 
                bot.send_audio(chat_id, f, caption="🎵 تم استخراج الصوت بنجاح")
            
        if os.path.exists(f_name): os.remove(f_name)
        bot.delete_message(chat_id, msg.message_id)
        update_user_profile(chat_id, "User", xp=100, dl=1)
    except Exception as e:
        bot.edit_message_text(f"❌ خطأ في الرابط أو الحجم: {str(e)[:50]}", chat_id, msg.message_id)

# --- [ 9. معالجة الأحداث والدردشة ] ---
current_urls = {}

@bot.message_handler(commands=['start'])
def start_handler(m):
    banned_list = load_data("banned")
    if m.from_user.id in banned_list:
        return bot.reply_to(m, "🚫 عذراً، لقد تم حظرك من قبل الإدارة.")
    
    users = load_data("users")
    if m.from_user.id not in users:
        users.append(m.from_user.id)
        save_data("users", users)
    
    update_user_profile(m.from_user.id, m.from_user.first_name)
    bot.send_message(m.chat.id, f"👑 أهلاً بك يا {m.from_user.first_name}\nأرسل أي رابط وسأقوم بمعالجته لك.", reply_markup=main_keyboard(m.from_user.id))

@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def link_handler(m):
    if m.from_user.id in load_data("banned"): return
    current_urls[m.from_user.id] = m.text
    bot.reply_to(m, "🗳 الرابط جاهز، اختر ما تريد:", reply_markup=dl_keyboard())

# --- [ 10. معالج أزرار الإدارة والمستخدم ] ---
@bot.callback_query_handler(func=lambda call: True)
def ui_manager(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    
    if "adm_" in call.data and uid != ADMIN_ID:
        return bot.answer_callback_query(call.id, "🚫 هذا القسم للمطور إبراهيم فقط!")

    if call.data == "adm_panel":
        bot.edit_message_text("🛠 لوحة الإذاعة - إبراهيم مصطفى 🛠", cid, mid, reply_markup=admin_keyboard())

    elif call.data == "adm_broadcast":
        msg = bot.send_message(cid, "📝 أرسل رسالة الإذاعة الآن:")
        bot.register_next_step_handler(msg, process_broadcast)

    elif call.data == "ui_back":
        bot.edit_message_text("🏠 القائمة الرئيسية", cid, mid, reply_markup=main_keyboard(uid))
        
    elif call.data == "m_vid":
        url = current_urls.get(uid)
        if url: 
            bot.delete_message(cid, mid)
            threading.Thread(target=secure_download, args=(cid, url, 'v')).start()
            
    elif call.data == "ui_me":
        u = load_data("ranks").get(str(uid), {"name":"User", "xp":0, "dl":0, "lvl":"مبتدئ"})
        bot.edit_message_text(f"👤 ملفك الشخصي:\n🎖 الرتبة: {u['lvl']}\n⭐ نقاطك: {u['xp']}\n📍 البصرة 🌴", cid, mid, reply_markup=main_keyboard(uid))

    elif call.data == "ui_top":
        ranks = load_data("ranks")
        top = sorted(ranks.items(), key=lambda x: x[1]['xp'], reverse=True)[:10]
        txt = "🏆 قائمة المتصدرين:\n\n" + "\n".join([f"{i+1} | {v['name']} -> {v['xp']}" for i, (k,v) in enumerate(top)])
        bot.edit_message_text(txt, cid, mid, reply_markup=main_keyboard(uid))

    elif call.data == "ui_gift":
        daily = load_data("daily")
        today = datetime.now().strftime("%Y-%m-%d")
        if daily.get(str(uid)) == today: 
            bot.answer_callback_query(call.id, "❌ استلمت جائزتك اليوم بالفعل!", show_alert=True)
        else:
            daily[str(uid)] = today
            save_data("daily", daily)
            update_user_profile(uid, call.from_user.first_name, xp=1000)
            bot.answer_callback_query(call.id, "🎁 حصلت على 1000 نقطة هدية!", show_alert=True)

# --- [ 11. وظيفة الإذاعة ] ---
def process_broadcast(m):
    users = load_data("users")
    count = 0
    bot.send_message(m.chat.id, f"⏳ جاري الإرسال إلى {len(users)} مستخدم...")
    for u in users:
        try:
            bot.send_message(u, f"📢 رسالة من الإدارة:\n\n{m.text}")
            count += 1
            time.sleep(0.1) # حماية من السبام
        except: pass
    bot.send_message(m.chat.id, f"✅ تم الإرسال إلى {count} مستخدم بنجاح.")

# --- [ 12. نظام التشغيل والاستمرارية ] ---
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
    threading.Thread(target=cleaner_engine, daemon=True).start()
    print("✅ البوت يعمل الآن (لوحة الإذاعة فقط)..")
    while True:
        try:
            bot.infinity_polling(timeout=120, long_polling_timeout=70)
        except Exception:
            time.sleep(5)
    
