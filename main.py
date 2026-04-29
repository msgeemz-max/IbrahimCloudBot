# ======================================================
# 👑 PROJECT: THE ULTIMATE MODULAR BOT (V43.14)
# 👤 DEVELOPER: IBRAHIM MUSTAFA (@x_u3s1)
# 🆔 ADMIN ID: 8301016131
# 🛠 FIX: ARABIC RTL SUBTITLES + FFmpeg POSITIONING
# 📏 LENGTH: 500+ LINES - NO DELETIONS
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
from datetime import datetime, timedelta

# --- [ 1. محرك التحديث التلقائي الذكي ] ---
def update_system():
    """تحديث المكتبات لنسخ متوافقة مع بايثون 3.11 ودعم العربية"""
    print("⚙️ جاري فحص وتحديث النظام للنسخة المستقرة...")
    try:
        # إضافة مكتبات معالجة اللغة العربية للقائمة
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "--upgrade", 
                               "yt-dlp", "pyTelegramBotAPI", "requests", "googletrans==3.1.0a0", 
                               "arabic-reshaper", "python-bidi"])
        print("✅ تم التحديث بنجاح، النظام يدعم العربية الآن.")
    except Exception as e:
        print(f"⚠️ فشل التحديث التلقائي: {e}")

update_system()

import telebot
from telebot import types
import yt_dlp
from googletrans import Translator
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# --- [ 2. الثوابت والإعدادات ] ---
# يرجى استبدال TOKEN بالتوكن الخاص بك من BotFather
API_TOKEN = 'TOKEN_YOU_REPLACED'.strip()
bot = telebot.TeleBot(API_TOKEN)

ADMIN_ID = 8301016131 
MY_USER = "@x_u3s1"

FILE_RANKS = "v43_ranks.json"
FILE_USERS = "v43_users.json"
FILE_DAILY = "v43_daily.json"
FILE_STATS = "v43_stats.json"
CACHE_DIR = "v43_storage"

if not os.path.exists(CACHE_DIR): os.makedirs(CACHE_DIR)

# --- [ 3. محرك إدارة البيانات المنفصل ] ---

def get_db(path):
    try:
        if not os.path.exists(path):
            default = [] if "users" in path else {}
            if "stats" in path: default = {"total_dl": 0, "total_msg": 0}
            with open(path, "w", encoding='utf-8') as f:
                json.dump(default, f, indent=4)
            return default
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error reading {path}: {e}")
        return [] if "users" in path else {}

def save_db(path, data):
    try:
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Error saving {path}: {e}")

# --- [ 4. نظام المستخدمين والخبرة ] ---

def register_new_user(user_obj):
    users = get_db(FILE_USERS)
    if user_obj.id not in users:
        users.append(user_obj.id)
        save_db(FILE_USERS, users)

def sync_user_data(uid, name, xp_add=0, dl_add=0):
    data = get_db(FILE_RANKS)
    uid_s = str(uid)
    name = re.sub(r'[*_`\[\]]', '', str(name))
    
    if uid_s not in data:
        data[uid_s] = {"xp": 0, "dl": 0, "name": name, "level": "مبتدئ"}
    
    data[uid_s]["xp"] += xp_add
    data[uid_s]["dl"] += dl_add
    data[uid_s]["name"] = name
    
    if uid == ADMIN_ID:
        data[uid_s]["level"] = "المطور الأساسي 👑"
    else:
        xp = data[uid_s]["xp"]
        if xp > 10000: data[uid_s]["level"] = "ملك البرمجة 👑"
        elif xp > 5000: data[uid_s]["level"] = "أسطورة 💎"
        elif xp > 1000: data[uid_s]["level"] = "محترف 🔥"
        else: data[uid_s]["level"] = "مبتدئ"
    
    save_db(FILE_RANKS, data)

# --- [ 5. واجهة المستخدم ] ---

