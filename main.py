#!/usr/bin/env python3
"""
🌍 UNIVERSAL TRANSLATOR BOT
10+ tilda tarjima qiladi
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tarjima tillari
LANGUAGES = {
    "uz": "🇺🇿 O'zbekcha",
    "en": "🇺🇸 English",
    "ru": "🇷🇺 Русский",
    "tr": "🇹🇷 Türkçe",
    "ar": "🇸🇦 العربية",
    "fa": "🇮🇷 فارسی",
    "ko": "🇰🇷 한국어",
    "ja": "🇯🇵 日本語",
    "zh": "🇨🇳 中文",
    "hi": "🇮🇳 हिन्दी",
    "es": "🇪🇸 Español",
    "fr": "🇫🇷 Français",
    "de": "🇩🇪 Deutsch",
    "it": "🇮🇹 Italiano",
}

class TranslatorBot:
    def __init__(self):
        self.user_langs = {}  # {user_id: {"from": "uz", "to": "en"}}
    
    async def start(self, update: Update, context: CallbackContext):
        """Botni boshlash"""
        user = update.effective_user
        
        welcome = f"""
        🌍 *Assalomu alaykum {user.first_name}!*
        
🤖 *Men Universal Tarjimon Botman*
        
✅ *10+ tilda tarjima:*
🇺🇿 O'zbekcha   🇺🇸 English
🇷🇺 Русский     🇹🇷 Türkçe
🇸🇦 العربية     🇮🇷 فارسی
🇰🇷 한국어       🇯🇵 日本語
🇨🇳 中文        🇮🇳 हिन्दी
🇪🇸 Español    🇫🇷 Français
        
