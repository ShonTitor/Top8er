from django.test import TestCase
from django.test import Client
from django.test import tag

from django.conf import settings

from bs4 import BeautifulSoup
from parameterized import parameterized

import os
import json
import random

def random_hex_rgb():
    s = "#"
    A = [str(i) for i in range(10)]
    A += ["A", "B", "C", "D", "E", "F"]
    for _ in range(6):
        s += random.choice(A)
    return s

class Top8erTests(TestCase):

    @parameterized.expand([slug for slug, _ in settings.GAMES])
    def test_get(self, slug):
        c = Client()
        r = c.get(f"/{slug}")
        assert r.status_code == 200

    @parameterized.expand(settings.GAMES)
    def test_post(self, slug, game):
        base_path = os.path.realpath(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.pardir))
        game_path = os.path.join(base_path, "generar", "assets", game)
        data_path = os.path.join(game_path, "game.json")

        assert os.path.exists(data_path)

        with open(data_path, "r") as f:
            game_data = f.read()
        
        game_data = json.loads(game_data)

        missing = []
        for char in game_data["characters"]:
            if game_data.get("colors") is None or not char in game_data["colors"]:
                N = 1
            else:
                N = len(game_data["colors"][char])

            for i in range(N):
                path = os.path.join(game_path, "portraits", char, f"{i}.png")
                if not os.path.exists(path):
                    missing.append(path)
        
        if game_data["hasIcons"]:
            colors = None
            if "iconColors" in game_data and game_data["iconColors"]:
                colors = game_data["iconColors"]
            elif game_data["colors"]:
                colors = game_data["colors"]
            
            if colors is None:
                chars = game_data["characters"]
            else:
                chars = list(colors.keys())
            
            for char in chars:
                if colors is None:
                    N = 1
                else:
                    N = len(colors[char])
                for i in range(N):
                    path = os.path.join(game_path, "icons", char, f"{i}.png")
                    if not os.path.exists(path):
                        missing.append(path)

        for m in missing:
            print("\nMissing file: ", m)

        self.assertTrue(len(missing) == 0)

        data = {
                "game": game,
                "lcolor1": random_hex_rgb(),
                "lcolor2": random_hex_rgb(),
                "ttext": "Top Text goes here",
                "btext": "Bottom Text goes here",
                "url": "top8er.com",
                "fontt": "auto",
                "fcolor1": random_hex_rgb(),
                "fscolor1": random_hex_rgb(),
                "fcolor2": random_hex_rgb(),
                "fscolor2": random_hex_rgb(),
                "blacksquares": True
        }

        for i in range(1,9):
            data[f"player{i}_name"] = f"Player{i}"
            data[f"player{i}_twitter"] = f"player{i}"

            char = random.choice(game_data["characters"])
            data[f"player{i}_char"] = char
            if game_data.get("colors") is None or not char in game_data["colors"]:
                data[f"player{i}_color"] = 0
            else:
                data[f"player{i}_color"] = random.randint(0, len(game_data["colors"][char])-1)
            

            data[f"player{i}_flag"] = "None"

            data[f"player{i}_extra1"] = "None"
            data[f"player{i}_extra2"] = "None"

        c = Client()
        r = c.post(f"/{slug}", data)

        assert r.status_code == 200

        soup = BeautifulSoup(r.content, 'html.parser')
        result_h1 = soup.find(id="result")

        self.assertIsNotNone(result_h1)


class Top8erAPITests(TestCase):

    @parameterized.expand([game for _, game in settings.GAMES])
    @tag("api")
    def test_game_data(self, game):
        c = Client()
        r = c.get(f"/api/game_data/{game}/")
        self.assertEqual(r.status_code, 200)

    @parameterized.expand(settings.GRAPHIC_TEMPLATES)
    @tag("api")
    def test_template_data(self, template):
        c = Client()
        r = c.get(f"/api/template_data/{template}/")
        self.assertEqual(r.status_code, 200)

    @tag("api")
    def test_games(self):
        c = Client()
        r = c.get(f"/api/games/")
        self.assertEqual(r.status_code, 200)

    @tag("api")
    def test_templates(self):
        c = Client()
        r = c.get(f"/api/templates/")
        self.assertEqual(r.status_code, 200)
    
    @tag("api")
    def test_generate(self):
        
        template = "top1er"
        game = "kf2"
        data = {
            "players": [{
                "name": "Riokaru",
                "character": [("Meta Knight", 0), None, None]
            }],
            "options": {
            }
        }
        c = Client()
        r = c.post(f"/api/generate/{template}/{game}/", data, content_type='application/json')
        self.assertEqual(r.status_code, 200)