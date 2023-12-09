import re
from PIL import Image
import cv2
import os
import random
import numpy as np
import Task1.main_task1 as BGGen
import Task4.layout as LayoutGen
import argparse
from Task4.preprocessing import detect_page

IN = "./in/"
OUT = "./out/"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--nb", type=int, default=20,
    help="Define the number of synthetic pages to generate"
)
parser.add_argument(
    "--gen_bg", type=int, default=0,
    help="Generate new background. 0=False, will use present background images\
            1=True, will regenerate new background"
)
parser.add_argument(
    "--overwrite", type=int, default=1,
    help="Default is 1. If set to 0 any new files will be added to the output instead of overwritting them, including the TSV file"
)

args = parser.parse_args()

if __name__ == "__main__":
    # files = os.listdir(IN)
    # if args.gen_bg or len(files) == 0:
    #     cv2_bg = BGGen.generate_background()
    #     sample = 1
    #     for i in cv2_bg:
    #         pil_bg = Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB))
    #         pil_bg.save(f"{IN}sample{sample}.png")
    #         sample+=1
    #
    # files = os.listdir(IN)
    config = LayoutGen.get_config()

    id = 300
    if args.overwrite or len(os.listdir(OUT))==0:
        for file in os.listdir(OUT):
            os.remove(OUT+file)
    else:
        id = max(re.findall(r"\d+", "-".join(map(str, os.listdir(OUT)))))

    for _ in range(args.nb):
        bg = BGGen.generate_background()
        # bg = random.choice(files)
        # bg = Image.open(IN+bg)
        orient, _ = detect_page(np.array(bg))
        if orient == 0:
            if id%2 == 0:
                id+=1
        else:
            if id%2 != 0:
                id+=1
        page_id = f"csg-0231_{id}"
        print("Generating " + page_id)
        img = LayoutGen.generate_layout(bg, config, page_id=page_id)
        img.save(OUT+page_id+".png")
        id += 1

