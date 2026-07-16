import os
import io
import json
import tempfile

try:
    from utils.font import best_font, fit_text, get_text_dimensions
    from utils.efz import efz_swap
    from utils.team_mode import team_portrait
except ModuleNotFoundError:
    from .utils.font import best_font, fit_text, get_text_dimensions
    from .utils.efz import efz_swap
    from .utils.team_mode import team_portrait

from PIL import Image, ImageDraw, ImageChops, ImageColor, ImageFont
 
class RereadableFile(io.BytesIO) :
    def read(self) :
        content = super().read()
        self.seek(0)
        return content

def get_image(thing, folder):
    if isinstance(thing, list):
        thing = thing[0] if thing else None
    if thing is None:
        return None
    if type(thing) is tuple:
        route = os.path.join(folder, thing[0], f"{thing[1]}.png")
        img = Image.open(route)
    elif type(thing) is str:
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

    negate = strexp.startswith("!")
    if negate:
        strexp = strexp[1:]

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

    return not bool(value) if negate else value

def evaluate_path_exp(pathexp, path_dict):
    if pathexp.startswith("@"):
        return path_dict.get(pathexp, pathexp)
    return os.path.join(path_dict["@template"], pathexp)

_MISSING = object()

def evaluate_attribute(attribute, data, layer, player_index, multiple_index):
    if attribute not in layer:
        return _MISSING

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
        if val is _MISSING:
            return default
        return val
    return get_attr

