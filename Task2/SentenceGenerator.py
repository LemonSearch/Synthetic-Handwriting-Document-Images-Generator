from PIL import Image, ImageFilter
import os
import random
import numpy as np

# sentence generator below
def load_images_for_sentence(sentence, image_dir):
    images = []
    collecting = False
    collected_chars = ""
    for char in sentence:
        # justify if it is like (christi)
        if collecting:
          if char == ')':
            collecting = False
            collected_chars += char
            
            image_path = os.path.join(image_dir, f"{collected_chars}.png")
            try:
              character_image = Image.open(image_path)
              images.append((collected_chars, character_image))
            except IOError:
              
              print(f"Image for {collected_chars} not found.")

            collected_chars = ""
          else:
            collected_chars += char
          continue

        if char == '(':
          collecting = True
          collected_chars += char
          continue
        
        if char != ' ':
          
          # small letter
          if char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'x', 'y', 'z', 'j', 'u', 'w']:
            image_path = os.path.join(image_dir, f"{char}_1.png")
            try:
              character_image = Image.open(image_path)
              images.append((char, character_image))
            except IOError:
              print(f"Image for {char} not found.")

          # notation
          elif char in ['.', ',', ';']:
            image_path = os.path.join(image_dir, f"{char}_notation.png")
            try:
              character_image = Image.open(image_path)
              images.append((char, character_image))
            except IOError:
              print(f"Image for {char} not found.")

          # number
          elif char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            image_path = os.path.join(image_dir, f"{char}_number.png")
            try:
              character_image = Image.open(image_path)
              images.append((char, character_image))
            except IOError:
              print(f"Image for {char} not found.")

          # upper letter
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

# when consider the distance between each letter, we need to justify both in total width and letter pasting
def calculate_size(loaded_images):
    total_width = 0
    max_height = 0
    letter_spaces = []
    word_spaces = []
    for char, image in loaded_images:
        if image:
            letter_spacing = random.randint(2, 3)
            right_offset = calculate_right_offset(char)
            total_width += image.size[0] + right_offset + letter_spacing
            max_height = max(max_height, image.size[1])
            letter_spaces.append(letter_spacing)
        else:
            word_spacing= random.randint(30, 50)
            total_width += word_spacing
            word_spaces.append(word_spacing)

    return total_width, max_height+34, letter_spaces, word_spaces

def transform_image(image):

    # make it blur
    blur_radius = random.uniform(0.9, 1)
    image = image.filter(ImageFilter.GaussianBlur(blur_radius))

    rotation_angle = random.uniform(-2, 2)
    rotated_image = image.rotate(rotation_angle, expand=True)

    scale_factor = random.uniform(0.98, 1.02)
    new_width = int(rotated_image.width * scale_factor)
    new_height = int(rotated_image.height * scale_factor)

    vertical_stretch_factor = random.uniform(0.98, 1.02)
    stretched_height = int(new_height * vertical_stretch_factor)

    transformed_image = rotated_image.resize((new_width, stretched_height), Image.BICUBIC)

    return transformed_image

def calculate_bottom_offset(char):
    bottom_offsets = {'f': -19, 'g': 0, 'p': -14, 'q': -14, 'j': -3, 'F': -13,
                      'G': -23, 'H': -31, 'J': -6, 'P': -20, 'Q': -22, 'R': -22,
                      'T': -31, 'Y': 0, 'Z': -30, 
                      '(christi)': -24, '(prae)': -16, '(que)': -14, '(em)': -34, '(am)': -34, '(et)': -34,}
    return bottom_offsets.get(char, -34)

def calculate_right_offset(char):
    right_offsets = {'f': -20}
    # , 'g': 0, 'p': -14, 'q': -14, 'j': -3, 'F': -13,' G': -23, 'H': -31, 'J': -6, 'P': -20, 'Q': -22, 'R': -22, 'T': -31, 'Y': 0, 'Z': -30
    return right_offsets.get(char, 0)

def make_black_transparent(image, shift_white_letter):

    img = image
    img = img.convert("RGBA")
    data = np.array(img)

    red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    dark_mask = (red < 100) & (green < 100) & (blue < 100)
    data[:,:,:4][dark_mask] = [0, 0, 0, 0]

    if shift_white_letter:
      # Invert bright pixels (RGB > 200)
      bright_mask = (red > 100) & (green > 100) & (blue > 100)
      data[:,:,0][bright_mask] = 255 - data[:,:,0][bright_mask]
      data[:,:,1][bright_mask] = 255 - data[:,:,1][bright_mask]
      data[:,:,2][bright_mask] = 255 - data[:,:,2][bright_mask]

    new_img = Image.fromarray(data)

    return new_img