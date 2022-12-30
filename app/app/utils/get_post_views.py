import requests


def get_views(path):
    url = f"https://api.telegra.ph/getViews/{path}?year=2022"
    return requests.get(url).json().get("result").get("views")

