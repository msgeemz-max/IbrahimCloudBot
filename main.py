# -*- coding: utf-8 -*-
# ======================================================
# 👑 PROJECT: THE GIANT EMPIRE SCRIPTS (V60.0)
# 👤 OWNER: IBRAHIM MUSTAFA (@x_u3s1)
# 🛠 ENGINE: PYTELEGRAMBOTAPI & YT-DLP
# 📍 REGION: BASRA, IRAQ 🇮🇶
# 🚀 TOTAL LINES: +300 FOR MAXIMUM STABILITY
# ======================================================

import os
import time
import json
import threading
import telebot
import requests
import random
from telebot import types
import yt_dlp

# --- [ إعدادات الهوية ] ---
TOKEN = '8168190815:AAE3mW6S1ntpmVx9OVvboofNm1VlHLjwx-o'
ADMIN_ID = 8301016131
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# --- [ تهيئة نظام قواعد البيانات ] ---
FILES = ['users.json', 'stats.json', 'settings.json']

def initialize_database():
    """وظيفة لتهيئة ملفات البيانات عند التشغيل الأول"""
    for file in FILES:
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as f:
                if 'users' in file:
                    json.dump([], f)
                else:
                    json.dump({}, f)
    print("✅ [DB] Database initialized successfully.")

initialize_database()

def load_data(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def log_user(uid, name):
    users = load_data('users.json')
    if uid not in users:
        users.append(uid)
        save_data('users.json', users)
    
    stats = load_data('stats.json')
    sid = str(uid)
    if sid not in stats:
        stats[sid] = {
            "name": name,
            "points": 10,
            "downloads": 0,
            "joined_at": time.ctime(),
            "level": "مواطن"
        }
        save_data('stats.json', stats)

# --- [ أنظمة الحماية والأدوات ] ---
def is_admin(uid):
    return uid == ADMIN_ID

def get_rank(uid, points):
    if is_admin(uid): return "مطور السكربت 👨‍💻"
    if points > 1000: return "إمبراطور 👑"
    if points > 500: return "جنرال ⚔️"
    if points > 100: return "فارس 🛡️"
    return "مواطن 👤"

# --- [ واجهات المستخدم - الكيبوردات ] ---
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("📥 تحميل من تيك توك")
    btn2 = types.KeyboardButton("🎁 هدية الإمبراطورية")
    btn3 = types.KeyboardButton("🏆 قائمة المتصدرين")
    btn4 = types.KeyboardButton("📊 ملفي الشخصي")
    btn5 = types.KeyboardButton("👨‍💻 مطور السكربت")
    btn6 = types.KeyboardButton("🛠 الإحصائيات العامة")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    return markup

def get_download_markup(url):
    markup = types.InlineKeyboardMarkup(row_width=2)
    v_btn = types.InlineKeyboardButton("🎬 فيديو (HD)", callback_data=f"v|{url}")
    a_btn = types.InlineKeyboardButton("🎵 صوت (MP3)", callback_data=f"a|{url}")
    markup.add(v_btn, a_btn)
    return markup

def admin_panel():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📢 إذاعة للمستخدمين", callback_data="admin_cast"),
        types.InlineKeyboardButton("📈 تقرير السيرفر", callback_data="admin_report")
    )
    return markup

# --- [ معالجة الأوامر الرئيسية ] ---
@bot.message_handler(commands=['start'])
def welcome_message(m):
    log_user(m.from_user.id, m.from_user.first_name)
    welcome_text = (
        f"🌟 *مرحباً بك في إمبراطورية العملاق*\n"
        f"━━━━━━━━━━━━━━\n"
        f"أهلاً بك يا {m.from_user.first_name}، أنت الآن تستخدم السكربت الأقوى لتحميل الميديا بأعلى دقة متوفرة.\n\n"
        f"✨ *مميزات النسخة V60.0:*\n"
        f"• تحميل تيك توك بدون علامة مائية.\n"
        f"• تحويل الفيديو إلى صوت MP3.\n"
        f"• نظام نقاط وتصنيف عالمي.\n"
        f"━━━━━━━━━━━━━━\n"
        f"📍 *الموقع:* البصرة، العراق"
    )
    bot.send_message(m.chat.id, welcome_text, reply_markup=get_main_keyboard())

