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
    plt.figure()    
    plt.hist(data, nbins)
    plt.title(title)
    plt.savefig(filename)
        