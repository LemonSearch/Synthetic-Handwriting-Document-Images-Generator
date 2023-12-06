from PIL import Image
import os
import random
import numpy as np

def load_images_for_sentence(sentence, image_dir):
    images = []
    for char in sentence:
        if char != ' ':
          if char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'x', 'y', 'z', 'j', 'u', 'w']:
            image_path = os.path.join(image_dir, f"{char}_1.png")
            try:
              character_image = Image.open(image_path)
              images.append((char, character_image))
            except IOError:
              print(f"Image for {char} not found.")
          else:
            image_path = os.path.join(image_dir, f"{char}_c_1.png")
            try:
              character_image = Image.open(image_path)
              images.append((char, character_image))
            except IOError:
              print(f"Image for {char} not found.")
        else:
          images.append((' ', None))
    return images

def calculate_size(loaded_images):
    total_width = 0
    max_height = 0
    letter_spaces = []
    word_spaces = []
    for _, image in loaded_images:
        if image:
            letter_spacing = random.randint(2, 3)
            total_width += image.size[0] + letter_spacing
            max_height = max(max_height, image.size[1])
            letter_spaces.append(letter_spacing)
        else:
            word_spacing= random.randint(30, 50)
            total_width += word_spacing
            word_spaces.append(word_spacing)

    return total_width, max_height+34+14, letter_spaces, word_spaces

def transform_image(image):
    rotation_angle = random.uniform(-2, 2)
    rotated_image = image.rotate(rotation_angle, expand=True)

    scale_factor = random.uniform(0.98, 1.02)
    new_width = int(rotated_image.width * scale_factor)
    new_height = int(rotated_image.height * scale_factor)

    vertical_stretch_factor = random.uniform(0.98, 1.02)
    stretched_height = int(new_height * vertical_stretch_factor)

    transformed_image = rotated_image.resize((new_width, stretched_height), Image.ANTIALIAS)

    return transformed_image

def create_final_image(loaded_images, total_width, max_height, letter_spaces, word_spaces):
    final_image = Image.new('RGB', (total_width, max_height), (0, 0, 0))
    current_width = 0
    letter_position = []
    letter_space_index = 0
    word_space_index = 0
    for char, image in loaded_images:
        letter_position.append(current_width)
        if image:
            image = transform_image(image)
            if char == 'f':
              offset = -19
            elif char == 'g':
              offset = 0
            elif char in ['p', 'q']:
              offset = -14
            elif char == 'j':
              offset = -3
            elif char == 'F':
              offset = -13
            elif char == 'G':
              offset = -23
            elif char == 'H':
              offset = -31
            elif char == 'J':
              offset = -6
            elif char == 'P':
              offset = -20
            elif char == 'Q':
              offset = -22
            elif char == 'R':
              offset = -22
            elif char == 'T':
              offset = -31
            elif char == 'Y':
              offset = 0
            elif char == 'Z':
              offset = -30
            else:
              offset = -34
            final_image.paste(image, (current_width, max_height - image.size[1] + offset))
            current_width += image.size[0] + letter_spaces[letter_space_index]
            letter_space_index += 1
        else:
            current_width += word_spaces[word_space_index]
            word_space_index += 1
    return final_image, letter_position

# demo:
# image_dir = './Dictionary'

# # Put your latin sentence here:
# # Hope our work will help more people.
# sentence = "Spes Laboris Nostri Plus Potest Adiuvare Homines YYYYY."

# loaded_images = load_images_for_sentence(sentence, image_dir)
# total_width, max_height, letter_spaces, word_spaces = calculate_size(loaded_images)
# final_image, letter_position = create_final_image(loaded_images, total_width, max_height, letter_spaces, word_spaces)
# final_image_path = os.path.join(image_dir, "final_sentence_image.png")
# final_image.save(final_image_path)
# print("Image created and saved to", final_image_path)