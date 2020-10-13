import os, base64, re
from io import BytesIO
from django.shortcuts import render, HttpResponse, loader
from .forms import makeform, SmashggForm
from .generar.perro import generate_banner
from .generar.getsets import event_data

def hestia(request, game, FormClass, hasextra=True):
    if hasextra : has_extra = "true"
    else : has_extra = "false"
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        form2 = SmashggForm(request.POST, request.FILES)
        v1 = form.is_valid()
        v2 = form2.is_valid()
        if v1 or v2 :
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
            try :                
                darkbg = request.POST["darken_bg"]
                if darkbg == "on" : darkbg = True
                else : darkbg = False
            except : darkbg = False
            if v2 :
                event = request.POST["event"]
                match = re.search("https://smash.gg/tournament/[^/]+/event/[^/]+", request.POST["event"])
                datos = event_data(event[17:match.end()])
            elif v1 :
                names = []
                twitter = []
                chars = []
                seconds = [[] for i in range(8)]
                for i in range(1,9) :
                    names.append(request.POST["name"+str(i)])
                    if request.POST["twitter"+str(i)] == "" :
                        twitter.append(None)
                    else :
                        twitter.append(request.POST["twitter"+str(i)])
                    chars.append( (request.POST["char"+str(i)],
                                   request.POST["color"+str(i)])
                                )
                    if hasextra :
                        for k in range(1,3) :
                            if request.POST["extra"+str(i)+str(k)] == "None" :
                                continue
                            else :
                                seconds[i-1].append((request.POST["extra"+str(i)+str(k)],
                                                   request.POST["extra_color"+str(i)+str(k)]))
                    
                players = [{"tag" : names[j],
                            "char" : chars[j],
                            "twitter" : twitter[j],
                            "secondaries" : seconds[j]
                                }
                           for j in range(8)]
                datos = { "players" : players,
                            "toptext" : request.POST["ttext"],
                            "bottomtext" : request.POST["btext"],
                            "url" : request.POST["url"],
                            "game" : game
                        }
            img = generate_banner(datos,
                                    customcolor= c1,
                                    customcolor2=c2,
                                    custombg=bg,
                                    darkenbg=darkbg
                                    )
            #img = base64.b64encode(img.tobytes())
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img = base64.b64encode(buffered.getvalue())
            img = str(img)[2:-1]
            context = { "img" : img }
            return render(request, 'gg.html' , context)

        else :
            context = { "hasextra" : has_extra }
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
               "hasextra" : has_extra
               }
    return render(request, 'index.html' , context)

def index(request) :
    FormClass = makeform()
    return hestia(request, "ssbu", FormClass)

def roa(request) :
    c = ["Absa", "Clairen", "Elliana", "Etalus",
         "Forsburn", "Kragg", "Maypul", "Orcane",
         "Ori and Sein", "Ranno", "Shovel Knight",
         "Sylvanos", "Wrastor", "Zetterburn"]
    FormClass = makeform(chars=c, numerito=21)
    return hestia(request, "roa", FormClass, hasextra=False)
