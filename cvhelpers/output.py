from pylab import *

def plot_image(image, show_in_grayscale=True):
    '''
    Displays the image using Matplotlib figure
    '''    
    
    imshow(image)
    if show_in_grayscale:
        gray()
        