def compute_distributed_layout(layer, data, player_index, amount, player_number):
    """
    For a "player_images" layer with multiple items per player and
    "distribute_evenly" set, works out where (and, optionally, how big) each
    *filled* slot (skipping any that are None/empty for this player) should
    draw so they're spread evenly across a span instead of sitting at fixed
    per-slot coordinates. Returns {slot_index: {"x": ..., "y"?: ..., "width"?: ..., "height"?: ...}},
    only for slots that should draw - keys other than "x" are only present
    when the corresponding "distribute_*" attribute below opts into them, so
    old callers that only ever set distribute_size/x1/x2 get identical
    behavior to before (fixed size, x-only repositioning).

    "distribute_size"/"distribute_x1"/"distribute_x2"/"distribute_x1_no_flag"/
    "distribute_row_top"/"distribute_row_height" may each be either a single
    value (applies to every player) or a player_number-length list (a
    different span/size/row per player row) - the latter lets one layer mix
    e.g. a wide full-row span for some players with a narrow half-width span
    for others.

    If "distribute_max_size" is set, item size becomes dynamic instead of
    fixed: each item grows to fill the row (up to that cap) as the actual
    count drops below `amount`, rather than staying a constant size with
    more gap around it. "distribute_gap" (default 0) sets the spacing kept
    between items while they're growing. Vertical centering only follows
    that dynamic size when "distribute_row_top"/"distribute_row_height" are
    both given - otherwise the y from the layer's static "position" list is
    left untouched, since it was computed for a fixed size.

    Once items hit their cap (or there's only one), the leftover span isn't
    split evenly on both sides - the block is right-aligned to distribute_x2
    instead. This is what makes it safe for another layer (a name box, a
    flag) to expand rightward into the space *before* the block via
    dynamic_x2_layer/dynamic_x_layer below: that space would otherwise be
    split half-and-half, leaving an equal, unusable gap on the far side.

    "distribute_max_size" caps item *height* (and is the width cap too,
    keeping items square, unless "distribute_max_width" is also given).
    When "distribute_max_width" is set higher than "distribute_max_size",
    items are allowed to grow wider than they are tall - up to that cap -
    to use up horizontal space a fixed-height square wouldn't have filled,
    instead of only stretch-filling by adding more gap. Height still shrinks
    below "distribute_max_size" (staying square) in the crowded case where
    even the minimum width doesn't fit the span at the nominal gap.

    The span's left edge can optionally shrink further left to reclaim the
    space a hidden flag/icon would have taken - but only when no player
    shares that value, so the portrait columns stay aligned. "distribute_group"
    (a player_number-length list of arbitrary group ids) scopes that check to
    only the current player's group instead of all players, for layouts where
    unrelated groups of rows shouldn't have to agree on flag presence.

    Returns a (layout, start_x) tuple - start_x is where the first *drawn*
    item actually starts (the left edge of the item block, after any
    centering), or the resolved distribute_x1 when nothing draws at all.
    Other layers (e.g. a name textbox or a flag) can use start_x to adapt
    their own position/size to how much room the items ended up using,
    instead of assuming they always reach all the way to distribute_x1.
    """
    def resolve(attr_name, default=None):
        val = layer.get(attr_name, default)
        if isinstance(val, list):
            return val[player_index] if player_index < len(val) else default
        return val

    field = layer.get("name", "")
    field_name = field[1:] if field.startswith(("%", "$")) else field
    player_data = data["players"][player_index]
    values = player_data.get(field_name) or []

    filled_slots = [j for j in range(amount) if j < len(values) and values[j] is not None]
    count = len(filled_slots)

    x1 = resolve("distribute_x1", 0)

    flag_field = layer.get("distribute_flag_field")
    if flag_field:
        groups = layer.get("distribute_group")
        if groups:
            group_id = groups[player_index] if player_index < len(groups) else None
            group_indices = [k for k in range(player_number) if k < len(groups) and groups[k] == group_id]
        else:
            group_indices = list(range(player_number))
        flag_reserved = any(data["players"][k].get(flag_field) for k in group_indices)
        if not flag_reserved:
            x1 = resolve("distribute_x1_no_flag", x1)

    if count == 0:
        return {}, x1

    max_size = resolve("distribute_max_size")
    dynamic_size = max_size is not None
    gap_setting = resolve("distribute_gap", 0)
    max_width = resolve("distribute_max_width", max_size) if dynamic_size else None
    if dynamic_size:
        x2 = resolve("distribute_x2", x1)
        span = x2 - x1
        if count == 1:
            item_width = min(max_width, span)
        else:
            ideal = (span - (count - 1) * gap_setting) / count
            item_width = min(max_width, ideal)
        # Height only follows max_size (the "square" cap) up to it - if
        # width had to shrink below it to fit (crowded case), height shrinks
        # to match and items stay square, same as the legacy fixed-size
        # behavior. Otherwise height stays fixed at max_size while width is
        # free to grow past it (up to max_width), widening the item instead.
        item_height = min(max_size, item_width)
    else:
        item_size = resolve("distribute_size", 0)
        x2 = resolve("distribute_x2", x1 + item_size)
        span = x2 - x1
        item_width = item_height = item_size

    if count == 1 and not dynamic_size:
        xs = [x1 + (span - item_width) / 2]
    elif count == 1:
        # Right-align rather than center: dynamic_x2_layer callers (a name
        # box, a flag) already expand into whatever room is left of this
        # item's start, so centering it would leave the space on *both*
        # sides unused - anchoring to x2 lets those other layers claim it.
        xs = [x2 - item_width]
    elif dynamic_size and item_width >= max_width:
        # Items are already at their cap - rather than stretch-justify them
        # across the whole (possibly much wider) span, which would leave
        # huge gaps, keep the nominal gap and right-align the resulting
        # block (see the count == 1 comment above for why not centered).
        content_width = count * item_width + (count - 1) * gap_setting
        start = x2 - content_width
        xs = [start + i * (item_width + gap_setting) for i in range(count)]
    else:
        gap = (span - count * item_width) / (count - 1)
        xs = [x1 + i * (item_width + gap) for i in range(count)]

    row_top = resolve("distribute_row_top")
    row_height = resolve("distribute_row_height")
    y = row_top + (row_height - item_height) / 2 if row_top is not None and row_height is not None else None

    result = {}
    for rank, slot in enumerate(filled_slots):
        entry = {"x": round(xs[rank])}
        if y is not None:
            entry["y"] = round(y)
        if dynamic_size:
            entry["width"] = round(item_width)
            entry["height"] = round(item_height)
        result[slot] = entry
    return result, round(xs[0])

