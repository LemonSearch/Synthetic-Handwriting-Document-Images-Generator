from PIL import Image, ImageDraw, ImageFont,  ImageFilter
import numpy as np
import random

def is_uppercase(letter):
    return letter.isupper()

def check_uppercase(text):
    for line in text:
        for letter in line:
            if is_uppercase(letter):
                print(letter)

def smudgeness(letter_image):
    smudged_letter = letter_image.filter(ImageFilter.SMOOTH)
    return smudged_letter

def reproduce_ink (image):
    image_height, image_width = image.size
    # Create an ink texture
    ink_texture = np.zeros((image_height, image_width, 3), dtype=np.uint8)  # Add an alpha channel
    ink_opacity = 0.5  # Ink opacity
    brown_color = (150, 75, 0)
    # Generate ink texture with varying shades of brown
    for i in range(image_height):
        for j in range(image_width):
            if np.random.rand() < ink_opacity:
                # Vary the intensity levels for red and green channels
                intensity = np.random.randint(50, 150)  # Adjust the range as needed
                ink_texture[i, j] = (intensity, intensity // 2, 0)  # Brown color
            else:
                ink_texture[i, j] = brown_color
    # Convert ink texture to PIL Image
    ink_texture_image = Image.fromarray(ink_texture, 'RGB')
    return ink_texture_image

def extract_text(filetext):
    with open(filetext, 'r') as f:
        # Read the entire contents of the file
        text = f.read()
        check_uppercase(text)
    return text

def reproduce_text(image_path, font_size, text_position, target_letter, filetext):

    # Load the image
    image = Image.open(image_path)
    # Load the TTF font
    font_path = "carolus.ttf"
    font = ImageFont.truetype(font_path, font_size)
    # Define ink texture parameters
    font_color = (137, 107, 81, 130)
    # Generate ink texture with varying shades of brown
    ink_texture_image = reproduce_ink(image)
    # Convert text to RGBA image
    text_image = Image.new('RGBA', image.size, (255, 255, 255, 0))  # Initialize with transparent background
    draw_text = ImageDraw.Draw(text_image)

    # Extract the transcript text from a file .txt
    text = extract_text(filetext)
    draw_text.text(text_position, text, font=font, fill=font_color)
    # Resize ink texture image if dimensions do not match
    if text_image.size != ink_texture_image.size:
        ink_texture_image = ink_texture_image.resize(text_image.size)

    # Blend the ink texture and text images using Image.composite
    blended_image = Image.composite(ink_texture_image, image, text_image)
    blended_image.show()
    blended_image.save("Blended_image.jpg")


""" 
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
 """

# Example usage
filetext = "transcript.txt"
image_path = "image.jpg"
font_size = 20
target_letter = "o"  # Specify the target letter
text_position = (130, 300)

reproduce_text(image_path, font_size, text_position, target_letter, filetext)