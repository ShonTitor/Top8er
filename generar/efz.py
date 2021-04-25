from PIL import Image

def efz_palette(path) :
    """
    Reads an EFZ .pal file and returns a list of its colors.
  
    Parameters:
    path (str): Path to the .pal file, can also be a file handle
  
    Returns:
    list: List of RGB color tuples read from the .pal file
    """
    if type(path) is str :
        # If a path is given, open the file
        palette = open(path, "rb")
    else :
        # If a file handle is give, leave as is
        palette = path
    # Read the binary data of the palette file
    data = palette.read()
    palette.close()
    colors = []
    color = []
    # Iterate for each byte in the data
    for i in range(1, len(data)) :
        color.append(s[i])
        # Every 3 bytes read are a color
        if i%3 == 0 :
            color = tuple(c[::-1])
            colors.append(c)
            color = []
    # If less than 40 colors were read, complete it with black
    if len(colors) < 40 :
        colors += [(0,0,0)]*(len(colors)-40)
    return colors


def efz_swap(file, pal1, pal2, akane=False) :
    """
    Swaps the palette of an EFZ sprite.
  
    Parameters:
    file (str): Path to the base sprite
    pal1 (str): Path to the .pal of the base sprite
    pal2 (str): Path to the palette to be applied
  
    Returns:
    list: List of RGB color tuples read from the .pal file
    """
    img = Image.open(file) # Base image
    orig = efz_palette(pal1) # Base palette
    new = efz_palette(pal2) # Palette to apply

    # Akane has some color conflicts
    if akane :
        orig = orig[:29]
        new = new[:29]
    # Alternative solution to Akane's problem
    #orig = orig[::-1]
    #new = new[::-1]

    # Dictionary where keys are the colors of the original palette
    # and values are their indices
    orig_dict = {orig[i]:i for i in range(len(orig))}
    # This list will contain on the position i, 
    # the coordinates of all pixels on the base image 
    # that match the ith color of the base palette
    match = [[] for o in orig]

    w,h = img.size
    # For each pixel
    for x in range(w) :
        for y in range(h) :
            color = img.getpixel((x,y))
            # We save the color on the matching bucket
            if color[:3] in orig_dict :
                match[orig_dict[color[:3]]].append((x,y))
    # Recoloring the base
    for i in range(len(match)) :
        for pixel in match[i] :
            alpha = img.getpixel(pixel)[3:]
            img.putpixel(pixel, new[i]+alpha)

    return img