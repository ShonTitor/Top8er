import base64
import json
import os
import re
from io import BytesIO
import traceback

from django.shortcuts import render

from top8er_app.cached_functions import game_data_from_json, read_home_data

from .forms import identify_slug, makeform, SmashggForm
from .generar.getsets import event_data, challonge_data, parrygg_data, sgg_data, tonamel_data
from .generar.perro import generate_banner

def graphic_from_request(request, game, hasextra=True, icon_sizes=(64, 32), default_bg="bg"):
    if request.POST["lcolor1"] == "#ff281a" :
        c1 = None
    else :
        c1 = request.POST["lcolor1"]
    if request.POST["lcolor2"] == "#ffb60c" :
        c2 = None
    else :
        c2 = request.POST["lcolor2"]
    if "background" not in request.FILES :
        bg = None
    else :
        bg = request.FILES["background"]

    # toggles
    darkbg = "darken_bg" in request.POST
    cshadow = "charshadow" in request.POST
    pr = "prmode" in request.POST
    blacksq = "blacksquares" in request.POST

    names = []
    twitter = []
    chars = []
    seconds = [[] for i in range(8)]
    flags = []
    custom_flags = []
    portraits = []
    for i in range(1,9) :
        names.append(request.POST["player"+str(i)+"_name"])
        flag = request.POST["player"+str(i)+"_flag"]
        flags.append(flag if flag != "None" else None)
        if  "player{}_portrait".format(i) in request.FILES :
            portraits.append(request.FILES["player{}_portrait".format(i)])
        else :
            portraits.append(None)
        if  "player{}_custom_flag".format(i) in request.FILES :
            custom_flags.append(request.FILES["player{}_custom_flag".format(i)])
        else :
            custom_flags.append(None)
        if request.POST["player"+str(i)+"_twitter"] == "" :
            twitter.append(None)
        else :
            twitter.append(request.POST["player"+str(i)+"_twitter"])
            
        if game == "efz" and "player"+str(i)+"_palette" in request.FILES :
            chars.append( (request.POST["player"+str(i)+"_char"],
                            request.FILES["player"+str(i)+"_palette"])
                        )
        else :
            chars.append( (request.POST["player"+str(i)+"_char"],
                            request.POST["player"+str(i)+"_color"])
                        )
        if hasextra :
            for k in range(1,3) :
                if request.POST["player"+str(i)+"_extra"+str(k)] == "None" :
                    continue
                else :
                    seconds[i-1].append((request.POST["player"+str(i)+"_extra"+str(k)],
                                        request.POST["player"+str(i)+"_extra_color"+str(k)]))

    if "logo" in request.FILES:
        logo = request.FILES["logo"]
    else:
        logo = None
        
    players = [{"tag" : names[j],
                "char" : chars[j],
                "twitter" : twitter[j],
                "secondaries" : seconds[j],
                "flag": flags[j],
                "custom_flag": custom_flags[j],
                "portrait": portraits[j]
                }
                for j in range(8)]
    
    # Process side event data
    side_event_title = request.POST.get("side_event_title", "").strip()
    side_event_players = []
    
    if side_event_title:
        for i in range(1, 9):
            side_player_name = request.POST.get(f"side_player{i}_name", "").strip()
            if side_player_name:
                side_player_char = request.POST.get(f"side_player{i}_char")
                side_player_color = request.POST.get(f"side_player{i}_color")
                side_player_twitter = request.POST.get(f"side_player{i}_twitter", "").strip()
                side_player_flag = request.POST.get(f"side_player{i}_flag")
                
                side_player_data = {
                    "tag": side_player_name,
                    "char": (side_player_char, side_player_color) if side_player_char else None,
                    "twitter": side_player_twitter if side_player_twitter else None,
                    "flag": side_player_flag if side_player_flag != "None" else None
                }
                
                # Handle custom flag
                if f"side_player{i}_custom_flag" in request.FILES:
                    side_player_data["custom_flag"] = request.FILES[f"side_player{i}_custom_flag"]
                else:
                    side_player_data["custom_flag"] = None
                
                # Handle portrait
                if f"side_player{i}_portrait" in request.FILES:
                    side_player_data["portrait"] = request.FILES[f"side_player{i}_portrait"]
                else:
                    side_player_data["portrait"] = None
                
                side_event_players.append(side_player_data)
    
    datos = { "players" : players,
                "toptext" : request.POST["ttext"],
                "bottomtext" : request.POST["btext"],
                "url" : request.POST["url"],
                "game" : game,
                "logo": logo,
                "side_event": {
                    "title": side_event_title,
                    "players": side_event_players
                } if side_event_title else None
            }

    fuente = request.POST["fontt"]
    if fuente == "auto" : 
        fuente = None
    if "font_file" in request.FILES :
        fuente = request.FILES["font_file"]
    
    img = generate_banner(datos,
                            customcolor= c1,
                            customcolor2=c2,
                            custombg=bg,
                            darkenbg=darkbg,
                            shadow=cshadow,
                            prmode=pr,
                            blacksquares=blacksq,
                            icon_sizes=icon_sizes,
                            font=fuente,
                            font_color1=request.POST["fcolor1"],
                            font_shadow1=request.POST["fscolor1"],
                            font_color2=request.POST["fcolor2"],
                            font_shadow2=request.POST["fscolor2"],
                            default_bg=default_bg
                            )
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img = base64.b64encode(buffered.getvalue())
    return str(img)[2:-1]

