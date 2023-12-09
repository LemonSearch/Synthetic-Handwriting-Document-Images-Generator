import cv2
import numpy as np
from PIL import Image
import random
import os

#Crop the image
def crop_image(image):
    height, width, _ = image.shape
    cropped_image = image[600:height-1000, 210:width-250]
    cv2.imwrite('crop_image.png', cropped_image)
    return cropped_image

#Detect the text regions
def get_text_regions(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imwrite('thresh_image.jpg', thresh)
    # Draw contours on the copy of the original text
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0,255,0), 2)
    #Save the image with contours
    cv2.imwrite("image_with_contours.png",image_with_contours)
    return contours

#Replace the text on the cropped image with the background color
def replace_text(image, text_regions, subregion_size=5, distance_factor=80, blur_size=5):
    result_image = image.copy()

    for contour in text_regions:
        # Get the bounding box of the text region
        x, y, w, h = cv2.boundingRect(contour)

        # Divide the text region into smaller sub-regions
        for i in range(0, h, subregion_size):
            for j in range(0, w, subregion_size):

                # Get the color of the background below the text (not detected as text)
                background_y = min(y + i + subregion_size // 2 + distance_factor, result_image.shape[0] - 1)
                background_x = min(x + j + subregion_size // 2 + distance_factor, result_image.shape[1] - 1)
                background_color = result_image[background_y, background_x]

                # Replace the sub-region with the background color
                result_image[y + i:y + i + subregion_size, x + j:x + j + subregion_size] = background_color

    return result_image

#Paste the result of erased text image on the original sample image
def paste_image(original_image, result_image, position):
    height, width, _ = result_image.shape
    original_image[position[1]:position[1]+height, position[0]:position[0]+width] = result_image

#Position and Paste the stains randomly from the stains folder(stains colleced from web)
def paste_stain(background, stain_path, position, scale_range=(0.1, 0.5), rotation_range=(0, 360)):
    stain = Image.open(stain_path).convert("RGBA")

    # Randomly scale the stain
    scale_factor = random.uniform(scale_range[0], scale_range[1])
    new_size = tuple(int(dim * scale_factor) for dim in stain.size)
    stain = stain.resize(new_size, Image.Resampling.LANCZOS)

    # Randomly rotate the stain
    rotation_angle = random.uniform(rotation_range[0], rotation_range[1])
    stain = stain.rotate(rotation_angle, Image.BICUBIC, expand=True)

    # Paste the stain onto the background
    background.paste(stain, position, stain)

#Function to generate the stained image
def generate_background_with_stains(original_background):
    background = original_background.convert("RGBA")
    stains_folder = "./Task1/Stains/"
    # Randomly choose a stain image
    stain_files = os.listdir(stains_folder)
    selected_stain = random.choice(stain_files)
    stain_path = os.path.join(stains_folder, selected_stain)

    # Randomly choose a position on the background
    position = (random.randint(210, background.width-250), np.random.randint(600, background.height-1000))

    # Paste the stain onto the background
    paste_stain(background, stain_path, position)

    # Save the resulting image
    # output_path = os.path.join(output_folder, f'result_image_{i + 1}.png')
    # background.save(output_path, format="PNG")
    # outputs.append(background)

    # Reset background for the next iteration
    # background = original_background
    return background


def generate_background():
    dataset = "./dataset/real documents/"
    new_bg = list()
    files = os.listdir(dataset)
    file = random.choice(files)
    image = cv2.imread(dataset+file)
    cropped_image = crop_image(image)
    text_regions = get_text_regions(cropped_image)
    result_image = replace_text(cropped_image, text_regions)
    paste_image(image, result_image, position=(220, 500))
    pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    new_bg = generate_background_with_stains(pil)
    
    return new_bg 

if __name__ == "__main__":
    image = cv2.imread('e-codices_csg-0231_088_max.jpg')
    cropped_image = crop_image(image)

    text_regions = get_text_regions(cropped_image)
    result_image = replace_text(cropped_image, text_regions)

    # Paste the result_image onto the original image
    paste_image(image, result_image, position=(220, 500))

    # Save the result
    cv2.imwrite('final_result.png', image)

    #Specify the paths to the images and folders
    background_path = "final_result.png"
    stains_folder = "Stains"
    output_folder = "GeneratedImages"
    num_images_to_generate = 13

    generate_background_with_stains(background_path, stains_folder, output_folder, num_images_to_generate)

