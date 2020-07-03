from PIL import Image, ImageDraw, ImageFont
import os

def draw_text(img, draw, pos, texto, font=None, fill=None,
              halo=True, shadow=True) :
    if shadow :
        #offset = int(font.size*0.06)
        offset = int((font.size**0.5)*0.8)
        draw.text((pos[0]+offset, pos[1]+offset), texto, font=font, fill=(0,0,0))
    draw.text(pos, texto, font=font, fill=fill)

def halve(t, n=2) :
    if type(t) is tuple : return (t[0]//n, t[1]//n)
    elif type(t) is list :
        t2 = []
        for i in t :
            t2.append(halve(i,n))
        return t2

def generate_banner(datos, custombg=None, customcolor=None, customcolor2=None,
                    fontcolor=(255,255,255), shadow=True) :
    players = datos["players"]

    path = os.path.realpath(__file__)
    path= os.path.abspath(os.path.join(path, os.pardir))
    template = os.path.join(path, "template")
    fonttc = os.path.join(path, "font.ttc")

    # Constantes
    portraits = os.path.join(path, "Fighter Portraits")
    SIZE = (5692,3200)
    HALF = (SIZE[0]//2, SIZE[1]//2)

    BIG = (1910, 1910)
    MED = (1031, 1031)
    SMA = (769, 769)

    POS = [(211, 541), (2211, 540), (3325, 540), (4438, 540),
           (2208, 1763), (3038, 1763), (3869, 1763), (4700, 1763)]

    SIZETWI = [(1932,159), (1031, 117), (1031, 117), (1031, 117),
               (771, 104), (771, 104), (771, 104), (771, 104)]

    POSTWI = [(211, 2496), (2211, 1592), (3325, 1592), (4438, 1592),
              (2208, 2551), (3038, 2551), (3869, 2551), (4700, 2551)]

    POSTXT = [(100, 100), (100, 3025), (3400, 110), (4300, 2900)]

    half = False
    if half :
        SIZE = halve(SIZE)
        BIG = halve(BIG)
        MED = halve(MED)
        SMA = halve(SMA)
        POS = halve(POS)
        POSTWI = halve(POSTWI)
        POSTXT = halve(POSTXT)

    # La que tal
    c = Image.new('RGBA', SIZE, (0, 0, 0, 0))

    # Fondo
    a  = Image.open(os.path.join(template,"bg.png"))
    c.paste(a, (0,0), mask=a)

    if custombg :
        f = Image.open(os.path.join(template, custombg))
        ancho, largo = f.size
        ancho, largo = SIZE[0], int(ancho*SIZE[0]/ancho)
        f = f.resize((ancho, largo), resample=Image.ANTIALIAS)
        c.paste(f, (0,int((SIZE[1]-largo)/2)))
        f = Image.new('RGBA', SIZE, (0, 0, 0, 180))
        c.paste(f, (0,0), mask=f)

    # Pa escribir
    draw = ImageDraw.Draw(c)

    # Ciclo de portraits
    for i in range(8) :
        if i == 0 : size = BIG
        elif i < 4 : size = MED
        else : size = SMA

        shape = [POS[i], (POS[i][0]+size[0], POS[i][1]+size[1])]
        draw.rectangle(shape, fill=(0,0,0))

        char = players[i]["char"]
        ruta = os.path.join(portraits, char[0])
        ruta = os.path.join(ruta, str(char[1])+".png")
        d = Image.open(ruta).resize(size, resample=Image.ANTIALIAS)
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

    a = Image.open(os.path.join(template,"numeros.png"))
    c.paste(a, (0,0), mask=a)

    # Textos de arriba y abajo
    fuente = ImageFont.truetype(fonttc, 120)
    draw_text(c, draw, POSTXT[0], datos["toptext"], font=fuente, fill=fontcolor, shadow=True)
    draw_text(c, draw, POSTXT[1], datos["bottomtext"], font=fuente, fill=fontcolor, shadow=False)

    fuente = ImageFont.truetype(fonttc, 100)
    urlmarg = (40-len(datos["url"]))*25
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
                pajarito = pajarito.resize(psize)
            c.paste(pajarito,
                    (int(POSTWI[i][0]+SIZETWI[i][0]*0.02), POSTWI[i][1]),
                    mask=pajarito)

            #a  = Image.open(os.path.join(template,"t"+str(i)+".png"))
            #c.paste(a, (0,0), mask=a)


            lon = len(players[i]["twitter"])
            sizef = (110*SIZETWI[i][1])//SIZETWI[0][1]
            tmarg = (25*SIZETWI[i][1])//SIZETWI[0][1]
            lmarg = (SIZETWI[i][0]-0.5*sizef*lon+pajarito.size[0])//2

            font = ImageFont.truetype(fonttc, sizef)
            draw_text(c, draw, (POSTWI[i][0]+lmarg, POSTWI[i][1]+tmarg),
                      players[i]["twitter"], font=font, fill=fontcolor, shadow=True)
        sizefont = int(size[0]*0.26)
        texto = players[i]["tag"]
        if len(texto) > 7 :
            sizefont = int(sizefont*7/len(texto))
        font = ImageFont.truetype(fonttc, sizefont)
        draw_text(c, draw, (POS[i][0] + (size[0]-0.5*sizefont*len(texto))//2,
                   POS[i][1]+int(size[0]*0.995)-sizefont),
                   texto, font=font, fill=fontcolor)
    c = c.resize(halve(c.size, 4), resample=Image.ANTIALIAS)
    return c

if __name__ == "__main__":
    # datos y configuración

    custombg = "bgusb.jpg"
    customcolor = (255, 201, 14)
    fontcolor = (255,255,255)
    shadow = True

    """
    texto = ["Morrocoyo", "Morrocoyoo","Morrocoyooo", "Morrocoyoooo",
             "Morrocoyooooo", "Morrocoyoooooo", "Morrocoyooooooo",
             "Morrocoyoooooooo"]
    texto = ["$Scruzz" for i in range(8)]
    texto = ["Morrocoyo", "Garu", "Vexx", "Kellios",
             "CarvaGrease", "Luigic7", "Lalter", "CartezSoul"]
    texto = ["$Cruz", "SexCruz", "XXXCruz", "Scruz",
             "CCruz", "ZCruz", "KCruz", "QKCruz"]
    personajes = [("Banjo & Kazooie", 0),
                  ("Incineroar", 2),
                  ("Terry", 1),
                  ("Piranha Plant", 0),
                  ("Dark Samus", 2),
                  ("Dr Mario", 4),
                  ("Captain Falcon", 4),
                  ("Yoshi", 1)]
    """

    """
    texto = ["morrocoYo", "GARU", "Pancakes", "VeXx",
             "BTO", "Vunioq", "Nandok", "Kellios"]
    #texto = ["ElMatadorDeBarquisimeto69" for i in range(8)]
    #texto = ["A" for i in range(8)]
    personajes = [("Robin", 0),
                  ("Joker", 0),
                  ("Inkling", 5),
                  ("Inkling", 2),
                  ("Mr Game and Watch", 0),
                  ("Samus", 0),
                  ("Sonic", 1),
                  ("Terry", 0)]
    twitter = ["@DanielRimeris", "@GARU_Sw", "@movpancakes", "@RisingVexx",
               "@HoyerBTO", "@Vunioq", "@Nandok_95", "@CarlosDQC"]
    #twitter = ["@DanielRimeris69" for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i]} for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Show Me your Moves - Ultimate Singles - Top 8",
             "bottomtext" : "22 de Febrero de 2020 - Caracas, Venezuela - 89 participantes",
             "url" : "facebook.com/groups/smashvenezuela",
             }
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

    texto = [s[:-1] for s in ["Min "*(i+1) for i in range(8)]]
    personajes = [("Min Min", i) for i in range(8)]
    twitter = ["MinMin0"+str(i+1) for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i]} for i in range(8)]
    datos = {"players" : players,
             "toptext" : "Min Min Min Min Min Min Min Min",
             "bottomtext" : "Min Min Min Min Min Min Min Min",
             "url" : "http://riokaru.pythonanywhere.com/",
             }

    import time
    t1 = time.time()
    img = generate_banner(datos, customcolor="#00bbfa", customcolor2="#001736")# customcolor="#287346", customcolor2="#ede07c")
    t2 = time.time()
    print(t2-t1)
    #img = img.resize(halve(img.size))
    img.show()
    img.save("derp.png")

    input()
