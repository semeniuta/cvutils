import cv2
import numpy as np

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