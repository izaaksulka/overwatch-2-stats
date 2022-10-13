
import pathlib
import pytesseract
from PIL import Image, ImageDraw
import json

# looks like it's this many pixels between each horizontal line in the stats board
VERTICAL_SPACING = 82
FIRST_PLAYER_TOP = 257
SECOND_PLAYER_TOP = FIRST_PLAYER_TOP + VERTICAL_SPACING * 1
THIRD_PLAYER_TOP = FIRST_PLAYER_TOP + VERTICAL_SPACING * 2
FOURTH_PLAYER_TOP = FIRST_PLAYER_TOP + VERTICAL_SPACING * 3
FIFTH_PLAYER_TOP = FIRST_PLAYER_TOP + VERTICAL_SPACING * 4
FIFTH_PLAYER_BOTTOM = FIRST_PLAYER_TOP + VERTICAL_SPACING * 5
SIXTH_PLAYER_TOP = 816
SEVENTH_PLAYER_TOP = SIXTH_PLAYER_TOP + VERTICAL_SPACING * 1
EIGTH_PLAYER_TOP = SIXTH_PLAYER_TOP + VERTICAL_SPACING * 2
NINTH_PLAYER_TOP = SIXTH_PLAYER_TOP + VERTICAL_SPACING * 3
TENTH_PLAYER_TOP = SIXTH_PLAYER_TOP + VERTICAL_SPACING * 4
TENTH_PLAYER_BOTTOM = SIXTH_PLAYER_TOP + VERTICAL_SPACING * 5

PLAYER_NAME_LEFT = 538
PLAYER_NAME_RIGHT = 824

ELIMS_LEFT = 917
ASSISTS_LEFT = 987
DEATHS_LEFT = 1059
DAMAGE_LEFT = 1135
HEALING_LEFT = 1283
MITIGATION_LEFT = 1413
MITIGATION_RIGHT = 1548


def generate_coordinates_for_player(top, bottom):
    return {
        "player_name": (PLAYER_NAME_LEFT, top, PLAYER_NAME_RIGHT, bottom),
        "elims": (ELIMS_LEFT, top, ASSISTS_LEFT, bottom),
        "assists": (ASSISTS_LEFT, top, DEATHS_LEFT, bottom),
        "deaths": (DEATHS_LEFT, top, DAMAGE_LEFT, bottom),
        "damage": (DAMAGE_LEFT, top, HEALING_LEFT, bottom),
        "healing": (HEALING_LEFT, top, MITIGATION_LEFT, bottom),
        "mitigation": (MITIGATION_LEFT, top, MITIGATION_RIGHT, bottom),
    }


two_k_coordinate_set = {
    "map_type_and_name": (138, 37, 852, 91),
    "game_time": (149, 96, 253, 130),
    "team_1": {
        "tank_1": generate_coordinates_for_player(FIRST_PLAYER_TOP, SECOND_PLAYER_TOP),
        "damage_1": generate_coordinates_for_player(SECOND_PLAYER_TOP, THIRD_PLAYER_TOP),
        "damage_2": generate_coordinates_for_player(THIRD_PLAYER_TOP, FOURTH_PLAYER_TOP),
        "healer_1": generate_coordinates_for_player(FOURTH_PLAYER_TOP, FIFTH_PLAYER_TOP),
        "healer_2": generate_coordinates_for_player(FIFTH_PLAYER_TOP, FIFTH_PLAYER_BOTTOM),
    },
    "team_2": {
        "tank_1": generate_coordinates_for_player(SIXTH_PLAYER_TOP, SEVENTH_PLAYER_TOP),
        "damage_1": generate_coordinates_for_player(SEVENTH_PLAYER_TOP, EIGTH_PLAYER_TOP),
        "damage_2": generate_coordinates_for_player(EIGTH_PLAYER_TOP, NINTH_PLAYER_TOP),
        "healer_1": generate_coordinates_for_player(NINTH_PLAYER_TOP, TENTH_PLAYER_TOP),
        "healer_2": generate_coordinates_for_player(TENTH_PLAYER_TOP, TENTH_PLAYER_BOTTOM),
    },
}


def parse_screenshot(path, coordinate_map):
    full_image = Image.open(path)

    # This changes the whole image to black except for pixels that were above a brightness threshold.  found here:
    # https://stackoverflow.com/a/72619741
    # Without this, the enemy team stats parse very badly (lots of letters instead of numbers).  I think
    # it's because of the red background.  Getting rid of everything except bright letters helps a lot.
    _, _, V = full_image.convert('HSV').split()
    full_image = V.point(lambda p: p > 220 and 255)

    debug_image = ImageDraw.Draw(full_image)

    def image_to_string(image):
        return pytesseract.image_to_string(image, config=("--psm 10")).strip()

    def parse_coordinate_map_recursive(coordinate_map):
        if (type(coordinate_map) is tuple):
            debug_image.rectangle(coordinate_map)
            return image_to_string(full_image.crop(coordinate_map))

        parsed_image = {}
        for key in coordinate_map:
            parsed_image[key] = parse_coordinate_map_recursive(
                coordinate_map[key])

        return parsed_image

    # parsed_image = {x: image_to_string(full_image.crop(
    #     resolution_coordinate_set[x])) for x in resolution_coordinate_set}

    parsed_data = parse_coordinate_map_recursive(coordinate_map)

    pathlib.Path('./tmp').mkdir(exist_ok=True)
    debug_image._image.save("tmp/debug-output.png")

    return parsed_data
    # name_only = full_image.crop((538, 257, 824, 330))
    # name_only.save('output.png')


path = 'example-data/push.png'

print(json.dumps(parse_screenshot(path, two_k_coordinate_set), indent=4))
