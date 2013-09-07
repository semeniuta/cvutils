# -*- coding: utf-8 -*-
import cv2
from cvfunctions import output, geometry
from matplotlib import pyplot as plt
import numpy as np
import math
import pandas as pd

def detect_dots(image, ndots=36, blur_window=0, iterate=True, threshold=25, thresh_decrement=0.1, max_iterations=100, min_circularity=0.8, max_circularity=1.2):
    
    if not blur_window == 0:
        image = cv2.medianBlur(image, blur_window)
    
    ndots_found = 0
    if not iterate:
        max_iterations = 1
    
    threshold += thresh_decrement   
    i = 0
    while ndots_found != ndots and i < max_iterations:      
        threshold -= thresh_decrement
        retval, im_t = cv2.threshold(image, threshold, 256, cv2.THRESH_BINARY)
        
        p = cv2.SimpleBlobDetector_Params()
        p.minCircularity = min_circularity
        p.maxCircularity = max_circularity
        p.filterByCircularity = True
        
        det = cv2.SimpleBlobDetector(p)
        
        blobs = det.detect(im_t)
        ndots_found = len(blobs)
        i += 1
        
    return blobs, im_t
    
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

def extract_points(blobs):    
    points = [([b.pt[0], b.pt[1]]) for b in blobs]
    return points
    
def display_dots_numbers(blobs, display_sizes=False):
    num = 0
    for b in blobs:
        x, y = b.pt

        if display_sizes:
            text = '%d (%.2f)' % (num, b.size)
        else:
            text = num
            
        plt.text(x, y, text, color='w')
        num += 1
     
def pyramid_is_turned_left(blobs):
    
    x_list = []
    y_list = []
    for b in blobs:
        x, y = b.pt
        x_list.append(x)
        y_list.append(y)
        
    y_min = min(y_list)
    y_max = max(y_list)
    
    x_y_min = x_list[y_list.index(y_min)]
    x_y_max = x_list[y_list.index(y_max)]
    
    return x_y_min < x_y_max
    
def draw_extreme_points(blobs):
    x, y = get_xy(blobs)
        
    y_min = min(y)
    y_max = max(y)
    
    x_min = min(x)
    x_max = max(x)
    
    point_x_min = (x_min, y[x.index(x_min)])
    point_x_max = (x_max, y[x.index(x_max)])
    
    point_y_min = (x[y.index(y_min)], y_min)
    point_y_max = (x[y.index(y_max)], y_max)
    
    x_points = [point_x_min[0], point_x_max[0], point_y_min[0], point_y_max[0]]
    y_points = [point_x_min[1], point_x_max[1], point_y_min[1], point_y_max[1]]
    
    print x_points
    print y_points    
    
    output.plot_points(x_points, y_points, 'c')    

def get_xy(blobs):
    x = []
    y = []
    for b in blobs:
        x.append(b.pt[0])
        y.append(b.pt[1])
    return x, y
    
def xy_lists_to_matrix(x, y):
    return np.transpose(np.vstack((x, y))) 
    
def get_lines(blobs):
    n = len(blobs)
    
    x, y = get_xy(blobs)    
    
    res = []
    for i in range(n):
        for j in range(i+1, n):
            a = (x[i] - x[j])**2
            b = (y[i] - y[j])**2
            dist = math.sqrt(a+b)
            x_list = [x[i], x[j]]
            y_list = [y[i], y[j]]
            slope, intercept = geometry.get_line_equation(x_list, y_list)
            res.append([i, j, dist, slope, intercept])
    
    df = pd.DataFrame(res, columns=['a', 'b', 'dist', 'slope', 'intercept'])
    
    return df
    
def build_chains(df):
    get_ab_tuple = lambda segment: (int(segment['a']), int(segment['b']))    
    
    chains = []
    index = 0    
    for i in df.index:
        starting_segment = df.ix[i]
        chains.append([starting_segment])
        for j in df.index:
            segment = df.ix[j]
            last_segment = chains[index][-1]
            if last_segment['b'] == segment['a']:
                slope_ratio = last_segment['slope'] / segment['slope']
                intercept_ratio = last_segment['intercept'] / segment['intercept']
                if (0.5 < slope_ratio < 1.5) and (0.5 < intercept_ratio < 1.5):
                    chains[index].append(segment)
        index += 1
                
    return chains
        
        
