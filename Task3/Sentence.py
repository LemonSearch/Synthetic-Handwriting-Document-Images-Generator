from PIL import Image
import os

def load_images_for_sentence(sentence, image_dir):
    images = []
    for char in sentence:
        if char != ' ':
            image_path = os.path.join(image_dir, f"{char}_1.png")
            try:
                character_image = Image.open(image_path)
                images.append((char, character_image))
            except IOError:
                print(f"Image for {char} not found.")
        else:
            images.append((' ', None))
    return images

def calculate_size(loaded_images, letter_spacing, word_spacing):
    total_width = sum(image.size[0] if image else word_spacing for _, image in loaded_images) + \
                  letter_spacing * (len([image for _, image in loaded_images if image]) - 1)
    max_height = max(image.size[1] for _, image in loaded_images if image)
    return total_width, max_height

def create_final_image(loaded_images, total_width, max_height, letter_spacing):
    final_image = Image.new('RGB', (total_width, max_height), (0, 0, 0))
    current_width = 0
    for char, image in loaded_images:
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

letter_spacing = 2
word_spacing = 45