import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8395342822:AAFw8Th9xsWioOoOu9QYQIIOufjPYdloq-g"
ACCESS_KEY = "APEX123"
ADMIN_ID = 7515864015

users = set()
authorized_users = set()

def menu():
    keyboard = [
        ["📱 Number Search"],
        ["📊 Bot Stats", "👨‍💻 Developer"],
        ["ℹ️ Help"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔐 Enter Access Key:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    users.add(user_id)

    # 🔐 ACCESS SYSTEM
    if user_id not in authorized_users:
        if text == ACCESS_KEY:
            authorized_users.add(user_id)
            await update.message.reply_text("✅ Access Granted!", reply_markup=menu())
        else:
            await update.message.reply_text("❌ Invalid Key")
        return

    # 📱 BUTTONS
    if text == "📱 Number Search":
        await update.message.reply_text("Send number 📱")
        context.user_data["search"] = True
        return

    elif text == "📊 Bot Stats":
        await update.message.reply_text(f"👥 Total Users: {len(users)}")
        return

    elif text == "👨‍💻 Developer":
        await update.message.reply_text("👨‍💻 Developer: @Dino11142")
        return

    elif text == "ℹ️ Help":
        await update.message.reply_text("Send number to get info 📱")
        return

    # 📢 BROADCAST
    if text == "/broadcast" and user_id == ADMIN_ID:
        await update.message.reply_text("📢 Send message to broadcast:")
        context.user_data["broadcast"] = True
        return

    if context.user_data.get("broadcast"):
        context.user_data["broadcast"] = False
        count = 0
        for user in users:
            try:
                await context.bot.send_message(chat_id=user, text=text)
                count += 1
            except:
                pass
        await update.message.reply_text(f"✅ Sent to {count} users")
        return

    # 🔍 NUMBER SEARCH
    if context.user_data.get("search"):
        context.user_data["search"] = False

        number = text
        url = f"https://yash-code-with-ai.alphamovies.workers.dev/?num={number}&key=7189814021"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                result = f"""
📊 RESULT

📱 Number: `{data.get('number', 'N/A')}`
👤 Name: `{data.get('name', 'N/A')}`
📶 Carrier: `{data.get('carrier', 'N/A')}`
📍 Location: `{data.get('location', 'N/A')}`
✅ Valid: `{data.get('valid', 'N/A')}`

━━━━━━━━━━━━━━━
Made by @T4HKR
DEVELOPER @Dino11142
Owner @XCWOM
"""
                await update.message.reply_text(result, parse_mode="Markdown")

            else:
                await update.message.reply_text("API Error ❌")

        except:
            await update.message.reply_text("Error ❌")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
