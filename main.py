import re
import os
import numpy as np
import Task1.main_task1 as BGGen
import Task4.layout as LayoutGen
import argparse
from Task4.preprocessing import detect_page
import time

IN = "./in/"
OUT = "./out/"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--nb", type=int, default=20,
    help="Define the number of synthetic pages to generate"
)
parser.add_argument(
    "--overwrite", type=int, default=1,
    help="Default is 1. If set to 0 any new files will be added to the output instead of overwritting them, including the TSV file"
)

args = parser.parse_args()

if __name__ == "__main__":
    config = LayoutGen.get_config()

    id = 300
    if args.overwrite or len(os.listdir(OUT))==0:
        for file in os.listdir(OUT):
            os.remove(OUT+file)
    else:
        id = int(max(re.findall(r"\d+", "-".join(map(str, os.listdir(OUT))))))

    runtimes = list()
    for _ in range(args.nb):
        start = time.perf_counter()
        bg = BGGen.generate_background()
        os.remove("./crop_image.png")
        os.remove("./image_with_contours.png")
        os.remove("./thresh_image.jpg")
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
        end = time.perf_counter()
        runtime = end-start
        runtimes.append(runtime)

    print(f"Average Runtime: {sum(runtimes)/len(runtimes)}")

