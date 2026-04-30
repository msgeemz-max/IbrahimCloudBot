# ======================================================
# 👑 PROJECT: THE ULTIMATE MODULAR BOT (V48.0)
# 👤 DEVELOPER: IBRAHIM MUSTAFA (@x_u3s1)
# 🆔 ADMIN ID: 8301016131
# 🛠 STATUS: AUTO-SPLIT ENGINE ENABLED (100MB+ READY)
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
    handlers=[logging.FileHandler('bot_v48.log'), logging.StreamHandler()]
)

# --- [ 2. محرك البيئة البرمجية المستقر ] ---
def setup_environment():
    """تجهيز المكتبات الأساسية لضمان عدم توقف البوت في Railway"""
    print("🚀 [STARTUP] جاري فحص المحركات البرمجية في البصرة...")
    # تم إضافة moviepy كشرط أساسي لعملية التقسيم
    required_libs = ["yt-dlp", "pyTelegramBotAPI", "requests", "certifi", "moviepy"]
    for lib in required_libs:
        try:
            __import__(lib.replace('-', '_'))
        except ImportError:
            print(f"📦 تثبيت المكتبة المفقودة: {lib}")
            subprocess.call([sys.executable, "-m", "pip", "install", lib, "--quiet"])
    print("✅ [SUCCESS] جميع المحركات جاهزة للعمل بكفاءة عالية.")

setup_environment()

import telebot
from telebot import types
import yt_dlp
import certifi
from moviepy.editor import VideoFileClip # استيراد أداة القص

# --- [ 3. الثوابت والإعدادات العميقة ] ---
API_TOKEN = '8168190815:AAG0U-eqjIvAr5HbtTWTGOqQzSRz9Pdx4AY'.strip()
bot = telebot.TeleBot(API_TOKEN, num_threads=30) 
ADMIN_ID = 8301016131 
MY_USER = "@x_u3s1"

DB_PATH = {
    "ranks": "v48_ranks.json",
    "users": "v48_users.json",
    "daily": "v48_daily.json",
    "settings": "v48_settings.json"
}
CACHE_DIR = "v48_storage_bin"

if not os.path.exists(CACHE_DIR): 
    os.makedirs(CACHE_DIR)

# --- [ 4. محرك إدارة البيانات القوي ] ---
def load_data(key):
    path = DB_PATH.get(key)
    try:
        if not os.path.exists(path):
            initial = [] if key == "users" else {}
            with open(path, "w", encoding='utf-8') as f:
                json.dump(initial, f, indent=4)
            return initial
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading {key}: {e}")
        return [] if key == "users" else {}

def save_data(key, data):
    try:
        with open(DB_PATH[key], "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving {key}: {e}")

# --- [ 5. نظام الرتب المتقدم ] ---
def get_rank_title(xp):
    ranks = [
        (100000, "إمبراطور الميديا 🌌"),
        (50000, "سيد التحميل 👑"),
        (20000, "الأسطورة البصرية 🏆"),
        (10000, "محمل ذهبي ✨"),
        (5000, "محترف 🔥"),
        (1000, "نشط جداً ⚡"),
        (0, "مبتدئ 👶")
    ]
    for limit, title in ranks:
        if xp >= limit: return title

def update_user_profile(uid, name, xp=0, dl=0):
    data = load_data("ranks")
    uid_s = str(uid)
    name = re.sub(r'[^\w\s]', '', str(name))
    if uid_s not in data:
        data[uid_s] = {
            "name": name, "xp": 0, "dl": 0, 
            "lvl": "مبتدئ 👶", "date": str(datetime.now().date())
        }
    data[uid_s]["xp"] += xp
    data[uid_s]["dl"] += dl
    data[uid_s]["lvl"] = get_rank_title(data[uid_s]["xp"])
    if uid == ADMIN_ID: data[uid_s]["lvl"] = "المطور الأساسي (ابن البصرة) 👑"
    save_data("ranks", data)

# --- [ 6. واجهات المستخدم الاحترافية ] ---
def main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📥 بدء التحميل", callback_data="ui_download"),
        types.InlineKeyboardButton("👤 الملف الشخصي", callback_data="ui_me"),
        types.InlineKeyboardButton("🏆 المتصدرين", callback_data="ui_top"),
        types.InlineKeyboardButton("🎁 هدية البصرة", callback_data="ui_gift"),
        types.InlineKeyboardButton("⚙️ الإحصائيات", callback_data="ui_stats"),
        types.InlineKeyboardButton("👨‍💻 مبرمج البوت", callback_data="ui_owner")
    )
    return markup

