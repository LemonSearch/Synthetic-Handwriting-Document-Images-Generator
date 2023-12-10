from PIL import Image, ImageFilter
import cv2
import os
import yaml
import numpy as np

DATASET = "../dataset/real documents/"


def detect_page(img, show=False):
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
        page.show()
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
        clo = Image.fromarray(closing)
        clo.show()
    cols.sort(key= lambda x: x[0])
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
        clo = Image.fromarray(closing)
        clo.show()

    return baselines

if __name__ == "__main__": 
    page_info = []
    dist = {0: [], 1: []}
    cols1 = {0: {"x": [], "y": [], "w": [], "h": []},
             1: {"x": [], "y": [], "w": [], "h": []}
             }
    cols2 = {0: {"x": [], "y": [], "w": [], "h": []},
             1: {"x": [], "y": [], "w": [], "h": []}
             }
    line1 = {0: [], 1: []}
    line2 = {0: [], 1: []}
    nb_lines = []
    for file in os.listdir(DATASET):
    # for file in ["e-codices_csg-0231_084_max.jpg"]:
        lines = list()
        cols = list()
        img = cv2.imread(DATASET+file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        p, inner_top = detect_page(img)
        
        page_cols = detect_cols(file, img)
        c = 0
        for col in page_cols:
            col_lines = detect_lines(img[col[1]:(col[1]+col[3]), col[0]:(col[0]+col[2])], True)
            col_lines.sort()
            lines.append(col_lines)
            if c == 0:
                cols1[p]["x"].append(col[0])
                cols1[p]["y"].append(col[1])
                cols1[p]["w"].append(col[2])
                cols1[p]["h"].append(col[3])
                line1[p].append(col_lines[0])
                c = 1
            else:
                cols2[p]["x"].append(col[0])
                cols2[p]["y"].append(col[1])
                cols2[p]["w"].append(col[2])
                cols2[p]["h"].append(col[3])
                line2[p].append(col_lines[0])
                c = 0
            nb_lines.append(len(col_lines))
        # line1[p].append(lines[0][0])
        # line2[p].append(lines[1][0])

        for col_lines in lines:
            for i in range(len(col_lines)-1):
                d = col_lines[i+1]-col_lines[i]
                dist[p].append(d)
    with open('config.yaml', 'w') as writer:
        data_doc = {
            'orient': {
            0:
                {
                    'col1': (float(np.array(cols1[0]["x"]).mean()),
                             float(np.array(cols1[0]["y"]).mean()),
                             float(np.array(cols1[0]["w"]).mean()),
                             float(np.array(cols1[0]["h"]).mean())
                             ),
                    'col1_std': (float(np.array(cols1[0]["x"]).std()),
                                 float(np.array(cols1[0]["y"]).std()),
                                 float(np.array(cols1[0]["w"]).std()),
                                 float(np.array(cols1[0]["h"]).std())
                                 ),
                    'col2': (float(np.array(cols2[0]["x"]).mean()), 
                             float(np.array(cols2[0]["y"]).mean()),
                             float(np.array(cols2[0]["w"]).mean()), 
                             float(np.array(cols2[0]["h"]).mean())
                             ),
                    'col2_std': (float(np.array(cols2[0]["x"]).std()), 
                                 float(np.array(cols2[0]["y"]).std()), 
                                 float(np.array(cols2[0]["w"]).std()), 
                                 float(np.array(cols2[0]["h"]).std())
                                 ),
                    'line1': float(np.array(line1[0]).mean()),
                    'line1_std': float(np.array(line1[0]).std()),
                    'line2': float(np.array(line2[0]).mean()),
                    'line2_std': float(np.array(line2[0]).std()),
                    "avg_line_d": float(np.array(dist[0]).mean()),
                    "line_d_std": float(np.array(dist[0]).std())
                },
            1:
                {
                    'col1': (float(np.array(cols1[1]["x"]).mean()), 
                             float(np.array(cols1[1]["y"]).mean()), 
                             float(np.array(cols1[1]["w"]).mean()), 
                             float(np.array(cols1[1]["h"]).mean())
                             ),
                    'col1_std': (float(np.array(cols1[1]["x"]).std()), 
                                 float(np.array(cols1[1]["y"]).std()), 
                                 float(np.array(cols1[1]["w"]).std()), 
                                 float(np.array(cols1[1]["h"]).std())
                                 ),
                    'col2': (float(np.array(cols2[1]["x"]).mean()), 
                             float(np.array(cols2[1]["y"]).mean()), 
                             float(np.array(cols2[1]["w"]).mean()), 
                             float(np.array(cols2[1]["h"]).mean())
                             ),
                    'col2_std': (float(np.array(cols2[1]["x"]).std()), 
                                 float(np.array(cols2[1]["y"]).std()), 
                                 float(np.array(cols2[1]["w"]).std()), 
                                 float(np.array(cols2[1]["h"]).std())
                                 ),
                    'line1': float(np.array(line1[1]).mean()),
                    'line1_std': float(np.array(line1[1]).std()),
                    'line2': float(np.array(line2[1]).mean()),
                    'line2_std': float(np.array(line2[1]).std()),
                    "avg_line_d": float(np.array(dist[1]).mean()),
                    "line_d_std": float(np.array(dist[1]).std()) 
                }
            }
        }
        yaml.dump(data_doc, writer)
        print(dist)
