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