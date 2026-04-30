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
# نستخدم السجلات لمراقبة كل صغيرة وكبيرة في البوت لضمان عدم توقفه
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot_v52.log'), logging.StreamHandler()]
)

# --- [ 2. محرك البيئة البرمجية المستقر ] ---
def setup_environment():
    """
    هذه الدالة تقوم بفحص المكتبات قبل التشغيل لضمان استقرار البيئة البرمجية في السيرفر.
    """
    print("🚀 [STARTUP] جاري فحص المحركات البرمجية في البصرة...")
    required_libs = ["yt-dlp", "pyTelegramBotAPI", "requests", "certifi", "moviepy"]
    for lib in required_libs:
        try:
            __import__(lib.replace('-', '_'))
        except ImportError:
            print(f"📦 جاري تثبيت المكتبة المفقودة: {lib}")
            subprocess.call([sys.executable, "-m", "pip", "install", lib, "--quiet"])
    print("✅ [SUCCESS] جميع المحركات جاهزة للعمل.")

# تشغيل الفحص الأولي
setup_environment()

import telebot
from telebot import types
import yt_dlp
import certifi
from moviepy.editor import VideoFileClip

# --- [ 3. الثوابت والإعدادات العميقة ] ---
API_TOKEN = '8168190815:AAG0U-eqjIvAr5HbtTWTGOqQzSRz9Pdx4AY'.strip()
bot = telebot.TeleBot(API_TOKEN, num_threads=100) # رفع عدد الخيوط لأقصى سرعة
ADMIN_ID = 8301016131 
MY_USER = "@x_u3s1"

# مسارات قواعد البيانات
DB_PATH = {
    "ranks": "v52_ranks.json",
    "users": "v52_users.json",
    "daily": "v52_daily.json",
    "settings": "v52_settings.json",
    "banned": "v52_banned.json"
}

# إنشاء مجلد التخزين المؤقت إذا لم يكن موجوداً
CACHE_DIR = "v52_storage_bin"
if not os.path.exists(CACHE_DIR): 
    os.makedirs(CACHE_DIR)
    print(f"📁 تم إنشاء مجلد الكاش: {CACHE_DIR}")

# --- [ 4. محرك إدارة البيانات ] ---
def load_data(key):
    """تحميل البيانات من ملفات JSON مع معالجة الأخطاء"""
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
    """حفظ البيانات وضمان عدم ضياع التنسيق"""
    try:
        with open(DB_PATH[key], "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving {key}: {e}")

# --- [ 5. نظام الرتب والمقامات ] ---
def get_rank_title(xp):
    """تحديد رتبة المستخدم بناءً على نقاط الخبرة"""
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
    """تحديث بيانات المستخدم وزيادة نقاطه"""
    data = load_data("ranks")
    uid_s = str(uid)
    if uid_s not in data:
        data[uid_s] = {
            "name": re.sub(r'[^\w\s]', '', str(name)),
            "xp": 0,
            "dl": 0,
            "lvl": "مبتدئ 👶",
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
    """لوحة التحكم الكاملة للمطور إبراهيم"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 إذاعة للمشتركين", callback_data="adm_broadcast"),
        types.InlineKeyboardButton("📊 إحصائيات دقيقة", callback_data="adm_full_stats"),
        types.InlineKeyboardButton("🚫 حظر مستخدم", callback_data="adm_ban"),
        types.InlineKeyboardButton("🟢 فك حظر", callback_data="adm_unban"),
        types.InlineKeyboardButton("📂 جلب قواعد البيانات", callback_data="adm_get_db"),
        types.InlineKeyboardButton("🗑 تنظيف الكاش", callback_data="adm_clean"),
        types.InlineKeyboardButton("🔄 ريستارت النظام", callback_data="adm_restart"),
        types.InlineKeyboardButton("📤 رفع ملف برمجي", callback_data="adm_upload"),
        types.InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="ui_back")
    )
    return markup

# --- [ 7. واجهات المستخدم ] ---
def main_keyboard(uid):
    """واجهة المستخدم الرئيسية المتعددة الخيارات"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("📥 بدء التحميل", callback_data="ui_download"),
        types.InlineKeyboardButton("👤 الملف الشخصي", callback_data="ui_me"),
        types.InlineKeyboardButton("🏆 المتصدرين", callback_data="ui_top"),
        types.InlineKeyboardButton("🎁 هدية البصرة", callback_data="ui_gift"),
        types.InlineKeyboardButton("⚙️ الإحصائيات", callback_data="ui_stats"),
        types.InlineKeyboardButton("👨‍💻 مبرمج البوت", callback_data="ui_owner"),
        types.InlineKeyboardButton("💬 الدعم الفني", callback_data="ui_support"),
        types.InlineKeyboardButton("ℹ️ عن النسخة V52", callback_data="ui_about")
    ]
    markup.add(*btns)
    if uid == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("🛠 لوحة الإدارة العليا 🛠", callback_data="adm_panel"))
    return markup

