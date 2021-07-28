import os, base64, re
from io import BytesIO
from django.shortcuts import render, HttpResponse, loader
import requests
from .forms import makeform, SmashggForm
from .generar.perro import generate_banner
from .generar.getsets import event_data, challonge_data

def hestia(request, game, FormClass,
           hasextra=True, color_guide=None, icon_sizes=(64, 32)):
    if hasextra : has_extra = "true"
    else : has_extra = "false"
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        form2 = SmashggForm(request.POST, request.FILES)
        v1 = form.is_valid()
        v2 = form2.is_valid()

        if v2 :
            event = request.POST["event"]
            match = re.search("https://smash.gg/tournament/[^/]+/event/[^/]+", request.POST["event"])
            if match :
                datos = event_data(event[17:match.end()])
            else :
                match = re.search("https://challonge.com/[^/]+", request.POST["event"])
                datos = challonge_data(event[22:match.end()])
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
            for i in range(1,9) :
                names.append(request.POST["player"+str(i)+"_name"])
                flag = request.POST["player"+str(i)+"_flag"]
                flags.append(flag if flag != "None" else None)
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
                
            players = [{"tag" : names[j],
                        "char" : chars[j],
                        "twitter" : twitter[j],
                        "secondaries" : seconds[j],
                        "flag": flags[j]
                            }
                       for j in range(8)]
            datos = { "players" : players,
                        "toptext" : request.POST["ttext"],
                        "bottomtext" : request.POST["btext"],
                        "url" : request.POST["url"],
                        "game" : game,
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
                                    )
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img = base64.b64encode(buffered.getvalue())
            img = str(img)[2:-1]

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
                        "result" : img
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
               "result" : None
               }
    return render(request, 'index.html' , context)

def index(request) :
    FormClass = makeform()
    c_guide = "https://www.ssbwiki.com/Alternate_costume_(SSBU)"
    return hestia(request, "ssbu", FormClass, color_guide=c_guide)

def roa(request) :
    c = ["Random", "Absa", "Clairen", "Elliana", "Etalus",
         "Forsburn", "Kragg", "Maypul", "Orcane",
         "Ori and Sein", "Ranno", "Shovel Knight",
         "Sylvanos", "Wrastor", "Zetterburn"]
    FormClass = makeform(chars=c, numerito=21, numerito_extra=1,
                        color1="#B4A5E6", color2="#261C50")
    return hestia(request, "roa", FormClass)

def sg(request) :
    c = ['Annie', 'Beowulf', 'Big Band', 'Cerebella', 'Double', 'Eliza',
         'Filia', 'Fukua', 'Ms Fortune', 'Painwheel', 'Parasoul',
         'Peacock', 'Robo Fortune', 'Squigly', 'Valentine']
    FormClass = makeform(chars=c, numerito=30, numerito_extra=1,
                         color1="#FF544A", color2="#E6DEBB")
    c_guide = "https://wiki.gbl.gg/w/Skullgirls"
    return hestia(request, "sg", FormClass, color_guide=c_guide)

def rr(request) :
    c = ["Afi and Galu", "Ashani", "Ezzie", "Kidd",
         "Raymer", "Seth", "Urdah", "Weishan", "Zhurong"]
    FormClass = makeform(chars=c, numerito=1, numerito_extra=1,
                         color1="#384BCB", color2="#40EB8F")
    return hestia(request, "rr", FormClass, icon_sizes=(80,50))

def melee(request) :
    c = ['Bowser', 'Captain Falcon', 'Donkey Kong', 'Dr Mario', 'Falco',
         'Fox', 'Ganondorf', 'Ice Climbers', 'Jigglypuff', 'Kirby', 'Link',
         'Luigi', 'Mario', 'Marth', 'Mewtwo', 'Mr Game & Watch', 'Ness',
         'Peach', 'Pichu', 'Pikachu', 'Roy', 'Samus', 'Sheik', 'Yoshi',
         'Young Link', 'Zelda']
    FormClass = makeform(chars=c, numerito=6)
    c_guide = "https://www.ssbwiki.com/Alternate_costume_(SSBM)"
    return hestia(request, "melee", FormClass, icon_sizes=(48,24))

def ggxx(request) :
    c = ['A.B.A', 'Anji Mito', 'Axl Low', 'Baiken', 'Bridget', 'Chipp Zanuff',
         'Dizzy', 'Eddie', 'Faust', 'I-No', 'Jam Kuradoberi', 'Johnny',
         'Justice', 'Kliff Undersn', 'Ky Kiske', 'May', 'Millia Rage',
         'Order-Sol', 'Potemkin', 'Robo-Ky', 'Slayer', 'Sol Badguy',
         'Testament', 'Venom', 'Zappa']
    FormClass = makeform(chars=c, numerito=22, hasextra=False,
                         color1="#EF0020", color2="#16E7DE")
    c_guide = "https://www.dustloop.com/wiki/index.php?title=Guilty_Gear_XX_Accent_Core_Plus_R"
    return hestia(request, "ggxx", FormClass, color_guide=c_guide, hasextra=False)

