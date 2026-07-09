import json
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8978022005:AAFBLbQJpv80AlikfnGOKuVD0wJC_1YB7Zo"

ADMIN_ID = 8568921826

DB_FILE = "answers.json"


# ساخت دیتابیس اگر وجود نداشت
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False)


def load_answers():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_answers(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# اضافه کردن پاسخ
async def add_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text

    try:
        data = text.split(" ", 1)[1]
        word, answer = data.split("|", 1)

        word = word.strip().lower()
        answer = answer.strip()

        answers = load_answers()
        answers[word] = answer
        save_answers(answers)

        await update.message.reply_text(
            f"✅ ثبت شد:\n\nکلمه: {word}\nپاسخ: {answer}"
        )

    except:
        await update.message.reply_text(
            "فرمت درست:\n/add کلمه | جواب"
        )


# حذف پاسخ
async def delete_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:
        word = update.message.text.split(" ", 1)[1].strip().lower()

        answers = load_answers()

        if word in answers:
            del answers[word]
            save_answers(answers)

            await update.message.reply_text(
                f"🗑 حذف شد: {word}"
            )
        else:
            await update.message.reply_text(
                "این کلمه وجود ندارد."
            )

    except:
        await update.message.reply_text(
            "فرمت درست:\n/del کلمه"
        )


# لیست کلمات
async def list_answers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    answers = load_answers()

    if not answers:
        await update.message.reply_text(
            "لیست خالی است."
        )
        return

    result = "📚 کلمات ثبت شده:\n\n"

    for key in answers:
        result += f"• {key}\n"

    await update.message.reply_text(result)


# پاسخ خودکار
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = update.message.text.lower()

    answers = load_answers()

    for word, reply in answers.items():

        if word in text:
            await update.message.reply_text(reply)
            break



def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler("add", add_answer)
    )

    app.add_handler(
        CommandHandler("del", delete_answer)
    )

    app.add_handler(
        CommandHandler("list", list_answers)
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            auto_reply
        )
    )


    print("Bot Started...")
    app.run_polling()



if __name__ == "__main__":
    main()