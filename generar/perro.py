from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode
import os, math

def draw_text(img, draw, pos, texto, font=None,
              fill=(255, 255, 255), shadow=(0,0,0)) :
    if shadow :
        #offset = int(font.size*0.06)
        offset = int((font.size**0.5)*0.55)
        draw.text((pos[0]+offset, pos[1]+offset), texto, font=font, fill=shadow)
    draw.text(pos, texto, font=font, fill=fill)

def has_glyph(font, glyph):
    for table in font['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False

def best_font(text, f1, f2) :
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

def fitting_font(draw, width, height, text, fontdir, guess) :
    lo = 1
    hi = guess
    guess = (lo+hi)//2
    fuente = ImageFont.truetype(fontdir, guess)
    x,y = draw.textsize(text, font=fuente)
    #intentos = 1
    lold, hiold = lo, hi
    while lo+1 < hi :
        #intentos += 1
        #guess -= 1
        if x > width or y > height :
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
    return fuente

        
def fit_text(img, draw, box, text, fontdir, guess=30, align="left", alignv="top",
             fill=(255, 255, 255), shadow=(0,0,0), forcedfont=None):
    #fontdir = best_font(text)
    x1,y1,x2,y2 = box
    width,height = (x2-x1, y2-y1)

    if forcedfont is None :
        fuente = fitting_font(draw, width, height, text, fontdir, guess)
    else :
        fuente = forcedfont
        
    x,y = draw.textsize(text, font=fuente)

    posx, posy = x1,y1
    
    if align == "center" :
        posx += (width-x)//2
    elif align == "right" :
        posx += width-x
        
    if alignv == "bottom" :
        posy += height-y
    elif alignv == "middle" :
        posy += (height-y)//2

    draw_text(img, draw, (posx, posy), text, font=fuente, fill=fill, shadow=shadow)

def efz_palette(path) :
    colors = []
    if type(path) is str :
        f = open(path, "rb")
    else :
        f = path
    s = f.read()
    f.close()
    i = 1
    c = []
    while i < len(s) :
        c.append(s[i])
        if i%3 == 0 :
            c = tuple(c[::-1])
            #print(c)
            colors.append(c)
            c = []
        i += 1
    while len(colors) < 40 :
        colors.append((0,0,0))
    return colors

def efz_swap(file, pal1, pal2, akane=False) :
    img = Image.open(file)
    orig = efz_palette(pal1)
    meme = efz_palette(pal2)

    #"""
    if akane :
        orig = orig[:29]
        meme = meme[:29]
    #"""

    #orig = orig[::-1]
    #meme = meme[::-1]

    quick_orig = {orig[i]:i for i in range(len(orig))}

    match = [[] for o in orig]

    w,h = img.size

    for x in range(w) :
        for y in range(h) :
            c = img.getpixel((x,y))
            if c[:3] in quick_orig :
                match[quick_orig[c[:3]]].append((x,y))

    for i in range(len(match)) :
        if meme[i][0] == 178 : print("AAA")
        for pixel in match[i] :
            alpha = img.getpixel(pixel)[3:]
            img.putpixel(pixel, meme[i]+alpha)

    return img

def generate_banner(datos, prmode=False, blacksquares=True,
                    custombg=None, darkenbg=True,
                    customcolor=None, customcolor2=None,
                    font=None,
                    fontcolor1=(255,255,255),fontscolor1=(0,0,0),
                    fontcolor2=(255,255,255),fontscolor2=(0,0,0),
                    shadow=True, icon_sizes=None,
                    teammode=False) :
    game = datos["game"]
    players = datos["players"]


    path = os.path.realpath(__file__)
    path = os.path.abspath(os.path.join(path, os.pardir))
    template = os.path.join(path, "template")
    if font :
        fonttc = os.path.join(path, 'fonts', font)
    else :
        yog_sothoth = datos["toptext"]+datos["bottomtext"]+datos["url"]
        for player in datos['players'] :
            yog_sothoth += player['tag']
        f1 = os.path.join(path, 'fonts','DFGothic-SU-WIN-RKSJ-H-01.ttf')
        f2 = os.path.join(path, 'fonts','sansthirteenblack.ttf')
        fonttc = best_font(yog_sothoth, f1, f2)

    # Constantes
    portraits = os.path.join(path, "assets", game, "portraits")
    icons = os.path.join(path, "assets", game, "icons")
    SIZE = (1423,800)

    BIG = (482, 482)
    MED = (257, 257)
    SMA = (191, 191)

    POS = [(53, 135), (553, 135), (831, 135), (1110, 135),
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
            c = Image.blend(f, c, 0.30)
    else :
        a  = Image.open(os.path.join(path, "assets", game, "bg.png")).convert("RGBA")
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

        if teammode and len(players[i]["secondaries"]) != 0 :
            chars = [players[i]["char"]] + players[i]["secondaries"]
            d = Image.new("RGBA", size, color=(255,255,255,0))
            j = 0
            for char in chars :
                ruta = os.path.join(portraits, char[0], str(char[1])+".png")
                
                if len(chars) == 3 :
                    newsize = int(0.7*size[0])                    
                    d2 = Image.open(ruta).convert("RGBA").resize((newsize, newsize))
                    offset = 0.14
                    m1 = 2.9
                    m2 = 0.8
                    if j == 0 :
                        position = ((size[0]-newsize)//2,
                                    (size[0]-newsize)//2)
                        base1 = size[0]-m2*size[0]
                        base2 = size[0]-(size[0]/m1)
                        is_out = lambda t : t[0]-t[1] < base1 or t[0]-t[1] > base2
                    elif j == 1 :
                        position = (-int(size[0]*offset),
                                    size[0]-newsize)
                        base = size[0]-m2*size[0]
                        is_out = lambda t : t[0]-t[1] > base
                    elif j == 2 :
                        position = (size[0]-newsize+int(size[0]*offset), 0)
                        base = size[0]-(size[0]/m1)
                        is_out = lambda t : t[0]-t[1] < base

                    x,y = position
                    if char[0] in ["Parasoul"] :
                        x += size[0]//10
                    elif char[0] in ["Ms Fortune", "Robo Fortune", "Valentine"] :
                        x += size[0]//20
                    elif char[0] in ["Big Band", "Beowulf"] :
                        x -= size[0]//20
                    elif char[0] in ["Painwheel"] :
                        y -= size[0]//20
                        x -= size[0]//20
                    position = (x,y)

                elif len(chars) <= 2 :
                    newsize = int(0.8*size[0])                    
                    d2 = Image.open(ruta).convert("RGBA").resize((newsize, newsize))
                    offset = 0.08
                    m = 0.6
                    if j == 0 :
                        position = (-int(size[0]*offset),
                                    size[0]-newsize)
                        base = size[0]-m*size[0]
                        is_out = lambda t : t[0]-t[1] > base
                    elif j == 1 :
                        position = (size[0]-newsize+int(size[0]*offset), 0)
                        base = size[0]-m*size[0]
                        is_out = lambda t : t[0]-t[1] < base

                    x,y = position
                    if char[0] in ["Parasoul"] :
                        x += size[0]//10
                    elif char[0] in ["Ms Fortune", "Robo Fortune", "Valentine"] :
                        x += size[0]//20
                    elif char[0] in ["Big Band", "Beowulf"] :
                        x -= size[0]//20
                    elif char[0] in ["Painwheel"] :
                        y -= size[0]//20
                        x -= size[0]//20
                    position = (x,y)
                    

                d3 = Image.new("RGBA", size, color=(255,255,255,0))
                h,w = d3.size
                d3.paste(d2, position, d2)
                    
                for x in range(h) :
                    for y in range(w) :
                        if is_out((x*1.4,y*0.6)) :
                            d3.putpixel((x,y), (255,255,255,0))
                        """
                        else :
                            continue
                            if j == 0 : d3.putpixel((x,y), (255,0,0,255))
                            elif j == 1 : d3.putpixel((x,y), (0,255,0,255))
                            else  : d3.putpixel((x,y), (0,0,255,255))
                        """
                d.paste(d3, (0,0), d3)
                
                j += 1
            #c.paste(d, POS[i], mask=d)
        else :
            char = players[i]["char"]
            ruta = os.path.join(portraits, char[0])
            if game == "efz" and not type(char[1]) is int and not len(char[1]) == 1 :
                rruta = os.path.join(ruta, "1.png")
                pal1 = os.path.join(ruta, "0.pal")
                d = efz_swap(rruta,
                             pal1,
                             char[1], akane=(char[0]=="Akane")
                             ).convert("RGBA").resize(size,
                                                      resample=Image.ANTIALIAS)
            else :
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

        # extras
        if not teammode :
            s_off = 0
            for char in players[i]['secondaries'] :
                try :
                    ruta_i = os.path.join(icons, char[0])
                    ruta_i = os.path.join(ruta_i, str(char[1])+".png")
                    ic = Image.open(ruta_i).convert("RGBA")
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
                except Exception as e :
                    print(e, str(ruta_i))

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
        
    if fontcolor1 != (255, 255, 255) and fontcolor1 != "#ffffff" :
        mask = a
        a = Image.new('RGBA', SIZE, fontcolor1)
    else :
        mask = a

    c.paste(a, (0,0), mask=mask)
    
    #c = Image.alpha_composite(a,c)

    # Textos de arriba y abajo
    fuente = ImageFont.truetype(fonttc, 30)
    #draw_text(c, draw, POSTXT[0], datos["toptext"], font=fuente, fill=fontcolor, shadow=True)
    #draw_text(c, draw, POSTXT[1], datos["bottomtext"], font=fuente, fill=fontcolor, shadow=False)

    fit_text(c, draw, (53, 45, 803, 80), datos["toptext"], fonttc,
             align="left", alignv="middle", fill=fontcolor2, shadow=fontscolor2)
    fit_text(c, draw, (53, 730, 997, 765), datos["bottomtext"], fonttc,
             align="left", alignv="middle", fill=fontcolor2, shadow=fontscolor2)

    fuente = ImageFont.truetype(fonttc, 25)
    urlmarg = (40-len(datos["url"]))*6
    #draw_text(c, draw, (POSTXT[2][0]+urlmarg,POSTXT[2][1]), datos["url"], font=fuente, fill=fontcolor, shadow=False)
    #draw_text(c, draw, POSTXT[3], "Design by:  @Elenriqu3\nGenerator by: @Riokaru", font=fuente, fill=fontcolor, shadow=True)

    fit_text(c, draw, (1075, 726, 1361, 778), "Design by:  @Elenriqu3\nGenerator by: @Riokaru", fonttc,
             align="right", alignv="middle", fill=fontcolor2, shadow=fontscolor2)
    fit_text(c, draw, (876, 45, 1367, 80), datos["url"], fonttc,
             align="right", alignv="middle", fill=fontcolor2, shadow=fontscolor2)

    # Ciclo de nombres
    pajarito = Image.open(os.path.join(template,"pajarito.png"))
    if fontcolor1 != (255, 255, 255) and fontcolor1 != "#ffffff" :
        a = Image.new('RGBA', pajarito.size, (255, 255, 255, 0))
        aa = Image.new('RGBA', pajarito.size, fontcolor1)
        a.paste(aa, (0,0), mask=pajarito)
        pajarito = a
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

            #lon = len(players[i]["twitter"])
            #sizef = (27*SIZETWI[i][1])//SIZETWI[0][1]
            #tmarg = (6*SIZETWI[i][1])//SIZETWI[0][1]
            #lmarg = (SIZETWI[i][0]-0.5*sizef*lon+pajarito.size[0])//2

            #"""
            xmarg = pajarito.size[0]*1.2
            tmarg = 0.1*SIZETWI[i][1]
            bmarg = 0.1*SIZETWI[i][1]

            cajita_twitter = (POSTWI[i][0]+xmarg, POSTWI[i][1]+tmarg,
                              POSTWI[i][0]+SIZETWI[i][0], POSTWI[i][1]+SIZETWI[i][1]-bmarg)

            width = cajita_twitter[2]-cajita_twitter[0]
            height = cajita_twitter[3]-cajita_twitter[1]
            ffont = fitting_font(draw, width, height, "A!"*8, fonttc, guess=54)

            fit_text(c, draw, cajita_twitter, players[i]["twitter"], fonttc, guess=54,
                     align="center", alignv="middle", forcedfont=ffont,
                     fill=fontcolor1, shadow=fontscolor1)
            #"""

            #font = ImageFont.truetype(fonttc, sizef)
            #draw_text(c, draw, (POSTWI[i][0]+lmarg, POSTWI[i][1]+tmarg),
            #          players[i]["twitter"], font=font, fill=fontcolor, shadow=True)

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
                 align="center", alignv="bottom",
                 fill=fontcolor1, shadow=fontscolor1)
        #draw_text(c, draw, (POS[i][0] + (size[0]-0.5*sizefont*len(texto))//2,
        #           POS[i][1]+int(size[0]*0.995)-sizefont),
        #           texto, font=font, fill=fontcolor)

    return c

if __name__ == "__main__":
    # datos y configuración

    #custombg = "bgusb.jpg"
    cc1 = None
    cc2 = None
    fontcolor = (255,255,255)
    shadow = True
    fuente = None
    ics = None
    fontc = (255, 255, 255)
    fontsc = (0,0,0)
    fontc2 = (255, 255, 255)
    fontsc2 = (0,0,0)
    bsq = True
    darken = True
    cbg = None
    teammode = False

    """
    texto = ["morrocoYo", "GARU", "Pancakes", "VeXx",
             "BTO", "Vunioq", "Nandok", "Kellios"]
    #texto = ["morrocoYó", "GARÜ", "Páncakes", "VëXx", "BTØ", "VüniØq", "Ñandok", "KëlliØs"]
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
    #twitter = ["@DanielRimeris69"]*8
    #twitter = ["A"*15 for i in range(8)]
    pockets = [[("Bowser", 5)], [("Falco", 5), ("Fox", 3)], [("Mega Man", 1)], [("Marth", 2)],
               [], [], [], []]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Show Me your Moves - Ultimate Singles - Top 8",
             #"toptext" : "あ"*40,
             "bottomtext" : "22 de Febrero de 2020 - Caracas, Venezuela - 89 participantes",
             #"bottomtext" : "あ"*50,
             "url" : "facebook.com/groups/smashvenezuela",
             #"url" : "あ"*40,
             "game" : "ssbu"
             }
    
    cc1 = (0,0,0)
    cc2 = (255,255,255)
    #fontc = (230, 230, 255)
    #fontsc = (0,0,100)
    fontc2 = (0,0,0)
    fontsc2 = (255, 255, 255)
    ics = None
    bsq = False
    darken = False
    cbg = "Untitled.png"
    #fuente = "sansblack.ttf"
    #fuente = "sansthirteenblack.ttf"
    #fuente = "DFGothic-SU-WIN-RKSJ-H-01.ttf"
    #fuente = "DFGothic-SU-WINP-RKSJ-H-02.ttf"
    #fuente = "DFGothic-SU-WING-RKSJ-H-03.ttf"
    #fuente = "BlackHoleBB.ttf"
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
    pockets = [[(random.choice(c), random.randint(0,26)),
                (random.choice(c), random.randint(0,26))][:random.randint(0,2)]
               for i in range(8)]
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
    teammode = True
    """

    """
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
    """

    """
    import random
    Chars = ['A.B.A', 'Anji Mito', 'Axl Low', 'Baiken', 'Bridget', 'Chipp Zanuff', 'Dizzy', 'Eddie', 'Faust', 'I-No', 'Jam Kuradoberi', 'Johnny', 'Justice', 'Kliff Undersn', 'Ky Kiske', 'May', 'Millia Rage', 'Order-Sol', 'Potemkin', 'Robo-Ky', 'Slayer', 'Sol Badguy', 'Testament', 'Venom', 'Zappa']
    colors = ['Full Art',
              'Default P', 'Default K', 'Default S', 'Default H', 'Default D',
              'EX P', 'EX K', 'EX S', 'EX H', 'EX D',
              'Slash P', 'Slash K', 'Slash S', 'Slash H', 'Slash D',
              'Reload P', 'Reload K', 'Reload S', 'Reload H', 'Reload D',
              'Portrait']
    C = {c:colors for c in Chars}
    #print(C)
    def randchar() :
        c = random.choice(list(C.keys()))
        #c = random.choice(["Faust", "Kliff Undersn", "Justice"])
        #c = random.choice(["Bridget", "Chipp Zanuff", "Baiken"])
        #c = "A.B.A"
        n = random.randint(1,20)
        #n = 0
        n = 21
        return (c,n)
    #texto = ["Player "+str(i) for i in range(1,9)]
    #personajes = [randchar() for i in range(8)]
    personajes = [(Chars[(i+len(Chars))%len(Chars)], 0) for i in range(8)]
    texto = [personajes[i][0] for i in range(8)]
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
    cc2 = (50, 0, 0)
    fontc = (255, 255, 50)
    """

    """
    import random
    C =     {'Hyde': ['Full Art', 'Black Eclipse', 'Twinkle White', 'Darkness Tempest', 'Light Forest', 'Nightmare', 'Red Pearl', 'Desert Wolf', 'Sea Water', 'Moonlight', 'Justice Rose', 'Blau Blitz', 'Sunlight Red', 'Vortex Galaxy', 'Cremisi Grotta', 'Holiness Star', 'Rosa Descendiente', 'Juillet Averse', 'Soul Lover', 'Caldo Trrente', 'Viridis Regulus', 'Shinku', 'Blanche Diable', 'Ocean Arctique', 'Citrus Fresh', 'Guilty Thorn', 'Schon Gift', 'Nutty Pastel', 'Clear Gale', 'Santana', 'Dark Matter', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Royal Calibur', 'Stella Nest', 'Little Briar Rose', 'Betrayal of Savior', 'Switching Contrast', 'Super Deformed'], 
    'Linne': ['Full Art', 'Canary Yellow', 'Solitude Spica', 'Rhodorite Garnet', 'Sylvania Keeper', 'Purple Powder', 'Pure Black', 'Ore Shine', 'Blue Ocean', 'Autumnal Leaves', 'Destruction Red', 'Brosche Saphir', 'Drought Ground', 'Acero Granizo', 'Isora Albero', 'Wind of Oasis', 'Perfume Lemon', 'Ciruela', 'Pupil Gloomy', 'Arche wave', 'Ritual Sacrifice', 'Spring Breeze', 'Lapin de Neige', 'Nacht Kirshblute', 'Bush Camouflage', 'Misty Crystal', 'Exotic Coral', 'Spunky Mint', 'Burial Agency', 'Water Imp', 'Nagger Brawny', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Waldstein': ['Full Art', 'Iron Beast', 'Crow Ash', 'Steel Tiger', 'Sapphire Bear', 'Magnetite Crystal', 'Coal Monster', 'Francium Maroon', 'Tungsten Yellow', 'Poison Bandit', 'Hihiirokane', 'Fegefeuer', 'Arctic Cold', 'Dschungel Wind', 'Hatred Flame', 'Eis mann', 'Bestie Erde', 'Kirschbaum', 'Depression Mind', 'Gray Fox', 'Apostle of Chaos', 'Big Foot', 'Crimson Ogre', 'Brawny Orc', 'Scorched Earth', "Thor's Hammer", 'Red Hot Steel', 'Vert Nil', 'Aschputtel', 'Drema Warden', 'Gold Lowe', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Royal Calibur', 'Stella Nest', 'Little Briar Rose', 'Betrayal of Savior', 'Switching Contrast', 'Super Deformed'], 
    'Carmine': ['Full Art', 'Red Heat Blood', 'Black Punishment', 'Aqua Regia', 'Ride on Light', 'Dead and Violet', 'Bloody Lost', 'Wild Fang', 'Bad Peace Forest', 'Fade Noise', 'Purplish Gouache', 'Strange Strawberry', 'Plena Noche', 'Emerald Island', 'Ortensia', 'Light of Daybreak', 'Flash Magic', 'Claro de Luna', 'Brave Satan', 'Peligro Diosa', 'Demon Angel', 'Crimson Surfer', 'Fake Hero', 'Liquid Metal', 'Noble Blood', 'Vegetarian', 'Mr. Monochrome', 'Surfusion Eau', 'Prunella Honey', 'Western Feast', 'Dead and Black', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Royal Calibur', 'Stella Nest', 'Little Briar Rose', 'Betrayal of Savior', 'Switching Contrast', 'Super Deformed'], 
    'Orie': ['Full Art', 'Justice Sprite', 'Night Shade', 'Tears of Salamander', "Saint's Mother", 'Storm Sylphid', 'Undine Rain', 'Athena Light', 'Evil Knight', 'Scamper Emerald', 'Efreet Flare', 'Rizo de Agua', 'Fallen Angels', 'Dios de la Muerte', 'Calm Pink', 'Orange Yogurt', 'Crimson Rouge', 'Mistiltein', 'Green Magnolia', 'Lluvia Medium', 'Moon Water', 'Alice Blue', 'Spectrum Rose', 'Campanula Purple', 'Cavalier Du Lac', 'Dry Blood', 'Walder Abendrot', 'Shade Gardian', 'Honorable Scar', 'Lumiere Solaire', 'Memorial Black', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Royal Calibur', 'Stella Nest', 'Little Briar Rose', 'Betrayal of Savior', 'Switching Contrast', 'Super Deformed'], 
    'Gordeau': ['Full Art', 'Robbery Purple', 'The Baron of Night', 'Poseidon', 'Red Azrael', 'Thunderbird', 'Vampire and Alcohol', 'Lancelot du Lac', 'Bamboo Scythe', 'Season of Harvest', 'Legend Vermilion', 'Scharlachrot', 'Fresco Verde', 'Shadow Vice', 'Emperor of Walnut', 'Mischievous Firefly', 'Turquoise Blue', 'Atonement Blood', 'Golden Summer', 'Hard Sleet', 'Frost Skeleton', 'Gusty Edge', 'Noble Impulse', 'Amore Formaggio', 'Jade Tempest', 'Deadvlei', 'False Dawn', 'Lunar Corona', 'Falconry Hawking', 'Righteous Daddy', 'Imitate Intrigant', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Royal Calibur', 'Stella Nest', 'Little Briar Rose', 'Betrayal of Savior', 'Switching Contrast', 'Super Deformed'], 
    'Merkava': ['Full Art', "Hell's Viper", 'Scallop', 'Brown Lizard', 'Scream Hades', 'Green Iguana', 'Bloody Basilisk', 'Violet Naja', 'Sea Snake', 'Dust Sand', 'Hephaistos', 'Wise Marlin', 'Noble Turtle', 'Ladybug', 'Sauterelle Prince', 'Rose Crane', 'Lark Dancer', 'Cruel Penguin', 'Killer Bee', 'Sombre Corbeau', 'Humble Falcon', 'Lila Giftschlange', 'Flamme Haare', 'Blame Strumm', 'Abitante de Vulcano', 'Gloomy Violet', 'Orange A La Mode', 'Gewitterwoke', 'Forest Gorilla', 'Motor Schlange', 'Marchen Merkava', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Royal Calibur', 'Stella Nest', 'Little Briar Rose', 'Betrayal of Savior', 'Switching Contrast', 'Super Deformed'], 
    'Vatista': ['Full Art', 'Mars Black', 'Lion Falls', 'Murder Dolls', 'Aurora Blue', 'Aureolin', 'Classic White', 'Luminous Pink', 'Fallen Leaves', 'Chromium Green', 'Crimson Lake', 'Lila Colina', 'Azul Agua', 'Regalo Tierra', 'Freddo Aria', 'Grass Fairy', 'Donner Geist', 'Black Magic', 'Knospe Gardenie', 'Rain Stream', 'Flor Ciruela', 'Cassata Al Forno', 'Moonshine Blue', 'Vento Aureo', 'Angelic Gospel', 'Cyber Fairy', 'Blitzschlag', 'Mystic Doll', 'Antique Luxury', 'Modern Gloom', 'Fairy Tale', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Seth': ['Full Art', 'Shadow Approaches', 'Light is Refuse', 'Rain Murder', 'Coin and Balance', 'The Edge of Poison', 'Light in Darkness', 'Ashes Incinerator', 'Clothed in Fire', 'Natural Tree', 'Nightcap Wine', 'Coral Comet', 'Glorious Brown', 'Cosmos Black', 'Pulito Foschia', 'Cerisier', 'Ombra Abisso', 'Luna Mezzanotte', 'Mountain July', 'Sunrise Yellow', 'Hawk Sign', 'Slight Haze', 'Desert Rose', 'Lunatic Clown', 'Crimson Meteor', 'Migrotory Locust', 'Monochrome Mirage', 'Spring Blizzard', 'Ruby Ball', 'Deep Forest Venerer', 'Banded Krait', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Yuzuriha': ['Full Art', 'Chaenomeles Sinensis', 'Siberian Iris', 'Betula Grossa', 'Water Drips', 'Successful Black', 'Globe Amaranth', 'Snow Drop', 'Autumn Flower', 'Gold Rush', 'Cluster Amaryllis', 'Cherry blossom', 'Dandelion', 'Underwater Sun', 'Shrine Maiden', 'Four Leaves', 'Dies Irae', 'Golden Done', 'Twig Palm', 'Ghiaccio Luce', 'Heliconiaceae', 'The New Squad', 'Short Circuit', 'Muddied Lady', 'Sea Soldier', 'Morning Glory', 'Vermillion Eye', 'Summer Heat Haze', 'Freesia Refracta', 'Black Rabbit', 'Primrose Yellow', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors','Super Deformed'], 
    'Hilda': ['Full Art', 'Morion Black', 'Brightness Amethyst', 'Beauty of Elysion', 'Half of Indigolite', 'Fire Ruby', 'Sapphire', 'Eroded Peridot', 'Golden Beryl', 'Calm in Passion', 'Blood Andesine', 'Ice Age', 'Laurel Tiara', 'Black Crimson', 'Aquamarine', 'Forest of Witch', 'Zinnoberrot Gelb', 'Cor de Rosa', 'Cool Purple', 'Illuminate White', 'Mal Despiadado', 'Gold and Silver', 'Lava Flow', 'Astuto Signora', 'Schneefee', 'End of Fall', 'Elegant Dunkelgrum', 'Juvenile Colors', 'Spring Phantasma', 'Sapphire Splash', 'Rose Garden', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Chaos': ['Full Art', 'Prateria Lupo', 'Iceberg Lince', 'Vulcano Squalo', 'Mare Leone', 'Landa Vipera', 'Altopiano Serpente', 'Giallo Gatto', 'Verde Bestia', 'Aldebaran', 'Grazia Fuoco', 'Jellyfish', 'Cremation Heretic', 'Moos Licht', 'Eclipse Day', 'Lapis Lazuli', 'Orquidea Submundo', 'Heat Haza', 'Nuit Tonnerre', 'Ground Horizon', 'Uninhabited Island', 'Regal Crest', 'Urban Camouflage', 'Planet Snatcher', 'Daphne Gray', 'Squash Yellow', 'Grapy Amethyst', 'Unter Vulkan', 'R.Fox &amp; G.Racoon', 'Ceresso Bestia', 'A Mere Buddy', 'Super Deformed'], 
    'Nanase': ['Full Art', 'Moulin a Vent', 'Altar of Iris', 'Blitz Flugel', 'Averse Ciel', 'Katze Madchen', 'Nature Gale', 'Seesse Luna', 'Sol Envidia', 'Glicina Boton', 'Mars Soir', 'Freeze Night', 'Thin Vermilion', 'Vert Clair de Lune', 'Glamorous Aura', 'Notre Dame', 'Apricot Tea', 'Stille Vulkan', 'Briny Air', 'Winter Nacht', 'Otaria Bianco', 'Juillet Peche', 'Le Lac Des Fees', 'Insulator Girl', 'Grizzled Doe', 'Stratoshpere', 'Gingko Biloba', 'Chitose Green', 'Luft Minze', 'Depletion Garden', 'Mystique Senior', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Byakuya': ['Full Art', 'Midnight Spider', 'Hell Smoke', 'Ende Regen', 'Drought Earth', 'Rotten Pomegranate', 'Falsehood Night', 'Maple October', 'Dirty Wisteria', 'Bamboo Spear', 'Withered Lilac', 'Blue Ripple', 'Another Galaxy', 'Knight of Mercury', 'Mud Crater', 'Bottom of Abyss', 'Desert Sun', 'Flash White', 'Fullmoon Light', 'Cunning Tiger', 'Valley Magnolia', 'Spurt of Blood', 'Deep Azalea', 'Madness Glow', 'Attack of the Orange', 'Gletscher Satchel', 'Plague Soleil', 'Creeping Villain', 'Tricolor Trooper', 'Rose Thorn', 'Norland Sibling', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Phonon': ['Full Art', 'Snake Keeper', 'Purple Pain', 'Emerald Seaserpent', 'Sugar Lightning', 'Rosaceous Naga', 'Green Thorn', 'Navy Lindworm', "Aiatar's Forest", 'Fafnir Rouge', 'Goddess Underworld', 'Twilight Nidhoggur', 'Cutie Quetzalcoatl', 'Lahamu Cherry', 'Lamia Amethyst', 'Ladon Brown', 'Wish of Melusine', 'Brilliant Leviathan', 'Egger Aitvaras', 'Kukulkan Green', 'Sunburned Itzama', 'Tiny Midgard', 'Hydra Swamp', 'Punane Pisuhand', 'Blame Vouivre', 'Azzurro Amphisbaena', 'Blessed Itzanma', 'Ouroboros Hue', 'Red Castle', 'Coatlicue Harvest', 'Hoydenish Breeze', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Mika': ['Full Art', 'Firmament Bullet', 'Rose Jasper', 'Frisches Grun', 'Lowenzahn', 'Impish Lightning', 'Swimmy Azure', 'Black Diamond', 'Energy Sign', 'Petty Rose', 'Vinous Arm', 'Sunny Promenade', 'Queen Valet', 'Fragrant Green', 'Meteor Impact', 'Sunglow Cloud', 'Petite Tigre', 'Sea of Tranquility', 'Puppyish Girl', 'Spicy Crab', 'Glacial Blow', 'Immeasurable Comet', 'Secret Garden', 'Sorrent Gold', 'Plic Ploc', 'Dragon Bless', 'Tiny Dwarf', 'Midnight Sun', 'Radiant Gauntlet', 'Electroactuation', 'Lucky Clover', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Wagner': ['Full Art', 'Judgement Blazer', 'White Lily', 'Viking Blue', 'Dark Nebula', 'Sharply Uvarovite', 'Abyss Walker', 'Eschscholtzia', 'Shadowy Iris', 'Beauty Gladiator', 'Vermillion Edge', 'Eis Herrscher', 'Bloodlust', 'Rapturous Green', 'Hazy Moon Night', 'Tiefsee Botschafter', 'Noble Fencer', 'Vivid Scarlet', 'Amethyst Sowrd', 'Sand Rose', 'Rage of Nature', 'Schelt Frau', 'Nacht Garten', 'Sakura Blade', 'Sacred Sabre', 'Autumn Abundance', 'Maidenly Rose', 'Dripping Blood', 'Icicle Pink', 'Vidofnir Feather', 'Longevity Witch', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Enkidu': ['Full Art', 'Saika Kissui', 'Sekishu Kuuken', 'Ryokurin Hakuha', 'Uguisu', 'Shiden Seisou', 'Kaikatsu Tenkuu', 'Jinrai Furetsu', 'Meimei Hakuhaku', 'Kakou Ryuryoku', 'Netsugan Reitei', 'Suo', 'Masuhana', 'Hakusha Seisyo', 'Akesumire', 'Nobori Arashi', 'Hanada Kohaku', 'Sakura Mochi', 'Koujin Banjo', 'Awa Chidori', 'Tanpopo', 'Ume Murasaki', 'Seiten Hekireki', 'Raitou Unpon', 'Yama Budo', 'Hanarokusyo', 'Akane Aokachi', 'Kaisei Sanmei', 'Tsuki Some', 'Aoni Fukahi', 'Tansyo Noumatsu', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Londrekia': ['Full Art', 'Frosty Knight', 'Moon Shade', 'Imperial Jade', 'Bernstein', 'Tranquille Mauve', 'Prototype Executor', 'Blood Oath', 'Glacier Light', 'Assassins Edge', 'Glimpse of Devil', 'Antarctic Emperor', 'Cyanotype', 'Vampire Lord', 'Sherwood Shooter', 'Dokkalfar', 'Visonary Myst', 'Rosa Moyesii', 'Zeit ist Geld', 'Styx Driftice', 'Celestial Nation', 'Jung Monarch', 'Morning Dew', 'Fruhling Nacht', 'Flugel Ritter', 'Eschatos Daylight', 'Military Officer', 'Ice Magician', 'Heartless Fellow', 'End of October', 'Grape Sherbert', 'Super Deformed'], 
    'Eltnum': ['Full Art', 'Alchemist', 'Black Barrel', 'Fleeting Lover', 'Great Sphynx', 'Fang and Nail', 'Transylvania Ghost', 'Wing of Horus', 'Aswan Falucca', 'Psycho Garden', 'Living Dead', 'Dunkelheit', 'Burn Gem', 'Nostalgia', 'Silence Iceberg', 'Neo Venus', 'Bello Girasole', 'Summer Vacation', 'Amore Pesco', 'Jet Black', 'Snow Fairy', 'Celadon Narcissus', 'Nile Over Knee', 'Girl Scout', 'Somei Yoshino', 'Desert Platoon', 'Blanc Neige', 'Gloom Neon', 'Peacock Leaf', 'Vivid Navy Blue', 'Phantasmal Candle', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed'], 
    'Akatsuki': ['Full Art', 'Blanc Rouge', 'Strong Red', 'Freeze Crest', 'Vestige Garrigue', 'Idesl Empire', 'Snow Harbor', 'Neve Tempo', 'June Sprout', 'Viola Notte', 'Puro Vizio', 'Pond Mars', 'Neve Granulosa', 'Smaragd Fluss', 'Cloudy Weather', 'Primerose Flavor', 'Wildness Parakeet', 'Landa Sereno', 'Glanz Eis', 'Crepuscolo Lampo', 'Diablo Noche', 'Marine Striker', 'Living God', 'Pixy Pink', 'Western Traveler', 'Noix Rouge', 'Fighting Blaster', 'March Into Snow', 'Oceanic Depths', 'Aufblitzen Motor', 'Dunkel Motor', 'Equatorial Wave', 'Inferno Blaze', 'Annular Eclipse', 'Seeds of Heaven', 'Clamorous Colors', 'Super Deformed']}

    def randchar(n=None) :
        c = random.choice(list(C.keys()))
        #c = "Merkava"
        if n is None :
            n = random.randint(1,len(C[c])-2)
            #n = len(C[c])-1
            n = 0
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
             "game" : "uni"
             }
    cc1 = (50, 20, 90)
    cc2 = (200, 90, 255)
    bsq = False
    """

    """
    import random
    C = ['Akane', 'Akiko', 'Ayu', 'Doppel', 'Ikumi', 'Kanna', 'Kano',
         'Kaori', 'Mai', 'Makoto', 'Mayu', 'Minagi', 'Mio', 'Misaki',
         'Mishio', 'Misuzu', 'Mizuka', 'Nayuki (asleep)', 'Nayuki (awake)',
         'Rumi', 'Sayuri', 'Shiori', 'UNKNOWN']
    def randchar(n=None) :
        c = random.choice(C)
        if n is None :
            n = random.randint(1,6)
            #n = len(C[c])-1
            #n = 0
        #n = os.path.join("efzpal", str(n)+".pal")
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
             "game" : "efz"
             }
    cc1 = (37, 53, 138)
    cc2 = (157, 202, 233)
    bsq = False
    """

    """
    import random
    C = ['Akiha', 'Aoko', 'Arcueid', 'Ciel', 'Hime', 'Hisui',
         'Koha-Mech', 'Kohaku', 'Kouma', 'Len', 'Maids', 'Mech-Hisui',
         'Miyako', 'NAC', 'Nanaya', 'Neco-Arc', 'Neco-Mech', 'Nero',
         'Powerd Ciel', 'Red Arcueid', 'Riesbyfe', 'Roa', 'Ryougi',
         'Satsuki', 'Seifuku', 'Sion', 'Tohno', 'V.Akiha', 'V.Sion',
         'Warachia', 'White Len']
    def randchar(n=None) :
        c = random.choice(C)
        if n is None :
            #n = random.randint(1,36)
            n = 0
        return (c,n)
    def randmoon(n=None) :
        C = ["Crescent", "Full", "Half"]
        c = random.choice(C)
        if n is None :
            #n = random.randint(1,36)
            n = 0
        return (c,n)
    
    texto = ["プレーヤー"+str(i) for i in range(1,9)]
    personajes = [randchar() for i in range(8)]
    twitter = ["player"+str(i) for i in range(1,9)]
    pockets = [[randmoon()] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Top Text goes here",
             "bottomtext" : "Bottom Text goes here",
             "url" : "https://top8er.com",
             "game" : "mbaacc"
             }
    cc1 = (23, 26, 69)
    cc2 = (68, 2, 6)
    bsq = False
    """

    """
    import random
    C = ['alice', 'aya', 'cirno', 'iku', 'komachi', 'marisa', 'meiling',
         'patchouli', 'reimu', 'reisen', 'remilia', 'sakuya', 'sanae',
         'suika', 'suwako', 'tenshi', 'utsuho', 'youmu', 'yukari', 'yuyuko']
    def randchar(n=None) :
        c = random.choice(C)
        if n is None : n = 0
        return (c,n)
    
    texto = ["Player "+str(i) for i in range(1,9)]
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
             "game" : "soku"
             }
    cc1 = (40, 81, 106)
    cc2 = (81, 163, 213)
    bsq = False
    """

    """
    import random
    C = ['Akira Yuki', 'Ako Tamaki', 'Asuna', 'Emi Yusa', 'Kirino Kousaka',
         'Kirito', 'Kuroko Shirai', 'Kuroyukihime', 'Mikoto Misaka',
         'Miyuki Shiba', 'Qwenthur Barbotage', 'Rentaro Satomi',
         'Selvaria Bles', 'Shana', 'Shizuo Heiwajima', 'Taiga Aisaka',
         'Tatsuya Shiba', 'Tomoka Minato', 'Yukina Himeragi', 'Yuuki Konno']
    def randchar(n=None) :
        c = random.choice(C)
        if n is None : n = 0 # random.randint(1,23)
        return (c,n)
    def randsupp() :
        C = ['Accelerator', 'Alicia', 'Boogiepop', 'Celty', 'Dokuro', 'Enju',
             'Erio', 'Froleytia', 'Haruyuki', 'Holo', 'Innocent Charm',
             'Iriya', 'Izaya', 'Kino', 'Kojou', 'Kouko', 'Kuroneko',
             'Leafa', 'LLENN', 'Mashiro', 'Miyuki', 'Pai', 'Rusian',
             'Ryuuji', 'Sadao', 'Tatsuya', 'Tomo', 'Touma', 'Uiharu',
             'Wilhelmina', 'Zero']
        return (random.choice(C), 0)
    
    texto = ["Player "+str(i) for i in range(1,9)]
    personajes = [randchar() for i in range(8)]
    twitter = ["player"+str(i) for i in range(1,9)]
    pockets = [[randsupp(), randsupp()][:random.randint(0,2)] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Top Text goes here",
             "bottomtext" : "Bottom Text goes here",
             "url" : "https://top8er.com",
             "game" : "dfci"
             }
    cc1 = (25, 25, 200)
    cc2 = (200, 25, 25)
    bsq = False
    """

    """
    import random
    C = ['Beef', 'Garlic', 'Noodle', 'Onion', 'Pork', 'Rice']
    def randchar(n=None) :
        c = random.choice(C)
        if n is None : n = 0
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
             "game" : "tla"
             }
    cc1 = (117, 60, 124)
    cc2 = (234, 121, 248)
    bsq = False
    """

    """
    import random
    C = ['Earth', 'Erile', 'Hiro', 'Hiro2', 'Jadou', 'Jadou2',
         'Krayce', 'Mayura', 'Orochimaru', 'Roze', 'Ryuken', 'Welles']
    def randchar(n=None) :
        c = random.choice(C)
        if n is None : n = random.randint(0,5)
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
             "game" : "svs"
             }
    cc1 = (35, 63, 145)
    cc2 = (228, 193, 73)
    bsq = False
    """

    #"""
    import random
    C = ['Alex', 'Chun-Li', 'Dudley', 'Elena', 'Akuma', 'Hugo',
         'Ibuki', 'Ken', 'Makoto', 'Necro', 'Oro', 'Q', 'Remy', 'Ryu',
         'Sean', 'Twelve', 'Urien', 'Yang', 'Yun']
    def randchar(n=None) :
        c = random.choice(C)
        if n is None : n = random.randint(0,1)
        return (c,n)
    
    texto = ["Player "+str(i) for i in range(1,9)]
    personajes = [randchar(0) for i in range(8)]
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
             "game" : "3s"
             }
    cc1 = (200, 60, 20)
    cc2 = (239, 143, 23)
    bsq = True
    #"""

    import time
    t1 = time.time()
    #img = generate_banner(datos, customcolor="#00bbfa", customcolor2="#001736")# customcolor="#287346", customcolor2="#ede07c")
    img = generate_banner(datos, icon_sizes=ics, shadow=True, prmode=False,
                          custombg=cbg, blacksquares=bsq, darkenbg = darken,
                          customcolor=cc1, customcolor2=cc2,
                          font=fuente,
                          fontcolor1=fontc, fontscolor1 = fontsc,
                          fontcolor2=fontc2, fontscolor2 = fontsc2,
                          teammode=teammode
                          )
    t2 = time.time()
    print(t2-t1)
    img.show()
    img.save("sample.png")

    input()

