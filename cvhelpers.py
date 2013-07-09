from PIL import Image
import numpy as np
import os
import mimetypes

def open_image(image_file, convert_option='L', return_as_array=True):
    image = Image.open(image_file).convert(convert_option)
    if return_as_array:
        return np.array(image)
    else:
        return image

def open_images_from_dir(directory):
    image_files = [os.path.join(directory, el) for el in os.listdir(directory)]
    image_files = filter(file_is_image, image_files)
    return [open_image(imgfile) for imgfile in image_files]
    
def file_is_image(filename):
    mt = mimetypes.guess_type(filename)
    return mt[0].split('/')[0] == 'image'
    
    
    
    
    
    
    
# Testing
if __name__ == '__main__':
    open_images_from_dir(r'D:\Dropbox\SINTEF\img\first_four')
    