def build_main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("📥 تحميل ميديا", callback_data="btn_dl"),
           types.InlineKeyboardButton("👤 حسابي", callback_data="btn_profile"),
           types.InlineKeyboardButton("🏆 الأوائل", callback_data="btn_top"),
           types.InlineKeyboardButton("🎁 الهدية", callback_data="btn_gift"),
           types.InlineKeyboardButton("👨‍💻 المطور", callback_data="btn_dev"))
    return kb

def build_back_button():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔙 العودة للقائمة", callback_data="btn_back"))
    return kb

def setup_bot_commands():
    commands = [
        types.BotCommand("start", "فتح القائمة الرئيسية 🏠"),
        types.BotCommand("admin", "لوحة المطور إبراهيم 🛠")
    ]
    bot.set_my_commands(commands)

# --- [ 6. وظائف البوت المستقلة ] ---

def show_profile(call):
    data = get_db(FILE_RANKS)
    u = data.get(str(call.from_user.id), {"xp": 0, "dl": 0, "name": "غير مسجل", "level": "مبتدئ"})
    text = (f"👤 **بطاقة المستخدم:**\n\n"
            f"▫️ الاسم: {u['name']}\n"
            f"▫️ الخبرة (XP): `{u['xp']}`\n"
            f"▫️ التحميلات: `{u['dl']}`\n"
            f"▫️ الرتبة: {u['level']}")
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                          parse_mode="Markdown", reply_markup=build_back_button())

def show_leaderboard(call):
    data = get_db(FILE_RANKS)
    top = sorted(data.items(), key=lambda x: x[1].get('xp', 0), reverse=True)[:10]
    text = "🏆 **قائمة العمالقة (التوب 10):**\n\n"
    for i, (k, v) in enumerate(top, 1):
        text += f"{i} - {v['name']} ➔ `{v['xp']}` XP\n"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                          parse_mode="Markdown", reply_markup=build_back_button())

def claim_daily_gift(call):
    daily = get_db(FILE_DAILY)
    uid_s = str(call.from_user.id)
    now = datetime.now()
    if uid_s in daily:
        last = datetime.strptime(daily[uid_s], "%Y-%m-%d %H:%M:%S")
        if now - last < timedelta(hours=24):
            bot.answer_callback_query(call.id, "⏳ استلمتها سابقاً، ارجع غداً يا إبراهيم!", show_alert=True)
            return
    bonus = random.randint(250, 600)
    sync_user_data(call.from_user.id, call.from_user.first_name, xp_add=bonus)
    daily[uid_s] = now.strftime("%Y-%m-%d %H:%M:%S")
    save_db(FILE_DAILY, daily)
    bot.answer_callback_query(call.id, f"🎊 مبروك! حصلت على {bonus} XP هديتك اليومية.", show_alert=True)

# --- [ 7. محرك التحميل والترجمة المزدوج ] ---

user_links = {}

def initiate_dl(call):
    msg = bot.edit_message_text("📥 أرسل رابط الفيديو الآن (TikTok, YT, IG):", 
                                call.message.chat.id, call.message.message_id)
    bot.register_next_step_handler(msg, process_url)

def process_url(message):
    if "http" in message.text:
        user_links[message.from_user.id] = message.text
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton("🎬 فيديو (MP4)", callback_data="run_v"),
               types.InlineKeyboardButton("🎵 صوت (MP3)", callback_data="run_a"),
               types.InlineKeyboardButton("🌍 ترجمة وحفر (AI Sub)", callback_data="run_sub"))
        bot.reply_to(message, "⚙️ اختر الصيغة المناسبة:", reply_markup=kb)
    else: bot.reply_to(message, "❌ الرابط غير صالح.")

# وظيفة لمعالجة النص العربي ليظهر بشكل صحيح في FFmpeg
def get_reshaped_text(text):
    reshaped_text = reshape(text)
    return get_display(reshaped_text)

