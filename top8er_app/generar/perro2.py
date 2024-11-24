import os
import io
import json
import requests
import re

try:
    from utils.font import best_font, fit_text
    from utils.efz import efz_swap
    from utils.team_mode import team_portrait
except ModuleNotFoundError:
    from .utils.font import best_font, fit_text
    from .utils.efz import efz_swap
    from .utils.team_mode import team_portrait

from PIL import Image, ImageDraw, ImageChops
 
class RereadableFile(io.BytesIO) :
    def read(self) :
        content = super().read()
        self.seek(0)
        return content

def get_image(thing, folder):
    if type(thing) is tuple:
        route = os.path.join(folder, thing[0], f"{thing[1]}.png")
        img = Image.open(route)
    elif type(thing) is str:
        url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        if re.match(url_pattern, thing):
            r = requests.get(thing, headers={'User-agent': 'Mozilla/5.0'})
            print(r.status_code)
            img = Image.open(io.BytesIO(r.content))
            #r = requests.get(thing).content
            #img = Image.open(io.BytesIO(r))
        else:
            route = os.path.join(folder, f"{thing}.png")
            img = Image.open(route)
    elif hasattr(thing, "read"):
        img = Image.open(thing)
    else:
        img = None
    return img

def resize_image(img, new_size, fit_method, align, alignv):
    width, height = img.size

    maybe_new_height = int((new_size[0] * height)/width)
    maybe_new_width = int((new_size[1] * width)/height)
    height_ratio = maybe_new_height/new_size[1]
    width_ratio = maybe_new_width/new_size[0]
    if fit_method == "fit":
        if height_ratio < 1:
            fit_method = "fit_x"
        elif width_ratio < 1:
            fit_method = "fit_y"
        elif width_ratio == 1 or height_ratio == 1:
            fit_method = "stretch"
    elif fit_method == "crop":
        if height_ratio > 1:
            fit_method = "fit_x"
        elif width_ratio > 1:
            fit_method = "fit_y"
        elif width_ratio == 1 or height_ratio == 1:
            fit_method = "stretch"

    if fit_method == "stretch":
        return img.resize(new_size, resample=Image.LANCZOS)
    elif fit_method == "fit_x":
        new_width = new_size[0]
        new_height = maybe_new_height
        new_img = img.resize((new_width, new_height), resample=Image.LANCZOS)

        if alignv == "middle":
            y = (new_height - new_size[1])//2
        elif alignv == "bottom":
            y = new_height - new_size[1]
        else:
            y = 0
        if new_height > new_size[1]:
            new_img = new_img.crop((0, y, new_width, y+new_size[1]))
        elif new_height < new_size[1]:
            y = -y
            canvas = Image.new('RGBA', new_size, (0, 0, 0, 0))
            canvas.paste(new_img, (0, y), mask=new_img)
            new_img = canvas
        return new_img
    elif fit_method == "fit_y":
        new_height = new_size[1]
        new_width = maybe_new_width
        new_img = img.resize((new_width, new_height), resample=Image.LANCZOS)

        if align == "center":
            x = (new_width - new_size[0])//2
        elif align == "right":
            x = new_width - new_size[0]
        else:
            x = 0
        if new_width > new_size[0]:
            new_img = new_img.crop((x, 0, x+new_size[0], new_height))
        elif new_width < new_size[0]:
            x = -x
            canvas = Image.new('RGBA', new_size, (0, 0, 0, 0))
            canvas.paste(new_img, (x, 0), mask=new_img)
            new_img = canvas
        return new_img
    return img

def evaluate_str_exp(strexp, player_data, options, layer, player_index, multiple_index):
    if type(strexp) is not str:
        return strexp
    
    multiple = layer.get("multiple", False) and multiple_index is not None

    value = None
    if strexp.startswith("$"):
        name = strexp[1:]
        value = options.get(name)
    elif strexp.startswith("%"):
        name = strexp[1:]
        if multiple:
            value = player_data[name][multiple_index]
        else:
            value = player_data.get(name)
    else:
        value = strexp

    return value

def evaluate_path_exp(pathexp, path_dict):
    if pathexp.startswith("@"):
        return path_dict.get(pathexp, pathexp)
    return os.path.join(path_dict["@template"], pathexp)

