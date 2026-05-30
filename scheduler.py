from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
import db

async def send_expiry_notifications(bot: Bot):
    bookings = db.get_expiring_bookings(60)  # за час
    for booking in bookings:
        booking_id, user_id, product_name, expires_at = booking
        try:
            await bot.send_message(user_id, f"⚠️ *Напоминание!*\n\nВаша бронь на «{product_name}» истекает через час — в {expires_at[11:16]}.\nУспейте выкупить товар!", parse_mode="Markdown")
        except Exception as e:
            print(f"Не удалось отправить уведомление {user_id}: {e}")

def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_expiry_notifications, "interval", minutes=30, args=[bot])
    scheduler.start()
    return scheduler
