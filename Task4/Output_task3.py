from PIL import Image, ImageDraw, ImageFont

def draw_text_with_boxes(image_path, font, font_size, text_position, font_color, text_path, max_line_width):
    image = Image.open(image_path)
    # Convert text to RGBA image
    font = ImageFont.truetype(font, font_size)
    font_color = (137, 107, 81, 240)
    text_image = Image.new('RGBA', image.size, (255, 255, 255, 0))  # Initialize with transparent background
    draw_text = ImageDraw.Draw(text_image)

    # Initialize variables
    lines = []
    current_line = ''
    current_x, current_y = text_position

    with open(text_path) as text:
        # Process text and create lines
        for word in text.readline().split():
            # Calculate the width of the word
            word_bbox = font.getbbox(word)
            word_width = word_bbox[2] - word_bbox[0]
            
            # Check if reaching max line width
            if len(current_line) * font_size + word_width > max_line_width:
                # Add current line to lines and start a new line
                lines.append(current_line)
                current_line = word
            else:
                current_line += word + ' '

        # Add the last line if not empty
        if current_line:
            lines.append(current_line)
    
    # Draw text onto the text image within each line
    for line in lines:
        line_bbox = (current_x, current_y, current_x + len(line) * font_size, current_y + font_size)
        draw_text.text((line_bbox[0], line_bbox[1]), line, fill=font_color, font=font, size=font_size)
        current_y += font_size * 1.5 # not necessary for the final output
    
    # Output: list of the lines
    return lines
