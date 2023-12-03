from PIL import Image, ImageDraw, ImageFont
import numpy as np
from faker import Faker
from .Sentence import load_images_for_sentence, calculate_size, create_final_image

def reproduce_ink (list_image):
    ink_images = []
    for image in list_image:
        image_width, image_height = image.size
        # Create an ink texture
        ink_texture = np.zeros((image_height, image_width, 3), dtype=np.uint8)  # Add an alpha channel
        ink_opacity = 0.5  # Ink opacity
        brown_color = (51, 34, 24)
        # Generate ink texture with varying shades of brown
        for i in range(image_height):
            for j in range(image_width):
                if np.random.rand() < ink_opacity:
                    # Vary the intensity levels for red and green channels
                    intensity = np.random.randint(34, 78)  # Adjust the range as needed
                    ink_texture[i, j] = (intensity, intensity // 2, 0)  # Brown color
                else:
                    ink_texture[i, j] = brown_color
        # Convert ink texture to PIL Image
        ink_texture_image = Image.fromarray(ink_texture, 'RGB')
        ink_images.append(ink_texture_image)
    return ink_images

def draw_text_with_boxes(font, font_size, text_position, text, max_line_width, image_dir):

    # Initialize variables
    images = []
    lines = []
    current_line = ''    
    letter_spacing = 2
    word_spacing = 45
    all_coordinates = [] # List to store coordinates of multiple images

    # Process text and create lines
    for word in text.split(' '):
        # Calculate the width of the word
        # (Flavien) I Added some paramters here that may be necessary
        word_bbox = font.getbbox(word, direction="ltr", language="la", anchor="ls")
        word_width = word_bbox[2] - word_bbox[0]
        # (Flavien) Use the line bbox directly to calculate the size
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
        loaded_images = load_images_for_sentence(line, image_dir)
        total_width, max_height = calculate_size(loaded_images, letter_spacing, word_spacing)
        final_image = create_final_image(loaded_images, total_width, max_height+40, letter_spacing)
        left, upper, right, lower = final_image.getbbox()
        """(Flavien) This should take the coordinated form the bbox of the text instead
            of the image generated from the text. This way we can have the coordinates of the baselie
            with the argument 'anchor='ls'' like I did before.
        """
        # Store coordinates in a list for the current line image
        coordinates = (left, upper, right, lower)
        # Append the coordinates to the list of all coordinates
        all_coordinates.append(coordinates)
        # Append the line images to the list of all lines
        images.append(final_image)
    # (flavien) Made the method return the coordinated in case I need them
    return images, all_coordinates

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
    text = generate_text()

    # Draw text on a separate image
    list_images, list_coord = draw_text_with_boxes(font, font_size, text_position, text, max_line_width, image_dir)

    # Generate ink texture with varying shades of brown
    ink_images = reproduce_ink(list_images)
    return list_images, ink_images, list_coord

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
