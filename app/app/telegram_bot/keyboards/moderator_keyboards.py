from aiogram import types


def get_post_approve_buttons(post_id: str):
    keyboard = types.InlineKeyboardMarkup()
    approve = types.InlineKeyboardButton(
        text="Одобрить",
        callback_data=f"postapprove_{post_id}"
    )
    not_approve = types.InlineKeyboardButton(
        text="Не одобрить",
        callback_data=f"postnotapprove_{post_id}"
    )
    keyboard.add(approve)
    keyboard.add(not_approve)
    return keyboard


def get_card_approve_buttons(card_id: str):
    keyboard = types.InlineKeyboardMarkup()
    approve = types.InlineKeyboardButton(
        text="Одобрить",
        callback_data=f"cardapprove_{card_id}"
    )
    not_approve = types.InlineKeyboardButton(
        text="Не одобрить",
        callback_data=f"cardnotapprove_{card_id}"
    )
    keyboard.add(approve)
    keyboard.add(not_approve)
    return keyboard
