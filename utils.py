import base64
from .generar.perro import generate_banner
from io import BytesIO

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