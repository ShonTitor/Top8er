from PIL import Image, ImageDraw, ImageFont
#from fontTools.ttLib import TTFont
#from fontTools.unicode import Unicode
import os

def draw_text(img, draw, pos, texto, font=None, fill=None,
              halo=True, shadow=True) :
    if shadow :
        #offset = int(font.size*0.06)
        offset = int((font.size**0.5)*0.55)
        draw.text((pos[0]+offset, pos[1]+offset), texto, font=font, fill=(0,0,0))
    draw.text(pos, texto, font=font, fill=fill)

def has_glyph(font, glyph):
    for table in font['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False

"""
def best_font(text) :
    f1 = os.path.join('fonts','DFGothic-SU-WING-RKSJ-H-03.ttf')
    f2 = os.path.join('fonts','sansthirteenblack.ttf')
    font1 = TTFont(f1)
    font2 = TTFont(f2)
    count1 = 0
    count2 = 0
    for c in list(text) :
        if not has_glyph(font1, c) :
            count1 += 1
        if not has_glyph(font2, c) :
            count2 += 1
    if count2 < count1 : return f2
    else : return f1
"""
    

def fit_text(img, draw, box, text, fontdir, guess=30, align="left", alignv="top",
             shadow=True):
    #fontdir = best_font(text)
    x1,y1,x2,y2 = box
    c1,c2 = (x2-x1, y2-y1)
    lo = 1
    hi = guess
    guess = (lo+hi)//2
    fuente = ImageFont.truetype(fontdir, guess)
    x,y = draw.textsize(text, font=fuente) #text_size(text, fuente)
    #while x > c1 or y > c2 :
    #intentos = 1
    lold, hiold = lo, hi
    while lo+1 < hi :
        #intentos += 1
        #guess -= 1
        if x > c1 or y > c2 :
            hi = guess
        else :
            lo = guess
        if (lold, hiold) == (lo, hi) :
            guess = lo
            break
        guess = (lo+hi)//2
        fuente = ImageFont.truetype(fontdir, guess)
        x,y = draw.textsize(text, font=fuente) #text_size(text, fuente)
    #print("intentos:", intentos)
    posx, posy = x1,y1
    
    if align == "center" :
        posx += (c1-x)//2
    if alignv == "bottom" :
        posy += c2-y
    elif alignv == "middle" :
        posy += (c2-y)//2

        
    draw_text(img, draw, (posx, posy), text, font=fuente)

def generate_banner(datos, prmode=False, blacksquares=True,
                    custombg=None, darkenbg=True,
                    customcolor=None, customcolor2=None,
                    font="font.ttc", fontcolor=(255,255,255), shadow=True,
                    icon_sizes=None) :
    game = datos["game"]
    players = datos["players"]


    path = os.path.realpath(__file__)
    path= os.path.abspath(os.path.join(path, os.pardir))
    template = os.path.join(path, "template")
    if font :
        fonttc = os.path.join(path, 'fonts', font)
    else :
        fonttc = os.path.join(path, 'fonts', "font.ttc")

    # Constantes
    portraits = os.path.join(path, "assets", game, "portraits")
    icons = os.path.join(path, "assets", game, "icons")
    SIZE = (1423,800)

    BIG = (483, 483)
    MED = (257, 257)
    SMA = (192, 192)

    POS = [(53, 135), (553, 135), (832, 135), (1110, 135),
           (553, 441), (760, 441), (968, 441), (1176, 441)]

    SIZETWI = [(483, 39), (257, 29), (257, 29), (257, 29),
               (192, 26), (192, 26), (192, 26), (192, 26)]

    POSTWI = [(52, 624), (552, 398), (831, 398), (1109, 398),
              (552, 637), (759, 637), (967, 637), (1175, 637)]

    POSTXT = [(53, 45), (53, 730), (875, 50), (1075, 725)]

    # La que tal
    c = Image.new('RGBA', SIZE, (0, 0, 0))

    # Fondo
    if custombg :
        f = Image.open(custombg, mode="r")
        ancho, largo = f.size
        a,b = int(ancho*SIZE[1]/largo), int(largo*SIZE[0]/ancho)
        if a < SIZE[0] :
            ancho, largo = SIZE[0], b
        else :
            ancho, largo = a, SIZE[1]
        f = f.resize((ancho, largo), resample=Image.ANTIALIAS)
        c.paste(f, ( int((SIZE[0]-ancho)/2), int((SIZE[1]-largo)/2) ) )
        if darkenbg :
            f = Image.new('RGBA', SIZE, (0, 0, 0, 0))
            c = Image.blend(c, f, 0.75)
    else :
        a  = Image.open(os.path.join(path, "assets", game, "bg.png"))
        c.paste(a, (0,0), mask=a)

    c = c.convert('RGB')

    # Pa escribir
    draw = ImageDraw.Draw(c)

    # Ciclo de portraits
    for i in range(8) :
        if i == 0 : size = BIG
        elif i < 4 : size = MED
        else : size = SMA

        if blacksquares :
            shape = [POS[i], (POS[i][0]+size[0], POS[i][1]+size[1])]
            draw.rectangle(shape, fill=(0,0,0))

        char = players[i]["char"]
        ruta = os.path.join(portraits, char[0])
        ruta = os.path.join(ruta, str(char[1])+".png")
        d = Image.open(ruta).convert("RGBA").resize(size, resample=Image.ANTIALIAS)
        
        # Intento de sombra
        if shadow :
            if customcolor : shadowcolor = customcolor
            else : shadowcolor = (255, 40, 56, 255)

            # offset de la sombra respecto al portrait
            shadowpos = int(size[0]*0.03)

            cuadrao = (  POS[i][0]+shadowpos,
                         POS[i][1]+shadowpos,
                         POS[i][0]+size[0],
                         POS[i][1]+size[1]
                      )
            cortao = (0, 0, size[0]-shadowpos, size[1]-shadowpos)
            dd =  d.crop(cortao)
            lasombra = Image.new('RGBA', cortao[2:], shadowcolor)

            c.paste(lasombra, cuadrao, mask=dd)
        c.paste(d, POS[i], mask=d)

    # Partes del template
    a  = Image.open(os.path.join(template,"marco.png"))
    if customcolor :
        y = Image.new('RGB', SIZE, customcolor)
        c.paste(y, (0,0), mask=a)
    else :
        c.paste(a, (0,0), mask=a)

    a  = Image.open(os.path.join(template,"polo.png"))
    if customcolor2 :
        y = Image.new('RGB', SIZE, customcolor2)
        c.paste(y, (0,0), mask=a)
    else :
        c.paste(a, (0,0), mask=a)

    if prmode :
        a = Image.open(os.path.join(template,"numerospr.png"))
    else :
        a = Image.open(os.path.join(template,"numeros.png"))
    c.paste(a, (0,0), mask=a)
    #c = Image.alpha_composite(a,c)

    # Textos de arriba y abajo
    fuente = ImageFont.truetype(fonttc, 30)
    draw_text(c, draw, POSTXT[0], datos["toptext"], font=fuente, fill=fontcolor, shadow=True)
    draw_text(c, draw, POSTXT[1], datos["bottomtext"], font=fuente, fill=fontcolor, shadow=False)

    fuente = ImageFont.truetype(fonttc, 25)
    urlmarg = (40-len(datos["url"]))*6
    draw_text(c, draw, (POSTXT[2][0]+urlmarg,POSTXT[2][1]), datos["url"], font=fuente, fill=fontcolor, shadow=False)
    draw_text(c, draw, POSTXT[3], "Design by:  @Elenriqu3\nGenerator by: @Riokaru", font=fuente, fill=fontcolor, shadow=True)

    # Ciclo de nombres
    pajarito = Image.open(os.path.join(template,"pajarito.png"))
    for i in range(8) :
        if i == 0 : size = BIG
        elif i < 4 : size = MED
        else : size = SMA
        if players[i]["twitter"] :
            # Cajita para twitter handle
            if customcolor :
                colorcito = customcolor
            else :
                colorcito = (255, 40, 56, 255)
            draw.rectangle([POSTWI[i],
                            (POSTWI[i][0]+SIZETWI[i][0],
                             (POSTWI[i][1]+SIZETWI[i][1]))],
                           fill=colorcito
                           )
            # Pajarito de Twitter
            if pajarito.size[1] != SIZETWI[i][1] :
                psize = ((pajarito.size[0]*SIZETWI[i][1])//pajarito.size[1],
                         SIZETWI[i][1])
                pajarito = pajarito.resize(psize, resample=Image.ANTIALIAS)
            c.paste(pajarito,
                    (int(POSTWI[i][0]+SIZETWI[i][0]*0.02), POSTWI[i][1]),
                    mask=pajarito)

            lon = len(players[i]["twitter"])
            sizef = (27*SIZETWI[i][1])//SIZETWI[0][1]
            tmarg = (6*SIZETWI[i][1])//SIZETWI[0][1]
            lmarg = (SIZETWI[i][0]-0.5*sizef*lon+pajarito.size[0])//2

            """
            xmarg = pajarito.size[0]*1.2
            tmarg = (SIZETWI[i][1])/SIZETWI[0][1]
            bmarg = (SIZETWI[i][1])/SIZETWI[0][1]

            cajita_twitter = (POSTWI[i][0]+xmarg, POSTWI[i][1]+tmarg,
                              POSTWI[i][0]+SIZETWI[i][0]-xmarg, POSTWI[i][1]+SIZETWI[i][1]-bmarg)

            fit_text(c, draw, cajita_twitter, players[i]["twitter"], fonttc, guess=54,
                     align="center", alignv="middle")
            """

            font = ImageFont.truetype(fonttc, sizef)
            draw_text(c, draw, (POSTWI[i][0]+lmarg, POSTWI[i][1]+tmarg),
                      players[i]["twitter"], font=font, fill=fontcolor, shadow=True)

        texto = players[i]["tag"].replace(". ", ".").replace(" | ", "|")
        """
        sizefont = int(size[0]*0.26)
        if len(texto) > 7 :
            sizefont = int(sizefont*7/len(texto))
        font = ImageFont.truetype(fonttc, sizefont)
        """

        cajita_nombre = (POS[i][0]+12, POS[i][1],
                         POS[i][0]+size[0]-12, POS[i][1]+size[1]*0.98)
        
        fit_text(c, draw, cajita_nombre, texto, fonttc, guess=int(size[0]*0.26),
                 align="center", alignv="bottom")
        #draw_text(c, draw, (POS[i][0] + (size[0]-0.5*sizefont*len(texto))//2,
        #           POS[i][1]+int(size[0]*0.995)-sizefont),
        #           texto, font=font, fill=fontcolor)

        # extras
        s_off = 0
        for char in players[i]['secondaries'] :
            try :
                ruta_i = os.path.join(icons, char[0])
                ruta_i = os.path.join(ruta_i, str(char[1])+".png")
                ic = Image.open(ruta_i)
                if size != BIG :
                    if icon_sizes : i_size = icon_sizes[1]
                    else : i_size = 32
                    ic = ic.resize((i_size, i_size),resample=Image.ANTIALIAS)
                    if size == MED :
                        rmarg = 8
                    else :
                        rmarg = 6
                else :
                    if icon_sizes : i_size = icon_sizes[0]
                    else : i_size = 64
                    ic = ic.resize((i_size, i_size),resample=Image.ANTIALIAS)
                    rmarg = 14
                c.paste(ic, (POS[i][0]+size[0]-i_size-rmarg, POS[i][1]+s_off*(i_size+4)+rmarg), mask=ic)
                s_off += 1
            except :
                print("not found: "+str(ruta_i))
    return c

if __name__ == "__main__":
    # datos y configuración

    custombg = "bgusb.jpg"
    customcolor = (255, 201, 14)
    fontcolor = (255,255,255)
    shadow = True
    fuente = None
    ics = None

    """
    texto = ["morrocoYo", "GARU", "Pancakes", "VeXx",
             "BTO", "Vunioq", "Nandok", "Kellios"]
    texto = ["morrocoÑo", "GARÜ", "Pおncakes", "VeXx",
             "BTØ", "Vünioq", "Ñandok", "Kellios"]
    personajes = [("Robin", 0),
                  ("Joker", 0),
                  ("Inkling", 5),
                  ("Inkling", 2),
                  ("Mr Game & Watch", 0),
                  ("Samus", 0),
                  ("Sonic", 1),
                  ("Terry", 0)]
    twitter = ["@DanielRimeris", "@GARU_Sw", "@movpancakes", "@RisingVexx",
               "@HoyerBTO", "@Vunioq", "@Nandok_95", "@CarlosDQC"]
    #twitter = ["A"*15 for i in range(8)]
    pockets = [[("Bowser", 5)], [("Falco", 5), ("Fox", 3)], [("Mega Man", 1)], [("Marth", 2)],
               [], [], [], []]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Show Me your Moves - Ultimate Singles - Top 8",
             "bottomtext" : "22 de Febrero de 2020 - Caracas, Venezuela - 89 participantes",
             "url" : "facebook.com/groups/smashvenezuela",
             "game" : "ssbu"
             }

    cc1 = None
    cc2 = None
    ics = None
    #fuente = "sansthirteenblack.ttf"
    #fuente = "sansblack.ttf"
    """
    

    """
    texto = ["CartezSoul", "Riokaru", "Luigic7", "Reyn",
             "3rdStrike", "SCruz", "Deathmouth", "Yuky-Pak"]
    twitter = ["@SilvxBexts", "@Riokaru", "@LuigiDiMartino", None,
               "@altuveguitar", None, "@BoseJoaoGamer", "@9msfts"]
    personajes = [("Pikachu", 2),
                  ("Mewtwo", 2),
                  ("King Dedede", 1),
                  ("Corrin", 0),
                  ("Ken", 3),
                  ("Banjo & Kazooie", 0),
                  ("Joker", 0),
                  ("Mario", 0)]

    datos = {"players" : players,
             "toptext" : "Saltynejas 6 - Ultimate Singles - Top 8",
             "bottomtext" : "14 de Febrero de 2020 - Universidad Simon Bolivar - 19 participantes"}

    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i]} for i in range(8)]
    """

    """
    texto = ["1stStrike", "2ndStrike", "3rdStrike", "4thStrike",
             "5thStrike", "6thStrike", "7thStrike", "8thStrike"]
    personajes = [("Ken", i) for i in range(8)]
    twitter = ["altuveguitar" for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i]} for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Conyazo3 Tournament - Street Fighter 3rd Strike - Top 8",
             "bottomtext" : "3 de Marzo de 2033 - Caracas, Memezuela - 33 participantes"}
    """
    """
    texto = [s[:-1] for s in ["Min "*(i+1) for i in range(8)]]
    personajes = [("Min Min", i) for i in range(8)]
    twitter = ["MinMin0"+str(i+1) for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i]} for i in range(8)]
    datos = {"players" : players,
             "toptext" : "Min Min Min Min Min Min Min Min",
             "bottomtext" : "Min Min Min Min Min Min Min Min",
             "url" : "https://top8er.com",
             }
    """

    """
    texto = ["Absa", "Clairen", "Elliana", "Etalus",
             "Forsburn", "Kragg", "Maypul", "Orcane"]
    personajes = [(texto[i], i) for i in range(7)] + [("Orcane",8)]
    twitter = ["@danfornace" for i in range(8)]
    pockets = [[(texto[i], 0), (texto[i], 0)] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "@danfornace I made this graphic generator for RoA ",
             "bottomtext" : "Please notice me @danfornace",
             "url" : "https://top8er.com",
             "game" : "roa"
             }
    cc1 = None
    cc2 = None
    ics = None
    """
    
    """
    texto = ["Afi and Galu", "Ashani", "Ezzie", "Kidd",
             "Raymer", "Urdah", "Weishan", "Zhurong"]
    personajes = [(texto[i], 0) for i in range(8)]
    twitter = ["@RushdownRevolt" for i in range(8)]
    #pockets = [[(texto[(i+1)%8],0), (texto[(i+2)%8],0)] for i in range(8)]
    pockets = [[] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Top text goes here",
             "bottomtext" : "Bottom text goes here",
             "url" : "https://top8er.com",
             "game" : "rr"
             }
    cc1 = (56,75,203)
    cc2 = (64, 235, 143)
    ics = (80,50)
    fuente = "sansthirteenblack.ttf"
    """

    """
    texto = ["Player "+str(i) for i in range(1,9)]
    #p = ["Banjo & Kazooie", "Bayonetta", "Bowser", "Bowser Jr", "Byleth", "Captain Falcon", "Chrom", "Cloud"]
    p = ["Samus", "Sheik", "Shulk", "Simon", "Snake", "Sonic", "Steve", "Terry"]
    personajes = [(p[i], i) for i in range(8)]
    twitter = ["player"+str(i) for i in range(1,9)]
    pockets = [[] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "",
             "bottomtext" : "",
             "url" : "https://top8er.com",
             "game" : "ssbu"
             }
    """

    """
    texto = ["Player "+str(i) for i in range(1,9)]
    import random
    c = ['Beowulf', 'Big Band', 'Cerebella', 'Double', 'Eliza', 'Filia', 'Fukua', 'Ms Fortune', 'Painwheel', 'Parasoul', 'Peacock', 'Robo Fortune', 'Squigly', 'Valentine']
    personajes = [(random.choice(c), random.randint(0,26)) for i in range(8)]
    twitter = ["player"+str(i) for i in range(1,9)]
    pockets = [[(random.choice(c), 0), (random.choice(c), 0)] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Top Text goes here",
             "bottomtext" : "Bottom Text goes here",
             "url" : "https://top8er.com",
             "game" : "sg"
             }
    cc1 = (215, 62, 62)
    cc2 = (203, 198, 186)
    """

    #"""
    import random
    C = {'Bowser': ['Default', 'Red', 'Blue', 'Black'], 'Captain Falcon': ['Default', 'Black', 'Red', 'White', 'Green', 'Blue'], 'Donkey Kong': ['Default', 'Black', 'Red', 'Blue', 'Green'], 'Dr Mario': ['Default', 'Red', 'Blue', 'Green', 'Black'], 'Falco': ['Default', 'Red', 'Blue', 'Green'], 'Fox': ['Default', 'Red', 'Blue', 'Green'], 'Ganondorf': ['Default', 'Red', 'Blue', 'Green', 'Purple'], 'Ice Climbers': ['Default', 'Green', 'Orange', 'Red'], 'Jigglypuff': ['Default', 'Red', 'Blue', 'Green', 'Yellow'], 'Kirby': ['Default', 'Yellow', 'Blue', 'Red', 'Green', 'White'], 'Link': ['Default', 'Red', 'Blue', 'Black', 'White'], 'Luigi': ['Default', 'White', 'Blue', 'Pink'], 'Mario': ['Default', 'Yellow', 'Black', 'Blue', 'Green'], 'Marth': ['Default', 'Red', 'Green', 'Black', 'White'], 'Mewtwo': ['Default', 'Red', 'Blue', 'Green'], 'Mr Game & Watch': ['Default', 'Red', 'Blue', 'Green'], 'Ness': ['Default', 'Yellow', 'Blue', 'Green'], 'Peach': ['Default', 'Yellow', 'White', 'Blue', 'Green'], 'Pichu': ['Default', 'Red', 'Blue', 'Green'], 'Pikachu': ['Default', 'Red', 'Blue', 'Green'], 'Roy': ['Default', 'Red', 'Blue', 'Green', 'Yellow'], 'Samus': ['Default', 'Pink', 'Black', 'Green', 'Purple'], 'Sheik': ['Default', 'Red', 'Blue', 'Green', 'White'], 'Yoshi': ['Default', 'Red', 'Blue', 'Yellow', 'Pink', 'Cyan'], 'Young Link': ['Default', 'Red', 'Blue', 'White', 'Black'], 'Zelda': ['Default', 'Red', 'Blue', 'Green', 'White']}
    def randchar() :
        c = random.choice(list(C.keys()))
        n = random.randint(0,len(C[c])-1)
        return (c,n)
    texto = ["プレーヤー"+str(i) for i in range(1,9)]
    #texto = ["お"*i for i in range(1,9)]
    personajes = [randchar() for i in range(8)]
    twitter = ["player"+str(i) for i in range(1,9)]
    pockets = [[randchar(), randchar()] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Top Text goes here",
             "bottomtext" : "Bottom Text goes here",
             "url" : "https://top8er.com",
             "game" : "melee"
             }
    cc1 = None
    cc2 = None
    ics = (48, 24)
    #"""

    """
    import random
    C = ['A.B.A', 'Anji Mito', 'Axl Low', 'Baiken', 'Bridget', 'Chipp Zanuff', 'Dizzy', 'Eddie', 'Faust', 'I-No', 'Jam Kuradoberi', 'Johnny', 'Justice', 'Kliff Undersn', 'Ky Kiske', 'May', 'Millia Rage', 'Order-Sol', 'Potemkin', 'Robo-Ky', 'Slayer', 'Sol Badguy', 'Testament', 'Venom', 'Zappa']
    colors = ['Full Art',
              'Default P', 'Default K', 'Default S', 'Default H', 'Default D',
              'EX P', 'EX K', 'EX S', 'EX H', 'EX D',
              'Slash P', 'Slash K', 'Slash S', 'Slash H', 'Slash D',
              'Reload P', 'Reload K', 'Reload S', 'Reload H', 'Reload D',
              'Portrait']#,'Face Art']
    C = {c:colors for c in C}
    def randchar() :
        c = random.choice(list(C.keys()))
        #c = random.choice(["Faust", "Kliff Undersn"])
        n = random.randint(1,len(C[c])-1)
        n = 21
        return (c,n)
    texto = ["Player "+str(i) for i in range(1,9)]
    personajes = [randchar() for i in range(8)]
    twitter = ["player"+str(i) for i in range(1,9)]
    pockets = [[] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Top Text goes here",
             "bottomtext" : "Bottom Text goes here",
             "url" : "https://top8er.com",
             "game" : "ggxx"
             }
    cc1 = None
    cc2 = None
    ics = None
    """

    import time
    t1 = time.time()
    #img = generate_banner(datos, customcolor="#00bbfa", customcolor2="#001736")# customcolor="#287346", customcolor2="#ede07c")
    img = generate_banner(datos, icon_sizes=ics, shadow=True, prmode=False, blacksquares=True,
                          customcolor=cc1, customcolor2=cc2, font=fuente)
    t2 = time.time()
    print(t2-t1)
    img.show()
    img.save("sample.png")

    input()
