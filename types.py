import keyboard
from mss import mss

from hint import show_types, destroy
from image import *

def minecraft_sizes():
    return { "left": 1068, "top": 600, "width": 852, "height": 480}
    # {
    #             "left": 0, "top": 30, "width": 1920, "height": 1060
    #         }
sizes = {
    "battle": {
        "width": minecraft_sizes()["width"],
        "height": minecraft_sizes()["height"],
        "panel": {
            "width": minecraft_sizes()["width"],
            "height": 164,
            "conditions": {
                "width": 160
            },
            "buttons": {
                "height": 50
            },
            "move": {
                "width": 290,
                "height": 70,
                "gap": {
                    "width": 8,
                    "height": 8,
                },
                "name": {
                    "height": 50
                },
                "pp": {
                    "height": 20
                }
            }
        },
        "pokemon_frame": {
            "icon": {
                "width": 100,
                "height":70
            },
            "width": 300,
            "height": 70,
            "name": {
                "enemy":{
                    "left": 100,
                    "top": 0,
                },
                "my": {
                    "left": 560,
                    "top": 250,
                },
                "width": 150,
                "height": 35
            },
            "health": {
                "height": 40
            }
        }}
}


def to_coord(left, top, width, height):
     return {
        "left": left,
        "top": top,
        "width": width,
        "height": height
    }

def enemy_frame_coord():
    enemy_frame_sizes = sizes["battle"]["pokemon_frame"]
    return to_coord(0, 0, enemy_frame_sizes["width"], enemy_frame_sizes["height"])

def enemy_name_coord():
    enemy_name_sizes = sizes["battle"]["pokemon_frame"]["name"]
    return to_coord(enemy_name_sizes["enemy"]["left"], enemy_name_sizes["enemy"]["top"], enemy_name_sizes["width"], enemy_name_sizes["height"])

def enemy_name_image(screen):
    return crop_image(screen, **enemy_name_coord())

def extract_enemy_name(screen):
    image = enemy_name_image(screen)
    image = increase_size_of_image(image, 2)
    image = filter_image_for_white(image)
    return get_text_from_image(image)

def moves_coord():
    panel_sizes = sizes["battle"]["panel"]
    move_sizes = panel_sizes["move"]
    gap = move_sizes["gap"]["width"]
    width = move_sizes["width"] * 2 + gap
    height = move_sizes["height"] * 2 + gap
    left = panel_sizes["width"] - panel_sizes["conditions"]["width"] - width - gap
    top = sizes["battle"]["height"]-panel_sizes["height"] + gap
    return to_coord(left, top, width, height)

def move_coord(number):
    pixelmon_logo_radius = 35
    move_type_icon = 45
    move_sizes = sizes["battle"]["panel"]["move"]
    gap = move_sizes["gap"]["width"]
    width, height = move_sizes["width"] - pixelmon_logo_radius - move_type_icon, move_sizes["height"]
    res = {}
    match number:
        case 1:
            res = to_coord(moves_coord()["left"] + move_type_icon, moves_coord()["top"], width , height)
        case 2:
            res = to_coord(moves_coord()["left"] + moves_coord()["width"] - width - move_type_icon , moves_coord()["top"], width, height)
        case 3:
            res = to_coord(moves_coord()["left"] + move_type_icon, moves_coord()["top"] + height + gap, width, height)
        case 4:
            res = to_coord(moves_coord()["left"] + moves_coord()["width"] - width - move_type_icon, moves_coord()["top"] + gap + height , width, height)
    return res


def move_name_coord(number):
    coord = move_coord(number)
    coord["height"] = sizes["battle"]["panel"]["move"]["name"]["height"]
    return coord

def move_name_image(minecraft_screen, number):
     return crop_image(minecraft_screen, **move_name_coord(number))

def move_pp_coord(number):
    coord = move_coord(number)
    coord["top"] = coord["top"] +  sizes["battle"]["panel"]["move"]["name"]["height"]
    coord["height"] = sizes["battle"]["panel"]["move"]["pp"]["height"]
    return coord

def move_pp_image(minecraft_screen, number):
    return crop_image(minecraft_screen, **move_pp_coord(number))

def extract_move_name(minecraft_screen, number):
    image = move_name_image(minecraft_screen, number)
    image = filter_image_for_gray(image)
    image = increase_size_of_image(image, 2)
    move_name = get_text_from_image(image).strip()
    return move_name

def get_all_moves_names(minecraft_screen):
    names = []
    for i in range(1, 5):
        names.append(extract_move_name(minecraft_screen, i))
    return names

minecraft_np_image = None
is_showing_types = False

def on_right_shift(key):
    print("Pressed Shift")
    global is_showing_types, minecraft_np_image
    if is_showing_types:
        print("Destroing types window... ")
        destroy()
    else:
        name = extract_enemy_name(minecraft_np_image)
        show_types(minecraft_sizes()["left"] + sizes["battle"]["pokemon_frame"]["width"], minecraft_sizes()["top"], name)
        print("Showing types window... ")
    is_showing_types ^= True

keyboard.on_release_key('right shift', on_right_shift)

def main():
    with mss() as sct:
        while True:
            screenshot = sct.grab(minecraft_sizes())
            np_image = np.array(screenshot)

            if np_image.shape[2] == 4:  # Check if image has 4 channels (RGBA)
                np_image = cv2.cvtColor(np_image, cv2.COLOR_BGRA2BGR)

            global minecraft_np_image
            minecraft_np_image = np_image
            # image = image.crop(box = (   1400,700, 1400+200, 700+150))
            # np_image = increase_size_of_image(np_image, 1)

            # np_image = filter_image_for_green(np_image)
            # time.sleep(1)
            np_image = crop_image(np_image, **enemy_name_coord())

            cv2.imshow('Red Pixels Highlighted - Others Gray', filter_image_for_white(np_image))

            # print(get_text_from_image(np_image))
            # time.sleep(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()