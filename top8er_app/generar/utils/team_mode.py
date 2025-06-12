import os

from PIL import Image

def team_portrait(chars, size, portraits_path):
    portrait = Image.new("RGBA", size, color=(255,255,255,0))
    # Iterating for each character
    for j in range(len(chars)) :
        char = chars[j]
        # Path to the current charactr portrait
        path = os.path.join(portraits_path, char[0], str(char[1])+".png")

        if len(chars) == 3 :
            newsize = int(0.7*size[0])                    
            d2 = Image.open(path).convert("RGBA").resize((newsize, newsize))
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
            d2 = Image.open(path).convert("RGBA").resize((newsize, newsize))
            offset = 0.06
            m = 0.6
            if j == 0 :
                position = (-int(size[0]*offset), size[0]-newsize)
                base = size[0]-m*size[0]
                is_out = lambda t : t[0]-t[1] > base
            elif j == 1 :
                position = (size[0]-newsize+int(size[0]*offset), 15)
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
        portrait.paste(d3, (0,0), d3)
        
        j += 1
    return portrait