def ggxrd(request) :
    c = ['Answer', 'Axl', 'Baiken', 'Bedman', 'Chipp', 'Dizzy', 'Elphelt', 'Faust', 'I-No', 
        'Jack-O', 'Jam', 'Johnny', 'Kum Haehyun', 'Ky', 'Leo', 'May', 'Millia', 'Potemkim', 
        'Ramlethal', 'Raven', 'Sin', 'Slayer', 'Sol', 'Venom', 'Zato'] 
    FormClass = makeform(chars=c, numerito=2, hasextra=False,
                         color1="#3a6446", color2="#09ed7a")
    return hestia(request, "ggxrd", FormClass, hasextra=False)

def ggst(request) :
    c = ['Anji', 'Axl', 'Chipp', 'Faust', 'Giovanna', 'Goldlewis', 
         'I-No', 'Ky', 'Leo', 'May', 'Millia',
         'Nagoriyuki', 'Potemkim', 'Ramlethal', 'Sol', 'Zato'] 
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#5e0a00", color2="#000000")
    return hestia(request, "ggst", FormClass, hasextra=False)

def uni(request) :
    c = ['Akatsuki', 'Byakuya', 'Carmine', 'Chaos', 'Eltnum', 'Enkidu',
         'Gordeau', 'Hilda', 'Hyde', 'Linne', 'Londrekia', 'Merkava',
         'Mika', 'Nanase', 'Orie', 'Phonon', 'Seth', 'Vatista', 'Wagner',
         'Waldstein', 'Yuzuriha']
    FormClass = makeform(chars=c, numerito=42, numerito_extra=1,
                         color1="#32145a", color2="#c814ff")
    c_guide = "https://wiki.gbl.gg/w/Under_Night_In-Birth/UNICLR"
    return hestia(request, "uni", FormClass, color_guide=c_guide)

def efz(request) :
    c = ['Akane', 'Akiko', 'Ayu', 'Doppel', 'Ikumi', 'Kanna', 'Kano',
         'Kaori', 'Mai', 'Makoto', 'Mayu', 'Minagi', 'Mio', 'Misaki',
         'Mishio', 'Misuzu', 'Mizuka', 'Nayuki (asleep)', 'Nayuki (awake)',
         'Rumi', 'Sayuri', 'Shiori', 'UNKNOWN']
    FormClass = makeform(chars=c, numerito=8, hasextra=False,
                         color1="#24358a", color2="#9dcae9",
                          efz=True)
    c_guide = "https://wiki.gbl.gg/w/Eternal_Fighter_Zero"
    return hestia(request, "efz", FormClass, color_guide=c_guide,
                  hasextra=False)

def mbaacc(request) :
    c = ['Akiha', 'Aoko', 'Arcueid', 'Ciel', 'Hime', 'Hisui',
         'Koha-Mech', 'Kohaku', 'Kouma', 'Len', 'Maids', 'Mech-Hisui',
         'Miyako', 'NAC', 'Nanaya', 'Neco-Arc', 'Neco-Mech', 'Nero',
         'Powerd Ciel', 'Red Arcueid', 'Riesbyfe', 'Roa', 'Ryougi',
         'Satsuki', 'Seifuku', 'Sion', 'Tohno', 'V.Akiha', 'V.Sion',
         'Warachia', 'White Len']
    ec = ["Crescent", "Full", "Half"]
    FormClass = makeform(chars=c, echars=ec, mb=True,
                         numerito=37, numerito_extra=1,
                         color1="#171a45", color2="#440206")
    c_guide = "https://wiki.gbl.gg/w/Melty_Blood/MBAACC"
    return hestia(request, "mbaacc", FormClass,
                  color_guide=c_guide, hasextra=True)

def soku(request) :
    c = ['alice', 'aya', 'cirno', 'iku', 'komachi', 'marisa', 'meiling',
         'patchouli', 'reimu', 'reisen', 'remilia', 'sakuya', 'sanae',
         'suika', 'suwako', 'tenshi', 'utsuho', 'youmu', 'yukari', 'yuyuko']
    FormClass = makeform(chars=c, numerito=1, color1='#28516a', color2='#51a3d5')
    return hestia(request, "soku", FormClass)

def slapcity(request) :
    c = ['Asha', 'Business Casual Man', 'Frallan', 'Goddess of Explosions', 'Ittle Dew',
         'Jenny Fox', 'Masked Ruby', 'Princess Remedy', 'Ultra Fishbunjin 3000']
    FormClass = makeform(chars=c, numerito=24, hasextra=False,
                         color1="#ff7100", color2='#25d0fb')
    c_guide = "https://slapwiki.com/SlapWiki/"
    return hestia(request, "slapcity", FormClass, color_guide=c_guide, hasextra=False)

