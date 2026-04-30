# ======================================================
# 👑 PROJECT: THE ELITE TIKTOK DOWNLOADER (V53.0)
# 👤 OWNER: IBRAHIM MUSTAFA (@x_u3s1)
# 🛠 STATUS: ULTRA STABLE | NO CONFLICT | NO CRASH
# 📍 REGION: BASRA, IRAQ 🇮🇶
# ======================================================

import os
import time
import json
import threading
import telebot
from telebot import types
import yt_dlp

# --- [ إعدادات الهوية والاتصال ] ---
TOKEN = '8168190815:AAE3mW6S1ntpmVx9OVvboofNm1VIHLjwx-o'
ADMIN_ID = 8301016131
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# --- [ نظام قاعدة البيانات ] ---
def setup_db():
    for f in ['users.json', 'stats.json']:
        if not os.path.exists(f):
            with open(f, 'w') as out: json.dump({} if 'stats' in f else [], out)

setup_db()

def get_db(f):
    with open(f, 'r') as file: return json.load(file)

def save_db(f, data):
    with open(f, 'w') as file: json.dump(data, file, indent=4)

def update_user(uid, name):
    stats = get_db('stats.json')
    s_id = str(uid)
    if s_id not in stats:
        stats[s_id] = {"name": name, "points": 0, "downloads": 0}
    stats[s_id]["points"] += 10
    stats[s_id]["downloads"] += 1
    save_db('stats.json', stats)

# --- [ الكيبوردات الشيك ] ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📥 تحميل تيك توك", "🎁 هدية يومية")
    markup.add("🏆 المتصدرين (Top 10)", "📊 الإحصائيات")
    markup.add("👨‍💻 المطور")
    return markup

def download_markup(url):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎬 فيديو بدقة عالية", callback_data=f"vid|{url}"),
        types.InlineKeyboardButton("🎵 صوت فقط (MP3)", callback_data=f"aud|{url}")
    )
    return markup

# --- [ معالج الأوامر الرئيسية ] ---
@bot.message_handler(commands=['start'])
def start(m):
    users = get_db('users.json')
    if m.from_user.id not in users:
        users.append(m.from_user.id)
        save_db('users.json', users)
    
    welcome_text = (
        f"👑 *أهلاً بك يا {m.from_user.first_name}*\n"
        "في أقوى سكربت لتحميل فيديوهات تيك توك بجودة عالية.\n\n"
        "📍 *المصدر:* البصرة - العراق\n"
        "🚀 *الحالة:* مستقر وجاهز للعمل"
    )
    bot.send_message(m.chat.id, welcome_text, reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handle_text(m):
    if m.text == "📥 تحميل تيك توك":
        bot.send_message(m.chat.id, "🔗 *أرسل رابط تيك توك الآن...*")
    
    elif m.text == "🎁 هدية يومية":
        bot.reply_to(m, "🎉 *حصلت على 20 نقطة هدية يومية!*")
        update_user(m.from_user.id, m.from_user.first_name)
    
    elif m.text == "📊 الإحصائيات":
        count = len(get_db('users.json'))
        bot.reply_to(m, f"📊 *إحصائيات البوت:*\n\n👥 عدد المشتركين: `{count}`\n⚙️ السيرفر: `Railway High Speed`")
    
    elif m.text == "👨‍💻 المطور":
        bot.reply_to(m, "👤 *المطور:* إبراهيم مصطفى\n🆔 *اليوزر:* @x_u3s1\n🇮🇶 *البلد:* العراق (البصرة)")

    elif m.text == "🏆 المتصدرين (Top 10)":
        stats = get_db('stats.json')
        top = sorted(stats.items(), key=lambda x: x[1]['points'], reverse=True)[:10]
        text = "🏆 *قائمة أكثر 10 مستخدمين جمعاً للنقاط:*\n\n"
        for i, (uid, data) in enumerate(top, 1):
            text += f"{i} - {data['name']} ⮕ `{data['points']}` نقطة\n"
        bot.send_message(m.chat.id, text)

    elif "tiktok.com" in m.text:
        bot.send_message(m.chat.id, "🧐 *تم كشف رابط تيك توك، اختر الصيغة:*", reply_markup=download_markup(m.text))

# --- [ محرك التحميل الذكي ] ---
def process_dl(chat_id, url, mode, name):
    msg = bot.send_message(chat_id, "⏳ *جاري التحميل بأعلى جودة ممكنة...*")
    try:
        t = int(time.time())
        path = f"file_{t}.%(ext)s"
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best' if mode == 'vid' else 'bestaudio/best',
            'outtmpl': path,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        bot.send_chat_action(chat_id, 'upload_video' if mode == 'vid' else 'upload_document')
        
        with open(filename, 'rb') as f:
            caption = f"✅ *تم التحميل بنجاح!*\n👤 *المستخدم:* {name}\n⚙️ *بواسطة:* @{bot.get_me().username}"
            if mode == 'vid':
                bot.send_video(chat_id, f, caption=caption)
            else:
                bot.send_audio(chat_id, f, caption=caption)
        
        os.remove(filename)
        bot.delete_message(chat_id, msg.message_id)
        update_user(chat_id, name)
    except Exception as e:
        bot.edit_message_text(f"❌ *عذراً، حدث خطأ:* الرابط قد يكون خاصاً أو هناك مشكلة بالسيرفر.", chat_id, msg.message_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    mode, url = call.data.split('|')
    threading.Thread(target=process_dl, args=(call.message.chat.id, url, mode, call.from_user.first_name)).start()
    bot.answer_callback_query(call.id, "بدأت المعالجة...")

# --- [ الحماية والتشغيل ] ---
if __name__ == "__main__":
    bot.remove_webhook() # يحل مشكلة الـ 409 Conflict نهائياً
    print("🚀 السكربت شغال بأعلى كفاءة في البصرة!")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
    
