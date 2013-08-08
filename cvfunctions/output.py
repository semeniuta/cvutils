from pylab import *
import matplotlib.pyplot as plt

def plot_image(image, show_in_grayscale=True):
    '''
    Displays the image using Matplotlib figure
    '''    
    plt.figure()
    imshow(image)
    if show_in_grayscale:
        gray()
    
def create_and_save_histogram(data, nbins, title, filename):
    ''' 
    Saves the histogram for the given data under the specified filename    
    '''
    create_histogram(data, nbins, title)
    save_current_figure(filename)
    
def create_histogram(data, nbins, title):
    plt.figure()    
    plt.hist(data, nbins)
    plt.title(title)
    
def save_current_figure(filename):
    plt.savefig(filename)

def draw_vertical_line(x, color='r', linewidth=1):
    plt.axvline(x, color=color, linewidth=linewidth)
    
def draw_horizontal_line(y, color='r', linewidth=1):
    plt.axhline(y, color=color, linewidth=linewidth)
    
def plot_points(x, y):
    plot(x, y, 'ro')

def plot_circles(circles, color='b'):
    circle_objects = [plt.Circle(center, radius, edgecolor=color, fill=False) for center, radius in circles]    
    fig = plt.gcf()
    for c in circle_objects:
        fig.gca().add_artist(c)
    
                
    