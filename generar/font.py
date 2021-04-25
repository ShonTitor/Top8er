from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

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