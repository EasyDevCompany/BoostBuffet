from flask_admin.contrib.sqla import ModelView


class MoovePostsView(ModelView):
    column_list = [
        "id",
        "title",
        "snippet",
        "post_url",
        "image_url",
        "created_at",
        "category",
    ]
