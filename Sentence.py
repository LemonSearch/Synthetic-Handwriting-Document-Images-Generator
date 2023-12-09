from PIL import Image, ImageDraw, ImageFilter
import os
import random
import numpy as np

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

    return total_width, max_height+34, letter_spaces, word_spaces

def transform_image(image):
    rotation_angle = random.uniform(-2, 2)
    rotated_image = image.rotate(rotation_angle, expand=True)

    scale_factor = random.uniform(0.98, 1.02)
    new_width = int(rotated_image.width * scale_factor)
    new_height = int(rotated_image.height * scale_factor)

    vertical_stretch_factor = random.uniform(0.98, 1.02)
    stretched_height = int(new_height * vertical_stretch_factor)

    transformed_image = rotated_image.resize((new_width, stretched_height), Image.BICUBIC)

    return transformed_image

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

    for char, image in loaded_images:
        if image:
            image = transform_image(image)
            offset = calculate_offset(char)
            if char.isupper():
                ink_char  = generate_ink_char(image)
                ink_chars.append(ink_char)
                letter_position.append(current_width)
                up_chars.append(char)
            final_image.paste(image, (current_width, max_height - image.size[1] + offset))
            current_width += image.size[0] + letter_spaces[letter_space_index]
            word_length += image.size[0] + letter_spaces[letter_space_index]
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
    #print("Pre_blending: ", max_height)
    return final_image, letter_position, word_coordinates, ink_chars, up_chars

def calculate_offset(char):
    offsets = {'f': -19, 'g': 0, 'p': -14, 'q': -14, 'j': -3, 'F': -13,
               'G': -23, 'H': -31, 'J': -6, 'P': -20, 'Q': -22, 'R': -22,
               'T': -31, 'Y': 0, 'Z': -30}
    return offsets.get(char, -34)

def make_black_transparent(image, shift_white_letter):

    img = image
    img = img.convert("RGBA")
    data = np.array(img)

    red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    dark_mask = (red < 100) & (green < 100) & (blue < 100)
    data[:,:,:4][dark_mask] = [0, 0, 0, 0]

    if shift_white_letter:
      # Invert bright pixels (RGB > 200)
      bright_mask = (red > 200) & (green > 200) & (blue > 200)
      data[:,:,0][bright_mask] = 255 - data[:,:,0][bright_mask]
      data[:,:,1][bright_mask] = 255 - data[:,:,1][bright_mask]
      data[:,:,2][bright_mask] = 255 - data[:,:,2][bright_mask]

    new_img = Image.fromarray(data)

    return new_img

# demo
image_dir = '.Task3/Dictionary/'

# # Put your latin sentence here:
# sentence = "nomenq genusql"
# # Hope our work will help more people.
# sentence = "Spes Laboris Nostri Plus Potest Adiuvare Homines YYYYY."

# loaded_images = load_images_for_sentence(sentence, image_dir)
# total_width, max_height, letter_spaces, word_spaces = calculate_size(loaded_images)
# final_image, letter_position = create_final_image(loaded_images, total_width, max_height, letter_spaces, word_spaces)
# final_image = make_black_transparent(final_image, shift_white_letter=True) # choose shift white letter to black or not
# final_image_path = os.path.join(image_dir, "final_sentence_image.png")
# final_image.save(final_image_path)
# print("Image created and saved to", final_image_path)