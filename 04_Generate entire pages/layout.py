from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps
from statistics import mean
import numpy as np
import yaml

COLS_W = 2635
COLS_H = 2860

L_MARGIN = 100
C_MARGIN = 90
R_MARGIN = 110
COL_WIDTH = 1120
COL_HEIGHT = 2870
LINE_HEIGHT = 110


class Manuscript:
    def __init__(self):
        self.background = Image.new(mode='RGB', size=(1, 1))

    def get_background(self, path):
        self.background = Image.open(path)

    def close_background(self):
        self.background.close()

    def show_background(self):
        self.background.show()

    def get_background_dim(self):
        width = self.background.width
        height = self.background.height
        return width, height

    def get_page_box(self):
        """
        Find approximate coordinate of the page document in the image
        """
        # First, filter the image to enhance the edge detection process
        gray_scale = self.background.convert("L")
        # Applying multiple filters, found by trial and error so not perfect
        filtered = gray_scale.filter(ImageFilter.EDGE_ENHANCE).filter(ImageFilter.SMOOTH).filter(ImageFilter.CONTOUR)\
                                        .filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
        bin = filtered.convert("1")
        # bin.show()
        array = np.asarray(bin)

        # travers the image on both axis, sum the pixels per slice to detect edges and get the coordinates
        # as the page is no perfectly straight use a small moving window and average the values
        # gather the approximate coordinates and average them to get the approximate coordinate of the page
        # ignore coordinates close to the edges of the image (false positive)
        w, h = self.get_background_dim()
        l = list()
        r = list()
        u = list()
        d = list()
        for x in range(10, w-10, 1):
            slice = array[:, x-1:x+1]
            avg = slice.sum()//3
            # print(x, avg)
            if avg >= 1000:
                if x <= w//2:
                    l.append(x)
                else:
                    r.append(x)
        for y in range(10, h-10, 1):
            slice = array[y-1:y+1, :]
            avg = slice.sum()//3
            # print(y, avg)
            if avg >= 600:
                if y <= h//2:
                    u.append(y)
                else:
                    d.append(y)
        # print(f"{len(l)} {len(u)} {len(r)} {len(d)}")
        return round(mean(l)), round(mean(u)), round(mean(r)), round(mean(d))


    def get_columns_coord(self):
        """
        Get the general location for the columns (not individually) centered on the center of the page
        Represented as a rectangle
        """
        _, _, page_r, page_d = self.get_page_box()
        center_x, center_y = page_r//2, page_d//2
        x0, y0 = center_x - COLS_W//2, center_y - COLS_H//2
        x1, y1 = center_x + COLS_W//2, center_y + COLS_H//2

        return x0, y0, x1, y1
    
    def get_col(self):
        """
        Return the bounding box for each column
        """
        xcol0, ycol0, xcol1, ycol1 = self.get_columns_coord()
        col1 = (xcol0+L_MARGIN, ycol0, xcol0+L_MARGIN+COL_WIDTH, ycol1)
        col2 = (col1[2] + C_MARGIN*2, ycol0, col1[2]+C_MARGIN*2+COL_WIDTH, ycol1)
        return col1, col2

    def get_lines(self):
        """
        Get each lines coordinates based on the columns coordinates
        """
        col1, col2 = self.get_col()
        lines = list()
        for col in [col1, col2]:
            for line in range(col[1], col[3]+LINE_HEIGHT, LINE_HEIGHT):
                lines.append((col[0], line, col[2], line))
        return lines



if __name__ == "__main__":
    data = {}
    with open("./config.yaml", "r") as config:
        data = yaml.full_load(config)
    # print(data)

    man = Manuscript()
    man.get_background("./Texterase/e1.jpg")
    # x0, y0, x1, y1 = man.get_columns_coord()
    # col1, col2 = man.get_col()
    lines = man.get_lines()

    font = ImageFont.truetype("./carolus-fg/carolus.ttf", size=85, encoding="unic")
    # print(font.getbbox("Hello, world!", direction="ltr", language="la", anchor="ls"))
    bg = man.background
    img = ImageDraw.Draw(bg)
    # img.rectangle([x0, y0, x1, y1], fill="black")
    # img.rectangle([*col1], fill="grey")
    # img .rectangle([*col2], fill="grey")
    # for line in lines:
        # img.line([*line], fill="yellow", width=5)
    lines = data["line_d_std"]/2 * np.random.randn(1, 25) + data["avg_line_d"]
    # print(lines)
    for col in range(1, 3):
        curr_x = data[f"col{col}"][0]
        curr_y = data[f"col{col}"][1] + data[f"lines{col}"]
        img.line([(curr_x, curr_y), (curr_x+data[f"col{col}"][2], curr_y)], fill="yellow", width=5)
        for line in lines[0]:
            curr_y += line
            # print(f"{curr_x=} {curr_y=}")
            img.line([(curr_x, curr_y), (curr_x+data[f"col{col}"][2], curr_y)], fill="yellow", width=5)

    mask = Image.new(mode="L", size=bg.size)
    m = ImageDraw.Draw(mask)
    # ink = Image.open("./Abstract-Black-Ink-Textures.jpg").resize(bg.size)
    ink2 = Image.open("./ink.png").resize(bg.size)

    # with open("./sample.txt", "r") as sample:
    #     words = sample.readline().split()
    #     margin = [C_MARGIN, R_MARGIN]
    #     idx = 0
    #     col = 0
    #     nb_line = 0
    #     for line in lines:
    #         ori_x, ori_y, end_x, end_y = line
    #         txt = words[idx]
    #         new_txt = txt
    #         bb = font.getbbox(txt, direction="ltr", language="la", anchor="ls")
    #         loc = bb[2] + ori_x
    #         # print(f"{loc=} vs {col[current_col][3]+margin[current_col]//3}")
    #         while loc < end_x-160:
    #             # adding a new word to the line would go over the column width + margin
    #             # print line without new word and start on a new line with new word
    #             txt = new_txt
    #             idx += 1
    #             new_txt += words[idx] + " "
    #             bb = font.getbbox(txt, direction="ltr", language="la", anchor="ls")
    #             loc = bb[2] + ori_x
    #
    #         ori_x, ori_y, _, _ = line
    #         m.text((ori_x, ori_y), txt, font=font, fill="white", language="la", direction="ltr", anchor="ls")
            # txt_mask = font.getmask2(txt, mode="L", direction="ltr", language="la", anchor="ls")
            # txt_mask2 = Image.frombytes(txt_mask[0].mode, txt_mask[0].size, bytes(txt_mask[0]))
            # mask.paste(txt_mask2, box=(ori_x, ori_y))
            
                
    # mask.show()
    bg.show()
    # final = Image.composite(bg, ink2, mask=ImageOps.invert(mask))
    # final.show()
    man.close_background()
