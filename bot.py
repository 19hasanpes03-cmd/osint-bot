import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_message = (
        f"🔍 Merhaba {user_name}!\n\n"
        "**OSINT v5** aktif ve kullanıma hazır. 🚀\n\n"
        "📋 **Mevcut Modüller:**\n"
        "• IP Sorgulama\n"
        "• Telefon Numarası Analizi\n"
        "• Sosyal Medya Tarama\n"
        "• E-posta Sızıntı Kontrolü\n\n"
        "Komut listesini görmek için /help yazabilirsin."
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 **OSINT Bot Komutları:**\n\n"
        "/start - Botu başlatır ve durumu gösterir\n"
        "/ip <hedef_ip> - IP adresi hakkında bilgi toplar\n"
        "/username <kullanıcı_adı> - Sosyal medya taraması yapar"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def ip_sorgu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Lütfen bir IP adresi girin.\nÖrnek: `/ip 8.8.8.8`", parse_mode="Markdown")
        return
    
    ip = context.args[0]
    await update.message.reply_text(f"🔍 `{ip}` için açık kaynak taraması başlatıldı...", parse_mode="Markdown")

def main():
    TOKEN = "8868694224:AAHbIvLbb3CpuJzIX6wUgzmvUWSRjBUYMdA"

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ip", ip_sorgu))

    logger.info("Bot çalıştırılıyor...")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
