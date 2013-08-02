from pylab import *
import matplotlib.pyplot as plt
from xlsxwriter.workbook import Workbook

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
    
def save_camera_intrinsics_to_excel_file(filename, intrinsics):
    wb = Workbook(filename)
    sheet = wb.add_worksheet()
    bold = wb.add_format({'bold': 1})
    sheet.write('B2', 'Camera matrix', bold)
    
    camera_matrix, dist_coefs = intrinsics
    
    rows, cols = camera_matrix.shape
    for i in range(rows):
        for j in range(cols):
            sheet.write(2+i, 1+j, camera_matrix[i, j])
            
    sheet.write('F2', 'Distortion coeffitients', bold)
    for i in range(len(dist_coefs)):
        sheet.write(2, 5+i, dist_coefs[i])
        
    wb.close()