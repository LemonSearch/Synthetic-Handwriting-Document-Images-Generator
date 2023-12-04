import cv2
import numpy as np
#import noise

#def generate_perlin_noise(shape, scale=10):
#    noise_array = np.zeros(shape)
 #   for i in range(shape[0]):
   #     for j in range(shape[1]):
     #       noise_array[i, j] = noise.pnoise2(i / scale, j / scale)

  #  return noise_array

def get_text_regions(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def blur_text_regions(image, text_regions, blur_size=5):
    result_image = image.copy()

    for contour in text_regions:
        # Get the bounding box of the text region
        x, y, w, h = cv2.boundingRect(contour)

        # Apply bilateral filter to the text region
        text_region = result_image[y:y + h, x:x + w]
        blurred_text_region = cv2.bilateralFilter(text_region, blur_size, 75, 75)

        # Replace the text region with the blurred version
        result_image[y:y + h, x:x + w] = blurred_text_region

    return result_image

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

    # Blur the replaced text regions for smoother blending
    result_image = blur_text_regions(result_image, text_regions, blur_size)

    return result_image

# Example usage
image = cv2.imread('e-codices_csg-0231_049_max.jpg')
text_regions = get_text_regions(image)
result_image = replace_text(image, text_regions)
cv2.imwrite('e5.jpg', result_image)