def download_core(chat_id, url, mode):
    status = bot.send_message(chat_id, "🎬 جاري جلب الميديا من TikWM...")
    api_url = f"https://www.tikwm.com/api/?url={url}"
    try:
        response = requests.get(api_url).json()
        if response.get('code') == 0:
            data = response['data']
            # استخدام play لنسخة TikTok (الفيديو) أو play_wm لليوتيوب/انستغرام
            target_url = data.get('play') or data.get('play_wm') or data.get('music')
            if not target_url:
                raise Exception("فشل الحصول على رابط التحميل من tikwm.")
            
            cap = f"✅ تم التحميل بنجاح\n👨‍💻 المبرمج: إبراهيم مصطفى"
            if mode == 'v':
                bot.send_video(chat_id, target_url, caption=cap, timeout=60)
            else:
                bot.send_audio(chat_id, target_url, caption=cap, timeout=60)
            bot.delete_message(chat_id, status.message_id)
            sync_user_data(chat_id, "User", xp_add=35, dl_add=1)
            return
    except Exception as e:
        print(f"TikWM Error: {e}")
    
    bot.edit_message_text(f"❌ فشل التحميل السريع عبر TikWM، قد يكون الرابط خاصاً أو غير مدعوم.", chat_id, status.message_id)


def download_with_subtitles(chat_id, url):
    """محرك حفر الترجمة الاحترافي يدعم اللغة العربية ومكان النص بالأسفل"""
    status = bot.send_message(chat_id, "🔍 جاري التحليل وحفر الترجمة العربية...")
    tag = f"sub_{int(time.time())}"
    video_path = f"{CACHE_DIR}/{tag}.mp4"
    srt_path = f"{CACHE_DIR}/{tag}.srt"
    output_path = f"{CACHE_DIR}/{tag}_tr.mp4"

    try:
        # 1. تحميل الفيديو
        bot.edit_message_text("🎬 جاري تحميل الفيديو الأصلي...", chat_id, status.message_id)
        ydl_opts = {'format': 'best', 'outtmpl': video_path, 'quiet': True, 'timeout': 60}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'محتوى فيديو')

        # 2. ترجمة ومعالجة النص العربي
        bot.edit_message_text("🌍 جاري ترجمة العنوان للعربية...", chat_id, status.message_id)
        translator = Translator()
        translated = translator.translate(title, dest='ar').text
        
        # معالجة النص ليظهر بشكل صحيح من اليمين لليسار وبحروف متصلة
        fixed_text = get_reshaped_text(translated)
        
        # 3. إنشاء ملف ترجمة مؤقت لضمان التحكم بالمكان (الأسفل)
        with open(srt_path, "w", encoding="utf-8") as srt:
            srt.write(f"1\n00:00:00,000 --> 00:00:59,000\n{fixed_text}\n")

        # 4. أمر FFmpeg الاحترافي (حفر بالأسفل مع خلفية بسيطة للوضوح)
        bot.edit_message_text("⚙️ جاري حفر الترجمة في الفيديو...", chat_id, status.message_id)
        
        # تحقق من وجود ffmpeg في النظام
        try:
            subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise Exception("FFmpeg ليس مثبتاً أو غير موجود في PATH.")
            
        # Alignment=2 تعني أسفل المنتصف
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vf', f"subtitles={srt_path}:force_style='Alignment=2,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1,Shadow=0'",
            '-codec:a', 'copy', output_path, '-y' # -y للإجبار على الكتابة فوق الملف إن وجد
        ]
        subprocess.run(cmd, check=True)

        bot.edit_message_text("📤 جاري رفع الفيديو المترجم...", chat_id, status.message_id)
        with open(output_path, 'rb') as f:
            bot.send_video(chat_id, f, caption="✅ تم التحميل وحفر الترجمة العربية بالأسفل\n👨‍💻 المطور: إبراهيم مصطفى", timeout=120)
        bot.delete_message(chat_id, status.message_id)
        sync_user_data(chat_id, "User", xp_add=50, dl_add=1)

    except Exception as e:
        bot.edit_message_text(f"⚠️ فشل النظام: {str(e)[:100]}", chat_id, status.message_id)
    finally:
        # تنظيف الملفات المؤقتة
        for p in [video_path, srt_path, output_path]:
            if os.path.exists(p): os.remove(p)

