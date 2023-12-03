from PIL import ImageDraw, Image, ImageOps
import yaml
import numpy as np
import Task3.Output_task3 as TextGen
import Task4.layout as LayoutGen

if __name__ == "__main__":
    data = dict()
    with open("./Task4/config.yaml") as config:
        data = yaml.full_load(config)

    man = LayoutGen.Manuscript()
    man.get_background("./Task4/Texterase/e1.jpg")
    # lines = man.get_lines()
    bg = man.background
    mask = Image.new("L", bg.size, 0)
    texture = Image.new("RGB", bg.size, (255,255,255))
    img = ImageDraw.Draw(bg)
    lines = np.round(data["line_d_std"]/2 * np.random.randn(1, 25) + data["avg_line_d"])
    nb_line = 0
    text, ink, coords = TextGen.reproduce_text(font_size=9, text_position=(0,0),\
                                               max_line_width=1100, image_dir="./Task3/Dictionary/")
    for col in range(1, 3):
        curr_x = data[f"col{col}"][0]
        curr_y = data[f"col{col}"][1] + data[f"lines{col}"]
        line_txt = text[nb_line]
        line_ink = ink[nb_line]
        line_coord = coords[nb_line]
        mask.paste(line_txt, (curr_x, curr_y))
        texture.paste(line_ink, (curr_x, curr_y))
        img.line([(curr_x, curr_y), (curr_x+data[f"col{col}"][2], curr_y)], fill="yellow", width=5)
        nb_line += 1
        for line in lines[0]:
            if nb_line == len(text)-1:
                nb_line = 0
            curr_y += line
            curr_y = int(curr_y)
            line_txt = text[nb_line]
            line_ink = ink[nb_line]
            line_coord = coords[nb_line]
            mask.paste(line_txt, (curr_x, curr_y))
            texture.paste(line_ink, (curr_x, curr_y))
            nb_line += 1

            # print(f"{curr_x=} {curr_y=}")
            img.line([(curr_x, curr_y), (curr_x+data[f"col{col}"][2], curr_y)], fill="yellow", width=5)

    # bg.show()
    final = Image.composite(bg, texture, mask=ImageOps.invert(mask))
    final.show()
    man.close_background()