def resolve_distribute_text_guard(layer, data, player_number, fonts):
    """
    If "distribute_text_field" is set on a distribute_evenly player_images
    layer, returns a per-player list to use as its "distribute_x1": each
    player's span start is pushed right far enough to guarantee room for
    that player's own text field (e.g. "tag") at its *worst-case* rendered
    width - the width it still comes out to when the text layer's own
    min_font_size floor overrides the normal fit-to-box search (see
    fitting_font: "a readability floor takes priority over strictly fitting
    the box"). Without this, an unusually long name can silently render
    wider than the box it was given and run into the flag/portraits, no
    matter how generous that box's *nominal* width is - a fixed-width box
    can never guarantee fitting arbitrary-length text at a fixed minimum
    readable size, so the portrait span has to be willing to yield room
    instead. Because the flag and the name box's own right edge already
    follow this same layer's start_x via "dynamic_x_layer"/
    "dynamic_x2_layer", pushing just this one value is enough to cascade
    the extra room to all three.

    "distribute_text_x1"/"distribute_text_min_size"/"distribute_text_margin"
    should mirror the guarded text layer's own left edge, min_font_size,
    and the gap kept before the span (each scalar or a player_number-length
    list, same convention as the other distribute_* attributes).
    "distribute_text_font" names an entry in `fonts` (defaults to "auto").

    The push is capped so at least MIN_SPAN of the span survives (using
    this layer's own "distribute_x2") - an absurdly long name should still
    never overlap anything, but it also shouldn't be able to invert the
    span and crash the resize; portraits just bottom out tiny instead.

    Returns the layer's original "distribute_x1" unchanged when
    "distribute_text_field" isn't set.
    """
    MIN_SPAN = 40

    base_x1 = layer.get("distribute_x1", 0)
    text_field = layer.get("distribute_text_field")
    if not text_field:
        return base_x1

    def resolve(val, i):
        return val[i] if isinstance(val, list) else val

    font_path = fonts.get(layer.get("distribute_text_font", "auto")) or fonts.get("auto")

    result = []
    players = data.get("players", [])
    for i in range(player_number):
        x1 = resolve(base_x1, i)
        min_size = resolve(layer.get("distribute_text_min_size", 0), i)
        text_value = players[i].get(text_field) if i < len(players) else None
        if font_path and min_size and text_value:
            font = ImageFont.truetype(font_path, min_size)
            text_w, _ = get_text_dimensions(str(text_value), font)
            text_x1 = resolve(layer.get("distribute_text_x1", 0), i)
            margin = resolve(layer.get("distribute_text_margin", 0), i)
            required = text_x1 + text_w + margin
            if required > x1:
                x2 = resolve(layer.get("distribute_x2", required), i)
                x1 = min(required, x2 - MIN_SPAN)
        result.append(x1)
    return result

