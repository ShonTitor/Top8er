import json
import os
import requests

from django.conf import settings
from django.core.cache import cache

def read_game_data(game):
    if game not in [g for _, g in settings.GAMES]:
        return None

    game_data = cache.get(f"game_data_{game}")

    if game_data is None or settings.DEBUG:
        data_path = os.path.join(settings.APP_BASE_DIR, "generar", "assets", game, "game.json")

        with open(data_path, "r") as f:
            game_data = f.read()

        game_data = json.loads(game_data)
        cache.set(f"game_data_{game}", game_data, 60*60)

    return game_data

def read_template_data(template, complete=False):
    if template not in settings.GRAPHIC_TEMPLATES:
        return None
    
    template_data = cache.get(f"template_data_{template}")

    if template_data is None or settings.DEBUG:
        data_path = os.path.join(settings.APP_BASE_DIR, "generar", "templates", template, "template.json")

        with open(data_path, "r") as f:
            template_data = f.read()

        template_data = json.loads(template_data)
        cache.set(f"template_data_{template}", template_data, 60*60)

    if not complete:
        template_data.pop("layers")
    return template_data

def read_home_data():
    home_data = cache.get("home_data")
    if home_data is not None and not settings.DEBUG:
        return home_data
    
    home_data = {
        "templates": settings.GRAPHIC_TEMPLATES,
    }

    minmal_game_data = {}
    for slug, code in settings.GAMES:
        game_data = read_game_data(code)
        minmal_game_data[slug] = {
            "path": code,
            "full_name": game_data["name"],
            "slug": slug,
        }

    home_data["categories"] = [
        {
            "category_name": cat,
            "games": sorted([
                {
                    "slug": slug,
                    "path": path,
                    "full_name": minmal_game_data[slug]["full_name"]
                }
                for slug, path in games
            ], key=lambda x: x["full_name"])
        }
        for cat, games in settings.CATEGORIES.items()
    ]

    cache.set("home_data", home_data, 60*60)
    return home_data

def game_data_from_json(game_path):
    game_data = read_game_data(game_path)

    if game_data["colors"] is None:
        game_data["colors"] = {c:["Default"] for c in game_data["characters"]}
    if "iconColors" not in game_data or game_data["iconColors"] is None:
        game_data["iconColors"] = game_data["colors"] #{c:["Default"] for c in game_data["characters"]}

    game_data["maxColors"] = max([len(colors) for colors in game_data["colors"].values()])
    game_data["maxIconColors"] = max([len(colors) for colors in game_data["iconColors"].values()])
    if not "characterShadows" in game_data:
        game_data["characterShadows"] = True
    return game_data

def get_sgg_videogame_data():
    sgg_videogame_data = cache.get("sgg_videogame_data")
    if sgg_videogame_data:
        return sgg_videogame_data
    
    videogame_data = json.loads(requests.get(url="https://api.smash.gg/videogames").content)
    videogame_data = videogame_data["entities"]["videogame"]

    game_dict = {
        v["id"]:v["name"]
        for v in videogame_data
    }

    cache.set("sgg_videogame_data", game_dict, 60*60*24)

    return game_dict

def get_sgg_char_data():
    game_ids_dict = get_sgg_videogame_data()

    sgg_char_data = cache.get("sgg_char_data")
    if sgg_char_data:
        return sgg_char_data

    char_data = json.loads(requests.get(url="https://api.smash.gg/characters").content)
    char_data = char_data["entities"]["character"]

    char_dict = {
        key:{
            c["id"]:c["name"]
            for c in char_data
            if c["videogameId"] == key
        }
        for key in game_ids_dict
    }

    cache.set("sgg_char_data", char_dict, 60*60*24)

    return char_dict