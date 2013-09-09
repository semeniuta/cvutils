from pylab import *
import matplotlib.pyplot as plt

def plot_image(image, show_in_grayscale=True):
    '''
    Displays the image using Matplotlib figure
    '''    
    imshow(image)
    if show_in_grayscale:
        gray()
    
def create_and_save_histogram(data, nbins, title, filename):
    ''' 
    Saves the histogram for the given data under the specified filename    
    '''
    res = create_histogram(data, nbins, title)
    save_current_figure(filename)
    return res
    
def create_histogram(data, nbins, title=None):
    res = plt.hist(data, nbins)
    if not title == None:
        plt.title(title)
    return res
    
def save_current_figure(filename):
    plt.savefig(filename)

def draw_vertical_line(x, color='r', linewidth=1):
    plt.axvline(x, color=color, linewidth=linewidth)
    
def draw_horizontal_line(y, color='r', linewidth=1):
    plt.axhline(y, color=color, linewidth=linewidth)
    
def plot_points(x, y, color='r'):
    plot(x, y, color + 'o')

def plot_circles(circles, color='b'):    
    circle_objects = [plt.Circle(center, radius, edgecolor=color, fill=False) for center, radius in circles]    
    fig = plt.gcf()
    for c in circle_objects:
        fig.gca().add_artist(c)
        
def plot_image_histogram(image, nbins=128, title=None):
    res = create_histogram(image.flatten(), nbins, title)  
    return res
    
def plot_several_image_histograms(images, names=None, nbins=128):    
    nimages = len(images)
    for i in range(nimages):
        plt.subplot(nimages, 1, i+1)
        plot_image_histogram(images[i], nbins, names[i])    
                
    