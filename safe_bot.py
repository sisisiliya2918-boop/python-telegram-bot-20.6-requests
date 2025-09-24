from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN = 7784857432:AAE4OaI61C8UlGEU_xKsweqm3PsfZvsnD3Q

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! البوت شغال ✅")

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