def hestia(request, game, FormClass,
           hasextra=True, color_guide=None, icon_sizes=(64, 32), color_dict=None,
           default_bg="bg"):
    
    # games_categories = [
    #     {
    #         'category_name': c,
    #         'games': [{'slug': game[0], 'path': game[1]} for game in settings.CATEGORIES[c]]
    #     }
    #     for c in settings.CATEGORIES_ORDER
    # ]
    games_categories = read_home_data()["categories"]

    if hasextra : has_extra = "true"
    else : has_extra = "false"
    
    if request.method == 'POST':
        if "event" in request.POST:
            form2 = SmashggForm(request.POST, request.FILES)
            v1 = False
            v2 = form2.is_valid()
        else:
            form = FormClass(request.POST, request.FILES)
            v1 = form.is_valid()
            v2 = False

        if v2 :
            url = request.POST["event"]

            data_functions = {
                "startgg": lambda x: sgg_data(x, game),
                "challonge": challonge_data,
                "tonamel": tonamel_data,
                "parrygg": parrygg_data
            }

            slug_type, slug = identify_slug(url)
            datos = data_functions.get(slug_type, lambda x: None)(slug)

            init_data = {}

            init_data["ttext"] = datos["toptext"]
            init_data["btext"] = datos["bottomtext"]
            init_data["url"] = datos["url"]

            for i in range(8) :
                try :
                    init_data["player"+str(i+1)] = {}
                    init_data["player"+str(i+1)]["name"] = datos["players"][i]["tag"]
                    init_data["player"+str(i+1)]["twitter"] = datos["players"][i].get("twitter", "")
                    init_data["player"+str(i+1)]["char"] = datos["players"][i].get("char", [None])[0]
                    init_data["player"+str(i+1)]["flag"] = datos["players"][i].get("flag", "None")
                except :
                    pass
            
            # Process side event link if provided
            side_event_url = request.POST.get("side_event_link", "").strip()
            if side_event_url:
                try:
                    side_slug_type, side_slug = identify_slug(side_event_url)
                    side_datos = data_functions.get(side_slug_type, lambda x: None)(side_slug)
                    
                    if side_datos and side_datos.get("players"):
                        init_data["side_event_title"] = side_datos.get("toptext", "Side Event")
                        
                        for i in range(min(8, len(side_datos["players"]))):
                            init_data["side_player"+str(i+1)] = {
                                "name": side_datos["players"][i]["tag"],
                                "twitter": side_datos["players"][i].get("twitter", ""),
                                "char": side_datos["players"][i].get("char", [None]),
                                "flag": side_datos["players"][i].get("flag", "None"),
                            }
                            if init_data["side_player"+str(i+1)]["char"] is not None:
                                init_data["side_player"+str(i+1)]["char"] = init_data["side_player"+str(i+1)]["char"][0]
                except Exception as ex:
                    print(f"Error loading side event data: {ex}")
                    traceback.print_exc()
                    pass
            
            context = { "hasextra" : has_extra,
                        "form" : FormClass(initial=init_data),
                        "form2" : SmashggForm(),
                        "off" : 2,
                        "color_guide" : color_guide,
                        "color_dict" : color_dict,
                        "game" : game,
                        "result" : None,
                        "games_categories": games_categories,
                      }
            return render(request, 'old_form.html' , context)
        if v1 :
            img = graphic_from_request(request, game, hasextra=hasextra, icon_sizes=icon_sizes, default_bg=default_bg)

            init_data = {}
            field_keys = filter(lambda k: not "player" in k and not "csrf" in k, request.POST.keys())
            for key in field_keys :
                init_data[key] = request.POST[key]
            check_field_keys = ["darken_bg", "blacksquares", "charshadow", "prmode"]
            for key in check_field_keys :
                init_data[key] = key in request.POST

            for i in range(1,9) :
                try :
                    init_data["player{}".format(i)] = {
                        "name": request.POST["player{}_name".format(i)],
                        "twitter": request.POST["player{}_twitter".format(i)],
                        "char": request.POST["player{}_char".format(i)],
                        "color": request.POST["player{}_color".format(i)],
                        "flag": request.POST["player{}_flag".format(i)],
                    }
                    for field in ["extra1", "extra_color1", "extra2", "extra_color2"] :
                        f = "player{}_{}".format(i, field)
                        if f in request.POST :
                            init_data["player{}".format(i)][field] = request.POST[f]
                            
                except :
                    pass

            # Preserve side event data
            for i in range(1, 9):
                try:
                    init_data["side_player{}".format(i)] = {
                        "name": request.POST.get("side_player{}_name".format(i), ""),
                        "twitter": request.POST.get("side_player{}_twitter".format(i), ""),
                        "char": request.POST.get("side_player{}_char".format(i), ""),
                        "color": request.POST.get("side_player{}_color".format(i), ""),
                        "flag": request.POST.get("side_player{}_flag".format(i), ""),
                    }
                    for field in ["extra1", "extra_color1", "extra2", "extra_color2"]:
                        f = "side_player{}_{}".format(i, field)
                        if f in request.POST:
                            init_data["side_player{}".format(i)][field] = request.POST[f]
                except:
                    pass

            context = { "hasextra" : has_extra,
                        "form" : FormClass(initial=init_data),
                        "form2" : SmashggForm(),
                        "off" : 2,
                        "color_guide" : color_guide,
                        "color_dict" : color_dict,
                        "game" : game,
                        "result" : img,
                        "base_url" : request.get_host(),
                        "games_categories": games_categories,
                      }
            return render(request, 'old_form.html' , context)

        else :
            context = {
               "hasextra" : has_extra,
               "color_guide" : color_guide,
               "color_dict" : color_dict,
               "game" : game,
               "result" : None,
               "games_categories": games_categories,
            }
            if "event" in request.POST :
                form = FormClass()
                context["off"] = 1
            else :
                form2 = SmashggForm()
                context["off"] = 2

            context["form"] = form
            context["form2"] = form2
    
            return render(request, 'old_form.html' , context)
            
            
    else :
        form = FormClass()
        form2 = SmashggForm()
    context = {
               "form" : form,
               "form2" : form2,
               "off" : 2,
               "hasextra" : has_extra,
               "color_guide" : color_guide,
               "color_dict" : color_dict,
               "game" : game,
               "result" : None,
               "base_url" : request.get_host(),
               "games_categories": games_categories,
               }
    return render(request, 'old_form.html' , context)

def response_from_json(request, game_path):
    game_data = game_data_from_json(game_path)
    iconColors = game_data.get("iconColors")
    FormClass = makeform(game=game_path,
                         chars=game_data["characters"],
                         echars=None if iconColors is None else list(iconColors.keys()),
                         numerito=game_data["maxColors"], 
                         numerito_extra=game_data["maxIconColors"],
                         hasextra=game_data["hasIcons"],
                         color1=game_data["defaultLayoutColors"][0],
                         color2=game_data["defaultLayoutColors"][1],
                         default_black_squares=game_data.get("blackSquares", True),
                         default_character_shadows=game_data.get("characterShadows", True))
    if iconColors:
        color_dict = iconColors.copy()
        color_dict.update(game_data["colors"])
    else:
        color_dict = game_data["colors"]
    color_dict = json.dumps({game_path: color_dict})[1:-1]
    return hestia(request, game_path, FormClass,
                  hasextra=game_data["hasIcons"], color_guide=game_data.get("colorGuide"),
                  color_dict=color_dict)

def is_url(string):
    if type(string) is not str:
        return False
    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    return re.match(url_pattern, string) is not None

