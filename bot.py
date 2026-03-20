import telebot
from telebot import types
import random
import string
import os

# Render এর Environment Variables থেকে টোকেনটি সংগ্রহ করবে
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

def analyze_password(pwd):
    score = 0
    if len(pwd) >= 12: score += 2
    elif len(pwd) >= 8: score += 1
    if any(c.islower() for c in pwd): score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in "!@#$%^&*()_+-=" for c in pwd): score += 1

    if score <= 2: return "খুবই দুর্বল (VERY WEAK) ❌"
    elif score <= 4: return "দুর্বল (WEAK) ⚠️"
    elif score == 5: return "ভালো (GOOD) ✅"
    else: return "অত্যন্ত শক্তিশালী (STRONG) 🔐"

def main_menu():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🔑 Generate Password", callback_data="gen_pass")
    btn2 = types.InlineKeyboardButton("🛡️ Security Tips", callback_data="sec_tips")
    markup.add(btn1)
    markup.add(btn2)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    banner = (
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🛡️ **PASSWORD SECURITY TOOL** 🛡️\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "হ্যালো! আমি আপনার পাসওয়ার্ড সুরক্ষিত রাখতে সাহায্য করবো।\n\n"
        "👉 **পাসওয়ার্ড চেক করতে সেটি সরাসরি মেসেজ করুন।**\n"
        "👉 **নতুন পাসওয়ার্ড তৈরি করতে নিচের বাটনে ক্লিক করুন।**"
    )
    bot.send_message(message.chat.id, banner, parse_mode="Markdown", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "gen_pass":
        length = 16
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        password = "".join(random.choice(chars) for _ in range(length))
        response = f"✅ **আপনার নতুন পাসওয়ার্ড:**\n\n`{password}`\n\nএটি কপি করে সুরক্ষিত কোথাও রাখুন।"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, response, parse_mode="Markdown", reply_markup=main_menu())
    
    elif call.data == "sec_tips":
        tips = (
            "💡 **Security Tips:**\n"
            "• কমপক্ষে ১২ অক্ষরের পাসওয়ার্ড ব্যবহার করুন।\n"
            "• বড় হাতের ও ছোট হাতের অক্ষর মিশিয়ে দিন।\n"
            "• সংখ্যা এবং স্পেশাল ক্যারেক্টার (!@#$) ব্যবহার করুন।\n"
            "• ব্যক্তিগত তথ্য (নাম, জন্মদিন) পাসওয়ার্ডে দেবেন না।"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, tips, parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def check_pass(message):
    result = analyze_password(message.text)
    response = (
        f"🔍 **Analysis Result:**\n\n"
        f"Password: `{message.text}`\n"
        f"Strength: **{result}**"
    )
    bot.reply_to(message, response, parse_mode="Markdown", reply_markup=main_menu())

# বটের কানেকশন বজায় রাখার জন্য
if __name__ == "__main__":
    print("বটটি সফলভাবে চালু হয়েছে...")
    bot.infinity_polling()
      
