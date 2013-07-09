from pylab import *

def plot_image(image, show_in_grayscale=True):
    imshow(image)
    if show_in_grayscale:
        gray()
        