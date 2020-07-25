import os, base64, re
from io import BytesIO
from django.shortcuts import render, HttpResponse, loader
from .forms import GenForm, SmashggForm
from .generar.perro import generate_banner
from .generar.getsets import event_data

def index(request):
    if request.method == 'POST':
        form = GenForm(request.POST, request.FILES)
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
            if v2 :
                event = request.POST["event"]
                match = re.search("https://smash.gg/tournament/[^/]+/event/[^/]+", request.POST["event"])
                datos = event_data(event[17:match.end()])
            elif v1 :
                names = []
                twitter = []
                chars = []
                for i in range(1,9) :
                    names.append(request.POST["name"+str(i)])
                    if request.POST["twitter"+str(i)] == "" :
                        twitter.append(None)
                    else :
                        twitter.append(request.POST["twitter"+str(i)])
                    chars.append( (request.POST["char"+str(i)],
                                   request.POST["color"+str(i)])
                                )
                players = [{"tag" : names[j],
                            "char" : chars[j],
                            "twitter" : twitter[j]
                                }
                           for j in range(8)]
                datos = { "players" : players,
                            "toptext" : request.POST["ttext"],
                            "bottomtext" : request.POST["btext"],
                            "url" : request.POST["url"]
                        }
            img = generate_banner(datos,
                                    customcolor= c1,
                                    customcolor2=c2,
                                    custombg=bg
                                    )
            #img = base64.b64encode(img.tobytes())
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img = base64.b64encode(buffered.getvalue())
            img = str(img)[2:-1]
            context = { "img" : img }
            return render(request, 'gg.html' , context)

        else :
            context = {}
            if "event" in request.POST :
                form = GenForm()
                context["off"] = 1
            else :
                form2 = SmashggForm()
                context["off"] = 2

            context["form"] = form
            context["form2"] = form2
    
            return render(request, 'index.html' , context)
            
            
    else :
        form = GenForm()
        form2 = SmashggForm()
    context = {
               "form" : form,
               "form2" : form2,
               "off" : 2
               }
    return render(request, 'index.html' , context)
