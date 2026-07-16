import math
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

def draw_text(draw, pos, text, font,
              fill=(255, 255, 255), shadow=None, shadow_offset=(0.55, 0.55),
              outline_thickness=0, outline_color=None, supersample=4, canvas=None, align="left"):
    """
    Draws text on an image on the given position, with an optional shadow
    and outline.

    If `canvas` is given, the text (and its outline/shadow) is rendered at
    `supersample` times the target resolution and then downsampled with a
    high-quality filter, so that the outline stroke and curved glyph edges
    come out smooth instead of jagged/pixelated. If `canvas` is not given,
    falls back to drawing directly with `draw` (no supersampling).

    Parameters:
    draw (ImageDraw): Draw object that will be used to render/measure the text
    pos (tuple): Coordinates in pixels where the text will be drawn
    text (str): String of text to be drawn
    font (ImageFont): Font object to be used to draw the text
    fill (tuple): Color tuple (or string) to be used as font color, defaults to white
    shadow (tuple): Color tuple (or string) to be used as font shadow color.
                    If the value is None, no shadow will be drawn.
    outline_thickness (int): Width in pixels of the outline stroke around the text.
    outline_color (tuple): Color of the outline. Defaults to `fill` if not given.
    canvas (Image): The image `draw` is bound to. Required to enable the
                    supersampled/anti-aliased rendering path.
    """
    if canvas is None:
        if shadow:
            offset_x = int((font.size**0.5)*shadow_offset[0])
            offset_y = int((font.size**0.5)*shadow_offset[1])
            draw.text((pos[0]+offset_x, pos[1]+offset_y), text, font=font, fill=shadow,
                      stroke_width=outline_thickness, stroke_fill=shadow, align=align
                      )
        draw.text(pos, text, font=font, fill=fill,
                  stroke_width=outline_thickness, stroke_fill=(outline_color or fill), align=align
                  )
        return

    shadow_pos = None
    if shadow:
        offset_x = int((font.size**0.5)*shadow_offset[0])
        offset_y = int((font.size**0.5)*shadow_offset[1])
        shadow_pos = (pos[0]+offset_x, pos[1]+offset_y)

    # Bounding box (in canvas coordinates) that needs to be covered by the
    # supersampled render: the main text plus, if present, the shadow copy.
    boxes = [draw.textbbox(pos, text, font=font, stroke_width=outline_thickness, align=align)]
    if shadow_pos:
        boxes.append(draw.textbbox(shadow_pos, text, font=font, stroke_width=outline_thickness, align=align))

    # textbbox() returns float coordinates when align is "center"/"right"
    # (multiline offsets are computed as fractional divisions) - floor the
    # mins and ceil the maxes so the layer fully covers the glyphs instead
    # of truncating them.
    x0 = math.floor(min(box[0] for box in boxes))
    y0 = math.floor(min(box[1] for box in boxes))
    x1 = math.ceil(max(box[2] for box in boxes))
    y1 = math.ceil(max(box[3] for box in boxes))

    if x1 <= x0 or y1 <= y0:
        # Nothing to draw (e.g. empty text)
        return

    width, height = x1-x0, y1-y0
    big_font = ImageFont.truetype(font.path, int(font.size*supersample))

    layer = Image.new('RGBA', (width*supersample, height*supersample), (0, 0, 0, 0))
    layer_draw = ImageDraw.Draw(layer)

    if shadow_pos:
        shadow_layer_pos = ((shadow_pos[0]-x0)*supersample, (shadow_pos[1]-y0)*supersample)
        layer_draw.text(shadow_layer_pos, text, font=big_font, fill=shadow,
                         stroke_width=outline_thickness*supersample, stroke_fill=shadow, align=align)

    text_layer_pos = ((pos[0]-x0)*supersample, (pos[1]-y0)*supersample)
    layer_draw.text(text_layer_pos, text, font=big_font, fill=fill,
                     stroke_width=outline_thickness*supersample, stroke_fill=(outline_color or fill), align=align)

    layer = layer.resize((width, height), resample=Image.LANCZOS)
    canvas.paste(layer, (x0, y0), mask=layer)


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


def fitting_font(draw, width, height, text, fontdir, guess, min_size=None, max_size=None) :
    """
    Returns the font object with the biggest size that
    would fit for a given text inside the given dimensions.

    Parameters:
    draw (ImageDraw): Draw object to calculate how much space the text takes
    width (int): Maximum width of the text (in pixels)
    height (int): Maximum height of the text (in pixels)
    fontdir (path): Path to the font file to be tested
    guess (int): Upper bound to the font size
    min_size (int): If given, never return a font smaller than this, even if
                     the text would then overflow the box (a readability
                     floor takes priority over strictly fitting the box).
    max_size (int): If given, never return a font bigger than this, so a
                     short string doesn't blow up just because the box has
                     room to spare in both dimensions.

    Returns:
    TTFont: Font object with the biggest size that would fit in the box
    """
    lo = 1
    hi = guess if max_size is None else min(guess, max_size)
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
    if min_size is not None and font.size < min_size:
        font = ImageFont.truetype(fontdir, min_size)
    return font

   
def fit_text(draw, box, text, fontdir, guess=30, align="left", alignv="top",
             fill=(255, 255, 255), shadow=(0,0,0), shadow_offset=(0.55, 0.55), forcedfont=None,
             outline_thickness=0, outline_color=None, canvas=None,
             min_font_size=None, max_font_size=None):
    """
    Draws text to an image with the biggest possible font size
    to fit inside a giving rectangle.

    Parameters:
    draw (ImageDraw): Draw object that will be used to render the text on the image
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
    canvas (Image): The image `draw` is bound to. If given, enables the
                    supersampled/anti-aliased rendering path (see draw_text).
    min_font_size (int): Floor for the auto-fit font size (see fitting_font).
    max_font_size (int): Ceiling for the auto-fit font size (see fitting_font).
    """
    x1,y1,x2,y2 = box
    # width and height of the bounding box
    width, height = (x2-x1, y2-y1)

    if forcedfont is None :
        # If forcedfont was not given, calculate the appropriate font size
        fuente = fitting_font(draw, width, height, text, fontdir, guess,
                               min_size=min_font_size, max_size=max_font_size)
    else :
        # If forcedfont was given, use it instead
        fuente = forcedfont
    # Bounding box of the glyphs (including the outline stroke, if any)
    # relative to a (0,0) draw origin. left/top are usually non-zero (font
    # bearing), meaning ink drawn at position P actually starts at
    # P + (left, top), not at P itself.
    left, top, right, bottom = draw.textbbox((0, 0), text, font=fuente, stroke_width=outline_thickness, align=align)
    x, y = right-left, bottom-top
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

    # Compensate for bearing so the glyphs' actual ink lands at (posx, posy),
    # not the nominal draw position.
    draw_pos = (posx - left, posy - top)

    draw_text(draw, draw_pos, text, fuente, fill=fill, shadow=shadow, shadow_offset=shadow_offset,
              outline_thickness=outline_thickness, outline_color=outline_color, canvas=canvas, align=align)