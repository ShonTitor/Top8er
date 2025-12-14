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

def convert_color_string_to_tuple(color_string):
    """Convert a hex color string to an RGB tuple."""
    return tuple(
        int(color_string.lstrip('#')[i:i+2], 16)
        for i in (0, 2, 4)
    )

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
        the_font = best_font(text_blob, [font_option1, font_option2])
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

    # Convert customcolors to tuples if they are strings
    if type(customcolor) is str:
        customcolor = convert_color_string_to_tuple(customcolor)
    if type(customcolor2) is str:
        customcolor2 = convert_color_string_to_tuple(customcolor2)
    
    # Calculate final canvas size (including side event if present)
    final_canvas_height = SIZE[1]
    row_height = 100
    columns = 4
    if "side_event" in data and data["side_event"]:
        side_event = data["side_event"]
        if side_event["title"] and side_event["players"]:
            num_players = len(side_event["players"])
            rows = (num_players + columns - 1) // columns
            side_event_height = 60 + (rows * row_height) + 40
            final_canvas_height = SIZE[1] + side_event_height
    
    FINAL_SIZE = (SIZE[0], final_canvas_height)
    
    # The final image will be stored in this image
    canvas = Image.new('RGBA', FINAL_SIZE, (0, 0, 0))
    # Flag parametes
    FLAG_SIZE = [100, 50, 50, 50, 40, 40, 40, 40]
    FLAG_POS = [(POS[i][0]+int(SIZE_SQUARE[i]*0.95)-FLAG_SIZE[i], 
                 POS[i][1]+int(SIZE_SQUARE[i]*0.74)-FLAG_SIZE[i]) 
                 for i in range(8)]

    # Background
    if custombg :
        background = Image.open(custombg, mode="r")
    else :
        background  = Image.open(os.path.join(path, "assets", game, "{}.png".format(default_bg))).convert("RGBA")
    
    # Resize and crop background to fit canvas while preserving aspect ratio
    bg_width, bg_height = background.size
    scale_w = FINAL_SIZE[0] / bg_width
    scale_h = FINAL_SIZE[1] / bg_height
    scale = max(scale_w, scale_h)  # Use max to ensure full coverage
    
    new_width = int(bg_width * scale)
    new_height = int(bg_height * scale)
    
    # Resize background preserving aspect ratio
    background = background.resize((new_width, new_height), resample=Image.LANCZOS)
    
    # Crop to canvas size (center crop)
    left = (new_width - FINAL_SIZE[0]) // 2
    top = (new_height - FINAL_SIZE[1]) // 2
    background = background.crop((left, top, left + FINAL_SIZE[0], top + FINAL_SIZE[1]))
    
    # Paste background and apply effects
    if custombg and not background.mode == 'RGBA':
        background = background.convert('RGBA')
    
    canvas.paste(background, (0, 0), mask=background if background.mode == 'RGBA' else None)
    
    if custombg and darkenbg :
        darken_layer = Image.new('RGBA', FINAL_SIZE, (0, 0, 0, 0))
        canvas = Image.blend(canvas, darken_layer, 0.30)

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
                    new_portrait = portrait.resize((new_width, size[1]), resample=Image.LANCZOS)
                    x_offset = (new_width-size[0])//2
                    new_portrait = new_portrait.crop((x_offset, 0, size[0]+x_offset, size[1]))
                elif portrait_width < portrait_height :
                    new_height = int((portrait_height/portrait_width)*size[0])
                    new_portrait = portrait.resize((size[0], new_height), resample=Image.LANCZOS)
                    y_offset = (new_height-size[1])//2
                    new_portrait = new_portrait.crop((0, y_offset, size[0], size[1]+y_offset))
                else :
                    new_portrait = portrait.resize(size, resample=Image.LANCZOS)
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
                portrait = new_portrait.resize(size, resample=Image.LANCZOS)

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
                    icon = icon.resize((i_size, i_size), resample=Image.LANCZOS)
                    canvas.paste(icon, 
                                (POS[i][0]+size[0]-i_size-right_margin, 
                                POS[i][1]+char_offset*(i_size+4)+right_margin), 
                                mask=icon)
                    char_offset += 1
                except Exception as e :
                    pass
                    #print(e, str(route), "perro")

    # Layout parts consisting of the portrait borders and swash.
    # The swash is the decorative border
    #   at the top-left and bottom-right of the graphic.
    # Marco contains the portrait borders and swash fill.
    part = Image.open(os.path.join(template,"marco.png"))
    if customcolor:
        solid = Image.new('RGB', SIZE, customcolor)
        canvas.paste(solid, (0,0), mask=part)
    else:
        canvas.paste(part, (0,0), mask=part)

    # polo contains the swash border only
    # This is so it can be colored differently if desired
    part = Image.open(os.path.join(template,"polo.png"))
    
    # Cut swash border image in half and place top half at top, bottom half at bottom
    polo_width, polo_height = part.size
    half_height = polo_height // 2
    
    # Top half of swash border
    top_half = part.crop((0, 0, polo_width, half_height))
    if customcolor2:
        solid_top = Image.new('RGB', (SIZE[0], half_height), customcolor2)
        canvas.paste(solid_top, (0, 0), mask=top_half)
    else:
        canvas.paste(top_half, (0, 0), mask=top_half)
    
    # Bottom half of swash border
    bottom_half = part.crop((0, half_height, polo_width, polo_height))
    bottom_y = FINAL_SIZE[1] - half_height
    
    # Flood fill the bottom-right area with customcolor
    if customcolor:
        # Convert bottom_half to RGBA to work with it
        bottom_half_filled = bottom_half.convert('RGBA')
        # Flood fill from bottom-right corner
        seed_x = bottom_half_filled.width - 5
        seed_y = bottom_half_filled.height - 5
        ImageDraw.floodfill(bottom_half_filled, (seed_x, seed_y), customcolor + (255,), thresh=400)
        
        # Paste the filled version
        canvas.paste(bottom_half_filled, (0, bottom_y), mask=bottom_half_filled)
    
    # Then overlay with customcolor2 (highlight color) for the border
    if customcolor2:
        solid_bottom = Image.new('RGB', (SIZE[0], half_height), customcolor2)
        canvas.paste(solid_bottom, (0, bottom_y), mask=bottom_half)
    else:
        canvas.paste(bottom_half, (0, bottom_y), mask=bottom_half)

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

    # Corner texts - will be adjusted if side event exists

    # Top text (stays at top)
    if data["logo"]:
        logo = Image.open(data["logo"]).convert("RGBA")
        logo_width, logo_height = logo.size
        new_logo_width = SIZELOGO[0]
        new_logo_height = int(new_logo_width * logo_height/logo_width)
        if new_logo_height > SIZELOGO[1]:
            new_logo_height = SIZELOGO[1]
            new_logo_width = int(new_logo_height * logo_width/logo_height)
        print(new_logo_height, new_logo_width)
        new_logo = logo.resize((new_logo_width, new_logo_height), resample=Image.LANCZOS)
        canvas.paste(new_logo, (POSLOGO[0], POSLOGO[1]+(SIZELOGO[1]-new_logo_height)//2), mask=new_logo)
    else:
        fit_text(draw, POSTXT[0], data["toptext"], the_font,
                align="left", alignv="middle", fill=font_color2, shadow=font_shadow2)
    
    # URL (stays at top right)
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
                pajarito = pajarito.resize(psize, resample=Image.LANCZOS)
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

    # Side event rendering
    if "side_event" in data and data["side_event"]:
        side_event = data["side_event"]
        if side_event["title"] and side_event["players"]:
            # Calculate side event dimensions
            side_players = side_event["players"]
            num_players = len(side_players)
            
            # Three columns layout
            rows = (num_players + columns - 1) // columns  # Ceiling division
            
            # Dimensions
            side_event_height = 100 + (rows * row_height) + 40  # Title + rows + padding
            
            # Canvas was already created with the right size, just update draw object
            draw = ImageDraw.Draw(canvas)
            
            # Position side event right after main content (twitter boxes end at ~663)
            side_event_y_start = 700

            # Draw side event title
            title_box = (50, side_event_y_start + 10, SIZE[0] - 50, side_event_y_start + 70)
            fit_text(draw, title_box, side_event["title"], the_font, guess=48,
                    align="center", alignv="middle",
                    fill=font_color1, shadow=font_shadow1)
            
            # Draw players in three columns
            player_y_start = side_event_y_start + 90
            column_width = SIZE[0] // columns - 15
            icon_size_side = 60
            
            # Load twitter icon
            twitter_icon_path = os.path.join(path, "assets", "social_icons", "twitter.png")
            try:
                twitter_icon = Image.open(twitter_icon_path).convert("RGBA")
            except:
                twitter_icon = None
            
            for idx, player in enumerate(side_players):
                col = idx % columns
                row = idx // columns
                placement_number = idx + 1
                
                x_start = col * column_width + 40
                y_start = player_y_start + (row * row_height)
                
                # Draw box around player entry
                box_padding = 5
                box_width = column_width - 20
                box_height = row_height - 20
                
                draw.rectangle([(x_start - box_padding, y_start - box_padding),
                               (x_start + box_width, y_start + box_height)],
                              outline=customcolor2, fill=customcolor, width=3)
                
                # Draw placement number
                number_box = (x_start, y_start, x_start + 30, y_start + 30)
                fit_text(draw, number_box, str(placement_number), the_font, guess=24,
                        align="center", alignv="middle",
                        fill=font_color1, shadow=font_shadow1)
                
                # Draw character icon if available
                icon_x = x_start + 35
                if player.get("char") and player["char"][0]:
                    try:
                        char_icon_path = os.path.join(icons, player["char"][0], 
                                                     str(player["char"][1]) + ".png")
                        char_icon = Image.open(char_icon_path).convert("RGBA")
                        char_icon = char_icon.resize((icon_size_side, icon_size_side), 
                                                    resample=Image.LANCZOS)
                        canvas.paste(char_icon, (icon_x, y_start), mask=char_icon)
                    except:
                        pass
                
                # Draw flag if available
                text_x = icon_x + icon_size_side + 10
                if player.get("flag") or player.get("custom_flag"):
                    try:
                        if player.get("custom_flag"):
                            flag = Image.open(player["custom_flag"]).convert("RGBA")
                        else:
                            flag = Image.open(os.path.join(flags_path, 
                                            player["flag"] + ".png")).convert("RGBA")
                        flag = flag.resize((40, 30), resample=Image.LANCZOS)
                        canvas.paste(flag, (text_x, y_start + 5), mask=flag)
                        text_x += 50
                    except:
                        pass
                
                # Draw player name
                name_box = (text_x, y_start, 
                           x_start + column_width - 20, y_start + 30)
                player_name = player["tag"]
                
                fit_text(draw, name_box, player_name, the_font, guess=24,
                        align="left", alignv="middle",
                        fill=(255, 255, 255), shadow=(0, 0, 0))
                
                # Draw twitter handle underneath if available
                if player.get("twitter"):
                    twitter_y = y_start + 32
                    twitter_x = text_x
                    
                    # Draw twitter icon
                    if twitter_icon:
                        twitter_icon_small = twitter_icon.resize((20, 20), resample=Image.LANCZOS)
                        canvas.paste(twitter_icon_small, (twitter_x, twitter_y), mask=twitter_icon_small)
                        twitter_x += 25
                    
                    # Draw twitter handle with @ sign
                    twitter_handle = "@" + player["twitter"] if not player["twitter"].startswith("@") else player["twitter"]
                    twitter_box = (twitter_x, twitter_y, 
                                  x_start + column_width - 100, twitter_y + 25)
                    fit_text(draw, twitter_box, twitter_handle, the_font, guess=18,
                            align="left", alignv="middle",
                            fill=(200, 200, 200), shadow=(0, 0, 0))
            
            # Update canvas size for bottom text positioning
            final_height = canvas.size[1]
    else:
        final_height = SIZE[1]
    
    # Draw bottom text and credits at the bottom of the (possibly extended) canvas
    bottom_text_y = final_height - 70
    credits_y = final_height - 74
    credits_url_y = final_height - 20
    
    # Bottom text
    bottom_text_box = (53, bottom_text_y, 997, bottom_text_y + 35)
    fit_text(draw, bottom_text_box, data["bottomtext"], the_font,
             align="left", alignv="middle", fill=font_color2, shadow=font_shadow2)
    
    # Credits
    credits_box = (1075, credits_y, 1361, credits_y + 52)
    fit_text(draw, credits_box, "Design by:  @Elenriqu3\nGenerator by: @Riokaru", the_font,
             align="right", alignv="middle", fill=font_color2, shadow=font_shadow2)
    
    # Credits URL
    credits_url_box = (1170, credits_url_y, 1361, credits_url_y + 15)
    fit_text(draw, credits_url_box, "made in www.top8er.com", the_font,
            align="right", alignv="middle", fill=font_color2, shadow=False)

    return canvas