📝 *Foydalanish:*
1. /lang - Tilni tanlash
2. Matn yuboring
3. Tarjima oling
        
        *Yaratuvchi:* @YourUsername
        """
        
        keyboard = [
            [InlineKeyboardButton("🌍 Tilni tanlash", callback_data="choose_lang")],
            [InlineKeyboardButton("ℹ️ Yordam", callback_data="help")],
            [InlineKeyboardButton("⚙️ Sozlamalar", callback_data="settings")]
        ]
        
        await update.message.reply_text(
            welcome,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
        # Foydalanuvchi ma'lumotini saqlash
        user_id = user.id
        if user_id not in self.user_langs:
            self.user_langs[user_id] = {"from": "auto", "to": "uz"}
    
    async def choose_language(self, update: Update, context: CallbackContext):
        """Til tanlash"""
        query = update.callback_query
        await query.answer()
        
        keyboard = []
        row = []
        
        for i, (code, name) in enumerate(LANGUAGES.items()):
            row.append(InlineKeyboardButton(name, callback_data=f"set_from_{code}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        
        keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back")])
        
        await query.edit_message_text(
            "📝 *Qaysi tildan tarjima qilmoqchisiz?*\n\n"
            "Manba tilni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def set_from_lang(self, update: Update, context: CallbackContext):
        """Manba tilini o'rnatish"""
        query = update.callback_query
        await query.answer()
        
        lang_code = query.data.replace("set_from_", "")
        user_id = query.from_user.id
        
        self.user_langs[user_id]["from"] = lang_code
        
        # Qaysi tilga tarjima qilish
        keyboard = []
        row = []
        
        for code, name in LANGUAGES.items():
            if code != lang_code:  # O'ziga tarjima qilishni oldini olish
                row.append(InlineKeyboardButton(name, callback_data=f"set_to_{code}"))
                if len(row) == 2:
                    keyboard.append(row)
                    row = []
        
        keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="choose_lang")])
        
        await query.edit_message_text(
            f"✅ *Manba tili:* {LANGUAGES[lang_code]}\n\n"
            "📝 *Qaysi tilga tarjima qilmoqchisiz?*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def set_to_lang(self, update: Update, context: CallbackContext):
        """Nishon tilini o'rnatish"""
        query = update.callback_query
        await query.answer()
        
        lang_code = query.data.replace("set_to_", "")
        user_id = query.from_user.id
        
        self.user_langs[user_id]["to"] = lang_code
        from_lang = self.user_langs[user_id]["from"]
        
        await query.edit_message_text(
            f"✅ *Sozlamalar saqlandi!*\n\n"
            f"🔤 *Manba:* {LANGUAGES[from_lang]}\n"
            f"🎯 *Nishon:* {LANGUAGES[lang_code]}\n\n"
            "📝 Endi tarjima qilish uchun matn yuboring!",
            parse_mode='Markdown'
        )
    
    async def translate_text(self, update: Update, context: CallbackContext):
        """Matnni tarjima qilish"""
        user_id = update.effective_user.id
        text = update.message.text
        
        if user_id not in self.user_langs:
            await update.message.reply_text("❌ Iltimos, avval /start bosing!")
            return
        
        if len(text) > 4000:
            await update.message.reply_text("❌ Matn 4000 belgidan oshmasligi kerak!")
            return
        
        # Foydalanuvchi til sozlamalari
        from_lang = self.user_langs[user_id]["from"]
        to_lang = self.user_langs[user_id]["to"]
        
        # Tarjima qilish (simulyatsiya)
        await update.message.chat.send_action(action="typing")
        
        translated = await self._simulate_translation(text, from_lang, to_lang)
        
        # Natijani yuborish
        result = f"""
🔤 *Tarjima natijasi:*

📝 *Asl matn:* ({LANGUAGES.get(from_lang, 'Auto')})
{text[:500]}{'...' if len(text) > 500 else ''}

🔄 *Tarjima:* ({LANGUAGES.get(to_lang, 'Unknown')})
{translated}

📊 *Statistika:*
• Belgilar: {len(text)} → {len(translated)}
• So'zlar: {len(text.split())} → {len(translated.split())}

🔗 *Tillar:* {LANGUAGES.get(from_lang, 'Auto')} → {LANGUAGES.get(to_lang, 'Unknown')}
        """
        
        await update.message.reply_text(result, parse_mode='Markdown')
    
    async def _simulate_translation(self, text: str, from_lang: str, to_lang: str) -> str:
        """Tarjima simulyatsiyasi"""
        # Real loyihada Google Translate API yoki boshqa xizmat ishlatiladi
        translations = {
            "uz": "Bu o'zbekcha matnning tarjimasidir.",
            "en": "This is a translation of the text.",
            "ru": "Это перевод текста.",
            "tr": "Bu, metnin çevirisidir.",
            "ar": "هذه ترجمة النص.",
            "fa": "این ترجمه متن است.",
            "ko": "이것은 텍스트 번역입니다.",
            "ja": "これはテキストの翻訳です。",
            "zh": "这是文本的翻译。",
            "hi": "यह पाठ का अनुवाद है।",
            "es": "Esta es una traducción del texto.",
            "fr": "Ceci est une traduction du texte.",
            "de": "Dies ist eine Übersetzung des Textes.",
            "it": "Questa è una traduzione del testo.",
        }
        
        return translations.get(to_lang, f"Tarjima: {text[:200]}...") + f"\n\n[⚠️ Demo rejim: Real tarjima uchun API kalit qo'shing]"
    
    async def help_command(self, update: Update, context: CallbackContext):
        """Yordam"""
        help_text = """
        🌍 *Universal Tarjimon Bot - Yordam*
        
        📋 *Buyruqlar:*
        /start - Botni boshlash
        /lang - Tilni o'zgartirish
        /help - Yordam
        /about - Bot haqida
        
        📝 *Foydalanish:*
        1. Avval /lang buyrug'i bilan tillarni tanlang
        2. Matn yuboring
        3. Tarjimani oling
        
        🌐 *Qo'llab-quvvatlanadigan tillar:*
        • O'zbekcha 🇺🇿
        • English 🇺🇸
        • Русский 🇷🇺
        • Türkçe 🇹🇷
        • العربية 🇸🇦
        • فارسی 🇮🇷
        • 한국어 🇰🇷
        • 日本語 🇯🇵
        • 中文 🇨🇳
        • हिन्दी 🇮🇳
        • Español 🇪🇸
        • Français 🇫🇷
        
        ⚡ *Limitlar:*
        • Bir martada 4000 belgi
        • Cheksiz tarjimalar
        
        👨💻 *Yaratuvchi:* @isoqov_co
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def about_command(self, update: Update, context: CallbackContext):
        """Bot haqida"""
        about_text = """
        🤖 *Universal Tarjimon Bot*
        
        *Version:* 1.0.0
        *Yaratilgan:* 2024
        *Platforma:* Telegram Bot API
        
        *Texnologiyalar:*
        • Python 3.10+
        • python-telegram-bot
        • Async/await
        
        *Imkoniyatlar:*
        • 10+ tilda tarjima
        • Tezkor ishlash
        • Oson interfeys
        • Real vaqtda
        
        *Rejalashtirilgan:*
        • Ovozli tarjima
        • Rasmdan matn
        • Chat tarjimasi
        
        *👨💻 Yaratuvchi:* @isoqov_co
        *📧 Bog'lanish:* your.email@example.com
        
        *💝 Agar bot yoqsa, do'stlaringizga ulashing!*
        """
        
        await update.message.reply_text(about_text, parse_mode='Markdown')

def main():
    """Botni ishga tushirish"""
    # Token ni tekshirish
    if TOKEN == "8566384804:AAFpCbo92jD2FOC5t9GqJm2dqPpDmF4Bcg0":
        print("❌ ERROR: Bot tokenini kiriting!")
        print("1. @BotFather ga boring")
        print("2. Yangi bot yarating")
        print("3. Token ni TOKEN o'zgaruvchisiga yozing")
        return
    
    # Botni yaratish
    bot = TranslatorBot()
    application = Application.builder().token(TOKEN).build()
    
    # Handlerlar
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("lang", bot.choose_language))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("about", bot.about_command))
    
    # Callback handlerlar
    application.add_handler(CallbackQueryHandler(bot.choose_language, pattern="choose_lang"))
    application.add_handler(CallbackQueryHandler(bot.set_from_lang, pattern="^set_from_"))
    application.add_handler(CallbackQueryHandler(bot.set_to_lang, pattern="^set_to_"))
    application.add_handler(CallbackQueryHandler(bot.start, pattern="back"))
    
    # Matn handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.translate_text))
    
    # Botni ishga tushirish
    print("🤖 Bot ishga tushmoqda...")
    print("🌍 Universal Tarjimon Bot")
    print("👨💻 Yaratuvchi: @isoqov_co")
    
    application.run_polling()

if __name__ == '__main__':
    main()