def dl_keyboard():
    """خيارات التحميل بعد إرسال الرابط"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎬 فيديو MP4", callback_data="m_vid"),
        types.InlineKeyboardButton("🎵 صوت MP3", callback_data="m_aud"),
        types.InlineKeyboardButton("🎞 GIF متحركة", callback_data="m_gif"),
        types.InlineKeyboardButton("🔙 إلغاء", callback_data="ui_back")
    )
    return markup

# --- [ 8. محرك التقسيم والتحميل العميق ] ---
def split_large_video(file_path, max_size_mb=45):
    """
    دالة ذكية لتقسيم الفيديوهات الكبيرة لتجاوز حدود تليجرام (50MB).
    """
    file_size = os.path.getsize(file_path) / (1024 * 1024)
    if file_size <= max_size_mb:
        return [file_path]
    
    print(f"✂️ الفيديو حجمه {file_size:.1f}MB، جاري التقسيم...")
    parts = []
    try:
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
    """محرك التحميل الآمن مع معالجة الاستثناءات"""
    status_msg = bot.send_message(chat_id, "⏳ جاري فحص الرابط ومعالجة البيانات...")
    try:
        file_id = f"v52_{int(time.time())}_{random.randint(100,999)}"
        path_tmpl = os.path.join(CACHE_DIR, f"{file_id}.%(ext)s")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': path_tmpl,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            bot.edit_message_text("📥 جاري سحب الملف من السيرفر...", chat_id, status_msg.message_id)
            info = ydl.extract_info(url, download=True)
            f_name = ydl.prepare_filename(info)
        
        if type_mode == 'v':
            video_parts = split_large_video(f_name)
            for i, p in enumerate(video_parts):
                bot.send_chat_action(chat_id, 'upload_video')
                with open(p, 'rb') as f:
                    cap = f"✅ الجزء {i+1} من الفيديو\n👤 بواسطة: {MY_USER}\n🚀 الإصدار: V52.0"
                    bot.send_video(chat_id, f, caption=cap)
                if p != f_name and os.path.exists(p): os.remove(p)
        
        elif type_mode == 'a':
            bot.send_chat_action(chat_id, 'upload_audio')
            with open(f_name, 'rb') as f:
                bot.send_audio(chat_id, f, caption=f"🎵 تم تحويل الرابط لصوت\n👤 المطور: {MY_USER}")
                
        if os.path.exists(f_name): os.remove(f_name)
        bot.delete_message(chat_id, status_msg.message_id)
        update_user_profile(chat_id, "User", xp=150, dl=1)
        
    except Exception as e:
        bot.edit_message_text(f"❌ خطأ تقني: {str(e)[:100]}", chat_id, status_msg.message_id)

# --- [ 9. معالجة الأحداث والدردشة ] ---
current_urls = {}

@bot.message_handler(commands=['start'])
def start_handler(m):
    uid = m.from_user.id
    if uid in load_data("banned"):
        return bot.reply_to(m, "🚫 عذراً، حسابك محظور من استخدام النظام.")
    
    users = load_data("users")
    if uid not in users:
        users.append(uid)
        save_data("users", users)
    
    update_user_profile(uid, m.from_user.first_name)
    welcome_text = (
        f"👑 أهلاً بك يا {m.from_user.first_name} في النسخة V52.0\n\n"
        "📍 بوت التحميل الأقوى والأسرع في العراق.\n"
        "🛠 تم التطوير بواسطة إبراهيم مصطفى.\n\n"
        "⬇️ أرسل أي رابط (تيك توك، يوتيوب، إنستا) للبدء."
    )
    bot.send_message(m.chat.id, welcome_text, reply_markup=main_keyboard(uid))

@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def link_handler(m):
    if m.from_user.id in load_data("banned"): return
    current_urls[m.from_user.id] = m.text
    bot.reply_to(m, "🗳 تم استلام الرابط بنجاح.\nما هي الصيغة المطلوبة؟", reply_markup=dl_keyboard())

# --- [ 10. معالج أزرار الإدارة والمستخدم PRO ] ---
@bot.callback_query_handler(func=lambda call: True)
def ui_manager(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    
    # حماية لوحة الأدمن
    if "adm_" in call.data and uid != ADMIN_ID:
        return bot.answer_callback_query(call.id, "🚫 تنبيه: أنت لا تملك صلاحيات المطور إبراهيم!", show_alert=True)

    # --- [ أزرار الإدارة ] ---
    if call.data == "adm_panel":
        bot.edit_message_text("🛠 لوحة الإدارة العليا (V52.0) 🛠\nمرحباً بك يا إبراهيم.", cid, mid, reply_markup=admin_keyboard())

    elif call.data == "adm_full_stats":
        u = load_data("users")
        b = load_data("banned")
        r = load_data("ranks")
        msg = f"📊 إحصائيات البوت الكاملة:\n\n👥 عدد المستخدمين: {len(u)}\n🚫 المحظورين: {len(b)}\n⭐ عدد الرتب المفعلة: {len(r)}"
        bot.answer_callback_query(call.id, msg, show_alert=True)

    elif call.data == "adm_broadcast":
        msg = bot.send_message(cid, "📝 أرسل الرسالة (نص، صورة، فيديو) لإذاعتها:")
        bot.register_next_step_handler(msg, process_broadcast)

    elif call.data == "adm_clean":
        files = os.listdir(CACHE_DIR)
        for f in files: os.remove(os.path.join(CACHE_DIR, f))
        bot.answer_callback_query(call.id, f"✅ تم تنظيف {len(files)} ملف من الكاش.", show_alert=True)

    elif call.data == "adm_restart":
        bot.edit_message_text("🔄 جاري إعادة تشغيل المحركات... انتظر 5 ثوانٍ.", cid, mid)
        time.sleep(2)
        os.execv(sys.executable, ['python'] + sys.argv)

    # --- [ أزرار المستخدم ] ---
    elif call.data == "ui_back":
        bot.edit_message_text("🏠 القائمة الرئيسية - اختر من الخيارات التالية:", cid, mid, reply_markup=main_keyboard(uid))
        
    elif call.data == "ui_me":
        u = load_data("ranks").get(str(uid), {"xp":0, "dl":0, "lvl":"مبتدئ"})
        info = (
            f"👤 معلومات حسابك:\n━━━━━━━━━━━━\n"
            f"🎖 الرتبة: {u['lvl']}\n"
            f"⭐ نقاط الخبرة: {u['xp']}\n"
            f"📥 مجموع التحميلات: {u['dl']}\n"
            f"📅 تاريخ الانضمام: {u.get('date', 'غير مسجل')}\n"
            f"📍 الموقع: العراق - البصرة 🌴"
        )
        bot.edit_message_text(info, cid, mid, reply_markup=main_keyboard(uid))

    elif call.data == "ui_top":
        data = load_data("ranks")
        top_list = sorted(data.items(), key=lambda x: x[1]['xp'], reverse=True)[:10]
        txt = "🏆 لوحة شرف المتصدرين (الأكثر تفاعلاً):\n━━━━━━━━━━━━\n"
        for i, (k, v) in enumerate(top_list):
            txt += f"{i+1} | {v['name'][:15]} ➔ {v['xp']} XP\n"
        bot.edit_message_text(txt, cid, mid, reply_markup=main_keyboard(uid))

    elif call.data == "ui_gift":
        daily = load_data("daily")
        today = datetime.now().strftime("%Y-%m-%d")
        if daily.get(str(uid)) == today:
            bot.answer_callback_query(call.id, "❌ لقد حصلت على هديتك اليوم بالفعل! عد غداً.", show_alert=True)
        else:
            daily[str(uid)] = today
            save_data("daily", daily)
            bonus = random.randint(500, 1500)
            update_user_profile(uid, call.from_user.first_name, xp=bonus)
            bot.answer_callback_query(call.id, f"🎁 مبروك! حصلت على {bonus} نقطة خبرة كهدية يومية.", show_alert=True)

    elif call.data == "m_vid":
        url = current_urls.get(uid)
        if url:
            bot.delete_message(cid, mid)
            threading.Thread(target=secure_download, args=(cid, url, 'v')).start()

    elif call.data == "ui_owner":
        bot.edit_message_text(f"👨‍💻 مطور البوت: إبراهيم مصطفى\nالمعرف: {MY_USER}\nالسكن: البصرة 🇮🇶", cid, mid, reply_markup=main_keyboard(uid))

# --- [ 11. وظائف الأدمن العميقة ] ---
def process_broadcast(m):
    users = load_data("users")
    success = 0
    fail = 0
    status = bot.send_message(m.chat.id, f"📢 جاري الإذاعة إلى {len(users)} مستخدم...")
    for u in users:
        try:
            if m.content_type == 'text': bot.send_message(u, m.text)
            elif m.content_type == 'photo': bot.send_photo(u, m.photo[-1].file_id, caption=m.caption)
            elif m.content_type == 'video': bot.send_video(u, m.video.file_id, caption=m.caption)
            success += 1
            time.sleep(0.05) # تجنب حظر التليجرام
        except: fail += 1
    bot.edit_message_text(f"✅ انتهت الإذاعة:\n🟢 نجاح: {success}\n🔴 فشل: {fail}", m.chat.id, status.message_id)

# --- [ 12. محرك التنظيف والاستقرار الذاتي ] ---
def maintenance_engine():
    """محرك يعمل في الخلفية لتنظيف الملفات وضمان عدم امتلاء الذاكرة"""
    while True:
        try:
            if os.path.exists(CACHE_DIR):
                for file in os.listdir(CACHE_DIR):
                    file_path = os.path.join(CACHE_DIR, file)
                    # حذف الملفات التي مر عليها أكثر من 10 دقائق
                    if os.path.getmtime(file_path) < time.time() - 600:
                        os.remove(file_path)
        except Exception as e:
            logging.error(f"Maintenance Error: {e}")
        time.sleep(300) # فحص كل 5 دقائق

# --- [ 13. تشغيل البوت النهائي ] ---
if __name__ == "__main__":
    # تشغيل محرك الصيانة في خيط منفصل
    threading.Thread(target=maintenance_engine, daemon=True).start()
    
    print("="*50)
    print(f"🚀 V52.0 IS LIVE | DEVELOPER: {MY_USER}")
    print(f"📍 SERVER: BASRA, IRAQ")
    print("="*50)
    
    while True:
        try:
            bot.infinity_polling(timeout=120, long_polling_timeout=80)
        except Exception as e:
            logging.error(f"Polling Crash: {e}")
            time.sleep(10) # إعادة تشغيل تلقائي بعد 10 ثوانٍ
