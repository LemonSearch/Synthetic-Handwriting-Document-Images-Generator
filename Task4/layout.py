import random
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import yaml
import string
import Task3.Output_task3 as TextGen
from Task4.preprocessing import detect_page

COLUMNS=["L", "R"]
PUNCTUATION = ",;.:-_"


def generate_layout(input_bg, config: dict, page_id):
    """
    Generate a new document image based on the input blank page image.
    """
    # determine which side of the book the page is: 0=right 1=left
    orient, _ = detect_page(np.array(input_bg))
    size = input_bg.size
    # create a mask in which to place the text mask
    mask = Image.new("L", size, 0)
    # Create an image in which to store the texture for each text lines
    texture = Image.new("RGB", size, (255, 255, 255))
    img = ImageDraw.Draw((input_bg))
    # Set the background to be drawn onto
    # bg = ImageDraw.Draw(input_bg)
    
    lines_spacing = get_random_value(
                        avg=config[orient]["avg_line_d"], 
                        std=config[orient]["line_d_std"],
                        type=2
                    )
    # Get the lines text, ink texture, coordinates and baseline from Task 3 
    text, ink, coords, baseline, tsv_line= TextGen.reproduce_text(font_size=8, text_position=(0,0),\
                                                         max_line_width=780, image_dir="./Task3/Dictionary/")
    # Select a random sampling of sentences for more randomness
    idx = random.sample(range(len(text)), 52)
    text_list = [text[i] for i in idx]
    ink_list = [ink[i] for i in idx]
    tsv_lines = [tsv_line[i] for i in idx]
    # Adjust the baseline to work appropriately
    baseline += 10
    # Counter to keep tracks of the lines
    nb_line = 0
    # Generate the lines for each columns
    for col in [1, 2]:
        # Get the x coordinate of the current column
        curr_x = get_random_value(
                    avg=config[orient][f"col{col}"][0],
                    std=config[orient][f"col{col}_std"][0],
                    type=col
                )
        if col == 1:
            curr_x -= 20
        else:
            curr_x += 30
        # Get the first line distance relative to the column location
        line_y = get_random_value(
                    avg=config[orient][f"line{col}"],
                    std=config[orient][f"line{col}_std"],
                    type=0
                )

        # Get the position of the first line in the page according to the average column position
        curr_y = get_random_value(
                    avg=(config[orient]["col1"][1]+config[orient]["col2"][1])/2,
                    std=(config[orient]["col1_std"][1]+config[orient]["col2_std"][1])/2,
                    type=col
                ) + line_y

        line_text = text_list[nb_line]
        line_ink = ink_list[nb_line]
        line_coord = line_text.getbbox()
        line_data = tsv_lines[nb_line]
        txt = line_data[0].split()
        word_pos = ",".join([f"{a}-{b}" for (a, b) in line_data[1]])
        mask.paste(line_text, (curr_x, curr_y-baseline))
        texture.paste(line_ink, (curr_x, curr_y-baseline))
        line_pos = (curr_x, curr_y-baseline, curr_x+line_coord[2], curr_y-baseline+line_coord[3])
        # img.line([(curr_x, curr_y), (curr_x+round(config[orient][f"col{col}"][2]), curr_y)], fill="yellow", width=5)
        write_tsv(page_id, COLUMNS[col-1], format_int(nb_line), line_pos, curr_y, txt, word_pos)
        nb_line +=1 
        for line in range(1, 26):
            # if nb_line == len(text)-1:
            #     nb_line = 0
            curr_y = int(curr_y+lines_spacing)
            line_text = text_list[nb_line]
            line_ink = ink_list[nb_line]
            line_coord = line_text.getbbox()
            line_data =tsv_lines[nb_line]
            txt = line_data[0].lower().split()
            word_pos = ",".join([f"{a}-{b}" for (a, b) in line_data[1]])
            mask.paste(line_text, (curr_x, curr_y-baseline))
            texture.paste(line_ink, (curr_x, curr_y-baseline))
            line_pos = (curr_x, curr_y-baseline, curr_x+line_coord[2], curr_y-baseline+line_coord[3])
            # img.rectangle(line_pos, fill="yellow", width=5)
            write_tsv(page_id, COLUMNS[col-1], format_int(nb_line), line_pos, curr_y, txt, word_pos)
            nb_line+=1
    final = Image.composite(input_bg, texture, mask=ImageOps.invert(mask))
    
    return final


def get_config():
    """
    Get the config from the YAML file, returns a dictionary
    """
    data =  dict()
    with open("./Task4/config.yaml") as config:
        data = yaml.full_load(config)
    return data["orient"]


def get_random_value(avg, std, type):
    """
    Return a randomly generated line spacing, from the calculated average and standard deviation
    Type: 0 = get between -1std and +1std; 1 = avg and +1std
    """
    if type == 0:
        return round(random.uniform(avg-std, avg+std))
    elif type == 1:
        return round(random.uniform(avg-std, avg))
    else:
        return round(random.uniform(avg, avg+std))


def write_tsv(page_id, column_id, line_id, line_pos, baseline, string, word_pos):
    header = f"{page_id}_{column_id}_{line_id}"
    line = f"{','.join(map(str, line_pos))}\t{baseline}\t{'-'.join(map(str, string))}\t{word_pos}"
    line_tsv = f"{header}\t{line}\n"
    with open("./out/ground_truth.tsv", "a") as tsv:
        tsv.write(line_tsv)


def format_int(line_id):
    line_id += 1
    if line_id > 26:
        line_id -= 26

    if line_id < 10:
        return f"0{line_id}"
    else:
        return f"{line_id}"
