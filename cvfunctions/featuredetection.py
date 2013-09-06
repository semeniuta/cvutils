# -*- coding: utf-8 -*-

import cv2

at_algorithms = {
    'mean': cv2.ADAPTIVE_THRESH_MEAN_C,
    'gaussian': cv2.ADAPTIVE_THRESH_GAUSSIAN_C 
}

def threshold_binary(image, threshold, maxval=256):
    retval, image_t = cv2.threshold(image, threshold, maxval, cv2.THRESH_BINARY)
    return image_t
    
def threshold_adaptive(image, method_key='gaussian', maxval=256, block_size=3, c_const=0.25):
    method = at_algorithms[method_key]
    threshold_type = cv2.THRESH_BINARY
    image_t = cv2.adaptiveThreshold(image, maxval, method, threshold_type, block_size, c_const)
    return image_t
    
def detect_circles_as_blobs(image, min_circularity, max_circularity):
    p = cv2.SimpleBlobDetector_Params()
    p.minCircularity = min_circularity
    p.maxCircularity = max_circularity
    p.filterByCircularity = True
    
    det = cv2.SimpleBlobDetector(p)
    
    blobs = det.detect(image)
    return blobs