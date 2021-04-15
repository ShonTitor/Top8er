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
                    offset = 0.06
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
            if teammode :
                shadowpos //= 2

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
