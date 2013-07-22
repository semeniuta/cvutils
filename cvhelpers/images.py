from PIL import Image
import numpy as np
import os
import mimetypes
from glob import glob

def open_image(image_file, convert_option='L', return_as_array=True):
    ''' 
    Opens an image file specified as a string
    
    Arguments:
    image_file -- path to the image file
    convert_option -- convert option applied to PIL.Image object
                      (default 'L' - grayscale)
    return_as_array -- if True, the array of pixels is returned, otherwise - 
                       a PIL.Image object
    '''
    image = Image.open(image_file).convert(convert_option)
    if return_as_array:
        return np.array(image)
    else:
        return image

def open_images_from_dir(directory):
    '''
    Open images from the specified directory and returns a list of pixel arrays
    for each image    
    '''
    image_files = [os.path.join(directory, el) for el in os.listdir(directory)]
    image_files = filter(file_is_image, image_files)
    return [open_image(imgfile) for imgfile in image_files]
    
def open_images_from_mask(mask):
    '''
    Open images from the specified mask 
    (e.g. r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg') 
    and returns a list of pixel arrays for each image    
    '''
    image_files = glob(mask)
    return [open_image(imgfile) for imgfile in image_files]
    
def file_is_image(filename):
    '''
    Checks if the specified file is an image
    '''
    mt = mimetypes.guess_type(filename)
    return mt[0].split('/')[0] == 'image'
    
def get_image_size(img):
    '''
    Retuns image size in pixels as a tuple with width and height length    
    '''
    h, w = img.shape
    return (w, h)
    