import cv2
import numpy as np

def calibrate_camera(images, pattern_size, square_size, chessboard_corners_results=None):
    '''
    Conducts camera calibration using the photos of chessboard pattern

    Arguments:
    images -- a list of images to process
    pattern_size -- dimmension of the chessboard pattern, e.g. (7, 8)
    square_size -- size of a square edge on the chessboard
    chessboard_corners_results -- a list of tuples got from the
                                  cv2.findChessboardCorners function call
                                  for each image (default None)
    
    Returns a tuple as a result of the cv2.calibrateCamera function call,
    containing the following calibration results:
    rms, camera_matrix, dist_coefs, rvecs, tvecs
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
    
def get_pattern_points(pattern_size, square_size):
    '''
    Returns a matrix of the pattern points for using in the
    calibration algorithm
    
    Arguments:
    pattern_size -- dimmension of the chessboard pattern, e.g. (7, 8)
    square_size -- size of a square edge on the chessboard
    '''
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    return pattern_points

def get_camera_intrinsic_parameters(camera_matrix):
    '''
    Returns a tuple of camera intrinsic parameters 
    (based on the camera matrix privided) in the following order:
    fx, fy, cx, cy
    '''
    fx = camera_matrix[0, 0]
    fy = camera_matrix[1, 1]
    cx = camera_matrix[0, 2]
    cy = camera_matrix[1, 2]
    
    return (fx, fy, cx, cy)
    
def get_camera_matrix(params):
    '''
    Returns camera matrix based on given intrinsic parameters
    of the camera: fx, fy, cx, cy (supplied as a sequence)
    '''
    
    fx, fy, cx, cy = params
    cm = np.zeros((3, 3))
    cm[0, 0] = fx
    cm[1, 1] = fy
    cm[0, 2] = cx
    cm[1, 2] = cy
    cm[2, 2] = 1
    
    return cm
    
def get_calibration_results_as_a_tuple(res):
    ''' 
    Returns a tuple of the following calibration results:
    rms, fx, fy, cx, cy, k1, k2, p1, p2, k3    
    '''
    rms, camera_matrix, dist_coefs, rvecs, tvecs = res       
    
    fx, fy, cx, cy = get_camera_intrinsic_parameters(camera_matrix)
    k1, k2, p1, p2, k3 = dist_coefs[0]
    
    return (rms, fx, fy, cx, cy, k1, k2, p1, p2, k3)      

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