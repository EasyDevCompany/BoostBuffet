from flask_admin.contrib.sqla import ModelView


class CardsView(ModelView):
    column_list = [
        "id",
        "username",
        "first_name",
        "surname",
        "raiting",
        "description",
        "first_tag",
        "second_tag",
        "aprroval_status",
        "role",
        "profesion",
    ]
