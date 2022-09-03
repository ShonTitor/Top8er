import base64
import json
import os
import re
from .generar.perro import generate_banner
from io import BytesIO
from io import BytesIO
from django.shortcuts import render
from .forms import makeform, SmashggForm
from .generar.getsets import event_data, challonge_data, tonamel_data

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
    datos = { "players" : players,
                "toptext" : request.POST["ttext"],
                "bottomtext" : request.POST["btext"],
                "url" : request.POST["url"],
                "game" : game,
                "logo": logo
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
           hasextra=True, color_guide=None, icon_sizes=(64, 32),
           default_bg="bg"):
    if hasextra : has_extra = "true"
    else : has_extra = "false"
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        form2 = SmashggForm(request.POST, request.FILES)
        v1 = form.is_valid()
        v2 = form2.is_valid()

        if v2 :
            event = request.POST["event"]
            patterns = [
                    # start gg
                    ("https://[www\.][smash]|[start].gg/tournament/[^/]+/event/[^/]+",
                     "tournament/[^/]+/event/[^/]+",
                     event_data, 0),
                     # challonge
                    ("https://challonge.com/[^/]+", ".com/[^/]+", challonge_data, 5),
                    # tonamel
                    ("https://tonamel.com/competition/[^/]+", ".com/competition/[^/]+", tonamel_data, 17),
                    ]
            for pattern, slug_pattern, data_function, offset in patterns:
                if re.search(pattern, event):
                    match = re.search(slug_pattern, event)
                    slug = match[0][offset:]
                    datos = data_function(slug)
            init_data = {}

            init_data["ttext"] = datos["toptext"]
            init_data["btext"] = datos["bottomtext"]
            init_data["url"] = datos["url"]

            for i in range(8) :
                try :
                    init_data["player"+str(i+1)] = {}
                    init_data["player"+str(i+1)]["name"] = datos["players"][i]["tag"]
                    init_data["player"+str(i+1)]["twitter"] = datos["players"][i]["twitter"]
                    init_data["player"+str(i+1)]["char"] = datos["players"][i]["char"][0]
                except :
                    pass
            
            context = { "hasextra" : has_extra,
                        "form" : FormClass(initial=init_data),
                        "form2" : SmashggForm(),
                        "off" : 2,
                        "color_guide" : color_guide,
                        "game" : game,
                        "result" : None
                      }
            return render(request, 'index.html' , context)
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

            context = { "hasextra" : has_extra,
                        "form" : FormClass(initial=init_data),
                        "form2" : SmashggForm(),
                        "off" : 2,
                        "color_guide" : color_guide,
                        "game" : game,
                        "result" : img,
                        "base_url" : request.get_host()
                      }
            return render(request, 'index.html' , context)

        else :
            context = {
               "hasextra" : has_extra,
               "color_guide" : color_guide,
               "game" : game,
               "result" : None
            }
            if "event" in request.POST :
                form = FormClass()
                context["off"] = 1
            else :
                form2 = SmashggForm()
                context["off"] = 2

            context["form"] = form
            context["form2"] = form2
    
            return render(request, 'index.html' , context)
            
            
    else :
        form = FormClass()
        form2 = SmashggForm()
    context = {
               "form" : form,
               "form2" : form2,
               "off" : 2,
               "hasextra" : has_extra,
               "color_guide" : color_guide,
               "game" : game,
               "result" : None,
               "base_url" : request.get_host()
               }
    return render(request, 'index.html' , context)

def game_data_from_json(game_path):
    base_path = os.path.realpath(__file__)
    base_path = os.path.abspath(os.path.join(base_path, os.pardir))
    data_path = os.path.join(base_path, "generar", "assets", game_path, "game.json")
    with open(data_path, "r") as f:
        game_data = json.loads(f.read())
    if game_data["colors"] is None:
        game_data["colors"] = {c:["Default"] for c in game_data["characters"]}
    if "iconColors" in game_data and game_data["iconColors"] is None:
        game_data["iconColors"] = {c:["Default"] for c in game_data["characters"]}
    else:
        game_data["iconColors"] = game_data["colors"]
    game_data["maxColors"] = max([len(colors) for colors in game_data["colors"].values()])
    game_data["maxIconColors"] = max([len(colors) for colors in game_data["iconColors"].values()])
    return game_data

def response_from_json(request, game_path):
    game_data = game_data_from_json(game_path)

    FormClass = makeform(chars=game_data["characters"],
                         numerito=game_data["maxColors"], 
                         numerito_extra=game_data["maxIconColors"],
                         hasextra=game_data["hasIcons"],
                         color1=game_data["defaultLayoutColors"][0],
                         color2=game_data["defaultLayoutColors"][1])
    return hestia(request, game_path, FormClass, hasextra=game_data["hasIcons"], color_guide=game_data["hasIcons"])