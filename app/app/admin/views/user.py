from flask_admin.contrib.sqla import ModelView


class TelegramUserView(ModelView):
    column_list = [
        "id",
        "telegram_id",
        "telegraph_access_token",
        "username",
        "first_name",
        "surname",
        "registration_date",
        "type",
        "raiting",
        "likes_amount",
        "followings",
        "role",
    ]


class FollowRelationView(ModelView):
    column_list = [
        "id",
        "FollowerID",
        "FollowingID",
    ]
