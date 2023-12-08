from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random
import csv
import os
import re
from faker import Faker
from .Sentence import load_images_for_sentence, calculate_size, create_final_image

def reproduce_ink (line_image, ink_chars, letter_positions, max_height, up_chars):
    density = 0.1 # Can be changed
    width, height = line_image.size
    # Create an ink texture
    ink_texture_image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(ink_texture_image)

    num_ink_spots = int(width * height * density)

    for _ in range(num_ink_spots):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        ink_color = (139, 69, 19, random.randint(0, 150))  # Varying transparency
        brush_size = random.randint(3, 5)

        # Use ellipses for ink spots
        draw.ellipse([x - brush_size, y - brush_size, x + brush_size, y + brush_size], fill=ink_color)

    # Apply blur for a subtle smudging effect
    ink_texture_image = ink_texture_image.filter(ImageFilter.GaussianBlur(radius=1))
    # for ink_char, letter_position, up_char, height in zip (ink_chars, letter_positions, up_chars, heights):
    #     if up_char == 'F':
    #         offset = -13
    #     elif up_char == 'G':
    #         offset = -23
    #     elif up_char == 'H':
    #         offset = -31
    #     elif up_char == 'J':
    #         offset = -6
    #     elif up_char == 'P':
    #         offset = -20
    #     elif up_char == 'Q':
    #         offset = -22
    #     elif up_char == 'R':
    #         offset = -22
    #     elif up_char == 'T':
    #         offset = -31
    #     elif up_char == 'Y':
    #         offset = 0
    #     elif up_char == 'Z':
    #         offset = -30
    #     else:
    #         offset = -34
    #     ink_texture_image.paste(ink_char, (letter_position, max_height - ink_char.size[1] + offset))
    # ink_texture_image.show()
    return ink_texture_image

# Function not used yet
def ground_truth (text, text_position, word_lengths, word_spaces, baseline_position, coordinates, filename):
    i=0
    j=0
    with open(filename, 'a', newline='') as csvfile:
        csvfile.write(f"{coordinates[0]},{coordinates[1]},{coordinates[2]},{coordinates[3]}\t")
        # Split the input string into words
        words = re.findall(r"[\w']+|[^\s\w]", text)
        # Separate each word with '-' and write to the TSV file
        for word in words:
            if j==0:
                csvfile.write(f"{word}")
                j=1
            else:
                csvfile.write(f"-{word}")
        csvfile.write("\t\t")
    with open(filename, 'a', newline='') as csvfile:
        for word_length, word_space in zip(word_lengths, word_spaces):
            if i==0:
                current_position = text_position[0]
                csvfile.write(f"{current_position}-{word_length}")
                i=1
            else:
                current_position = word_length + word_space
                csvfile.write(f",{current_position}-{current_position+word_length}")
        csvfile.write("\n")

def draw_text_with_boxes(font, font_size, text_position, text, max_line_width, image_dir):
    # Initialize variables
    images = []
    lines = []
    ink_images = []
    current_line = ''
    i = 0
    row_spacing = -2    # set row spacing
    offset = 34
    all_coordinates = [] # List to store coordinates of multiple images
    filename = 'ground_truth.tsv'
    if os.path.exists(filename):
        # Truncate the file
        os.truncate(filename, 0)

    # Process text and create lines
    for word in text.split(' '):
        # Calculate the width of the word
        # (Flavien) I Added some paramters here that may be necessary
        word_bbox = font.getbbox(word)
        word_width = word_bbox[2] - word_bbox[0]
        line_bbox = font.getbbox(current_line, direction='ltr', language='la', anchor='ls')
        line_width = line_bbox[2] - line_bbox[0]
        # Check if reaching max line width
        if (line_width + word_width)*font_size >= max_line_width:
            # Add current line to lines and start a new line
            lines.append(current_line)
            current_line = word
        else:
            current_line += word + ' '

    # Add the last line if not empty
    if current_line:
        lines.append(current_line)

    for line in lines:
        print(line)
        loaded_images = load_images_for_sentence(line, image_dir)
        total_width, max_height, letter_spaces, word_spaces = calculate_size(loaded_images)
        final_image, letter_positions, word_lengths, word_spaces, ink_chars, up_chars = create_final_image(loaded_images, total_width, max_height+40, letter_spaces, word_spaces)
        #final_image.show()
        ink_texture_image = reproduce_ink(final_image, ink_chars, letter_positions, max_height, up_chars)
        left, upper, right, lower = final_image.getbbox()
        # Store coordinates in a list for the current line image
        coordinates = (left, upper, right, lower)
        # Baseline position 
        baseline_position = max_height - offset
        # print(baseline_position)
        # print(coordinates)
        # TO FINISH
        ground_truth(line, text_position, word_lengths, word_spaces, baseline_position, coordinates, filename)
        # Append the coordinates to the list of all coordinates
        all_coordinates.append(coordinates)
        # Append the line image to the list of all lines images
        images.append(final_image)
        # Append the ink line to the list of all lines ink images
        ink_images.append(ink_texture_image)
    # (flavien) Made the method return the coordinated in case I need them
    return images, all_coordinates, ink_images, baseline_position

def generate_text(fake_txt=False):
        latin_text = ""
        if fake_txt:
            fake = Faker('la')  # 'la' is the language code for Latin

            latin_text = fake.text(max_nb_chars=1000)  # Adjust the number as needed
        else:
            with open("./Task3/latin.txt") as latin:
                latin_text = latin.read(2000)

        return latin_text

def reproduce_text(font_size, text_position, max_line_width, image_dir):
    # Load the TTF font
    # (flavien) Had to change the path to be relative to the main.py
    font_path = "./Task3/carolus.ttf"
    font = ImageFont.truetype(font_path, font_size, encoding="unic")

    # Extract the transcript text from a file .txt
    # 
    text = generate_text()
    # text = "Test for the INK Texture Generation to check the UPPERCASES"
    # Draw text on a separate image
    list_images, list_coord, blended_ink_images, baseline = draw_text_with_boxes(font, font_size, text_position, text, max_line_width, image_dir)

    return list_images, blended_ink_images, list_coord, baseline

# Example usage
if __name__ == "__main__":
    font_size = 13
    text_position = (50, 200)
    max_line_width = 1200
    image_dir = "./Dictionary/" # Insert your directory

    t, i, c = reproduce_text(font_size, text_position, max_line_width, image_dir)
    t[0].show()
    i[0].show()
    print(c[0])
