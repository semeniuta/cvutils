import cv2
import numpy as np

def calibrate_camera(images, pattern_size, square_size, chessboard_corners_results=None):
    '''
    returns: rms, camera_matrix, dist_coefs, rvecs, tvecs
    '''    
    pattern_points = get_pattern_points(pattern_size, square_size)
    object_points = []
    image_points = []
    
    for current_index in range(len(images)):
        img = images[current_index]        
        h, w = img.shape
        
        if chessboard_corners_results == None:
            found, corners = cv2.findChessboardCorners(img, pattern_size)       
        else:
            found, corners = chessboard_corners_results[current_index]
        
        if not found:
            continue
        else:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)           
        
        image_points.append(corners.reshape(-1, 2))
        object_points.append(pattern_points)
        
    res = cv2.calibrateCamera(object_points, image_points, (w, h))
    return res
    
def chessboard_corners_maxtrix_to_lists(matrix):
    x_list = []
    y_list = []
    for el in matrix:
        x, y = el[0]
        x_list.append(x)
        y_list.append(y)
    return (x_list, y_list)
    
def get_pattern_points(pattern_size, square_size):
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    return pattern_points