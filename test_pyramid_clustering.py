# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid, transform, output
from cvclasses.stereovisionsystem import StereoVisionSystem
from cvclasses.camera import Camera
import os
import random
from matplotlib import pyplot as plt
import numpy as np

from scipy.cluster.vq import kmeans, vq

cm = ConfigManager()

set_phone = cm.get_imageset_full_mask('pyramid_withphone_2')
set1 = cm.get_imageset_full_mask('pyramid_left')
set2 = cm.get_imageset_full_mask('pyramid_right')

images1 = images.open_images_from_mask(set1)
images2 = images.open_images_from_mask(set2)

def get_rand_color():
    colors = ['r', 'g', 'b', 'c', 'm']
    randcolor = colors[random.randint(0, len(colors)-1)]
    return randcolor

def kmeans_clustering(data, nclusters):
    centroids, _ = kmeans(data, nclusters)
    idx, _ = vq(data,centroids)
    return centroids, idx    
    
def display_clustering_results(data, centroids, idx, nclusters, new_figure=True):
    if new_figure:    
        plt.figure()
    for i in range(nclusters): 
        randcolor = get_rand_color()
        output.plot_points(data[idx==i,0], data[idx==i,1], randcolor)
    plt.plot(centroids[:,0], centroids[:,1], 'sy')    

def display_segments(xy_current_cluster, color):
    for row in xy_current_cluster:
        x = row[:2]
        y = row[2:]
        plt.plot(x, y, color)

def get_xy(df):
    return np.array(df.loc[:, 'x0':'y1'])
    
def get_lineeq(df):
    return np.array(df.loc[:, ['slope', 'intercept']])
    
def get_xy_avg(df):
    return np.array(df.loc[:, 'x':'y'])
    

def cluster_segments_by_lines_equations(res_f, display_images=True):
    lineeq = get_lineeq(res_f)
    xy = get_xy(res_f)
    xy_avg = get_xy_avg(res_f)
    
    #data = np.array(res_f.loc[:, 'x0':'dist'])    
    data = lineeq    
    
    nclusters = 12
    centroids, idx = kmeans_clustering(data, nclusters)
    
    if display_images:
        for i in range(nclusters):    
            randcolor = get_rand_color()
            xy_current_cluster = xy[idx==i]
            output.plot_image(im)    
            display_segments(xy_current_cluster, randcolor)
    
    display_clustering_results(data, centroids, idx, nclusters)
    
def cluster_segments_by_xy_avg(res_f):
    xy_avg = get_xy_avg(res_f)
    nclusters = 12
    data = xy_avg
    centroids, idx = kmeans_clustering(data, nclusters)
    output.plot_image(im)
    
    xy = get_xy(res_f)
    for i in range(nclusters):
        randcolor = get_rand_color()
        xy_current_cluster = xy[idx==i]            
        display_segments(xy_current_cluster, randcolor)
         
    #display_clustering_results(data, centroids, idx, nclusters, False)

if __name__ == '__main__':
    im = images1[4]
        
    dots, im_t = pyramid.detect_dots(im)
        
    res = pyramid.get_lines(dots)
    res_sorted = res.sort(columns=['dist'])
    num_small_segments = 150
    res_f = res_sorted.head(num_small_segments)
    
    cluster_segments_by_lines_equations(res_f, True)    
    
    #cluster_segments_by_xy_avg(res_f)