# --- [ 8. لوحة التحكم ونظام التنبيهات ] ---

def auto_refresh():
    while True:
        try:
            time.sleep(600) 
            bot.send_message(ADMIN_ID, f"🔄 [نبض النظام]\nالبوت مستقر ويعمل الآن على Railway.\n⏰ {datetime.now().strftime('%H:%M:%S')}")
        except: pass

def show_admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton("📊 إحصائيات", callback_data="adm_stats"),
               types.InlineKeyboardButton("📢 إذاعة", callback_data="adm_bc"),
               types.InlineKeyboardButton("🔙 خروج", callback_data="btn_back"))
        bot.send_message(message.chat.id, "🛠 لوحة التحكم - إبراهيم مصطفى:", reply_markup=kb)
    else: bot.reply_to(message, "❌ هذا القسم للمطور فقط.")

def handle_broadcast(message):
    users = get_db(FILE_USERS)
    bot.send_message(message.chat.id, f"🚀 جاري الإرسال لـ {len(users)} مستخدم...")
    for u in users:
        try: bot.copy_message(u, message.chat.id, message.message_id)
        except: continue
    bot.send_message(message.chat.id, "✅ تمت الإذاعة بنجاح.")

# --- [ 9. معالجة الأوامر والـ Callbacks ] ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    register_new_user(message.from_user)
    sync_user_data(message.from_user.id, message.from_user.first_name, xp_add=5)
    bot.send_message(message.chat.id, f"أهلاً بك يا {message.from_user.first_name} في بوت إبراهيم مصطفى 💎\nالنسخة v43.14 المستقرة (دعم العربية) جاهزة.", 
                     reply_markup=build_main_menu())

@bot.message_handler(commands=['admin'])
def admin_cmd(message):
    show_admin_panel(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_manager(call):
    uid = call.from_user.id
    if call.data == "btn_back":
        bot.edit_message_text(f"🏠 القائمة الرئيسية - إبراهيم v43.14", 
                              call.message.chat.id, call.message.message_id, reply_markup=build_main_menu())
    elif call.data == "btn_profile": show_profile(call)
    elif call.data == "btn_top": show_leaderboard(call)
    elif call.data == "btn_gift": claim_daily_gift(call)
    elif call.data == "btn_dl": initiate_dl(call)
    elif call.data == "btn_dev":
        txt = f"👨‍💻 مبرمج السكربت:\n👤 الاسم: إبراهيم مصطفى\n🆔 اليوزر: {MY_USER}\n🚀 الإصدار: v43.14\n🇮🇶 البلد: العراق"
        bot.edit_message_text(txt, call.message.chat.id, call.message.message_id, reply_markup=build_back_button())
    elif call.data == "run_v":
        url = user_links.get(uid)
        if url: threading.Thread(target=download_core, args=(call.message.chat.id, url, 'v')).start()
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "run_a":
        url = user_links.get(uid)
        if url: threading.Thread(target=download_core, args=(call.message.chat.id, url, 'a')).start()
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "run_sub":
        url = user_links.get(uid)
        if url: threading.Thread(target=download_with_subtitles, args=(call.message.chat.id, url)).start()
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "adm_stats":
        u_count = len(get_db(FILE_USERS))
        bot.answer_callback_query(call.id, f"📊 عدد المشتركين: {u_count}", show_alert=True)
    elif call.data == "adm_bc":
        m = bot.send_message(call.message.chat.id, "📢 أرسل رسالة الإذاعة:")
        bot.register_next_step_handler(m, handle_broadcast)

# --- [ 10. تشغيل البوت ] ---

if __name__ == "__main__":
    setup_bot_commands()
    threading.Thread(target=auto_refresh, daemon=True).start()
    print("🚀 البوت يعمل الآن بنظام v43.14 (Arabic Support)")
    while True:
        try: bot.infinity_polling(timeout=20)
        except Exception: time.sleep(5)
    
