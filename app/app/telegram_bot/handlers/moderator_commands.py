from aiogram import types
from uuid import uuid4

from dependency_injector.wiring import inject, Provide

from app.core.config import settings

from app.telegram_bot.loader import bot, dp

from app.core.containers import Container, TelegramUser, Posts, Cards
from app.db.session import scope
from app.telegram_bot.keyboards.moderator_keyboards import get_post_approve_buttons, get_card_approve_buttons



@dp.message_handler(commands=["post_to_approve"], state="*")
@inject
async def process_start_command(
        message: types.Message,
        rep_telegram_user = Provide[Container.repository_telegram_user],
        repository_posts = Provide[Container.repository_posts]):
    scope.set(str(uuid4))
    user = rep_telegram_user.get(telegram_id=int(message.from_user.id))
    if user and user.role == TelegramUser.UserRole.moderator:
        most_outdated_post = repository_posts.most_outdated_post()
        if most_outdated_post:
            await message.answer(most_outdated_post.telegraph_url, reply_markup=get_post_approve_buttons(post_id=most_outdated_post.id))
        else:
            await message.answer("Все посты проверены")
    else:
        await message.answer("У вас нет прав для данной команды.")


@dp.callback_query_handler(lambda c: "postapprove_" in c.data)
@dp.callback_query_handler(lambda c: "postnotapprove_" in c.data)
@inject
async def save_user(
        callback_query: types.CallbackQuery,
        repository_posts = Provide[Container.repository_posts],
        cards_service = Provide[Container.cards_service]):
    user_info = callback_query.data.split("_")
    if user_info[0] == "postapprove":
        post = repository_posts.get(id=user_info[1])
        repository_posts.update(
            db_obj=post,
            obj_in={
                "status": Posts.PostStatus.published
            }
        )
        await callback_query.message.delete()
        await callback_query.message.answer("Статус обновлён на опубликованный")

        await cards_service.add_raiting(user_id=post.author.id, moderator_id=callback_query.from_user.id, raiting=2_000)

        message = await bot.send_message(
            settings.CHANNEL_POSTS,
            f'<b>{post.title}</b> \n{post.subtitle} \nАвтор: @{post.author.username} \n{post.telegraph_url}',
            parse_mode='HTML'
        )
        await bot.send_message(
            post.author.telegram_id,
            'Ваш пост опубликован в канале',
            parse_mode='HTML'
        )
        await bot.forward_message(
            chat_id=post.author.telegram_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
    else:
        post = repository_posts.get(id=user_info[1])
        repository_posts.update(
            db_obj=post,
            obj_in={
                "status": Posts.PostStatus.not_approved
            }
        )

        await callback_query.message.delete()
        await callback_query.message.answer("Статус обновлён на не одобренный")
        await bot.send_message(
            post.author.telegram_id,
            f'Ваш пост {post.telegraph_url} не был одобрен модератором',
            parse_mode='HTML'
        )


@dp.message_handler(commands=["card_to_approve"], state="*")
@inject
async def process_start_command(
        message: types.Message,
        rep_telegram_user = Provide[Container.repository_telegram_user],
        reposotory_cards = Provide[Container.reposotory_cards]):
    scope.set(str(uuid4))
    user = rep_telegram_user.get(telegram_id=int(message.from_user.id))
    if user and user.role == TelegramUser.UserRole.moderator:
        most_outdated_card = reposotory_cards.most_outdated_card()
        if most_outdated_card:
            await message.answer(f"{settings.WEBAPP_URL}networking/{most_outdated_card.username}", reply_markup=get_card_approve_buttons(card_id=most_outdated_card.id))
        else:
            await message.answer("Все карты проверены")
    else:
        await message.answer("У вас нет прав для данной команды.")


@dp.callback_query_handler(lambda c: "cardapprove_" in c.data)
@dp.callback_query_handler(lambda c: "cardnotapprove_" in c.data)
@inject
async def save_user(
        callback_query: types.CallbackQuery,
        reposotory_cards = Provide[Container.reposotory_cards]):
    user_info = callback_query.data.split("_")
    if user_info[0] == "cardapprove":
        card = reposotory_cards.get(id=user_info[1])
        reposotory_cards.update(
            db_obj=card,
            obj_in={
                "aprroval_status": Cards.ApprovalStatus.approved
            }
        )
        await callback_query.message.delete()
        await callback_query.message.answer("Статус обновлён на опубликованный")
        await bot.send_message(
            card.author.telegram_id,
            'Ваш карточка одобрена!',
            parse_mode='HTML'
        )
    else:
        card = reposotory_cards.get(id=user_info[1])
        reposotory_cards.delete(db_obj=card, commit=True)
        await callback_query.message.delete()
        await callback_query.message.answer("Статус обновлён на не одобренный")
        await bot.send_message(
            card.author.telegram_id,
            f'Ваш карточка не была одобрена модератором',
            parse_mode='HTML'
        )
