import os

from .utils.font import draw_text, has_glyph, best_font, fitting_font, fit_text
from .utils.efz import efz_palette, efz_swap
from .utils.team_mode import team_portrait

from PIL import Image, ImageDraw, ImageFont


def generate_banner(data, prmode=False, blacksquares=True,
                    custombg=None, darkenbg=True,
                    customcolor=None, customcolor2=None,
                    font=None, teammode=False,
                    font_color1=(255,255,255), font_shadow1=(0,0,0),
                    font_color2=(255,255,255), font_shadow2=(0,0,0),
                    shadow=True, icon_sizes=(32, 64)) :
    """
    Generates a top 8 graphic with the given parameters.
  
    Parameters:
    data (dict): Dictionary of tournament results with the following structure
        players: List of dicts that contain player data with the following structure
            tag: Player's gamer tag
            twitter: Player's twitter username
            char: (str, int) with the player's main character and index of alt skin
            secondaries: list of up to 2 secondary characters (str, int)
        toptext: Text to be displayed on the top left of the graphic
        bottomtext: Text to be displayed on the bottom left of the graphic
        url: URL of the tournament (top right text)
        game: Short hand of the game (matching the assets folder)
    prmode (bool): If True, placing numbers go from 1 to 8 (no 5th ot 7th ties)
    blacksquares (bool): Puts a solid black square behind each character if True
    custombg (TextIOWrapper): Custom background image file
    darkenbg (bool): Makes the background slightly darker (only if custom)
    customcolor1 (tuple): Main layout color (can also be an RGB string)
    customcolor2 (tuple): Hightlight layout color (can also be an RGB string)
    font (str): Path to the font. If not given, one is selected automatically
    teammode (bool): Experimental. Puts 2 or 3 characters in a single square.
    font_color1 (tuple): Font color for player names, twitter handles and standings
    font_shadow1 (tuple): Shadow color for player names, twitter handles and standings
    font_color2 (tuple): Font color for corner text
    font_shadow2 (tuple): Shadow color for corner text
    shadow (bool): If true, draws a colored shadow behind each character
    icon_sizes (tuple): Overrides default icon sizes (big, small and medium)
  
    Returns:
    Image: PIL Image of the top 8 graphic
    """
    game = data["game"]
    players = data["players"]

    # Getting the path of the current file
    path = os.path.realpath(__file__)
    path = os.path.abspath(os.path.join(path, os.pardir))
    # Path to the template directory
    template = os.path.join(path, "template")
    if font :
        # Path to the font file, if given
        the_font = os.path.join(path, 'fonts', font)
    else :
        # Choosing the best font based on the amount of missing special characters
        text_blob = data["toptext"]+data["bottomtext"]+data["url"]
        for player in data['players'] :
            text_blob += player['tag']
        font_option1 = os.path.join(path, 'fonts','DFGothic-SU-WIN-RKSJ-H-01.ttf')
        font_option2 = os.path.join(path, 'fonts','sansthirteenblack.ttf')
        the_font = best_font(text_blob, font_option1, font_option2)
    # Paths to assets
    portraits = os.path.join(path, "assets", game, "portraits")
    icons = os.path.join(path, "assets", game, "icons")

    # Constants
    SIZE = (1423,800) # Size of the whole cambas
    BIG = (482, 482) # Size of the biggest character square (1st place)
    MED = (257, 257) # Size of the medium character squares (2nd to 4th places)
    SMA = (191, 191) # Size of the small character squares (5th place and lower)
    # Position of the top left pixel of each square
    POS = [(53, 135), (553, 135), (831, 135), (1110, 135),
           (553, 441), (760, 441), (968, 441), (1176, 441)]
    # Size of twitter boxes
    SIZETWI = [(483, 39), (257, 29), (257, 29), (257, 29),
               (192, 26), (192, 26), (192, 26), (192, 26)]
    # Position of the top left pixel of each twitter box
    POSTWI = [(52, 624), (552, 398), (831, 398), (1109, 398),
              (552, 637), (759, 637), (967, 637), (1175, 637)]
    # Position of texts in the corner
    POSTXT = [(53, 45), (53, 730), (875, 50), (1075, 725)]
    # The final image will be stored in this image
    canvas = Image.new('RGBA', SIZE, (0, 0, 0))

    # Background
    if custombg :
        background = Image.open(custombg, mode="r")
        width, height = background.size
        w, h = int(width*SIZE[1]/height), int(height*SIZE[0]/width)
        if w < SIZE[0] :
            width, height = SIZE[0], h
        else :
            width, height = w, SIZE[1]
        # Resizing the background to fit the canvas
        background = background.resize((width, height), resample=Image.ANTIALIAS)
        canvas.paste(background, (int((SIZE[0]-width)/2), int((SIZE[1]-height)/2)) )
        if darkenbg :
            background = Image.new('RGBA', SIZE, (0, 0, 0, 0))
            canvas = Image.blend(canvas, canvas, 0.30)
    else :
        background  = Image.open(os.path.join(path, "assets", game, "bg.png")).convert("RGBA")
        canvas.paste(background, (0,0), mask=background)

    canvas = canvas.convert('RGB')
    # Draw object, to draw text on the image
    draw = ImageDraw.Draw(canvas)

    # Portrait loop
    for i in range(8) :
        # Getting the corresponding size
        if i == 0 :
            size = BIG
        elif i < 4 :
            size = MED
        else :
            size = SMA
        # Fills the square with solid black if the option is enabled
        if blacksquares :
            shape = [POS[i], (POS[i][0]+size[0], POS[i][1]+size[1])]
            draw.rectangle(shape, fill=(0,0,0))
        # Experimental, many characters in a single square
        if teammode and len(players[i]["secondaries"]) != 0 :
            chars = [players[i]["char"]] + players[i]["secondaries"]
            portrait = team_portrait(chars, size, portraits)
        else :
            char = players[i]["char"]
            route = os.path.join(portraits, char[0])
            # EFZ palette swap
            if game == "efz" and not type(char[1]) is int and not len(char[1]) == 1 :
                base = os.path.join(route, "1.png")
                palette = os.path.join(route, "0.pal")
                portrait = efz_swap(base,
                                    palette,
                                    char[1], 
                                    akane=(char[0]=="Akane"))
                portrait = portrait.convert("RGBA").resize(size, resample=Image.ANTIALIAS)
            else :
                route = os.path.join(route, str(char[1])+".png")
                portrait = Image.open(route).convert("RGBA").resize(size, resample=Image.ANTIALIAS)
        # Character portrait shadow
        if shadow :
            if customcolor : 
                shadowcolor = customcolor
            else : 
                shadowcolor = (255, 40, 56, 255)
            # Offset of the shadow relative to the portrait portrait
            shadowpos = int(size[0]*0.03)
            if teammode :
                shadowpos //= 2
            box = (POS[i][0]+shadowpos,
                   POS[i][1]+shadowpos,
                   POS[i][0]+size[0],
                   POS[i][1]+size[1])
            cropbox = (0, 0, size[0]-shadowpos, size[1]-shadowpos)
            mask =  portrait.crop(cropbox)
            the_shadow = Image.new('RGBA', cropbox[2:], shadowcolor)
            # Using the original portrait as transparency mask
            canvas.paste(the_shadow, box, mask=mask)
        # Pasting the portrait in place
        canvas.paste(portrait, POS[i], mask=portrait)

        # Secondary and tertiary character icons
        if not teammode :
            char_offset = 0
            for char in players[i]['secondaries'] :
                try :
                    route = os.path.join(icons, char[0], str(char[1])+".png")
                    icon = Image.open(route).convert("RGBA")
                    if size != BIG :
                        i_size = icon_sizes[1]
                        if size == MED :
                            right_margin = 8
                        else :
                            right_margin = 6
                    else :
                        i_size = icon_sizes[0]
                        rmarg = 14
                    icon = icon.resize((i_size, i_size),resample=Image.ANTIALIAS)
                    canvas.paste(icon, 
                                (POS[i][0]+size[0]-i_size-right_margin, 
                                POS[i][1]+s_offset*(i_size+4)+right_margin), 
                                mask=icon)
                    char_offset += 1
                except Exception as e :
                    print(e, str(route))

    # Layout parts
    part  = Image.open(os.path.join(template,"marco.png"))
    if customcolor :
        solid = Image.new('RGB', SIZE, customcolor)
        canvas.paste(solid, (0,0), mask=part)
    else :
        canvas.paste(part, (0,0), mask=part)

    part = Image.open(os.path.join(template,"polo.png"))
    if customcolor2 :
        solid = Image.new('RGB', SIZE, customcolor2)
        canvas.paste(solid, (0,0), mask=part)
    else :
        canvas.paste(part, (0,0), mask=part)

    if prmode :
        part = Image.open(os.path.join(template,"numerospr.png"))
    else :
        part = Image.open(os.path.join(template,"numeros.png"))

    if font_color1 != (255, 255, 255) and font_color1 != "#ffffff" :
        mask = part
        part = Image.new('RGBA', SIZE, font_color1)
    else :
        mask = part

    canvas.paste(part, (0,0), mask=mask)

    # Corner texts
    font_instance = ImageFont.truetype(the_font, 30)
    # Top and bottom texts
    fit_text(draw, (53, 45, 803, 80), data["toptext"], the_font,
             align="left", alignv="middle", fill=font_color2, shadow=font_shadow2)
    fit_text(draw, (53, 730, 997, 765), data["bottomtext"], the_font,
             align="left", alignv="middle", fill=font_color2, shadow=font_shadow2)
    font_instance = ImageFont.truetype(the_font, 25)
    urlmarg = (40-len(data["url"]))*6
    # Credits and url
    fit_text(draw, (1075, 726, 1361, 778), "Design by:  @Elenriqu3\nGenerator by: @Riokaru", the_font,
             align="right", alignv="middle", fill=font_color2, shadow=font_shadow2)
    fit_text(draw, (876, 45, 1367, 80), data["url"], the_font,
             align="right", alignv="middle", fill=font_color2, shadow=font_shadow2)

    pajarito = Image.open(os.path.join(template,"pajarito.png")) # Twitter bird icon
    # Recolor bid icon if needed
    if font_color1 != (255, 255, 255) and font_color1 != "#ffffff" :
        box = Image.new('RGBA', pajarito.size, (255, 255, 255, 0))
        solid = Image.new('RGBA', pajarito.size, font_color1)
        box.paste(solid, (0,0), mask=pajarito)
        pajarito = box
    # Names loop
    for i in range(8) :
        if i == 0 : 
            size = BIG
        elif i < 4 : 
            size = MED
        else : 
            size = SMA
        # Twitter box and username
        if players[i]["twitter"] :
            if customcolor :
                color = customcolor
            else :
                color = (255, 40, 56, 255)
            # Drawing twitter box
            draw.rectangle([POSTWI[i],
                            (POSTWI[i][0]+SIZETWI[i][0],
                             (POSTWI[i][1]+SIZETWI[i][1]))],
                           fill=color
                           )
            # Twitter bird icon
            if pajarito.size[1] != SIZETWI[i][1] :
                psize = ((pajarito.size[0]*SIZETWI[i][1])//pajarito.size[1],
                         SIZETWI[i][1])
                pajarito = pajarito.resize(psize, resample=Image.ANTIALIAS)
            canvas.paste(pajarito,
                    (int(POSTWI[i][0]+SIZETWI[i][0]*0.02), POSTWI[i][1]),
                    mask=pajarito)

            left_margin = pajarito.size[0]*1.2
            top_margin = 0.1*SIZETWI[i][1]
            bottom_margin = 0.1*SIZETWI[i][1]

            twitter_box = (POSTWI[i][0]+left_margin, 
                           POSTWI[i][1]+top_margin,
                           POSTWI[i][0]+SIZETWI[i][0],
                           POSTWI[i][1]+SIZETWI[i][1]-bottom_margin)

            width = twitter_box[2]-twitter_box[0]
            height = twitter_box[3]-twitter_box[1]
            ffont = fitting_font(draw, width, height, "A!"*8, the_font, guess=54)
            # Twitter handle
            fit_text(draw, twitter_box, players[i]["twitter"], the_font, guess=54,
                     align="center", alignv="middle", forcedfont=ffont,
                     fill=font_color1, shadow=font_shadow1)

        name = players[i]["tag"].replace(". ", ".").replace(" | ", "|")

        cajita_nombre = (POS[i][0]+12, POS[i][1],
                         POS[i][0]+size[0]-12, POS[i][1]+size[1]*0.98)
        # Player name
        fit_text(draw, cajita_nombre, name, the_font, guess=int(size[0]*0.26),
                 align="center", alignv="bottom",
                 fill=font_color1, shadow=font_shadow1)

    return canvas
