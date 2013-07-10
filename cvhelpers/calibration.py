import cv2
import numpy as np
from cvhelpers import images as cvhimages

def calibrate_camera(image_names, pattern_shape, square_size):
    '''
    returns: rms, camera_matrix, dist_coefs, rvecs, tvecs
    '''    
    pattern_points = get_pattern_points(pattern_shape, square_size)
    object_points = []
    image_points = []
    
    failures_indices = []
    for current_index in range(len(image_names)):
        image_file = image_names[current_index]        
        img = cvhimages.open_image(image_file)
        h, w = img.shape
        found, corners = cv2.findChessboardCorners(img, pattern_shape)       
        
        if not found:
            failures_indices.append(current_index)
            continue
        
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)           
        
        image_points.append(corners.reshape(-1, 2))
        object_points.append(pattern_points)
        
    res = cv2.calibrateCamera(object_points, image_points, (w, h))
    return (res, failures_indices)

def find_chessboard_corners(image, pattern_size):
    return cv2.findChessboardCorners(image, pattern_size)
    
def chessboard_corners_maxtrix_to_lists(matrix):
    x_list = []
    y_list = []
    for el in matrix:
        x, y = el[0]
        x_list.append(x)
        y_list.append(y)
    return (x_list, y_list)
    
def get_pattern_points(pattern_shape, square_size):
    pattern_points = np.zeros((np.prod(pattern_shape), 3), np.float32)
    pattern_points[:,:2] = np.indices(pattern_shape).T.reshape(-1, 2)
    pattern_points *= square_size
    return pattern_points