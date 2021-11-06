import os
import io

from .utils.font import best_font, fitting_font, fit_text
from .utils.efz import efz_swap
from .utils.team_mode import team_portrait

from PIL import Image, ImageDraw, ImageFont
 
class RereadableFile(io.BytesIO) :
    def read(self) :
        content = super().read()
        self.seek(0)
        return content

def generate_banner(data, prmode=False, old_number_style=True, blacksquares=True,
                    custombg=None, darkenbg=True,
                    customcolor=None, customcolor2=None,
                    font=None, teammode=False,
                    font_color1=(255,255,255), font_shadow1=(0,0,0),
                    font_color2=(255,255,255), font_shadow2=(0,0,0),
                    shadow=True, icon_sizes=(64, 32),
                    default_bg="bg") :
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
        if type(font) is str :
            the_font = os.path.join(path, 'fonts', font)
        else :
            font_bytes = font.read()
            f = RereadableFile(font_bytes)
            the_font = f
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
    flags_path = os.path.join(path, "assets", "flags")

    # Constants
    SIZE = (1423,800) # Size of the whole canvas
    SIZE_SQUARE = [482, 257, 257, 257, 191, 191, 191, 191]
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
    # Boxes of texts in the corner
    POSTXT = [(53, 45, 803, 80), # top left
              (53, 730, 997, 765), # bottom left
              (1075, 726, 1361, 778), # botttom right (credits)
              (1170, 780, 1361, 795), # bottom right (credits url small)
              (876, 45, 1367, 80) # top right (url)
              ]
    POSLOGO = (53, 15) # (53, 15, 803, 125)
    SIZELOGO = (750, 110)
    # The final image will be stored in this image
    canvas = Image.new('RGBA', SIZE, (0, 0, 0))
    # Flag parametes
    FLAG_SIZE = [100, 50, 50, 50, 40, 40, 40, 40]
    FLAG_POS = [(POS[i][0]+int(SIZE_SQUARE[i]*0.95)-FLAG_SIZE[i], 
                 POS[i][1]+int(SIZE_SQUARE[i]*0.74)-FLAG_SIZE[i]) 
                 for i in range(8)]

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
            canvas = Image.blend(canvas, background, 0.30)
    else :
        background  = Image.open(os.path.join(path, "assets", game, "{}.png".format(default_bg))).convert("RGBA")
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
            if players[i]["portrait"]:
                portrait = Image.open(players[i]["portrait"]).convert('RGBA')
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
                    portrait = portrait.convert("RGBA")
                else :
                    route = os.path.join(route, str(char[1])+".png")
                    portrait = Image.open(route).convert("RGBA")

            if players[i]["portrait"]:
                # Resizing and cropping to fit the square
                portrait_width, portrait_height = portrait.size
                if portrait_width > portrait_height :
                    new_width = int((portrait_width/portrait_height)*size[1])
                    new_portrait = portrait.resize((new_width, size[1]), resample=Image.ANTIALIAS)
                    x_offset = (new_width-size[0])//2
                    new_portrait = new_portrait.crop((x_offset, 0, size[0]+x_offset, size[1]))
                elif portrait_width < portrait_height :
                    new_height = int((portrait_height/portrait_width)*size[0])
                    new_portrait = portrait.resize((size[0], new_height), resample=Image.ANTIALIAS)
                    y_offset = (new_height-size[1])//2
                    new_portrait = new_portrait.crop((0, y_offset, size[0], size[1]+y_offset))
                else :
                    new_portrait = portrait.resize(size, resample=Image.ANTIALIAS)
                portrait = new_portrait
            else :
                # Resizing to fit the square
                portrait_width, portrait_height = portrait.size
                if portrait_width > portrait_height :
                    new_portrait =  Image.new('RGBA', (portrait_width, portrait_width), (0, 0, 0, 0))
                    new_portrait.paste(portrait, (0, (portrait_width-portrait_height)//2), mask=portrait)
                elif portrait_width < portrait_height :
                    new_portrait =  Image.new('RGBA', (portrait_height, portrait_height), (0, 0, 0, 0))
                    new_portrait.paste(portrait, ((portrait_height-portrait_width)//2, 0), mask=portrait)
                else :
                    new_portrait = portrait
                portrait = new_portrait.resize(size, resample=Image.ANTIALIAS)

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

        if players[i]["flag"] or players[i]["custom_flag"]:
            if players[i]["custom_flag"]:
                flag = Image.open(players[i]["custom_flag"]).convert("RGBA")
            else:
                flag = Image.open(os.path.join(flags_path, players[i]["flag"]+".png")).convert("RGBA")
            flag_width, flag_height = flag.size
            if flag_width > flag_height :
                new_flag_width = FLAG_SIZE[i]
                new_flag_height = int((flag_height/flag_width)*FLAG_SIZE[i])
                flag_x_offset = 0
                flag_y_offset = FLAG_SIZE[i]-new_flag_height
            else :
                new_flag_height = FLAG_SIZE[i]
                new_flag_width = int((flag_width/flag_height)*FLAG_SIZE[i])
                flag_x_offset = FLAG_SIZE[i]-new_flag_width
                flag_y_offset = 0
            flag = flag.resize((new_flag_width, new_flag_height))
            canvas.paste(flag, (FLAG_POS[i][0]+flag_x_offset, FLAG_POS[i][1]+flag_y_offset), mask=flag)

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
                        right_margin = 14
                    icon = icon.resize((i_size, i_size),resample=Image.ANTIALIAS)
                    canvas.paste(icon, 
                                (POS[i][0]+size[0]-i_size-right_margin, 
                                POS[i][1]+char_offset*(i_size+4)+right_margin), 
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

    # Placing numbers
    if old_number_style:
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
    else:
        if prmode :
            placing_numbers = list(range(1,9))
        else :
            placing_numbers = [1,2,3,4,5,5,7,7]
        for i in range(8):
            fit_text(draw, (int(POS[i][0]+SIZE_SQUARE[i]*0.02), int(POS[i][1]+SIZE_SQUARE[i]*0.02),
                            POS[i][0]+int(SIZE_SQUARE[i]*0.3), POS[i][1]+int(SIZE_SQUARE[i]*0.3)), 
                    str(placing_numbers[i]), the_font,
                    align="left", alignv="top", guess=150,
                    fill=font_color1, shadow=font_shadow1)

    # Corner texts

    # Top and bottom texts
    if data["logo"]:
        logo = Image.open(data["logo"]).convert("RGBA")
        logo_width, logo_height = logo.size
        new_logo_width = SIZELOGO[0]
        new_logo_height = int(new_logo_width * logo_height/logo_width)
        if new_logo_height > SIZELOGO[1]:
            new_logo_height = SIZELOGO[1]
            new_logo_width = int(new_logo_height * logo_width/logo_height)
        print(new_logo_height, new_logo_width)
        new_logo = logo.resize((new_logo_width, new_logo_height), resample=Image.ANTIALIAS)
        canvas.paste(new_logo, (POSLOGO[0], POSLOGO[1]+(SIZELOGO[1]-new_logo_height)//2), mask=new_logo)
    else:
        fit_text(draw, POSTXT[0], data["toptext"], the_font,
                align="left", alignv="middle", fill=font_color2, shadow=font_shadow2)
    fit_text(draw, POSTXT[1], data["bottomtext"], the_font,
             align="left", alignv="middle", fill=font_color2, shadow=font_shadow2)

    # Credits
    fit_text(draw, POSTXT[2], "Design by:  @Elenriqu3\nGenerator by: @Riokaru", the_font,
             align="right", alignv="middle", fill=font_color2, shadow=font_shadow2)
    fit_text(draw, POSTXT[3], "made in www.top8er.com", the_font,
            align="right", alignv="middle", fill=font_color2, shadow=False)
    # URL
    fit_text(draw, POSTXT[4], data["url"], the_font,
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
