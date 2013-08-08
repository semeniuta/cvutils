# -*- coding: utf-8 -*-
import cv2
from cvfunctions import output

def detect_dots(image):
    retval, im_t = cv2.threshold(image, 20, 256, cv2.THRESH_BINARY)
    
    p = cv2.SimpleBlobDetector_Params()
    p.minCircularity = 0.83
    p.maxCircularity = 1.2
    p.filterByCircularity = True
    
    det = cv2.SimpleBlobDetector(p)
    
    blobs = det.detect(im_t)
    return blobs
    
def display_dots(image, blobs):
    x_list = []
    y_list = []
    size_list = []
    for b in blobs:
        x, y = b.pt
        x_list.append(x)
        y_list.append(y)
        size_list.append(b.size)
    
    circles = [((x_list[i], y_list[i]), size_list[i]) for i in range(len(blobs))]
    
    output.plot_image(image)    
    output.plot_circles(circles)
    output.plot_points(x_list, y_list)