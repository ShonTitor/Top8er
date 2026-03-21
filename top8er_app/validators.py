"""Validation helpers for the api_generate view."""

from django.conf import settings
from django.core.files.base import ContentFile
from itertools import product
from PIL import Image as PilImage
from .utils import is_url

import base64
import logging
import os

logger = logging.getLogger(__name__)


def validate_options(options_data, options_schema, request_files):
    """
    Validate and coerce options fields.

    Returns:
        (data_dict, errors_list)  — data_dict maps option name → value.
    """
    data = {}
    errors = []

    for option in options_schema:
        required = option.get("required", False)
        name = option["name"]
        value = options_data.get(name)
        enable_image_uploading = option.get("enable_image_uploading", False)

        is_image = False
        if is_url(value) and option["type"] != "text":
            errors.append({
                "scope": "options",
                "field": name,
                "message": "URL images are not supported; please provide images as base64"
            })
            value = None
        elif hasattr(value, "read"):
            is_image = True
        elif value and isinstance(value, dict) and 'base64' in value:
            try:
                value = ContentFile(
                    base64.b64decode(value['base64']),
                    name=value.get('name', f"option_{name}.png")
                )
                is_image = True
            except Exception:
                logger.exception("Base64 decode failed for option %s", name)
                errors.append({
                    "scope": "options",
                    "field": name,
                    "message": "Invalid base64 data"
                })

        if is_image and option["type"] != "font":
            try:
                PilImage.open(value).verify()
                value.seek(0)
            except Exception:
                errors.append({
                    "scope": "options",
                    "field": name,
                    "message": "Invalid or corrupt image file"
                })
                value = None
                is_image = False

        if is_image and not enable_image_uploading:
            errors.append({
                "scope": "options",
                "field": name,
                "message": "Image uploading is not allowed for this field"
            })

        if required and value is None:
            errors.append({
                "scope": "options",
                "field": name,
                "message": "This field is required"
            })

        if value is None and "default" in option:
            value = option["default"]

        if value is not None:
            data[name] = value

    return data, errors


