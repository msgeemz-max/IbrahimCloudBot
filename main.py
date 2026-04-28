import telebot
from telebot import types
from pymongo import MongoClient

# إعداداتك السحابية ✅
TOKEN = '8168190815:AAG0U-eqjIvAr5HbtTWTGOqQzSRz9Pdx4AY'
MONGO_URL = "mongodb+srv://msgeemz_db_user:gLSEVJrCkMUkPBzZ@cluster0.ciygstj.mongodb.net/?appName=Cluster0"

bot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGO_URL)
db = client['ibrahim_db']
users = db['users']

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    if not users.find_one({"id": uid}):
        users.insert_one({"id": uid, "points": 0, "name": message.from_user.first_name})
    bot.send_message(message.chat.id, f"أهلاً {message.from_user.first_name}! بوتك الآن مربوط بالسحاب ☁️")

if __name__ == "__main__":
    bot.infinity_polling()
  
