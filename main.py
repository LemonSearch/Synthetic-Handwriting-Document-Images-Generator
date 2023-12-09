from PIL import ImageDraw, Image, ImageOps
import cv2
import yaml
import numpy as np
import random
import Task1.TextErase_MarginProtect as BGGen
import Task3.Output_task3 as TextGen
import Task4.layout as LayoutGen
from Task4.preprocessing import detect_page 

if __name__ == "__main__":
    cv2_bg = BGGen.generate_background()
    bgs = list()
    sample = 1
    for i in cv2_bg:
        pil_bg = Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB))
        ori, _ = detect_page(img=cv2.cvtColor(i, cv2.COLOR_BGR2RGB))
        if ori == 0:
            bgs.append(pil_bg)
    config = LayoutGen.get_config()

    for bg in bgs:
        img = LayoutGen.generate_layout(bg, config)
        img.show()
        if sample:
            break
    #     # man = LayoutGen.Manuscript()
    #     # man.get_background("./Task4/Texterase/e1.jpg")
    #     # lines = man.get_lines()
    #     # bg = man.background
    #     orient, _ = detect_page(img=np.array(bg))
    #     mask = Image.new("L", bg.size, 0)
    #     texture = Image.new("RGB", bg.size, (255,255,255))
    #     img = ImageDraw.Draw(bg)
    #     lines = np.round(random.uniform(data["orient"][orient]["avg_line_d"],
    #                                         data["orient"][orient]["avg_line_d"] + data["orient"][orient]["line_d_std"]*2))
    #     nb_line = 0
    #     text, ink, coords, baseline = TextGen.reproduce_text(font_size=9, text_position=(0,0),\
    #                                                max_line_width=1100, image_dir="./Task3/Dictionary/")
    #     baseline += 40
    #     for col in range(1, 3):
    #         curr_x = round(data["orient"][orient][f"col{col}"][0])
    #         line_y = np.round(random.uniform(data["orient"][orient][f"line{col}"] - data["orient"][orient][f"line{col}_std"],
    #                                         data["orient"][orient][f"line{col}"] + data["orient"][orient][f"line{col}_std"]))
    #         curr_y = round(data["orient"][orient][f"col{col}"][1] + line_y)
    #         line_txt = text[nb_line]
    #         line_ink = ink[nb_line]
    #         line_coord = coords[nb_line]
    #         mask.paste(line_txt, (curr_x, curr_y-baseline))
    #         texture.paste(line_ink, (curr_x, curr_y-baseline))
    #         img.line([(curr_x, curr_y), (curr_x+round(data["orient"][orient][f"col{col}"][2]), curr_y)], fill="yellow", width=5)
    #         nb_line += 1
    #         for line in range(1, 25):
    #             if nb_line == len(text)-1:
    #                 nb_line = 0
    #             curr_y += lines
    #             curr_y = int(curr_y)
    #             line_txt = text[nb_line]
    #             line_ink = ink[nb_line]
    #             line_coord = coords[nb_line]
    #             mask.paste(line_txt, (curr_x, curr_y-baseline))
    #             texture.paste(line_ink, (curr_x, curr_y-baseline))
    #             nb_line += 1
    #
    #             # print(f"{curr_x=} {curr_y=}")
    #             img.line([(curr_x, curr_y), (curr_x+round(data["orient"][orient][f"col{col}"][2]), curr_y)], fill="yellow", width=5)
    #
    #     # bg.show()
    #     final = Image.composite(bg, texture, mask=ImageOps.invert(mask))
    #     final.save(f"./out/sample_{sample}.png")
    #     sample += 1
    #     # man.close_backgroundc()
    
