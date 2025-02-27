import os
import sys
import logging
import aiofiles
import base64
import bz2
import gzip
import lzma
import zlib
import marshal
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get Bot Token from Environment
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logger.error("Error: TELEGRAM_BOT_TOKEN is not set in environment variables.")
    sys.exit(1)

# Secure Obfuscation Function
def obfuscate_code(code: str, layers: int = 5) -> str:
    """Obfuscates Python code by applying multiple encoding layers."""
    security_check = """
if str(__import__('sys').version[0:4]) != '{py_version}':
    print("This code doesn't work in your Python version")
    print("Your version: ", str(__import__('sys').version[0:4]))
    print("You need to install Python {py_version}")
    __import__("sys").exit(2008)
if __Author__ != ('WGeorgeCode', 'Ansyso'):
    raise MemoryError('>> GOOD LUCK!! CONMEMAY') from None
""".format(py_version=str(sys.version[:4]))

    obfuscated = code
    for _ in range(layers):
        obfuscated = base64.a85encode(
            bz2.compress(
                lzma.compress(
                    zlib.compress(
                        gzip.compress(
                            marshal.dumps(obfuscated.encode())
                        )
                    )
                )
            )
        ).decode()

        obfuscated = f"""__Author__ = ('WGeorgeCode', 'Ansyso')
{security_check}
_py = vars(globals()['__builtins__'])
try:
    _py['exec'](_py['__import__']('marshal').loads(_py['__import__']('gzip').decompress(
    _py['__import__']('zlib').decompress(_py['__import__']('lzma').decompress(
    _py['__import__']('bz2').decompress(_py['__import__']('base64').a85decode("{obfuscated}"))))))))
except Exception as e:
    __import__('sys').exit(e)
"""

    return obfuscated

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the bot starts."""
    await update.message.reply_text("Hello! Send me a Python file to obfuscate.")

async def obfuscate(update: Update, context: CallbackContext) -> None:
    """Handles file uploads and obfuscates the Python code."""
    document = update.message.document

    if not document.file_name.endswith(".py"):
        await update.message.reply_text("Please send a valid Python file (.py).")
        return

    file = await document.get_file()
    file_path = f"/tmp/{document.file_name}"

    try:
        await file.download(file_path)

        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            original_code = await f.read()

        obfuscated_code = obfuscate_code(original_code)

        output_path = file_path.replace(".py", "_obf.py")
        async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
            await f.write(obfuscated_code)

        await update.message.reply_document(document=open(output_path, "rb"))

    except Exception as e:
        logger.error(f"Error obfuscating file: {e}")
        await update.message.reply_text("An error occurred while processing your file.")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)

def main():
    """Main function to run the bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.FILE_EXTENSION("py"), obfuscate))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
