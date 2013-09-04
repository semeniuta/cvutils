# -*- coding: utf-8 -*-

''' 
The pyramid_measurement module contains the functions used for measuring 
the distances between dots on the pyramid images

@author: Oleksandr Semeniuta
'''

from cvfunctions import pyramid
from cvfunctions import geometry
from cvfunctions import stereovision
import matplotlib.pyplot as plt

def measure_distances(points1, points2, indices, segments, p1, p2):
    '''
    Measures distances of the specified segments between the identified 
    points on the pyramid image

    Arguments:
    points1, points 2 -- lists of point coordinates [(x0, y0), (x1, y1) ...] 
                         for the first and the second set of images

    indices -- a dictionary that defines the correspondence between the same
               points on the first and the second image, where keys are 
               accordingly the indices of the points on the first image,
               and the values - on the second
    segments -- a list of segments to measure, containing the tuples of the
                (a, b) format, where a, b - the indices of points expressed 
                in terms of the first image indices
    p1, p2 -- projection matrices for the first and the second camera
              (obtained after computing rectification transforms)
    '''    
    
    interest_points_1, interest_points_2 = get_interest_points(points1, points2, indices)

    res_real = stereovision.triangulate_points(p1, p2, interest_points_1, interest_points_2)
    
    i1_list = list(indices.iterkeys())
    res_dict = {i1_list[i]: res_real[i] for i in range(len(i1_list))}
    
    dist = lambda a, b: geometry.compute_distance(*[res_dict[i] for i in (a, b)])
    
    d = [dist(a, b) for a, b in segments]
    
    return d
    
def display_measurements(points1, points2, indices, segments, images, blobs, distances):
    '''
    Graphically displays the result of distance measurement on the Matplotlib
    plots

    Arguments:
    points1, points 2 -- lists of point coordinates [(x0, y0), (x1, y1) ...] 
                         for the first and the second set of images

    indices -- a dictionary that defines the correspondence between the same
               points on the first and the second image, where keys are 
               accordingly the indices of the points on the first image,
               and the values - on the second
    segments -- a list of segments to measure, containing the tuples of the
                (a, b) format, where a, b - the indices of points expressed 
                in terms of the first image indices
    images -- two images supplied as a sequence
    blobs -- two lists of found blobs on the correspodning first and 
             second images: [blobs1, blobs2]
    distances -- measured distances between the specified segments
    '''
    
    interest_points_1, interest_points_2 = get_interest_points(points1, points2, indices)
    i1_list = list(indices.iterkeys())
    pixel_dict_1 = {i1_list[i]: interest_points_1[i] for i in range(len(i1_list))}
    pixel_dict_2 = {i1_list[i]: interest_points_2[i] for i in range(len(i1_list))}
    pd = [pixel_dict_1, pixel_dict_2]
    for i in range(2):
        pyramid.display_dots(images[i], blobs[i])
        pyramid.display_dots_numbers(blobs[i])
        for segm_ind in range(len(segments)):
            a, b = segments[segm_ind]
            p1 = pd[i][a]
            p2 = pd[i][b]
            x = [p1[0], p2[0]]
            y = [p1[1], p2[1]]
            plt.plot(x, y, 'c')
            center = geometry.compute_segment_center(p1, p2)
            plt.text(center[0], center[1], '%.3f' % distances[segm_ind], color='#ffff99')
            
def get_interest_points(points1, points2, indices):
    ''' 
    Forms two lists of interest points further uses for stereo matching    
    '''
    interest_points_1 = [points1[i1] for i1, i2 in indices.iteritems()]
    interest_points_2 = [points2[i2] for i1, i2 in indices.iteritems()]
    return interest_points_1, interest_points_2