@bot.message_handler(commands=['admin'])
def open_admin(m):
    if is_admin(m.from_user.id):
        bot.send_message(m.chat.id, "🛠 *أهلاً مطور إبراهيم، اختر إجراءً من اللوحة:*", reply_markup=admin_panel())
    else:
        bot.reply_to(m, "⚠️ هذا الأمر خاص بمطور السكربت فقط.")

# --- [ معالجة النصوص والأزرار ] ---
@bot.message_handler(func=lambda m: True)
def handle_帝国_interactions(m):
    uid = m.from_user.id
    text = m.text

    if text == "📥 تحميل من تيك توك":
        bot.send_message(m.chat.id, "🚀 *أرسل رابط تيك توك الآن، وسأقوم بمعالجته فوراً...*")

    elif text == "🎁 هدية الإمبراطورية":
        stats = load_data('stats.json')
        sid = str(uid)
        gift_points = random.randint(20, 100)
        stats[sid]["points"] += gift_points
        save_data('stats.json', stats)
        bot.reply_to(m, f"🎉 *مبروك! لقد حصلت على {gift_points} نقطة كهدية من الإمبراطورية.*")

    elif text == "📊 ملفي الشخصي":
        stats = load_data('stats.json').get(str(uid), {})
        rank = get_rank(uid, stats.get('points', 0))
        profile = (
            f"👤 *معلوماتك الشخصية:*\n"
            f"━━━━━━━━━━━━━━\n"
            f"📛 الاسم: {stats.get('name')}\n"
            f"💰 النقاط: `{stats.get('points')}`\n"
            f"📥 التحميلات: `{stats.get('downloads')}`\n"
            f"🎖 الرتبة: *{rank}*\n"
            f"━━━━━━━━━━━━━━"
        )
        bot.send_message(m.chat.id, profile)

    elif text == "🏆 قائمة المتصدرين":
        stats = load_data('stats.json')
        top = sorted(stats.items(), key=lambda x: x[1]['points'], reverse=True)[:10]
        leaderboard = "🏆 *أقوى 10 أباطرة في السكربت:*\n\n"
        for i, (user_id, data) in enumerate(top, 1):
            leaderboard += f"{i}. {data['name']} ⮕ `{data['points']}` نقطة\n"
        bot.send_message(m.chat.id, leaderboard)

    elif text == "👨‍💻 مطور السكربت":
        dev_info = (
            f"👑 *مطور السكربت العملاق:*\n\n"
            f"👤 *الاسم:* إبراهيم مصطفى\n"
            f"🆔 *اليوزر:* @x_u3s1\n"
            f"🇮🇶 *السكن:* العراق - البصرة\n\n"
            f"السكربت يعمل على سيرفرات Railway ومحدث لعام 2026."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("المطور إبراهيم 💬", url="https://t.me/x_u3s1"))
        bot.send_message(m.chat.id, dev_info, reply_markup=markup)

    elif text == "🛠 الإحصائيات العامة":
        users_count = len(load_data('users.json'))
        bot.reply_to(m, f"📊 *إحصائيات الإمبراطورية:*\n\n👥 عدد المستخدمين: `{users_count}`\n⚡️ السرعة: `ممتازة`\n🛠 الحالة: `مستقر`")

    elif "tiktok.com" in text:
        bot.send_message(m.chat.id, "✨ *تم كشف الرابط.. اختر الصيغة المطلوبة:*", reply_markup=get_download_markup(text))

