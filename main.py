import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from casino import SlotMachine, check_win
from database import init_db, get_user_balance, update_user_balance

load_dotenv()

# Инициализация базы данных
init_db()

# Константы игры
COST_PER_SPIN = 10
START_BALANCE = 1000

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    balance = get_user_balance(user.id)
    
    if balance is None:
        balance = START_BALANCE
        update_user_balance(user.id, balance)
    
    await update.message.reply_text(
        f"🎰 Добро пожаловать, {user.first_name}!\n"
        f"💰 Ваш баланс: {balance} монет\n\n"
        "Используйте команды:\n"
        "/spin - Крутить слоты (10 монет)\n"
        "/balance - Проверить баланс\n"
        "/addcoins - Пополнить баланс",
        reply_markup=spin_keyboard()
    )

def spin_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🎰 Крутить!", callback_data="spin")]])

async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)
    
    if balance < COST_PER_SPIN:
        await update.message.reply_text("❌ Недостаточно монет для игры!")
        return
    
    # Обновляем баланс
    new_balance = balance - COST_PER_SPIN
    update_user_balance(user_id, new_balance)
    
    # Генерируем результат
    slot = SlotMachine()
    result = slot.spin()
    win_amount = check_win(result)
    
    if win_amount > 0:
        new_balance += win_amount
        update_user_balance(user_id, new_balance)
        win_msg = f"🎉 Победа! +{win_amount} монет!"
    else:
        win_msg = "😢 Повезет в следующий раз!"
    
    # Форматируем результат слота
    slot_display = " | ".join(result)
    
    await update.message.reply_text(
        f"🔄 Результат: [ {slot_display} ]\n"
        f"{win_msg}\n"
        f"💰 Новый баланс: {new_balance} монет",
        reply_markup=spin_keyboard()
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)
    await update.message.reply_text(f"💰 Ваш баланс: {balance} монет")

async def add_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    update_user_balance(user_id, 1000, increment=True)
    await update.message.reply_text("✅ +1000 монет зачислены на счет!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "spin":
        await spin(update, context)

def main():
    app = Application.builder().token(os.getenv("TOKEN")).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spin", spin))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("addcoins", add_coins))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
