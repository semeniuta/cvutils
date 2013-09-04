# -*- coding: utf-8 -*-

from cvfunctions import pyramid
from cvfunctions import geometry
from cvfunctions import stereovision
import matplotlib.pyplot as plt

def measure_distances(points1, points2, indices, segments, p1, p2):
    interest_points_1, interest_points_2 = get_interest_points(points1, points2, indices)

    res_real = stereovision.triangulate_points(p1, p2, interest_points_1, interest_points_2)
    
    i1_list = list(indices.iterkeys())
    res_dict = {i1_list[i]: res_real[i] for i in range(len(i1_list))}
    
    dist = lambda a, b: geometry.compute_distance(*[res_dict[i] for i in (a, b)])
    
    d = [dist(a, b) for a, b in segments]
    
    return d
    
def display_measurements(points1, points2, indices, segments, images, blobs, distances):
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
    interest_points_1 = [points1[i1] for i1, i2 in indices.iteritems()]
    interest_points_2 = [points2[i2] for i1, i2 in indices.iteritems()]
    return interest_points_1, interest_points_2