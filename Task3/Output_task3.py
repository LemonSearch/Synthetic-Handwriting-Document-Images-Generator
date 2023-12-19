from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
from faker import Faker
from .Sentence import load_images_for_sentence, calculate_size, create_final_image, calculate_bottom_offset

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
    #print(max_height)
    for ink_char, letter_position, up_char in zip (ink_chars, letter_positions, up_chars):
        offset = calculate_bottom_offset(up_char)
        ink_texture_image.paste(ink_char, (letter_position, max_height + 40 - ink_char.size[1] + offset))
    ink_texture_image = ink_texture_image.filter(ImageFilter.GaussianBlur(radius=1.3))
    #ink_texture_image.show()
    return ink_texture_image

def text_lines(font, font_size, text_position, text, max_line_width, image_dir):
    # Initialize variables
    images = []
    lines = []
    ink_images = []
    tsv_line = []
    current_line = ''
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
        line_bbox = font.getbbox(current_line)
        line_width = line_bbox[2] - line_bbox[0]
        # Check if reaching max line width
        if (line_width + word_width)*font_size >= max_line_width:
            # Add current line to lines and start a new line
            lines.append(current_line)
            current_line = word + ' '
        else:
            current_line += word + ' '

    # Add the last line if not empty
    if current_line:
        lines.append(current_line)

    for line in lines:
        #print(line)
        loaded_images = load_images_for_sentence(line, image_dir)
        total_width, max_height, letter_spaces, word_spaces = calculate_size(loaded_images)
        final_image, letter_positions, word_coordinates, ink_chars, up_chars = create_final_image(loaded_images, total_width, max_height, letter_spaces, word_spaces)
        #final_image.show()
        ink_texture_image = reproduce_ink(final_image, ink_chars, letter_positions, max_height, up_chars)
        left, upper, right, lower = final_image.getbbox()
        # Store coordinates in a list for the current line image
        coordinates = (left, upper, right, lower)
        # Baseline position 
        baseline_position = max_height - offset
        # Append the coordinates to the list of all coordinates
        all_coordinates.append(coordinates)
        # Append the line image to the list of all lines images
        images.append(final_image)
        # Append the ink line to the list of all lines ink images
        ink_images.append(ink_texture_image)
        
        tsv_line.append((line, word_coordinates))
    # (flavien) Made the method return the coordinated in case I need them
    return images, all_coordinates, ink_images, baseline_position, tsv_line

def generate_text(fake_txt=False):
        latin_text = ""
        if fake_txt:
            fake = Faker('la')  # 'la' is the language code for Latin

            latin_text = fake.text(max_nb_chars=1000)  # Adjust the number as needed
        else:
            with open("./Task3/latin.txt") as latin:
                latin_text = latin.read()

        return latin_text

def reproduce_text(font_size, text_position, max_line_width, image_dir):
    # Load the TTF font
    # (flavien) Had to change the path to be relative to the main.py
    font_path = "./Task3/carolus.ttf"
    font = ImageFont.truetype(font_path, font_size, encoding="unic")

    # Extract the transcript text from a file .txt
    text = generate_text()
    # Draw text on a separate image
    list_images, list_coord, blended_ink_images, baseline, tsv_line = text_lines(font, font_size, text_position, text, max_line_width, image_dir)

    return list_images, blended_ink_images, list_coord, baseline, tsv_line

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
