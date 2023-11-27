import numpy as np


class Plane:

    def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None

    def __str__(self):
        return f"{self.a:.3f}*x + {self.b:.3f}*y + {self.c:.3f}*z + {self.d:.3f}*d = 0"

    def get_y_from_x_z(self, x, z):
        return (self.a * x + self.c * z + self.d) / -self.b

    def get_distance_from_point(self, point):
        dist = ((self.a * point.x + self.b * point.y + self.c * point.z + self.d) /
                ((self.a ** 2 + self.b ** 2 + self.c ** 2) ** 0.5))
        return dist

    @classmethod
    def calk_plane_from_scan(cls, scan):
        plane = cls()
        N, L = cls._get_N_L_matrices(scan)
        acd = np.linalg.solve(N, L)
        plane.a = acd[0]
        plane.b = -1
        plane.c = acd[1]
        plane.d = acd[2]
        return plane

    @staticmethod
    def _get_N_L_matrices(scan):
        A = []
        la, lc, ld = 0, 0, 0
        for point in scan:
            a = point.x
            c = point.z
            d = 1
            A.append([a, c, d])
            y = point.y
            la += a * y
            lc += c * y
            ld += d * y
        A = np.array(A)
        L = np.array([la, lc, ld])
        N = A.T @ A
        return N, L
