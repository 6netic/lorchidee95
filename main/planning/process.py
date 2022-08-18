from os import listdir, path
import cv2
import numpy as np
import pytesseract
from re import search


class Process:

    def extractLines(self, img_dir):
        """ Extracts lines and date from all image files """

        # Following line to hide on linux server
        # pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"
        files_list, lines = [], []
        global date
        for file in listdir(img_dir):
            files_list.append(file)
        # Ordering files number in jpg folder
        files_list = sorted(files_list, key=lambda x: int(x[-5:-4]))
        for file in files_list:
            img_path = path.join(img_dir, file)
            img_bgr = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            gray_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            blur_img = cv2.blur(gray_img, (1, 1), 0)
            _, thresh = cv2.threshold(blur_img, 246, 252, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours_list = []
            # Browsing each contour found
            for cnt in contours:
                # Selects only big rectangles
                area = cv2.contourArea(cnt)
                if area > 5000:
                    # calculates the perimeter of closed contour (True)
                    perimeter = cv2.arcLength(cnt, True)
                    # approximates the shape of the contour
                    approx = cv2.approxPolyDP(cnt, 0.01 * perimeter, True)
                    if len(approx) == 4:
                        cv2.drawContours(img_bgr, cnt, -1, (255, 0, 255), 1)
                        # Re-ordering coordinates
                        new_coords = np.zeros_like(approx)
                        coords = approx.reshape((4, 2))
                        addition = coords.sum(axis=1)
                        new_coords[0] = coords[np.argmin(addition)]
                        new_coords[3] = coords[np.argmax(addition)]
                        difference = np.diff(coords, axis=1)
                        new_coords[1] = coords[np.argmin(difference)]
                        new_coords[2] = coords[np.argmax(difference)]
                        # Flattening to 1D array as contiguous values of len(8)
                        points = new_coords.ravel()
                        numbers = [points[4], points[5], points[6], points[7], points[0], points[1], points[2], points[3]]
                        for number in numbers:
                            contours_list.append(number)
            # Adds rectangle zone that will be put at the end later
            contours_list = [contours_list[0], contours_list[1] + 100, contours_list[2], contours_list[3] + 100] + \
                            contours_list
            new_list, final_coords = [], []
            # Re-orders contours_list and saves it in new_list
            for i in range(0, len(contours_list), 4):
                new_list += contours_list[-4:]
                del contours_list[-4:]
            for i in range(0, len(new_list), 4):
                coord = new_list[i:i + 8]
                if len(coord) == 8:
                    final_coords.append(coord)
            # Extracting date
            if file == files_list[0]:
                date_coords = final_coords[1]
                coord_x, coord_y = [date_coords[0], date_coords[2], date_coords[4], date_coords[6]], \
                                   [date_coords[1], date_coords[3], date_coords[5], date_coords[7]]
                min_coord_x, max_coord_x = min(coord_x), max(coord_x)
                min_coord_y, max_coord_y = min(coord_y), max(coord_y)
                area_img = img_rgb[min_coord_y:max_coord_y, min_coord_x:max_coord_x]
                date = area_img[0:max_coord_y, 420:568]
                date = pytesseract.image_to_string(date).replace("\n", "").strip()
            # Browsing each row by starting from the 4th rectangle zone
            for row in final_coords[3:]:
                coord_x, coord_y = [row[0], row[2], row[4], row[6]], [row[1], row[3], row[5], row[7]]
                min_coord_x, max_coord_x = min(coord_x), max(coord_x)
                min_coord_y, max_coord_y = min(coord_y), max(coord_y)
                area_img = img_rgb[min_coord_y:max_coord_y, min_coord_x:max_coord_x]
                # Browsing each column
                column_1 = area_img[0:max_coord_y, 0:75]
                column_2 = area_img[0:max_coord_y, 76:295]
                column_3 = area_img[0:max_coord_y, 296:559]
                column_4 = area_img[0:max_coord_y, 560:883]
                column_5 = area_img[0:max_coord_y, 884:1247]
                column_6 = area_img[0:max_coord_y, 1248:1359]
                column_7 = area_img[0:max_coord_y, 1360:1477]
                text_zones = [column_1, column_2, column_3, column_4, column_5, column_6, column_7]
                one_row = []
                for zone in text_zones:
                    text = pytesseract.image_to_string(zone)
                    text = text.strip().replace("\n", " ")
                    one_row.append(text)
                # Tests if we have a date, so it will be a valid line
                if search('^[0-1][0-9]:[0-5][0-9]$', one_row[0]):
                    lines.append(one_row)
        return date, lines


    def convertDate(self, date):
        """ Converts the date to slash or to dash """

        date_list = []
        for one in date:
            if one.find("/", 1, 4) != -1:
                new_one = one.split("/")
                new_one = new_one[2], new_one[1], new_one[0]
                new_one = "-".join(new_one)
                date_list.append(new_one)
        return date_list
