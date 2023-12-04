from PIL import Image, ImageOps
import os
import random

def load_images_for_sentence(sentence, image_dir):
    images = []
    for char in sentence:
        if char != ' ':
            image_path = os.path.join(image_dir, f"{char}_1.png")
            try:
                character_image = Image.open(image_path)
                images.append((char, character_image))
            except IOError:
                pass
                #print(f"Image for {char} not found.")
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
            letter_spacing = random.randint(1, 3)  # Can be changed the range
            word_spacing= random.randint(5, 45)  # Can be changed the range
            total_width += image.size[0] + word_spacing
            max_height = max(max_height, image.size[1])
            total_width += len([image for _, image in loaded_images]) * letter_spacing
            letter_spaces.append(letter_spacing)
            word_spaces.append(word_spacing)
    return total_width, max_height, letter_spaces, word_spaces

def create_final_image(loaded_images, total_width, max_height, letter_spaces, word_spaces):
    final_image = Image.new('L', (total_width, max_height), 0)
    current_width = 0
    for (char, image), letter_spacing, word_spacing in zip(loaded_images, letter_spaces, word_spaces):
        if image:
            if char in ['p', 'q']:
                offset = -14
                final_image.paste(image, (current_width, max_height - image.size[1] + offset))
            elif char in ['f']:
                offset = -19
                final_image.paste(image, (current_width, max_height - image.size[1] + offset))
            elif char in ['g']:
                offset = 0
                final_image.paste(image, (current_width, max_height - image.size[1] + offset))
            else:
                offset = -34
                final_image.paste(image, (current_width, max_height - image.size[1] + offset))
            current_width += image.size[0] + letter_spacing
        else:
            current_width += word_spacing
    return final_image