def evaluate_attribute(attribute, data, layer, player_index, multiple_index):
    if attribute not in layer:
        return

    multiple = layer.get("multiple", False) and multiple_index is not None

    player_data = None
    if player_index is not None:
        player_data = data["players"][player_index]

    options = data["options"]

    attrs = layer[attribute]

    strexp = None
    if type(attrs) is not list:
        strexp = attrs
    elif multiple:
        if player_index is not None:
            strexp = attrs[player_index][multiple_index]
        else:
            strexp = attrs[multiple_index]
    else:
        if player_index is not None:
            strexp = attrs[player_index]
        else:
            strexp = attrs  

    return evaluate_str_exp(strexp, player_data, options, layer, player_index, multiple_index)

def get_attr_fun(data, layer, player_index, multiple_index):
    def get_attr(attr, default=None):
        val = evaluate_attribute(attr, data, layer, player_index, multiple_index)
        if val is None:
            return default
        return val
    return get_attr

def draw_image_layer(canvas, layer, data, path_dict, player_index=None, multiple_index=None):
    get_attr = get_attr_fun(data, layer, player_index, multiple_index)

    condition = get_attr("condition", True)
    if not condition:
        return

    file_path = evaluate_path_exp(layer.get("source_folder", "@template"), path_dict)

    image_type = get_attr("image_type")
    if image_type:
        file_path = os.path.join(file_path, image_type)
    
    name = get_attr("name")
    if name:
        part = get_image(name, file_path)
    elif "filename" in layer:
        filename = get_attr("filename")
        if filename is None:
            return
        part  = Image.open(os.path.join(file_path, filename))
    else:
        return
    
    part = part.convert("RGBA")

    darken_condition = get_attr("darken_condition", False)
    if darken_condition:
        proportion = layer.get("darken_proportion", 0.3)
        black = Image.new('RGBA', part.size, (0, 0, 0, 255))
        part = Image.blend(black, part, 1-proportion)

    position = get_attr("position", (0,0))
    fit_type = get_attr("fit_type", "fit")
    align = get_attr("align", "center")
    alignv = get_attr("alignv", "middle")

    size = get_attr("size")
    if size:
        part = resize_image(part, size, fit_type, align, alignv)

    color = get_attr("color")

    ignore_colors = get_attr("ignore_recoloring_with", [])
    if color in ignore_colors:
        color = None

    enable_shadow = get_attr("shadow_condition", False)

    # Character portrait shadow
    if enable_shadow:
        size = part.size
        shadow_color = get_attr("shadow_color", (0,0,0,255))

        # Offset of the shadow relative to the portrait portrait
        shadow_offset = get_attr("shadow_offset", (0, 0))

        mask = ImageChops.offset(part, shadow_offset[0], shadow_offset[1])
        shadow_size = (size[0] - abs(shadow_offset[0]),
                        size[1] - abs(shadow_offset[1]))
        shadow_position = (position[0] + max(0, shadow_offset[0]),
                            position[1] + max(0, shadow_offset[1]))
        cropbox = (
            max(shadow_offset[0], 0),
            max(shadow_offset[1], 0),
            shadow_size[0] + max(shadow_offset[0], 0),
            shadow_size[1] + max(shadow_offset[1], 0)
        )
        mask = mask.crop(cropbox)
        shadow = Image.new('RGBA', shadow_size, shadow_color)
        canvas.paste(shadow, shadow_position, mask=mask)

    if color:
        solid = Image.new('RGB', part.size, color)
        canvas.paste(solid, position, mask=part)
    else :
        canvas.paste(part, position, mask=part)

def draw_text_layer(draw, layer, data, path_dict, fonts, player_index=None, multiple_index=None):
    get_attr = get_attr_fun(data, layer, player_index, multiple_index)

    condition = get_attr("condition", True)
    if not condition:
        return

    textbox = tuple(get_attr("textbox"))

    text = get_attr("content")
    if text is None:
        text = get_attr("name", "")

    align = get_attr("align", "center")
    alignv = get_attr("alignv", "middle")

    font_color = get_attr("font_color")

    font_shadow_condition = get_attr("font_shadow_condition", False)
        
    font_shadow_color = None
    if font_shadow_condition:
        font_shadow_color = get_attr("font_shadow_color")
        font_shadow_offset = get_attr("font_shadow_offset", [0.55, 0.55])
    else:
        font_shadow_color = None
        font_shadow_offset = None

    font = get_attr("font", "auto")
    if font not in fonts:
        font = "auto"
    font = fonts[font]

    enable_outline = get_attr("font_outline_condition", False)
    if enable_outline:
        outline_color = get_attr("font_outline_color", "#000000")
        outline_thickness = get_attr("font_outline_thickness", 1)
    else:
        outline_thickness = 0
        outline_color = None

    fit_text(draw, textbox, text, font, guess=10000,
            align=align, alignv=alignv,
            fill=font_color, shadow=font_shadow_color, shadow_offset=font_shadow_offset,
            outline_thickness=outline_thickness, outline_color=outline_color)

