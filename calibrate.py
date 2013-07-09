from cvhelpers import images as cvhimages
from cvhelpers import calibration as cvhcalib
import cv2
from glob import glob

# PARAMETERS
images_mask = r'D:\Dropbox\SINTEF\img\first_four\*_0.bmp'
pattern_shape = (8, 8)
square_size = 3.0

images_names = glob(images_mask)
res = [(cv2.findChessboardCorners(cvhimages.open_image(img), pattern_shape), img) for img in images_names]

pattern_points = cvhcalib.get_pattern_points(pattern_shape, square_size)
object_points = []
image_points = []
for func_out, img_name in res:
    found, corners = func_out
    if not found:
        print 'Chessboard not found on %s' % img_name
        continue
    image_points.append(corners.reshape(-1, 2))
    object_points.append(pattern_points)
    
rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, pattern_shape)
    
print camera_matrix
        
    






    
