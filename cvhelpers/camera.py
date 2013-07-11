class Camera:
    def __init__(self, camera_matrix):
        self.fx = camera_matrix[0, 0]
        self.fy - camera_matrix[1, 1]
        self.cx = camera_matrix[0, 2]
        self.cy - camera_matrix[1, 2]