def draw_rectangle_layer(draw, layer, data, player_index=None, multiple_index=None):
    get_attr = get_attr_fun(data, layer, player_index, multiple_index)

    condition = get_attr("condition", True)
    if not condition:
        return

    color = get_attr("color", "#000000")

    shape = get_attr("shape")

    if shape:
        draw.rectangle(shape, fill=color)

def generate_graphic(data):

    # Getting the path of the current file
    path = os.path.realpath(__file__)
    path = os.path.abspath(os.path.join(path, os.pardir))

    # Path to the template directory
    template_name = data.get("template", "default")
    template_path = os.path.join(path, "templates", template_name)
    with open(os.path.join(template_path, "template.json"), "r") as f:
        template_data = json.loads(f.read())

    available_fonts = template_data["available_fonts"]
    fonts = {}
    for key, value in available_fonts.items():
        fonts[key] = os.path.join(template_path, value)

    # Choosing the best font based on the amount of missing special characters
    text_blob = ""
    for option in template_data["options"]:
        if option["type"] == "text":
            text_blob += data["options"][option["name"]]
    for player in data['players'] :
        text_blob += player['name']
    the_font = best_font(text_blob, list(fonts.values()))
    fonts["auto"] = the_font

    # Constants
    SIZE = template_data["canvas_size"] # Size of the whole canvas
    PLAYER_NUMBER = template_data["player_number"]

    # Settings
    game = data.get("game")
    game_path = os.path.join(path, "assets", game)
    
    flags_path = os.path.join(path, "assets", "flags")
    social_path = os.path.join(path, "assets", "social_icons")

    path_dict = {
        "@template": template_path,
        "@game": game_path,
        "@flags": flags_path,
        "@social": social_path
    }

    # The final image will be stored in this variable
    canvas = Image.new('RGBA', SIZE, (0, 0, 0))

    # Draw object, to draw text on the image
    draw = ImageDraw.Draw(canvas)

    for layer in template_data["layers"][::-1]:

        layer_type = layer["type"]

        if layer_type == "option":
            option = data["options"][layer["name"]]
            layer = layer["choices"][option]
            layer_type = layer["type"]
        
        if layer_type == "image":
            draw_image_layer(canvas, layer, data, path_dict)

        elif layer_type == "player_images":
            multiple = layer.get("multiple", False)
            if multiple:
                for i in range(PLAYER_NUMBER):
                    amount = evaluate_attribute("amount", data, layer, i, None)
                    for j in range(amount):
                        draw_image_layer(canvas, layer, data, path_dict, player_index=i, multiple_index=j)
            else:
                for i in range(PLAYER_NUMBER):
                    draw_image_layer(canvas, layer, data, path_dict, player_index=i, multiple_index=None)
        
        elif layer_type == "text":
            draw_text_layer(draw, layer, data, path_dict, fonts, player_index=None, multiple_index=None)            
            
        elif layer_type == "player_text":
            multiple = layer.get("multiple", False)
            if multiple:
                for i in range(PLAYER_NUMBER):
                    amount = evaluate_attribute("amount", data, layer, i, None)
                    for j in range(amount):
                        draw_text_layer(draw, layer, data, path_dict, fonts, player_index=i, multiple_index=j)
            else:
                for i in range(PLAYER_NUMBER):
                    draw_text_layer(draw, layer, data, path_dict, fonts, player_index=i)

        elif layer_type == "rectangle":
            draw_rectangle_layer(draw, layer, data)
        
        elif layer_type == "player_rectangles":
            multiple = layer.get("multiple", False)
            if multiple:
                for i in range(PLAYER_NUMBER):
                    amount = evaluate_attribute("amount", data, layer, i, None)
                    for j in range(amount):
                        draw_rectangle_layer(draw, layer, data, player_index=i, multiple_index=j)
            else:
                for i in range(PLAYER_NUMBER):
                    draw_rectangle_layer(draw, layer, data, player_index=i)
                    
        else:
            print("NOT IMPLEMENTED", layer_type)

    return canvas.convert("RGB")