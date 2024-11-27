import os
import subprocess

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a download link, and I'll fetch it for you!")

# Command to handle download links
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    link = message.strip()
    print(link)
    # Check if the message is a valid URL
    if not link.startswith("http://") and not link.startswith("https://"):
        await update.message.reply_text("Please send a valid URL.")
        return

    await update.message.reply_text("Downloading your file...")
    # Set up Aria2 command
    file_name = "downloaded_file"
    command = ["aria2c", "-o", file_name, link]

    try:
        subprocess.run(command, check=True)
        await update.message.reply_text("Download complete. Uploading the file...")
        
        # Send the file back to the user
        with open(file_name, "rb") as f:
            await update.message.reply_document(document=f)
        
        # Clean up the file
        os.remove(file_name)
    except Exception as e:
        await update.message.reply_text(f"Failed to download: {e}")

# Main function to set up the bot
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))

    app.run_polling()

if __name__ == "__main__":
    main()
