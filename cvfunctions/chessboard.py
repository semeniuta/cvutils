# -*- coding: utf-8 -*-

import cv2
from cvfunctions import output
from cvfunctions.images import open_images_from_mask

def find_chessboard_corners(images, pattern_size, searchwin_size=5, findcbc_flags=None):
    ''' 
    Finds chessboard corners on each image from the specified list. 
    Returns a list of tuples, returned from  
    cv2.findChessboardCorners function
    '''    
    chessboard_corners_results = []
    for img in images:
        if findcbc_flags == None:
            res = cv2.findChessboardCorners(img, pattern_size) 
        else:
            res = cv2.findChessboardCorners(img, pattern_size, flags=findcbc_flags) 
        chessboard_corners_results.append(res)
        
        found, corners = res
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (searchwin_size, searchwin_size), (-1, -1), term)      
            
    return chessboard_corners_results


def filter_chessboard_corners_results(chessboard_corners_results, images):
    ''' 
    Filter out the images that failed during the cv2.findChessboardCorners call
    
    Returns a tuple containing two lists:
     - filtered chessboard corners results
     - filtered images
    '''
    
    found = [res[0] for res in chessboard_corners_results]
    filtered_images = []
    filtered_chessboard_corners_results = []
    for i in range(len(found)):
        if found[i]:
            filtered_images.append(images[i])
            filtered_chessboard_corners_results.append(chessboard_corners_results[i])
    return (filtered_chessboard_corners_results, filtered_images)

def filter_chessboard_corners_results_stereo(chessboard_corners_results_left, chessboard_corners_results_right, images_left, images_right):
    ''' 
    Filter out the images taken by two cameras (stereo system)
    that failed during the cv2.findChessboardCorners call. Only the image pairs
    that both (left and right) have passed the cv2.findChessboardCorners call 
    will remain in the returned lists - others will be filtered out
    
    Returns a tuple containing four lists:
     - filtered chessboard corners results for left camera image set
     - filtered chessboard corners results for right camera image set
     - filtered images from left camera
     - filtered images from right camera
    '''    
    
    images_left_filtered = []
    images_right_filtered = []
    corners_left_filtered = []
    corners_right_filtered = []
    for i in range(len(images_left)):
        found_left = chessboard_corners_results_left[i][0]
        found_right = chessboard_corners_results_right[i][0]
        if found_left and found_right:
            images_left_filtered.append(images_left[i])
            images_right_filtered.append(images_right[i])
            corners_left_filtered.append(chessboard_corners_results_left[i])
            corners_right_filtered.append(chessboard_corners_results_right[i])
    return (corners_left_filtered, corners_right_filtered, images_left_filtered, images_right_filtered)

def open_images_and_find_corners(images_mask, pattern_size, findcbc_flags=None):
    ''' 
    Open the images and find chessboard corners on them. 
    Then filter out the images (and corresponding corners)
    that failed during the cv2.findChessboardCorners call 
    '''
    opened_images = open_images_from_mask(images_mask)
    chessboard_corners_results = find_chessboard_corners(opened_images, pattern_size, findcbc_flags=findcbc_flags)
          
    corners_filtered, images_filtered = filter_chessboard_corners_results(chessboard_corners_results, opened_images)
    return corners_filtered, images_filtered


def chessboard_corners_maxtrix_to_lists(matrix):
    '''
    Convert the result of the cv2.findChessboardCorners function call to 
    two lists of the corresponding X and Y points. 
    Returns a tuple (x_list, y_list)
    '''    
    x_list = []
    y_list = []
    for el in matrix:
        x, y = el[0]
        x_list.append(x)
        y_list.append(y)
    return (x_list, y_list)
    
def plot_corners(image, corners):
    output.plot_image(image)
    x, y = chessboard_corners_maxtrix_to_lists(corners[1])
    output.plot_points(x, y)
    