from aiogram import types


def get_approve_buttons(post_id: str):
    keyboard = types.InlineKeyboardMarkup()
    approve = types.InlineKeyboardButton(
        text="Одобрить",
        callback_data=f"approve_{post_id}"
    )
    not_approve = types.InlineKeyboardButton(
        text="Не одобрить",
        callback_data=f"notapprove_{post_id}"
    )
    keyboard.add(approve)
    keyboard.add(not_approve)
    return keyboard
