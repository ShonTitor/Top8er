from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

def draw_text(draw, pos, text, font,
              fill=(255, 255, 255), shadow=None, shadow_offset=(0.55, 0.55),
              outline_thickness=0, outline_color=None):
    """
    Draws text on an image on the given position, with an optional shadow.
  
    Parameters:
    draw (ImageDraw): Draw object that will be used to render the text on the image
    pos (tuple): Coordinates in pixels where the text will be drawn
    text (str): String of text to be drawn
    font (ImageFont): Font object to be used to draw the text
    fill (tuple): Color tuple (or string) to be used as font color, defaults to white
    shadow (tuple): Color tuple (or string) to be used as font shadow color.
                    If the value is None, no shadow will be drawn.
    """  
    if shadow:
        offset_x = int((font.size**0.5)*shadow_offset[0])
        offset_y = int((font.size**0.5)*shadow_offset[1])
        draw.text((pos[0]+offset_x, pos[1]+offset_y), text, font=font, fill=shadow,
                  stroke_width=outline_thickness, stroke_fill=shadow
                  )

    draw.text(pos, text, font=font, fill=fill, 
              stroke_width=outline_thickness, stroke_fill=(outline_color or fill)
              )


def has_glyph(font, glyph):
    """
    Checks if a font has a given glyph.
  
    Parameters:
    font (TTFont): Font object 
    glyph (str): Single character string to be searched for
  
    Returns:
    bool: True if the font has the glyph
  
    """
    for table in font['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False


def best_font(text, fonts):
    """
    Takes a string and two fonts, returns the font with the least missing glyphs.
  
    Parameters:
    text (str): String to be checked for missing glyphs
    fonts (list): List of font file paths
  
    Returns:
    str: Path to the font with the least missing glyphs
    """
    best = fonts[0]
    best_hits = 0
    for f in fonts:
        hits = 0
        font = TTFont(f)
        for c in list(text):
            if has_glyph(font, c):
                hits += 1
        if hits > best_hits:
            best = f
            best_hits = hits

    return best


def get_text_dimensions(text_string, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text_string, font=font)
    return width, height


def fitting_font(draw, width, height, text, fontdir, guess) :
    """
    Returns the font object with the biggest size that
    would fit for a given text inside the given dimensions.
  
    Parameters:
    draw (ImageDraw): Draw object to calculate how much space the text takes
    width (int): Maximum width of the text (in pixels)
    height (int): Maximum height of the text (in pixels)
    fontdir (path): Path to the font file to be tested
    guess (int): Upper bound to the font size
  
    Returns:
    TTFont: Font object with the biggest size that would fit in the box
    """
    lo = 1
    hi = guess
    guess = (lo+hi)//2
    font = ImageFont.truetype(fontdir, guess)
    x,y = get_text_dimensions(text, font)
    # Binary search (could probably be improved by using an heuristic instead)
    lold, hiold = lo, hi
    while lo+1 < hi :
        if x > width or y > height :
            hi = guess
        else :
            lo = guess
        if (lold, hiold) == (lo, hi) :
            guess = lo
            break
        guess = (lo+hi)//2
        font = ImageFont.truetype(fontdir, guess)
        x,y = get_text_dimensions(text, font)
    return font

   
def fit_text(draw, box, text, fontdir, guess=30, align="left", alignv="top",
             fill=(255, 255, 255), shadow=(0,0,0), shadow_offset=(0.55, 0.55), forcedfont=None,
             outline_thickness=0, outline_color=None):
    """
    Draws text to an image with the biggest possible font size
    to fit inside a giving rectangle.
  
    Parameters:
    Draw object that will be used to render the text on the image
    box (tuple): bounding box for the text as a 4-tuple
    fontdir (path): Path to the font file to be used
    guess (int): Upper bound to the font size
    align (str): Horizontal align ('left', 'right' or 'center') defaults to left
    alignv (str): Vertical align ('top', 'bottom' or 'middle') defaults to top
    fill (tuple): Color tuple (or string) to be used as font color, defaults to white
    shadow (tuple): Color tuple (or string) to be used as font shadow color
                    If the value is None, no shadow will be drawn
    forcedfont (TTFont): If given, ignores fontdir and is used instead
                         No size calculations are performed in this case
    """
    x1,y1,x2,y2 = box
    # width and height of the bounding box
    width, height = (x2-x1, y2-y1)

    if forcedfont is None :
        # If forcedfont was not given, calculate the appropriate font size
        fuente = fitting_font(draw, width, height, text, fontdir, guess)
    else :
        # If forcedfont was given, use it instead
        fuente = forcedfont
    # width and height of the text
    x,y = get_text_dimensions(text, font=fuente)
    # top left corner of the bounding box
    posx, posy = x1,y1
    # Adjusting for horizontal align
    if align == "center" :
        posx += (width-x)//2
    elif align == "right" :
        posx += width-x
    # Adjusting for vertical align
    if alignv == "bottom" :
        posy += height-y
    elif alignv == "middle" :
        posy += (height-y)//2

    draw_text(draw, (posx, posy), text, fuente, fill=fill, shadow=shadow, shadow_offset=shadow_offset,
              outline_thickness=outline_thickness, outline_color=outline_color)