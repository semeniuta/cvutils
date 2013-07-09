import cv2
from pylab import *
from cvhelpers import images
from cvhelpers import calibration
from cvhelpers import output

image_file = r'D:\Dropbox\SINTEF\img\first_four\00000001_0.bmp'
#image_file = r'D:\Dropbox\SINTEF\img\opencv_sample\left03.jpg'
image = images.open_image(image_file)

patternSize = (8, 7)

res = cv2.findChessboardCorners(image, patternSize)
print res
matrix = res[1]
x, y = calibration.chessboard_corners_maxtrix_to_lists(matrix)

output.plot_image(image)
plot(x, y, 'ro')