def draw_image_layer(canvas, layer, data, path_dict, player_index=None, multiple_index=None, position_override=None, size_override=None):
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
        if part is None:
            return
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
    # "dynamic_x_layer" centers this image between another distribute_evenly
    # layer's actual per-player start_x and a matching dynamic name box -
    # used to keep the flag equidistant from the name text and the first
    # character portrait even as that gap grows/shrinks per player. Mirrors
    # draw_text_layer's "dynamic_x2_layer"/"dynamic_x2_margin" - pass the
    # same margin to both so the flag centers in the same gap the name box
    # stopped short of.
    # Read straight off the layer (not via get_attr) - this is a literal
    # layer-name reference, not player data, and get_attr would otherwise
    # mistake a "%"-prefixed name for a "%field" player-data lookup.
    dynamic_layer = layer.get("dynamic_x_layer")
    if dynamic_layer and position_override is None and player_index is not None:
        starts = data.get("_distribute_starts", {}).get(dynamic_layer)
        if starts is not None:
            margin = get_attr("dynamic_x_margin", 0)
            own_size = get_attr("size")
            own_width = own_size[0] if own_size else 0
            new_x = starts[player_index] - (margin + own_width) / 2
            position = (round(new_x), position[1])
    if position_override is not None:
        ox, oy = position_override
        position = (ox, position[1] if oy is None else oy)
    fit_type = get_attr("fit_type", "fit")
    align = get_attr("align", "center")
    alignv = get_attr("alignv", "middle")

    size = size_override if size_override is not None else get_attr("size")
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

def draw_text_layer(canvas, draw, layer, data, path_dict, fonts, player_index=None, multiple_index=None):
    get_attr = get_attr_fun(data, layer, player_index, multiple_index)

    condition = get_attr("condition", True)
    if not condition:
        return

    textbox = list(get_attr("textbox"))
    # "dynamic_x2_layer" lets this box's right edge follow another
    # distribute_evenly layer's actual per-player start_x (see the
    # pre-pass in generate_graphic) instead of a fixed x2 - so e.g. a name
    # box can widen into space a below-max item count left unused. Read
    # straight off the layer (not via get_attr) since this is a literal
    # layer-name reference, not player data - get_attr would otherwise
    # mistake a "%"-prefixed name for a "%field" player-data lookup.
    dynamic_layer = layer.get("dynamic_x2_layer")
    if dynamic_layer and player_index is not None:
        starts = data.get("_distribute_starts", {}).get(dynamic_layer)
        if starts is not None:
            margin = get_attr("dynamic_x2_margin", 0)
            textbox[2] = starts[player_index] - margin
    textbox = tuple(textbox)

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
        if not isinstance(font_shadow_offset, (list, tuple)):
            font_shadow_offset = [0.55, 0.55]
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

    guess = get_attr("font_guess", 10000)
    min_font_size = get_attr("font_min_size")
    max_font_size = get_attr("font_max_size")

    fit_text(draw, textbox, text, font, guess=guess,
            align=align, alignv=alignv,
            fill=font_color, shadow=font_shadow_color, shadow_offset=font_shadow_offset,
            outline_thickness=outline_thickness, outline_color=outline_color, canvas=canvas,
            min_font_size=min_font_size, max_font_size=max_font_size)

def draw_rectangle_layer(draw, layer, data, player_index=None, multiple_index=None, canvas=None):
    get_attr = get_attr_fun(data, layer, player_index, multiple_index)

    condition = get_attr("condition", True)
    if not condition:
        return

    color = get_attr("color", "#000000")
    opacity = get_attr("opacity", 1.0)
    stroke_width = get_attr("stroke_width")

    shape = get_attr("shape")

    if not shape:
        return

    # Same "dynamic_x_layer" convention as draw_image_layer - recenters this
    # box's x-span (keeping its authored width) around a distribute_evenly
    # layer's actual per-player start_x, e.g. so a flag's border tracks the
    # flag when the flag itself is dynamically repositioned. Read straight
    # off the layer (not via get_attr) since this is a literal layer-name
    # reference, not player data - get_attr would otherwise mistake a
    # "%"-prefixed name for a "%field" player-data lookup.
    dynamic_layer = layer.get("dynamic_x_layer")
    if dynamic_layer and player_index is not None:
        starts = data.get("_distribute_starts", {}).get(dynamic_layer)
        if starts is not None:
            shape = list(shape)
            margin = get_attr("dynamic_x_margin", 0)
            width = shape[2] - shape[0]
            new_x1 = starts[player_index] - (margin + width) / 2
            shape[0] = new_x1
            shape[2] = new_x1 + width

    if stroke_width:
        # Stroke-only (no fill): PIL draws this inward from the given
        # bounds, so callers wanting a border centered on an edge should
        # pass the outer bounds with stroke_width = 2x the desired pad.
        draw.rectangle(shape, outline=color, width=stroke_width)
        return

    if opacity >= 1 or canvas is None:
        draw.rectangle(shape, fill=color)
        return

    # Partial opacity needs real alpha-compositing against whatever is
    # already on the canvas; ImageDraw.rectangle would just overwrite the
    # pixels (including alpha) instead of blending with layers below it.
    r, g, b = ImageColor.getrgb(color)[:3]
    alpha = max(0, min(255, round(opacity * 255)))
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle(shape, fill=(r, g, b, alpha))
    canvas.alpha_composite(overlay)

