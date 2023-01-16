from aiogram import types
from uuid import uuid4

from dependency_injector.wiring import inject, Provide

from app.core.config import settings

from app.telegram_bot.loader import bot, dp

from app.core.containers import Container, TelegramUser, Posts
from app.db.session import scope
from app.telegram_bot.keyboards.moderator_keyboards import get_approve_buttons



@dp.message_handler(commands=["to_approve"], state="*")
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
            await message.answer(most_outdated_post.telegraph_url, reply_markup=get_approve_buttons(post_id=most_outdated_post.id))
        else:
            await message.answer("Все посты проверены")
    else:
        await message.answer("У вас нет прав для данной команды.")


@dp.callback_query_handler(lambda c: "approve_" in c.data)
@dp.callback_query_handler(lambda c: "notapprove_" in c.data)
@inject
async def save_user(
        callback_query: types.CallbackQuery,
        repository_posts = Provide[Container.repository_posts]):
    user_info = callback_query.data.split("_")
    if user_info[0] == "approve":
        post = repository_posts.get(id=user_info[1])
        repository_posts.update(
            db_obj=post,
            obj_in={
                "status": Posts.PostStatus.published
            }
        )
        await callback_query.message.delete()
        await callback_query.message.answer("Статус обновлён на опубликованный")
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