

class Point:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.v_y = None
        self.v_d = None

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, z={self.z})"
