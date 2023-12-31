from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)

router = Router()


welcome_message = """
Hey! What's up?\n
Looking where to hang out?\n
I got you covered! Press the button below to find the best places.
"""


@router.message(Command("start"))
async def command_start(message: Message, bot: Bot, base_url: str):
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="See Venues", web_app=WebAppInfo(url=f"{base_url}")),
    )
    await message.answer(
        welcome_message,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="See Venue Listing", web_app=WebAppInfo(url=f"{base_url}")
                    )
                ]
            ]
        ),
    )
