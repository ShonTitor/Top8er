from top8er_app.cached_functions import read_game_data, read_home_data, read_template_data
from top8er_app.generar.getsets import sgg_data
from .utils import graphic_from_request, response_from_json, is_url
from .generar.perro2 import generate_graphic

from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from io import BytesIO
from itertools import product

import base64
import json
import os
import requests

class salu2(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            img = graphic_from_request(request, request.POST['game'], hasextra=False, icon_sizes=(64, 32), default_bg="bg")
            return Response({
                "base64_img": img
                })
        except Exception as e:
            return Response({"jaja": "salu2", "error": str(e)}, status=500)
        
class api_game_data(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, game):
        if game in [g for _, g in settings.GAMES]:
            game_data = read_game_data(game)
            return Response(game_data)
        else:
            return Response({}, status=404)
        
class api_template_data(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, template):
        if template in settings.GRAPHIC_TEMPLATES:
            template_data = read_template_data(template)
            return Response(template_data)
        else:
            return Response({}, status=404)

class api_games(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(settings.GAMES)
        
class api_templates(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(settings.GRAPHIC_TEMPLATES)
    
class api_home_data(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        home_data = read_home_data()
        return Response(home_data)

class api_results(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        slug = request.GET.get("slug")
        slug = "tournament/gaita-gear/event/las-gaitas-de-strive"
        data = sgg_data(slug, "ggst")
        return Response(data)

class api_generate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, template, game):

        template_data = read_template_data(template, complete=True)
        game_data = read_game_data(game)

        if template_data is None or game_data is None:
            return Response({}, status=404)
        
        if type(request.data) is dict:
            request_data = request.data
        else:
            if "data" not in request.data:
                return Response("Content type must either be 'application/json' or include a 'data' key with json content", 
                                status=400)
            try:
                request_data = json.loads(request.data["data"])
            except Exception:
                return Response("Could not parse the value of the key 'data', must be json", status=400)
        
        player_fields = template_data["player_fields"]
        options = template_data["options"]
        player_number = template_data["player_number"]

        data = {
            "game": game,
            "template": template,
            "players": [{} for _ in range(player_number)],
            "options": {}
        }
        errors = []

        base_keys = ["players", "options"]

        for key in base_keys:
            if key in request_data:
                continue

            errors.append({
                "scope": "root",
                "field": key,
                "message": "This key is required"
            })

        if len(errors) > 0:
            return Response(errors, 400)
        
        for option in options:
            required = option.get("required", False)
            name = option["name"]
            value = request_data["options"].get(name)
            enable_image_uploading = option.get("enable_image_uploading", False)

            is_image = False
            if is_url(value) and option["type"] != "text":
                with requests.get(value, stream=True) as r:
                    request_size = int(r.headers['content-length'])
                if request_size > 10485760: # 10 MB
                    errors.append({
                        "scope": "player_fields",
                        "field": name,
                        "message": "Images must not be over 10 MB"
                    })
                is_image = True
            elif hasattr(value, "read"):
                is_image = True

            if is_image and not enable_image_uploading:
                errors.append({
                    "scope": "options",
                    "field": name,
                    "message": "Image uploading is not allowed for this field"
                })

            if required and value is None:
                errors.append({
                    "scope": "options",
                    "field": name,
                    "message": "This field is required"
                })
            
            if value is None and "default" in option:
                value = option["default"]
            
            if value is not None:
                data["options"][name] = value

        players = request_data.get("players")
        if len(players) != player_number:
            errors.append({
                "scope": "root",
                "field": "players",
                "message": f"Number of players doesn't match, must be {player_number}"
            })
        
        if len(errors) > 0:
            return Response(errors, 400)
        
        for player_field, i in product(player_fields, range(player_number)):
            field_type = player_field["type"]
            name = player_field["name"]
            value = players[i].get(name)
            enable_image_uploading = player_field.get("enable_image_uploading", False)
            multiple = player_field.get("multiple", False)
            if multiple:
                amount = player_field["amount"]
                if type(amount) is list:
                    amount = amount[i]
                else:
                    amount = amount

            if type(value) is list and len(value) == 2 and\
                type(value[0]) is str and type(value[1]) is int:
                    value = tuple(value)
            
            if type(value) is not list:
                value = [value]

            for k, element in enumerate(value):
                if type(element) is list and len(element) == 2 and\
                   type(element[0]) is str and type(element[1]) is int:
                    value[k] = tuple(value[k])

            if enable_image_uploading:
                if multiple:
                    file_key = ""
                    for j in range(amount):
                        file_key = f"player_{i}_{name}_{j}"
                        if file_key in request.FILES:
                            if len(value) < j+1:
                                value += [None for _ in range(j+1-len(value))]
                            value[j] = request.FILES[file_key]
                else:
                    file_key = f"player_{i}_{name}"
                    if file_key in request.FILES:
                        value = [request.FILES[file_key]]

            for v in value:
                is_image = False
                if is_url(v):
                    with requests.get(v, stream=True) as r:
                        request_size = int(r.headers['content-length'])
                    if request_size > 10485760: # 10 MB
                        errors.append({
                            "scope": "player_fields",
                            "field": name,
                            "message": "Images must not be over 10 MB"
                        })
                    is_image = True
                elif hasattr(v, "read"):
                    is_image = True

                if is_image and not enable_image_uploading:
                    errors.append({
                        "scope": "player_fields",
                        "field": name,
                        "message": "Image uploading is not allowed for this field"
                    })

            if multiple:
                required_many = player_field.get("required_many", [required for _ in range(amount)])
                for k in range(amount):
                    if (len(value) > k and value[k] is None and required_many[k]) or\
                       (len(value) <= k and required_many[k]):
                        errors.append({
                            "scope": "player_fields",
                            "field": name,
                            "message": f"{name} with index {k} is required"
                        })
            else:
                required = player_field.get("required", False)
                if required and value[0] is None:
                    errors.append({
                        "scope": "player_fields",
                        "field": name,
                        "message": "This field is required"
                    })

            if value[0] is None and "default" in player_field:
                default = player_field["default"]
                if multiple:
                    value = [default for _ in range(amount)]
                else:
                    value = [default]

            if field_type == "select":
                choices = player_field["options"]
                if choices == "flags":
                    choices = settings.FLAGS
                
                for v in value:
                    if v is not None and not v in choices\
                        and not(is_image and enable_image_uploading):
                        errors.append({
                            "scope": "player_fields",
                            "field": name,
                            "message": f"{v} is not a valid option, options are {choices}"
                        })
            
            elif field_type == "character":
                for j, char in enumerate(value):
                    if "image_types" in player_field:
                        image_types = player_field["image_types"]
                    else:
                        image_types = player_field["image_types_multiple"]

                    if type(char) is tuple:
                        if multiple:
                            image_type = image_types[i][j]
                        else:
                            image_type[i]
                        
                        if image_type == "icons":
                            icon_colors = game_data.get("iconColors", {})
                            if not game_data.get("hasIcons") or\
                               char[0] not in icon_colors:
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no icon image available for character {char[0]}"
                                })
                            if len(icon_colors.get(char[0], [None])) <= char[1]:
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no icon image available for {char[0]} with index {char[1]}"
                                })
                        elif image_type == "portraits":
                            characters = game_data.get("characters", [])
                            colors = game_data.get("colors", {})
                            if colors is None:
                                colors = {}
                            assert colors is not None
                            if char[0] not in characters:
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no portrait image available for character {char[0]}"
                                })
                            if len(colors.get(char[0], [None])) <= char[1]:
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no portrait image available for {char[0]} with index {char[1]}"
                                })
                        else:
                            char_path = os.path.join(settings.APP_BASE_DIR, "generar", "assets", game, char[0], f"{char[1]}.png")
                            if not os.path.exists(char_path):
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no {image_type} image available for {char[0]}"
                                })

            if not multiple:
                value = value[0]

            if value is not None:
                data["players"][i][name] = value
        
        if len(errors) > 0:
            return Response(errors, 400)
        img = generate_graphic(data)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        b64_img = base64.b64encode(buffered.getvalue())
        return Response({"base64_img": b64_img})

def response_from_game_path(game):
    return lambda x: response_from_json(x, game)

def react_view(request):
    return render(request, 'index.html')