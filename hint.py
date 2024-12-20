import tkinter as tk
from PIL import Image, ImageTk
from pixelmon import damage_multipliers_of_pokemon


def create_image_grid(window, text_and_images):
    row = 0
    col = 0
    for text, image_paths in text_and_images:
        label = tk.Label(window, text=text, fg="white", bg="black", font=("Arial", 12))
        label.grid(row=row, column=0)
        col += 1
        for image_path in image_paths:
            type_sprite = Image.open(f"type_sprites/{image_path}.png")
            type_sprite = ImageTk.PhotoImage(type_sprite)

            image_label= tk.Label(window, bg="black", image=type_sprite)
            image_label.image = type_sprite  # Keep a reference to avoid garbage collection
            image_label.grid(row=row, column=col)

            col += 1
        if col != 0:
            row += 1
            col = 0  # Move to the next row after each group of images

root = None

def show_types(x, y, pokemon_name):
    global root
    root = tk.Tk()

    root.overrideredirect(True)

    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "black")

    root.configure(bg="black")
    root.geometry(f"+{x}+{y}")

    create_image_grid(root, damage_multipliers_of_pokemon(pokemon_name))

    root.update()

def destroy():
    global root
    root.destroy()

def main():
    show_types(500, 300, "zacian")


if __name__ == "__main__":
    main()