def validate_players(players_data, player_fields, player_number, game_data, request_files, game=""):
    """
    Validate and coerce player fields.

    Returns:
        (players_list, errors_list)  — players_list is a list of dicts.
    """
    players = [{} for _ in range(player_number)]
    errors = []

    for player_field, i in product(player_fields, range(player_number)):
        errors_before = len(errors)
        field_type = player_field["type"]
        name = player_field["name"]

        if not isinstance(players_data[i], dict):
            errors.append({
                "scope": "root",
                "field": "players",
                "message": f"Player at index {i} must be a JSON object",
                "player_index": i
            })
            continue

        value = players_data[i].get(name)
        enable_image_uploading = player_field.get("enable_image_uploading", False)
        multiple = player_field.get("multiple", False)
        if multiple:
            amount = player_field["amount"]
            if type(amount) is list:
                amount = amount[i]

        if type(value) is list and len(value) == 2 and \
                type(value[0]) is str and type(value[1]) is int:
            value = tuple(value)

        if type(value) is not list:
            value = [value]

        for k, element in enumerate(value):
            if type(element) is list and len(element) == 2 and \
                    type(element[0]) is str and type(element[1]) is int:
                value[k] = tuple(value[k])

        if enable_image_uploading:
            if multiple:
                for j in range(amount):
                    file_key = f"player_{i}_{name}_{j}"
                    if file_key in request_files:
                        if len(value) < j + 1:
                            value += [None for _ in range(j + 1 - len(value))]
                        value[j] = request_files[file_key]
                    elif j < len(value) and value[j] and isinstance(value[j], dict) and 'base64' in value[j]:
                        try:
                            value[j] = ContentFile(
                                base64.b64decode(value[j]['base64']),
                                name=value[j].get('name', f"player_{i}_{name}_{j}.png")
                            )
                        except Exception:
                            logger.exception("Base64 decode failed for player %d field %s index %d", i, name, j)
                            errors.append({
                                "scope": "player_fields",
                                "field": name,
                                "message": "Invalid base64 data"
                            })
            else:
                file_key = f"player_{i}_{name}"
                if file_key in request_files:
                    value = [request_files[file_key]]
                elif value[0] and isinstance(value[0], dict) and 'base64' in value[0]:
                    try:
                        value = [ContentFile(
                            base64.b64decode(value[0]['base64']),
                            name=value[0].get('name', f"player_{i}_{name}.png")
                        )]
                    except Exception:
                        logger.exception("Base64 decode failed for player %d field %s", i, name)
                        errors.append({
                            "scope": "player_fields",
                            "field": name,
                            "message": "Invalid base64 data"
                        })

        for k, v in enumerate(value):
            is_image = False
            if is_url(v):
                errors.append({
                    "scope": "player_fields",
                    "field": name,
                    "message": "URL images are not supported; please provide images as base64"
                })
                value[k] = None
            elif hasattr(v, "read"):
                is_image = True
                try:
                    PilImage.open(v).verify()
                    v.seek(0)
                except Exception:
                    errors.append({
                        "scope": "player_fields",
                        "field": name,
                        "message": "Invalid or corrupt image file"
                    })
                    value[k] = None
                    is_image = False

            if is_image and not enable_image_uploading:
                errors.append({
                    "scope": "player_fields",
                    "field": name,
                    "message": "Image uploading is not allowed for this field"
                })

        if multiple:
            required_field = player_field.get("required", False)
            if isinstance(required_field, list) and len(required_field) > 0 and isinstance(required_field[0], list):
                required_many = required_field[i]
            else:
                required_many = player_field.get("required_many", [required_field for _ in range(amount)])
            for k in range(amount):
                if (len(value) > k and value[k] is None and required_many[k]) or \
                        (len(value) <= k and required_many[k]):
                    errors.append({
                        "scope": "player_fields",
                        "field": name,
                        "message": f"{name} with index {k} is required"
                    })
        else:
            required = player_field.get("required", False)
            if required and value[0] is None:
                errors.append({
                    "scope": "player_fields",
                    "field": name,
                    "message": "This field is required"
                })

        if value[0] is None and "default" in player_field:
            default = player_field["default"]
            if multiple:
                value = [default for _ in range(amount)]
            else:
                value = [default]

        if field_type == "select":
            choices = player_field["options"]
            if choices == "flags":
                choices = settings.FLAGS

            for v in value:
                if v is not None and v not in choices \
                        and not (hasattr(v, "read") and enable_image_uploading):
                    errors.append({
                        "scope": "player_fields",
                        "field": name,
                        "message": f"{v} is not a valid option, options are {choices}"
                    })

        elif field_type == "character":
            for j, char in enumerate(value):
                if "image_types" in player_field:
                    image_types = player_field["image_types"]
                else:
                    image_types = player_field["image_types_multiple"]

                if type(char) is tuple:
                    if multiple:
                        image_type = image_types[i][j]
                    else:
                        image_type = image_types[i]

                    if image_type == "icons":
                        icon_colors = game_data.get("iconColors") or {}
                        if not game_data.get("hasIcons"):
                            errors.append({
                                "scope": "player_fields",
                                "field": name,
                                "message": f"There is no icon image available for character {char[0]}"
                            })
                        elif icon_colors:
                            if char[0] not in icon_colors:
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no icon image available for character {char[0]}"
                                })
                            if len(icon_colors.get(char[0], [None])) <= char[1]:
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no icon image available for {char[0]} with index {char[1]}"
                                })
                        else:
                            characters = game_data.get("characters", [])
                            if char[0] not in characters:
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no icon image available for character {char[0]}"
                                })
                    elif image_type == "portraits":
                        characters = game_data.get("characters", [])
                        colors = game_data.get("colors") or {}
                        if char[0] not in characters:
                            errors.append({
                                "scope": "player_fields",
                                "field": name,
                                "message": f"There is no portrait image available for character {char[0]}"
                            })
                        if len(colors.get(char[0], [None])) <= char[1]:
                            errors.append({
                                "scope": "player_fields",
                                "field": name,
                                "message": f"There is no portrait image available for {char[0]} with index {char[1]}"
                            })
                    else:
                        characters = game_data.get("characters", [])
                        if char[0] not in characters:
                            errors.append({
                                "scope": "player_fields",
                                "field": name,
                                "message": f"Character {char[0]} is not valid"
                            })
                        else:
                            char_path = os.path.join(
                                settings.APP_BASE_DIR, "generar", "assets", game, char[0], f"{char[1]}.png"
                            )
                            if not os.path.exists(char_path):
                                errors.append({
                                    "scope": "player_fields",
                                    "field": name,
                                    "message": f"There is no {image_type} image available for {char[0]}"
                                })

        if not multiple:
            value = value[0]

        if value is not None:
            players[i][name] = value

        for err in errors[errors_before:]:
            err["player_index"] = i

    return players, errors
