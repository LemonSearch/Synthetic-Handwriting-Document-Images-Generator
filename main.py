from PIL import ImageDraw
import yaml
import numpy as np
import Task4.Output_task3 as TextGen
import Task4.layout as LayoutGen

if __name__ == "__main__":
    data = dict()
    with open("./Task4/config.yaml") as config:
        data = yaml.full_load(config)

    man = LayoutGen.Manuscript()
    man.get_background("./Task4/Texterase/e1.jpg")
    # lines = man.get_lines()
    bg = man.background
    img = ImageDraw.Draw(bg)
    lines = data["line_d_std"]/2 * np.random.randn(1, 25) + data["avg_line_d"]
    for col in range(1, 3):
        curr_x = data[f"col{col}"][0]
        curr_y = data[f"col{col}"][1] + data[f"lines{col}"]
        img.line([(curr_x, curr_y), (curr_x+data[f"col{col}"][2], curr_y)], fill="yellow", width=5)
        for line in lines[0]:
            curr_y += line
            # print(f"{curr_x=} {curr_y=}")
            img.line([(curr_x, curr_y), (curr_x+data[f"col{col}"][2], curr_y)], fill="yellow", width=5)

    bg.show()
    man.close_background()

    r = TextGen.draw_text_with_boxes("./Task4/Texterase/e1.jpg", "./Task3/carolus.ttf", 13, (50, 200),\
                               "o", "./Task3/transcript.txt", 1200)
    print(r)