def generate_graphic(data):

    # Getting the path of the current file
    path = os.path.realpath(__file__)
    path = os.path.abspath(os.path.join(path, os.pardir))

    # Path to the template directory
    template_name = data.get("template", "default")
    template_path = os.path.join(path, "templates", template_name)
    with open(os.path.join(template_path, "template.json"), "r", encoding="utf-8") as f:
        template_data = json.loads(f.read())

    available_fonts = template_data["available_fonts"]
    fonts = {}
    for key, value in available_fonts.items():
        fonts[key] = os.path.join(template_path, value)

    # Register any uploaded font files from options
    _temp_font_files = []
    for option in template_data.get("options", []):
        if option.get("type") == "font":
            opt_name = option["name"]
            opt_val = data["options"].get(opt_name)
            if opt_val is not None and hasattr(opt_val, "read"):
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ttf")
                tmp.write(opt_val.read())
                tmp.close()
                _temp_font_files.append(tmp.name)
                fonts["__uploaded__"] = tmp.name
                data["options"][opt_name] = "__uploaded__"

    # Choosing the best font based on the amount of missing special characters
    text_blob = ""
    for option in template_data["options"]:
        if option["type"] == "text":
            text_blob += data["options"][option["name"]]
    player_text_fields = [f["name"] for f in template_data.get("player_fields", []) if f.get("type") == "text"]
    for player in data['players']:
        for field_name in player_text_fields:
            value = player.get(field_name)
            if isinstance(value, list):
                text_blob += "".join(v for v in value if isinstance(v, str))
            elif isinstance(value, str):
                text_blob += value
    if fonts:
        fonts["auto"] = best_font(text_blob, list(fonts.values()))

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

    # Pre-pass: for every distribute_evenly player_images layer with
    # "distribute_text_field" set, widen its own "distribute_x1" (in place,
    # on this request's own copy of template_data) to guarantee room for
    # that player's text at its worst-case (min-font-size) rendered width -
    # see resolve_distribute_text_guard. Must run before the start_x
    # pre-pass below, since that's what "dynamic_x2_layer"/"dynamic_x_layer"
    # read to position the name box and flag - widening distribute_x1 here
    # is what lets a long name push both of them out of its way.
    for layer in template_data["layers"]:
        if layer.get("type") == "player_images" and layer.get("multiple") and layer.get("distribute_evenly") \
                and layer.get("distribute_text_field"):
            layer["distribute_x1"] = resolve_distribute_text_guard(layer, data, PLAYER_NUMBER, fonts)

    # Pre-pass: for every distribute_evenly player_images layer, work out
    # per-player where its item block actually starts (see
    # compute_distributed_layout's start_x). Other layers (a name textbox,
    # a flag) can key off this via "dynamic_x2_layer"/"dynamic_x_layer" to
    # adapt their own position to how much room the items ended up using -
    # e.g. widening into space a below-max character count left unused.
    distribute_starts = {}
    for layer in template_data["layers"]:
        if layer.get("type") == "player_images" and layer.get("multiple") and layer.get("distribute_evenly"):
            layer_name = layer.get("name")
            if not layer_name:
                continue
            starts = []
            for i in range(PLAYER_NUMBER):
                amount = evaluate_attribute("amount", data, layer, i, None)
                _, start_x = compute_distributed_layout(layer, data, i, amount, PLAYER_NUMBER)
                starts.append(start_x)
            distribute_starts[layer_name] = starts
    data["_distribute_starts"] = distribute_starts

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
                distribute = layer.get("distribute_evenly", False)
                for i in range(PLAYER_NUMBER):
                    amount = evaluate_attribute("amount", data, layer, i, None)
                    if distribute:
                        layout, _ = compute_distributed_layout(layer, data, i, amount, PLAYER_NUMBER)
                        for j, entry in layout.items():
                            size_override = (entry["width"], entry["height"]) if "width" in entry else None
                            draw_image_layer(canvas, layer, data, path_dict, player_index=i, multiple_index=j,
                                              position_override=(entry["x"], entry.get("y")), size_override=size_override)
                    else:
                        for j in range(amount):
                            draw_image_layer(canvas, layer, data, path_dict, player_index=i, multiple_index=j)
            else:
                for i in range(PLAYER_NUMBER):
                    draw_image_layer(canvas, layer, data, path_dict, player_index=i, multiple_index=None)
        
        elif layer_type == "text":
            draw_text_layer(canvas, draw, layer, data, path_dict, fonts, player_index=None, multiple_index=None)

        elif layer_type == "player_text":
            multiple = layer.get("multiple", False)
            if multiple:
                for i in range(PLAYER_NUMBER):
                    amount = evaluate_attribute("amount", data, layer, i, None)
                    for j in range(amount):
                        draw_text_layer(canvas, draw, layer, data, path_dict, fonts, player_index=i, multiple_index=j)
            else:
                for i in range(PLAYER_NUMBER):
                    draw_text_layer(canvas, draw, layer, data, path_dict, fonts, player_index=i)

        elif layer_type == "rectangle":
            draw_rectangle_layer(draw, layer, data, canvas=canvas)

        elif layer_type == "player_rectangles":
            multiple = layer.get("multiple", False)
            if multiple:
                for i in range(PLAYER_NUMBER):
                    amount = evaluate_attribute("amount", data, layer, i, None)
                    for j in range(amount):
                        draw_rectangle_layer(draw, layer, data, player_index=i, multiple_index=j, canvas=canvas)
            else:
                for i in range(PLAYER_NUMBER):
                    draw_rectangle_layer(draw, layer, data, player_index=i, canvas=canvas)
                    
        elif layer_type == "per_player_option":
            # Dispatches a different sub-layer per player based on a computed key.
            # key starting with "#" counts non-null values in player_data[field].
            key_expr = layer["key"]
            max_choice = max((int(k) for k in layer["choices"] if k.isdigit()), default=1)
            for i in range(PLAYER_NUMBER):
                player_data = data["players"][i]
                if key_expr.startswith("#"):
                    field = key_expr[1:]
                    values = player_data.get(field, [])
                    count = sum(1 for v in values if v is not None) if isinstance(values, list) else (1 if values is not None else 0)
                    key = str(min(max(count, 1), max_choice))
                else:
                    key = str(evaluate_str_exp(key_expr, player_data, data["options"], layer, i, None))
                sublayer = layer["choices"].get(key)
                if sublayer is None:
                    continue
                multiple = sublayer.get("multiple", False)
                if multiple:
                    amount = evaluate_attribute("amount", data, sublayer, i, None)
                    for j in range(amount):
                        draw_image_layer(canvas, sublayer, data, path_dict, player_index=i, multiple_index=j)
                else:
                    draw_image_layer(canvas, sublayer, data, path_dict, player_index=i)

        else:
            print("NOT IMPLEMENTED", layer_type)

    result = canvas.convert("RGB")
    for tmp_path in _temp_font_files:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
    return result