# --- [ محرك التحميل المتطور ] ---
def download_engine(chat_id, url, mode, user_name):
    temp_msg = bot.send_message(chat_id, "⏳ *جاري الاتصال بخوادم تيك توك...*")
    try:
        file_id = f"empire_{int(time.time())}"
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best' if mode == 'v' else 'bestaudio/best',
            'outtmpl': f"{file_id}.%(ext)s",
            'quiet': True,
            'no_warnings': True,
            'geo_bypass': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            bot.edit_message_text("📥 *جاري سحب البيانات وبدء التحميل...*", chat_id, temp_msg.message_id)
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        bot.send_chat_action(chat_id, 'upload_video' if mode == 'v' else 'record_audio')
        
        with open(filename, 'rb') as f:
            caption = f"✅ *تم التحميل بنجاح بواسطة العملاق*\n👤 *بطلب من:* {user_name}\n🚀 *السرعة:* عالية جداً"
            if mode == 'v':
                bot.send_video(chat_id, f, caption=caption, supports_streaming=True)
            else:
                bot.send_audio(chat_id, f, caption=caption)

        stats = load_data('stats.json')
        sid = str(chat_id)
        if sid in stats:
            stats[sid]["points"] += 5
            stats[sid]["downloads"] += 1
            save_data('stats.json', stats)

        os.remove(filename)
        bot.delete_message(chat_id, temp_msg.message_id)

    except Exception as error:
        print(f"Error: {error}")
        bot.edit_message_text("❌ *عذراً!* حدث خطأ أثناء التحميل. تأكد من أن الحساب ليس خاصاً.", chat_id, temp_msg.message_id)

# --- [ نظام الإذاعة (برودكاست) ] ---
def start_broadcast(m):
    users = load_data('users.json')
    broadcast_text = m.text
    success = 0
    fail = 0
    
    status_msg = bot.send_message(m.chat.id, f"⌛ جاري الإذاعة إلى `{len(users)}` مستخدم...")
    
    for user_id in users:
        try:
            bot.send_message(user_id, f"📢 *إعلان من الإمبراطورية:*\n\n{broadcast_text}")
            success += 1
        except:
            fail += 1
            
    bot.edit_message_text(f"✅ تم الانتهاء من الإذاعة!\n\n🟢 نجاح: `{success}`\n🔴 فشل: `{fail}`", m.chat.id, status_msg.message_id)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if "|" in call.data:
        mode, url = call.data.split('|')
        threading.Thread(target=download_engine, args=(call.message.chat.id, url, mode, call.from_user.first_name)).start()
        bot.answer_callback_query(call.id, "جاري البدء...")
    
    elif call.data == "admin_report":
        users = len(load_data('users.json'))
        bot.answer_callback_query(call.id, "جاري جلب التقرير...")
        bot.send_message(call.message.chat.id, f"📈 *تقرير الإمبراطورية:* \n\nالمستخدمين: {users}\nالسيرفر: Railway\nالحالة: Online")
    
    elif call.data == "admin_cast":
        if is_admin(call.from_user.id):
            msg = bot.send_message(call.message.chat.id, "📩 أرسل نص الرسالة التي تريد إذاعتها الآن:")
            bot.register_next_step_handler(msg, start_broadcast)
        else:
            bot.answer_callback_query(call.id, "⚠️ غير مسموح لك.")

# --- [ نظام التشغيل والحماية من التوقف ] ---
def run_empire_bot():
    """وظيفة لتشغيل البوت مع معالجة الأخطاء لضمان الاستمرارية"""
    while True:
        try:
            bot.remove_webhook()
            print("🚀 [START] Empire Giant Script is now active on Railway!")
            bot.infinity_polling(timeout=90, long_polling_timeout=50)
        except Exception as e:
            print(f"⚠️ [RESTART] Bot crashed, restarting in 5 seconds... Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_empire_bot()

# ======================================================
# نهاية السكربت - صنع بكل إتقان لإبراهيم مصطفى
# ======================================================
