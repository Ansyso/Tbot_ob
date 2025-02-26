import os
import sys
import logging
import asyncio

try:
    import bz2, gzip, lzma, zlib, marshal, base64
except ModuleNotFoundError:
    bz2 = __import__('bz2')
    gzip = __import__('gzip')
    lzma = __import__('lzma')
    zlib = __import__('zlib')
    marshal = __import__('marshal')
    base64 = __import__('base64')

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
    sys.exit("Error: TELEGRAM_BOT_TOKEN is not set in environment variables.")

# Obfuscation Function
def __obf_____(obj):
    ____ = "__import__('base64').a85encode(__import__('bz2').compress(__import__('lzma').compress(__import__('zlib').compress(__import__('gzip').compress(__import__('marshal').dumps(obj))))))"
    ___x_ = eval(____)
    return repr(___x_)

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the bot is started."""
    await update.message.reply_text("Hello! Send me a Python file to obfuscate.")

async def obfuscate(update: Update, context: CallbackContext) -> None:
    """Handles file uploads and obfuscates the Python code."""
    document = update.message.document

    if not document.file_name.endswith(".py"):
        await update.message.reply_text("Please send a valid Python file (.py).")
        return

    file = await document.get_file()
    file_path = f"/tmp/{document.file_name}"
    await file.download(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        _code = f.read()

    _lyr = 5  # Default layer, can be customized
    ___sec___ = f"""
if str(__import__('sys').version[0:4]) != '{str(__import__('sys').version[0:4])}':
    print("This code doesn't work in your Python version")
    print("Your version: ", str(__import__('sys').version[0:4]))
    print("You need to install Python {str(__import__('sys').version[0:4])}")
    __import__("sys").exit(2008)
if __Author__ != ('WGeorgeCode', 'Ansyso'):
    raise MemoryError('>> GOOD LUCK!! CONMEMAY') from None
"""

    for i in range(_lyr):
            _code = str(f"""__Author__ = ('WGeorgeCode', 'Ansyso')
{___sec___}
_pymeomeo = vars(globals()['__builtins__'])
try:_pymeomeo['exec'](_pymeomeo['__import__']('marshal').loads(_pymeomeo['__import__']('gzip').decompress(_pymeomeo['__import__']('zlib').decompress(_pymeomeo['__import__']('lzma').decompress(_pymeomeo['__import__']('bz2').decompress(_pymeomeo['__import__']('base64').a85decode(""") + str(__obf_____(_code))+""")))))))
except Exception as e:__import__('sys').exit(e)"""


    for i in range(_lyr * 2):
        _code = str(f"""__Author__ = ('WGeorgeCode', 'Ansyso')\n{___sec___}\n_pymeomeo = vars(globals()['__builtins__'])\ntry:_pymeomeo['exec'](_pymeomeo['__import__']('marshal').loads(_pymeomeo['__import__']('gzip').decompress(_pymeomeo['__import__']('zlib').decompress(_pymeomeo['__import__']('lzma').decompress(_pymeomeo['__import__']('bz2').decompress(_pymeomeo['__import__']('base64').a85decode({str(__obf_____(_code))}))))))))\nexcept Exception as e:__import__('sys').exit(e)""")

    output_path = file_path.replace(".py", "_obf.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(_code)

    await update.message.reply_document(document=open(output_path, "rb"))
    os.remove(file_path)
    os.remove(output_path)

def main():
    """Main function to run the bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PYTHON, obfuscate))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
