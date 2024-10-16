
import logging
import random
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
from typing import Optional

# Set up logging for debugging and monitoring
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Admin usernames
ADMINS = ["AbdurehimK55", "MisterAbboud", "Ke34m"]

# Define your FAQ responses
FAQ_RESPONSES = {
    "📝እንዴት መመዝገብ ይቻላል?": (
        "ለመመዝገብ እባክዎን ለእርዳታ አስተዳዳሪውን (Admin) ያነጋግሩ: \n"
        "Ustaz Abdurahim(https://t.me/AbdurehimK55) \n"
        "Abdurahman(https://t.me/MisterAbboud) \n"
        "Eman(https://t.me/Ke34m)"
    ),
    "📅 የክፍል መርሃ ግብር?": (
        "ትምህርቶቻችን በየሳምንቱ \nሰኞ፣\nማክሰኞ፣\nእሮብ፣\nአርብ እና\n ቅዳሜ ከምሽቱ 2:30 ይጀምራል እና ከጥዋቱ 12:30 ይጀምራል።\n"
        "የእኛ የቁርአን ትምህርት ፕሮግራማችን እነዚህን ያካትታል፣\n"
        "✨ነዘር\n"
        "✨ተጅዊድ\n"
        "✨ሒፍዝ እና\n"
        "✨ቃዒደቱ-ን-ኑራኒያ"
    ),
    "💰 ክፍያዎች?": "የእኛ የቁርዓን ትምህርት ፕሮግራማችን የክፍያ መጠን በወር 400 ብር ነው።",
    "🕒 የኮርሱ ቆይታ?": "የኮርሱ ቆይታ ለ6 ወራት ነው።",
    "📞 ለበለጠ መረጃ?": (
        "ለበለጠ መረጃ በቴሌግራም Ustaz Abdurahim: (https://t.me/AbdurehimK55) ሊያገኙን ይችላሉ።"
    )
}

# Define Hadiths
HADITHS = [
    "حديث البخاري\n: قال النبي ﷺ: خيركم من تعلم القرآن وعلمه. \nነብዩ (ሶ.ዐ.ወ) እንዲህ ብለዋል፡- 🕋ከናንተ (ሙስሊሞች) በላጩ ቁርኣንን ተምረው ያስተማሩት ናቸው።🌙(ሳሂህ አል ቡኻሪ)",
    "حديث مسلم\n: قال النبي ﷺ: اقرأوا القرآن، فإنه يأتي يوم القيامة شفيعاً لأصحابه.”\nነብዩ (ሶ.ዐ.ወ) እንዲህ አሉ፡- * 🕌ቁርኣንን አንብብ በትንሣኤ ቀን ለአነባቢዎቹ አማላጅ ሆኖ ይመጣልና*⭐ (ሶሒህ ሙስሊም)",
    " حديث الترمذي\n: قال النبي ﷺ: من قرأ حرفاً من كتاب الله فله به حسنة، والحسنة بعشر أمثالها.”\nነብዩ (ሶ.ዐ.ወ) እንዲህ ብለዋል፡- *🌃ከአላህ ኪታብ የተጻፈ ደብዳቤ ያነበበ ሰው ምንዳ ያገኛል። ምንዳውም በአስር ይጨመርለታል።*🌟 (ቲርሚዚ)"
]

last_hadith_index = -1

# Helper function to check admin status
def is_admin(username: Optional[str]) -> bool:
    return username in ADMINS

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    global last_hadith_index
    user_name = update.effective_user.first_name
    greeting = f"االسَّلامُ عَلَيْكُم ورَحْمَةُ اللهِ وَبَرَكاتُهُه\n{user_name}!"

    last_hadith_index = (last_hadith_index + 1) % len(HADITHS)
    hadith = HADITHS[last_hadith_index]

    keyboard = [
        ["📝እንዴት መመዝገብ ይቻላል?", "📅 የክፍል መርሃ ግብር?"],
        ["💰 ክፍያዎች?", "🕒 የኮርሱ ቆይታ?"],
        ["📞 ለበለጠ መረጃ?"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text(f"{greeting}\n\n{hadith}\n\nእባክዎ ከታች ካለው አማራጭ ውስጥ ጥያቄ ይምረጡ፡፡", reply_markup=reply_markup)

# FAQ handler
async def faq_handler(update: Update, context: CallbackContext) -> None:
    question = update.message.text
    logger.info(f"Received FAQ request: {question} from {update.effective_user.username}")
    if question in FAQ_RESPONSES:
        response = FAQ_RESPONSES[question]
        await update.message.reply_text(response)

# Feedback handling
async def feedback_handler(update: Update, context: CallbackContext) -> None:
    if is_admin(update.effective_user.username):
        await update.message.reply_text("Please provide the feedback text to forward to all admins.")
        return

    feedback = update.message.text
    logger.info(f"Received feedback: {feedback} from {update.effective_user.username}")
    
    # Forward feedback to all admins
    for admin in ADMINS:
        try:
            await context.bot.send_message(chat_id=f"@{admin}", text=f"Feedback received from {update.effective_user.username}:\n\n{feedback}")
        except Exception as e:
            logger.error(f"Failed to forward feedback to {admin}: {e}")
    
    await update.message.reply_text("Thank you for your feedback! It has been forwarded to the admins.")

# Error handler
async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise EnvironmentError("TELEGRAM_BOT_TOKEN environment variable not set.")
    
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r"^📝እንዴት መመዝገብ ይቻላል\?$"), faq_handler))
    application.add_handler(MessageHandler(filters.Regex(r"^📅 የክፍል መርሃ ግብር\?$"), faq_handler))
    application.add_handler(MessageHandler(filters.Regex(r"^💰 ክፍያዎች\?$"), faq_handler))
    application.add_handler(MessageHandler(filters.Regex(r"^🕒 የኮርሱ ቆይታ\?$"), faq_handler))
    application.add_handler(MessageHandler(filters.Regex(r"^📞 ለበለጠ መረጃ\?$"), faq_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_handler))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
