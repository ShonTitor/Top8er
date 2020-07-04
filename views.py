import os, base64
from io import BytesIO
from django.shortcuts import render, HttpResponse, loader
from .forms import GenForm
from .generar.perro import *

def index(request):
    if request.method == 'POST':
        form = GenForm(request.POST, request.FILES)
        if form.is_valid():
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
                        "url" : "https://riokaru.pythonanywhere.com/"
                    }
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
        form = GenForm()

    context = {"range" : list(range(1,9)),
               "raange" : list(range(8)),
               "chars" : ['Banjo & Kazooie', 'Bayonetta', 'Bowser', 'Bowser Jr', 'Byleth', 'Captain Falcon', 'Chrom', 'Cloud', 'Corrin', 'Daisy', 'Dark Pit', 'Dark Samus', 'Diddy Kong', 'Donkey Kong', 'Dr Mario', 'Duck Hunt', 'Falco', 'Fox', 'Ganondorf', 'Greninja', 'Hero', 'Ice Climbers', 'Ike', 'Incineroar', 'Inkling', 'Isabelle', 'Jigglypuff', 'Joker', 'Ken', 'King Dedede', 'King K Rool', 'Kirby', 'Link', 'Little Mac', 'Lucario', 'Lucas', 'Lucina', 'Luigi', 'Mario', 'Marth', 'Mega Man', 'Meta Knight', 'Mewtwo', 'Mii Brawler', 'Mii Gunner', 'Mii Swordfighter', 'Mr Game and Watch', 'Ness', 'Olimar', 'Pac-Man', 'Palutena', 'Peach', 'Pichu', 'Pikachu', 'Piranha Plant', 'Pit', 'Pokémon Trainer', 'Richter', 'Ridley', 'ROB', 'Robin', 'Rosalina and Luma', 'Roy', 'Ryu', 'Samus', 'Sheik', 'Shulk', 'Simon', 'Snake', 'Sonic', 'Terry', 'Toon Link', 'Villager', 'Wario', 'Wii Fit Trainer', 'Wolf', 'Yoshi', 'Young Link', 'Zelda', 'Zero Suit Samus'],
               "form" : form
               }
    return render(request, 'index.html' , context)
