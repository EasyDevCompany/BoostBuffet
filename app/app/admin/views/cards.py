from flask_admin.contrib.sqla import ModelView


class CardsView(ModelView):
    column_list = [
        "id",
        "username",
        "first_name",
        "surname",
        "raiting",
        "description",
        "bio",
        "aprroval_status",
        "role",
        "first_tag",
        "second_tag",
        "third_tag",
        "proffesion",
        "chat_open",
        "author_id",
    ]
