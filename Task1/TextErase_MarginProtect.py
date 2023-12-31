import cv2
import numpy as np
import os

def crop_image(image):
    height, width, _ = image.shape
    cropped_image = image[500:height-1000, 100:width-500]
    cv2.imwrite('crop_image.jpg', cropped_image)
    return cropped_image

def get_text_regions(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def replace_text(image, text_regions, subregion_size=5, distance_factor=80, blur_size=5):
    result_image = image.copy()

    for contour in text_regions:
        # Get the bounding box of the text region
        x, y, w, h = cv2.boundingRect(contour)

        # Divide the text region into smaller sub-regions
        for i in range(0, h, subregion_size):
            for j in range(0, w, subregion_size):
                subregion = image[y + i:y + i + subregion_size, x + j:x + j + subregion_size]

                # Get the color of the background below the text (not detected as text)
                background_y = min(y + i + subregion_size // 2 + distance_factor, result_image.shape[0] - 1)
                background_x = min(x + j + subregion_size // 2 + distance_factor, result_image.shape[1] - 1)
                background_color = result_image[background_y, background_x]

                # Replace the sub-region with the background color
                result_image[y + i:y + i + subregion_size, x + j:x + j + subregion_size] = background_color

    return result_image

def paste_image(original_image, result_image, position=(100, 500)):
    height, width, _ = result_image.shape
    original_image[position[1]:position[1]+height, position[0]:position[0]+width] = result_image


def generate_background(file_list=None):
    dataset = "./dataset/real documents/"
    originals = list()
    new_bg = list()
    if file_list:
        originals = [cv2.imread(dataset+file) for file in file_list]
    else:

        files = os.listdir(dataset)
        originals = [cv2.imread(dataset+file) for file in files]
    
    for image in originals:
        cropped_image = crop_image(image)
        text_regions = get_text_regions(cropped_image)
        result_image = replace_text(cropped_image, text_regions)
        paste_image(image, result_image, position=(100, 500))
        new_bg.append(image)
    return new_bg 


# Example usage
if __name__ == "__main__": 
    image = cv2.imread('e-codices_csg-0231_049_max.jpg')
    cropped_image = crop_image(image)

    text_regions = get_text_regions(cropped_image)
    result_image = replace_text(cropped_image, text_regions)

    # Paste the result_image onto the original image
    paste_image(image, result_image, position=(100, 500))

    # Save the result
    cv2.imwrite('final_result.jpg', image)
