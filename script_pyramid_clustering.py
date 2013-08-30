# -*- coding: utf-8 -*-

'''
Script that tries to cluster the pyramid dots into logical groups
'''

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, output
from cvfunctions import pyramid
import random
from matplotlib import pyplot as plt
import numpy as np
from numpy.lib.function_base import average


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

def display_segments(xy, ab_current_cluster, color):
    for a, b in ab_current_cluster:
        plot_line(xy, a, b, color)
    
def get_lineeq(df):
    return np.array(df.loc[:, ['slope', 'intercept']])

def get_ab(df):
    return np.array(df.loc[:, ['a', 'b']])
    
def plot_line(xy, a, b, color):
    x = [xy[a][0], xy[b][0]]
    y = [xy[a][1], xy[b][1]]
    plt.plot(x, y, color)

def chains(im, df):
    chains = pyramid.build_chains(df) 
    chains_f = []
    for c in chains:
        if len(c) > 2:
            chains_f.append(c)
            
    for i in range(len(chains_f)):
        output.plot_image(im)  
        for segment in chains_f[i]:        
            plot_line(xy, segment['a'], segment['b'], 'r')
    
    avg_slopes = []
    avg_intercepts = []
    for c in chains:
        slopes = [segment['slope'] for segment in c]
        intercepts = [segment['intercept'] for segment in c]
        avg_slopes.append(average(slopes))
        avg_intercepts.append(average(intercepts))
        
    for i in range(len(chains)):
        for j in range(len(chains)):
            slope_ratio = avg_slopes[i] / avg_slopes[j]
            intercept_ratio = avg_intercepts[i] / avg_intercepts[j]
            if 0.5 < slope_ratio < 1.5 and 0.5 < intercept_ratio < 1.5:
                print i, j, slope_ratio, intercept_ratio

if __name__ == '__main__':
    
    DISP = False    
    
    im = images1[1]
        
    blobs, im_t = pyramid.detect_dots(im)
        
    lines_df = pyramid.get_lines(blobs)
    xy_lists = pyramid.get_xy(blobs)    
    xy = pyramid.xy_lists_to_matrix(*xy_lists)
    
    lines_df_sorted = lines_df.sort(columns=['dist'])

    df = lines_df_sorted.head(70)
    
    ab_good = get_ab(df)
    output.plot_image(im)   
    for a, b in ab_good:
        plot_line(xy, a, b, 'r') 
            
    lineeq = get_lineeq(df)
    ab = get_ab(df)
    
    data = lineeq        
    
    nclusters = 12
    centroids, idx = kmeans_clustering(data, nclusters)
    
    chains(im, df)
    
    if DISP: 
        
        for i in range(nclusters):    
            randcolor = get_rand_color()
            ab_current_cluster = ab[idx==i]
            print len(ab_current_cluster)
    
            output.plot_image(im)    
            display_segments(xy, ab_current_cluster, randcolor)
      
        display_clustering_results(data, centroids, idx, nclusters)