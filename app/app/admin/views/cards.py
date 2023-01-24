from flask_admin.contrib.sqla import ModelView


class CardsView(ModelView):
    column_list = [
        "id",
        "telegraph_url",
        "path",
        "title",
        "subtitle",
        "content",
        "category",
        "views_count",
        "comments_count",
        "likes_amount",
        "created_at",
        "card_id",
    ]
