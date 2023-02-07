from flask_admin.contrib.sqla import ModelView


class PostsView(ModelView):
    column_list = [
        "id",
        "telegraph_url",
        "channel_link",
        "path",
        "title",
        "content",
        "status",
        "views_amount",
        "likes_amount",
        "raiting",
        "created_at",
        "author_id",
    ]
