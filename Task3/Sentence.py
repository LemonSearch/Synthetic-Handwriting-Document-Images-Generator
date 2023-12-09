from PIL import Image, ImageFilter, ImageDraw
import os
import random
import numpy as np
from Task2.SentenceGenerator import load_images_for_sentence, calculate_size, transform_image, calculate_bottom_offset, calculate_right_offset, make_black_transparent

# ink generator
def generate_ink_char(character_image):
    copy_image = character_image.copy()
    copy_image = copy_image.convert("RGBA")
    density = 0.1 # Can be changed
    width, height = copy_image.size
    # Create an ink texture
    draw = ImageDraw.Draw(copy_image)

    num_ink_spots = int(width * height * density)

    for _ in range(num_ink_spots):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        
        ink_color = (92, 64, 51, random.randint(100, 150))  # Varying transparency
        brush_size = random.randint(1, 5)

        # Use ellipses for ink spots
        draw.ellipse([x - brush_size, y - brush_size, x + brush_size, y + brush_size], fill=ink_color)
        
    copy_image = copy_image.filter(ImageFilter.GaussianBlur(radius=1))
    return copy_image

def create_final_image(loaded_images, total_width, max_height, letter_spaces, word_spaces):
    final_image = Image.new('RGB', (total_width, max_height), (0, 0, 0))
    current_width = 0
    word_length = 0
    letter_position = []
    word_coordinates = []
    ink_chars = []
    up_chars = []
    letter_space_index = 0
    word_space_index = 0

    start_word = -1
    end_word = -2

    for char, image in loaded_images:
        # print('char: ', char)
        if image:
            image = transform_image(image)
            bottom_offset = calculate_bottom_offset(char)
            right_offset = calculate_right_offset(char)
            if char.isupper():
                ink_char  = generate_ink_char(image)
                ink_chars.append(ink_char)
                letter_position.append(current_width)
                up_chars.append(char)
            final_image.paste(image, (current_width, max_height - image.size[1] + bottom_offset))
            current_width += image.size[0] + right_offset + letter_spaces[letter_space_index]
            word_length += image.size[0] + right_offset + letter_spaces[letter_space_index]
            letter_space_index += 1
        else:
            start_word = current_width - word_length
            end_word = current_width
            word_coordinates.append((start_word, end_word))
            current_width += word_spaces[word_space_index]
            word_length = 0
            word_space_index += 1
    # checks if the line ends with a space
    if start_word == end_word:
        word_coordinates.pop()
    return final_image, letter_position, word_coordinates, ink_chars, up_chars