def dfci(request) :
    c = ['Akira Yuki', 'Ako Tamaki', 'Asuna', 'Emi Yusa', 'Kirino Kousaka',
         'Kirito', 'Kuroko Shirai', 'Kuroyukihime', 'Mikoto Misaka',
         'Miyuki Shiba', 'Qwenthur Barbotage', 'Rentaro Satomi',
         'Selvaria Bles', 'Shana', 'Shizuo Heiwajima', 'Taiga Aisaka',
         'Tatsuya Shiba', 'Tomoka Minato', 'Yukina Himeragi', 'Yuuki Konno']
    ec = ['Accelerator', 'Alicia', 'Boogiepop', 'Celty', 'Dokuro', 'Enju',
             'Erio', 'Froleytia', 'Haruyuki', 'Holo', 'Innocent Charm',
             'Iriya', 'Izaya', 'Kino', 'Kojou', 'Kouko', 'Kuroneko',
             'Leafa', 'LLENN', 'Mashiro', 'Miyuki', 'Pai', 'Rusian',
             'Ryuuji', 'Sadao', 'Tatsuya', 'Tomo', 'Touma', 'Uiharu',
             'Wilhelmina', 'Zero']
    FormClass = makeform(chars=c, echars=ec, mb=True,
                         numerito=25, numerito_extra=1,
                         color1="#1919c8", color2="#c81919")
    c_guide = "https://wiki.gbl.gg/w/Dengeki_Bunko:_Fighting_Climax/DFCI"
    return hestia(request, "dfci", FormClass,
                  color_guide=c_guide, hasextra=True)

def tla(request) :
    c = ['Beef', 'Garlic', 'Noodle', 'Onion', 'Pork', 'Rice']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#753c7c", color2='#ea79f8')
    return hestia(request, "tla", FormClass, hasextra=False)

def svs(request) :
    c = ['Earth', 'Erile', 'Hiro', 'Hiro2', 'Jadou', 'Jadou2',
         'Krayce', 'Mayura', 'Orochimaru', 'Roze', 'Ryuken', 'Welles']
    FormClass = makeform(chars=c, numerito=6, hasextra=False,
                         color1="#233f91", color2='#e4c149')
    return hestia(request, "svs", FormClass, hasextra=False)

def sf3s(request) :
    c = ['Akuma', 'Alex', 'Chun-Li', 'Dudley', 'Elena', 'Hugo',
         'Ibuki', 'Ken', 'Makoto', 'Necro', 'Oro', 'Q', 'Remy', 'Ryu',
         'Sean', 'Twelve', 'Urien', 'Yang', 'Yun']
    FormClass = makeform(chars=c, numerito=14, hasextra=False,
                         color1="#c83c14", color2='#ef8f17')
    c_guide = "https://www.zytor.com/~johannax/jigsaw/sf/3s.html"
    return hestia(request, "3s", FormClass, hasextra=False,
                  color_guide=c_guide)

def sfst(request) :
    c = ['Blanka', 'Boxer', 'Cammy', 'Chun Li', 'Claw', 'Dee Jay',
         'Dhalsim', 'Dictator', 'E.Honda', 'Fei Long', 'Guile', 'Ken',
         'Ryu', 'Sagat', 'T.Hawk', 'Zangief']
    FormClass = makeform(chars=c, numerito=9, hasextra=False,
                         color1="#d214a0", color2="#d8d819")
    return hestia(request, "sfst", FormClass, hasextra=False)

def AsuraBuster(request) :
    c = ['Alice', 'Alice!', 'Chen-Mao', 'Goat', 'Leon', 'Nanami', 'Rokurouta', 
         'Rose Mary', 'Sittara', 'Taros', 'Yashaou', 'Zam-B', 'Zinsuke']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#ba2315", color2="#1f0141")
    return hestia(request, "AsuraBuster", FormClass, hasextra=False)

def kf2(request) :
    c = ['Archer', 'Artist', 'Bandana Dee', 'Beam', 'Beetle', 'Bell', 'Bomb', 
         'Cutter', 'Fighter', 'Gooey', 'Hammer', 'King Dedede', 'Magolor', 'Meta Knight', 
         'Ninja', 'Parasol', 'Staff', 'Sword', 'Water', 'Whip', 'Wrestler', 'Yo-yo']
    FormClass = makeform(chars=c, numerito=3, hasextra=True,
                         color1="#1f0141", color2="#ffff11")
    return hestia(request, "kf2", FormClass, hasextra=True)

def pplus(request) :
    c = ['Bowser', 'Captain Falcon', 'Charizard', 'Dedede', 'Diddy Kong', 'Donkey Kong', 
    'Falco', 'Fox', 'Ganondorf', 'Ice Climbers', 'Ike', 'Ivysaur', 'Jigglypuff', 'Kirby', 'Knuckles',
    'Link', 'Lucario', 'Lucas', 'Luigi', 'Mario', 'Marth', 'Meta Knight', 'Mewtwo', 
    'Mr. Game and Watch', 'Ness', 'Olimar', 'Peach', 'Pikachu', 'Pit', 'ROB', 'Roy', 'Samus', 
    'Sheik', 'Snake', 'Sonic', 'Squirtle', 'Toon Link', 'Wario', 'Wolf', 'Yoshi', 'Zelda', 
    'Zero Suit Samus']
    FormClass = makeform(chars=c, numerito=18, hasextra=True,
                         color1="#0c3e48", color2="#42dbac")
    return hestia(request, "p+", FormClass, hasextra=True)