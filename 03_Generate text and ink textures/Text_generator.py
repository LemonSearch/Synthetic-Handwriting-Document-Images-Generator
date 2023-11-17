from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import random

def is_uppercase(letter):
    return letter.isupper()

def check_uppercase_letters(filename):
    for line in text:
        for letter in line:
            if is_uppercase(letter):
                print(letter)

def reproduce_text(image_path, font_size, font_color, text_position, target_letter, filetext):
    # Open the filetext and check the letters
    with open(filetext, 'r') as f:
        text = f.read()
    check_uppercase_letters(text)
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    # Load the TTF font
    font_path = "carolus.ttf"
    font = ImageFont.truetype(font_path, font_size)
    # Draw the text on the image
    draw.text(text_position, text, font=font, fill=font_color)
    image.show()
    mask_region(image, font, target_letter)



def mask_region(image, font, target_letter):
    # Create a separate image with a lesser size than the original image
    mask_image = Image.new('L', (font_size * len(target_letter), font_size), 0)
    mask_draw = ImageDraw.Draw(mask_image)

    # Draw the target letter on the mask image
    mask_draw.text((0, 0), target_letter, font=font, fill=255)

    # Convert the mask image to grayscale
    mask_image = mask_image.convert('L')

    # Apply intensity adjustment to the target letter on the mask image
    enhancer = ImageEnhance.Brightness(mask_image)
    mask_image = enhancer.enhance(0.9)

    # Extract the region of interest from the original image
    # region_of_interest = image.crop((text_position[0], text_position[1], text_position[0] + font_size * len(target_letter), text_position[1] + font_size))

    # Calculate the actual position of the target letter within the bounding box
    target_letter_width = 0
    for char in text[:text.index(target_letter)]:
        char_mask = font.getmask(char)
        char_width, char_height = char_mask.size
        target_letter_width += char_width

    target_letter_position = (text_position[0] + target_letter_width, text_position[1])

    # Extract the region of interest from the original image
    region_of_interest = image.crop((target_letter_position[0], target_letter_position[1],
                                      target_letter_position[0] + font_size * len(target_letter),
                                      target_letter_position[1] + font_size))

    # Apply the mask to the region of interest
    result_region = Image.new('RGB', region_of_interest.size, (0, 0, 0))
    result_region.paste(region_of_interest, mask=mask_image)
    
    # Paste the modified region back into the original image
    image.paste(result_region, box=target_letter_position)

    # Save the modified image
    image.save("modified_image.jpg")

# Example usage
filetext = "transcript.txt"
image_path = "image.jpg"
text = "Hello, world!"
font_size = 16
target_letter = "o"  # Specify the target letter
font_color = (137, 107, 81)
text_position = (130, 250)

reproduce_text(image_path, font_size, font_color, text_position, target_letter, filetext)