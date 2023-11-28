from PIL import Image, ImageFilter
import cv2
import os
import yaml
import numpy as np

DATASET = "../dataset/real documents/"


def detect_page(name, img, show=False):
    inner_top = (0,0)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    threshold = 55
    size = 89
    thresholded = cv2.adaptiveThreshold(
        gray,255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
        size, threshold
    )
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 75))
    closing = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, rect_kernel, iterations=4)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, 
                                                     cv2.CHAIN_APPROX_SIMPLE)

    img2 = img.copy()
    p = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # convex_contour = cv2.convexHull(cnt)
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 1000000:
            d1 = x
            d2 = img2.shape[1]-(x+w)
            if d1 > d2:
                p = 1
                inner_top = (x+w, y)
            else:
                inner_top = (x,y)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if show:
        page = Image.fromarray(img2)
        page.show(title=name)
    return p, inner_top

def detect_cols(name, img, show=False):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    threshold = 105
    size = 101
    if "051" in name:
        threshold = 85
    if "184" in name:
        threshold = 115

    thresholded = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
        size, threshold
    )
 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (60, 100))
    closing = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, rect_kernel)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, 
                                                     cv2.CHAIN_APPROX_SIMPLE)

    img2 = img.copy()
    col = 0
    cols = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        if area > 1000000 and col < 2:
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cols.append((x,y,w,h))
            col += 1

    if show:
        bounds = Image.fromarray(img2)
        bounds.show()
    return cols
    

def detect_lines(col_img, show=False):
    gray = cv2.cvtColor(col_img, cv2.COLOR_RGB2GRAY)
    threshold = 95
    size = 35

    thresholded = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
        size, threshold
    )
 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 2))
    closing = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, rect_kernel, iterations=4)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, 
                                                     cv2.CHAIN_APPROX_SIMPLE)

    img2 = col_img.copy()
    baselines = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        if area > 10000:
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            baselines.append(y+h)

    if show:
        bounds = Image.fromarray(img2)
        bounds.show()

    return baselines


page_info = []
# for file in os.listdir(DATASET):
for file in ["e-codices_csg-0231_084_max.jpg"]:
    lines = []
    cols = []
    img = cv2.imread(DATASET+file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    p, inner_top = detect_page(file, img)
    page_cols = detect_cols(file, img)
    for col in page_cols:
        col_lines = detect_lines(img[col[1]:(col[1]+col[3]), col[0]:(col[0]+col[2])])
        col_lines.sort()
        lines.append(col_lines)
    dist = []
    for col_lines in lines:
        for i in range(len(col_lines)-1):
            d = col_lines[i+1]-col_lines[i]
            dist.append(d)
    page_info.append((p, inner_top, *page_cols, *lines))
    print(page_info)
    print(len(page_info[0][4]), len(page_info[0][5]))
    with open('config.yaml', 'w') as writer:
        data_doc = {
            'orient': p,
            'anchor': inner_top,
            'col1': page_cols[0],
            'col2': page_cols[1],
            'lines1': lines[0][0],
            'lines2': lines[1][0],
            "avg_line_d": float(np.array(dist).mean()),
            "line_d_std": float(np.array(dist).std())
        }
        yaml.dump(data_doc, writer)
    print(np.array(dist).mean(), np.array(dist).std())
    # print(dist)