def dl_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎬 فيديو MP4", callback_data="m_vid"),
        types.InlineKeyboardButton("🎵 صوت MP3", callback_data="m_aud"),
        types.InlineKeyboardButton("🔙 رجوع", callback_data="ui_back")
    )
    return markup

# --- [ 7. محرك التقسيم الذكي (Smart Splitter) ] ---
def split_large_video(file_path, max_size_mb=48):
    """وظيفة لتقسيم الفيديو إذا تجاوز حجمه المسموح في تليجرام"""
    file_size = os.path.getsize(file_path) / (1024 * 1024)
    if file_size <= max_size_mb:
        return [file_path]

    print(f"✂️ الملف حجمه {int(file_size)}MB.. جاري التقسيم...")
    parts = []
    try:
        video = VideoFileClip(file_path)
        duration = video.duration
        # حساب عدد الأجزاء المطلوبة
        num_parts = int(file_size // max_size_mb) + 1
        part_duration = duration / num_parts

        for i in range(num_parts):
            start_t = i * part_duration
            end_t = min((i + 1) * part_duration, duration)
            part_name = file_path.replace(".mp4", f"_part{i+1}.mp4")
            
            # قص وحفظ الجزء بصيغة متوافقة
            new_part = video.subclip(start_t, end_t)
            new_part.write_videofile(part_name, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True, verbose=False, logger=None)
            parts.append(part_name)
        
        video.close()
        return parts
    except Exception as e:
        logging.error(f"Split Error: {e}")
        return [file_path] # العودة للملف الأصلي في حال فشل القص

# --- [ 8. محرك التحميل المحدث (Anti-Limit Engine) ] ---
def secure_download(chat_id, url, type_mode):
    msg = bot.send_message(chat_id, "⏳ جاري فحص الرابط ومعالجة الجودة (تخطي قيود الـ 50MB)...")
    
    # محاولة التحميل السريع (للملفات الصغيرة فقط)
    try:
        if type_mode == 'v': # فقط في حالة الفيديو نحاول التحميل السريع أولاً
            api_res = requests.get(f"https://www.tikwm.com/api/?url={url}", timeout=10).json()
            if api_res.get('code') == 0:
                link = api_res['data'].get('play')
                # نفحص حجم الرابط المباشر قبل الإرسال إذا أمكن
                head = requests.head(link)
                size = int(head.headers.get('content-length', 0)) / (1024*1024)
                if size < 49:
                    bot.send_video(chat_id, link, caption="✅ تم التحميل السريع (V48.0)")
                    bot.delete_message(chat_id, msg.message_id)
                    update_user_profile(chat_id, "User", xp=40, dl=1)
                    return
    except: pass

    # محاولة YT-DLP مع محرك التقسيم (للملفات الكبيرة مثل 107MB)
    bot.edit_message_text("🔄 جاري تفعيل محرك التقسيم الآلي (تخطي حدود الـ 50MB)...", chat_id, msg.message_id)
    try:
        file_id = f"file_{int(time.time())}_{random.randint(100,999)}"
        path_tmpl = os.path.join(CACHE_DIR, f"{file_id}.%(ext)s")
        
        y_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': path_tmpl,
            'quiet': True,
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(y_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            f_name = ydl.prepare_filename(info)
            if not os.path.exists(f_name):
                f_name = f_name.rsplit('.', 1)[0] + ".mp4"

        f_size = os.path.getsize(f_name) / (1024 * 1024)
        
        if type_mode == 'v':
            # تشغيل محرك التقسيم إذا لزم الأمر
            video_parts = split_large_video(f_name)
            
            for index, part in enumerate(video_parts):
                with open(part, 'rb') as f:
                    cap = f"✅ فيديو كامل (4K)\n📍 الجزء {index+1}/{len(video_parts)}" if len(video_parts) > 1 else "✅ تم التحميل بواسطة إبراهيم مصطفى"
                    bot.send_video(chat_id, f, caption=cap)
                # حذف الجزء بعد الإرسال إذا كان مقصوصاً
                if part != f_name: os.remove(part)
        else:
            # للصوت فقط
            with open(f_name, 'rb') as f:
                bot.send_audio(chat_id, f, caption="✅ تم استخراج الصوت بنجاح")

        if os.path.exists(f_name): os.remove(f_name)
        bot.delete_message(chat_id, msg.message_id)
        update_user_profile(chat_id, "User", xp=100, dl=1)
        
    except Exception as e:
        bot.edit_message_text(f"❌ فشل التحميل: تأكد من الرابط أو حاول لاحقاً.", chat_id, msg.message_id)
        logging.error(f"Download error: {e}")

# --- [ 9. معالج الأوامر والدردشة ] ---
current_urls = {}

@bot.message_handler(commands=['start'])
def start_handler(m):
    u = m.from_user
    users = load_data("users")
    if u.id not in users:
        users.append(u.id)
        save_data("users", users)
    update_user_profile(u.id, u.first_name)
    welcome = (f"👑 أهلاً يا {u.first_name}!\nتم تفعيل محرك التقسيم لرفع الملفات الكبيرة (100MB+).\nأرسل أي رابط الآن.")
    bot.send_message(m.chat.id, welcome, reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def link_handler(m):
    current_urls[m.from_user.id] = m.text
    bot.reply_to(m, "🗳 تم استلام الرابط، اختر الصيغة:", reply_markup=dl_keyboard())

# --- [ 10. معالج الأزرار التفاعلية ] ---
@bot.callback_query_handler(func=lambda call: True)
def ui_manager(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id

    if call.data == "ui_back":
        bot.edit_message_text("🏠 القائمة الرئيسية", cid, mid, reply_markup=main_keyboard())
    elif call.data == "m_vid":
        url = current_urls.get(uid)
        if url:
            bot.delete_message(cid, mid)
            threading.Thread(target=secure_download, args=(cid, url, 'v')).start()
    elif call.data == "m_aud":
        url = current_urls.get(uid)
        if url:
            bot.delete_message(cid, mid)
            threading.Thread(target=secure_download, args=(cid, url, 'a')).start()
    elif call.data == "ui_me":
        u_data = load_data("ranks").get(str(uid), {"name":"User", "xp":0, "dl":0, "lvl":"مبتدئ"})
        text = f"👤 بطاقة المستخدم:\n━━━━\n🎖 الرتبة: {u_data['lvl']}\n⭐ نقاطك: {u_data['xp']}\n📥 تحميلاتك: {u_data['dl']}\n━━━━"
        bot.edit_message_text(text, cid, mid, reply_markup=main_keyboard())
    elif call.data == "ui_top":
        all_users = load_data("ranks")
        sorted_top = sorted(all_users.items(), key=lambda x: x[1]['xp'], reverse=True)[:10]
        text = "🏆 المتصدرين:\n"
        for i, (k, v) in enumerate(sorted_top, 1):
            text += f"{i} | {v['name']} ➔ {v['xp']} XP\n"
        bot.edit_message_text(text, cid, mid, reply_markup=main_keyboard())
    elif call.data == "ui_gift":
        daily = load_data("daily")
        today = datetime.now().strftime("%Y-%m-%d")
        if daily.get(str(uid)) == today:
            bot.answer_callback_query(call.id, "❌ عد غداً!", show_alert=True)
        else:
            daily[str(uid)] = today
            save_data("daily", daily)
            update_user_profile(uid, call.from_user.first_name, xp=300)
            bot.answer_callback_query(call.id, "🎁 حصلت على 300 نقطة!", show_alert=True)
    elif call.data == "ui_stats":
        total = len(load_data("users"))
        bot.edit_message_text(f"📊 الإحصائيات:\n👥 مستخدمين: {total}\n🛰 الحالة: تقسيم فعال ✅", cid, mid, reply_markup=main_keyboard())
    elif call.data == "ui_owner":
        bot.edit_message_text(f"👨‍💻 المطور: إبراهيم مصطفى\n📍 البصرة 🌴", cid, mid, reply_markup=main_keyboard())
    elif call.data == "ui_download":
        bot.edit_message_text("📥 أرسل الرابط الآن للمباشرة:", cid, mid)

# --- [ 11. نظام التنظيف ] ---
def cleaner_engine():
    while True:
        try:
            if os.path.exists(CACHE_DIR):
                for file in os.listdir(CACHE_DIR):
                    f_p = os.path.join(CACHE_DIR, file)
                    if os.path.getmtime(f_p) < time.time() - 600:
                        os.remove(f_p)
        except: pass
        time.sleep(600)

if __name__ == "__main__":
    print(f"✅ [V48.0] IS LIVE. MEGA TOOLS ENABLED. OWNER: IBRAHIM MUSTAFA")
    threading.Thread(target=cleaner_engine, daemon=True).start()
    while True:
        try:
            bot.infinity_polling(timeout=120, long_polling_timeout=70)
        except Exception as e:
            time.sleep(10)
    
