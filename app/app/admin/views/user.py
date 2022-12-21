from flask_admin.contrib.sqla import ModelView


class TelegramUserView(ModelView):
    column_list = [
        "id",
        "telegram_id",
        "username",
        "registration_date",
        "type",
        "raiting",
        "likes_amount",
    ]


class TelegramUserTokenView(ModelView):
    column_list = [
        "id",
        "user_id",
        "created_at",
    ]