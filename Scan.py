import random
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

from Plane import Plane
from Point import Point


class Scan:

    def __init__(self, name):
        self.name = name
        self.points = []
        self.len = 0
        self.min_x, self.min_y, self.min_z = None, None, None
        self.max_x, self.max_y, self.max_z = None, None, None
        self.base_plane = None
        self.sub_plane = None
        self.mse_y = None
        self.mse_d = None
        self.type_ = None
        self.material = None
        self.angle = None

    def __iter__(self):
        return iter(self.points)

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return f"Scan(name={self.name})"

    def __str__(self):
        return f"Scan(name={self.name}, mse_y={self.mse_y:.6f}, mse_d={self.mse_d:.6f})"

    def get_sub_scan(self, point_count, random_seed=None):
        if point_count < 0 or point_count > len(self):
            raise ValueError(f"Неправильное количество точек в субскане. Передано: {point_count}"
                             f" в скане: {len(self)} точек")
        if random_seed is not None:
            random.seed(random_seed)
        sub_scan = deepcopy(self)
        sub_scan.points = random.sample(sub_scan.points, point_count)
        sub_scan.sub_plane = Plane.calk_plane_from_scan(sub_scan)
        return sub_scan

    @classmethod
    def load_scan_from_file(cls, scan_name, filepath, type_=None, material=None, angle=None):
        scan = cls(scan_name)
        scan.type_ = type_
        scan.material = material
        scan.angle = angle
        with open(filepath, "rt") as file_read:
            file_read.readline()
            for line in file_read:
                point = Point(*[float(el) for el in line.strip().split()[:3]])
                scan.points.append(point)
                cls._update_scan_borders(scan, point)
        scan.len = len(scan.points)
        scan.base_plane = Plane.calk_plane_from_scan(scan)
        scan._calk_scan_mse_y()
        scan._calk_scan_mse_d()
        return scan

    def _calk_scan_mse_y(self):
        vv = 0
        for point in self:
            plane_y = self.base_plane.get_y_from_x_z(point.x, point.z)
            v_y = plane_y - point.y
            point.v_y = v_y
            vv += v_y ** 2
            self.mse_y = (vv / (len(self) - 1)) ** 0.5
        return self.mse_y

    def _calk_scan_mse_d(self):
        vv = 0
        for point in self:
            v_d = self.base_plane.get_distance_from_point(point)
            point.v_d = v_d
            vv += v_d ** 2
            self.mse_d = (vv / (len(self) - 1)) ** 0.5
        return self.mse_d

    def plot(self, point_size=50):
        ScanPlotterMPL(point_size=point_size).plot(scan=self)

    @staticmethod
    def _update_scan_borders(scan, point):
        """
        Проверяет положение в точки в существующих границах скана
        и меняет их при выходе точки за их пределы
        :param scan: скан
        :param point: точка
        :return: None
        """
        if scan.min_x is None:
            scan.min_x, scan.max_x = point.x, point.x
            scan.min_y, scan.max_y = point.y, point.y
            scan.min_z, scan.max_z = point.z, point.z
        if point.x < scan.min_x:
            scan.min_x = point.x
        if point.x > scan.max_x:
            scan.max_x = point.x
        if point.y < scan.min_y:
            scan.min_y = point.y
        if point.y > scan.max_y:
            scan.max_y = point.y
        if point.z < scan.min_z:
            scan.min_z = point.z
        if point.z > scan.max_z:
            scan.max_z = point.z


class ScanPlotterMPL:
    """
    Отрисовка скана в виде облака точек через библиотеку matplotlib
    """

    def __init__(self, point_size=5):
        super().__init__()
        self.fig = None
        self.ax = None
        self.point_size = point_size

    def calk_plot_limits(self, scan):
        """
        Рассчитывает область построения скана для сохранения пропорций вдоль осей
        :param scan: скан который будет отрисовываться
        :return: Словарь с пределами построения модель вдоль трех осей
        """
        min_x, min_y, min_z = scan.min_x, scan.min_y, scan.min_z
        max_x, max_y, max_z = scan.max_x, scan.max_y, scan.max_z
        try:
            limits = [max_x - min_x,
                      max_y - min_y,
                      max_z - min_z]
        except TypeError:
            return
        length = max(limits) / 2
        x_lim = [((min_x + max_x) / 2) - length, ((min_x + max_x) / 2) + length]
        y_lim = [((min_y + max_y) / 2) - length, ((min_y + max_y) / 2) + length]
        z_lim = [((min_z + max_z) / 2) - length, ((min_z + max_z) / 2) + length]
        return {"X_lim": x_lim, "Y_lim": y_lim, "Z_lim": z_lim}

    def set_plot_limits(self, plot_limits):
        """
        Устанавливает в графике области построения в соответствии с переданными значениями
        :param plot_limits: словарь с границами области построения
        :return: None
        """
        self.ax.set_xlim(*plot_limits["X_lim"])
        self.ax.set_ylim(*plot_limits["Y_lim"])
        self.ax.set_zlim(*plot_limits["Z_lim"])

    @staticmethod
    def calk_mpl_colors(plot_data):
        """
        пересчитывает данные цвета точек в формат для библиотеки matplotlib
        :param plot_data: данные для которых нужно пересчитать цвета
        :return: Список с цветами в формате для библиотеки matplotlib
        """
        c_lst = []
        for point_color in plot_data["color"]:
            color = [color / 255.0 for color in point_color]
            c_lst.append(color)
        return c_lst

    def get_plot_data(self, scan):
        """
        Запускает процедуру разряжения скана если задан атрибут __sampler
        возвращает словарь с данными для визуализации разреженных данных
        :param scan: скан, который требуется разрядить и подготовить к визуализации
        :return: словарь с данными для визуализации
        """
        x_lst, y_lst, z_lst = [], [], []
        for point in scan:
            x_lst.append(point.x)
            y_lst.append(point.y)
            z_lst.append(point.z)
        return {"x": x_lst, "y": y_lst, "z": z_lst, "scan": scan}

    def _plot_plane(self, scan: Scan, plane):
        x = np.arange(scan.min_x, scan.max_x + 1e-6, scan.max_x - scan.min_x)
        z = np.arange(scan.min_z, scan.max_z + 1e-6, scan.max_z - scan.min_z)
        x, z = np.meshgrid(x, z)
        y = (plane.a * x + plane.c * z + plane.d) / -plane.b
        self.ax.plot_surface(x, y, z, alpha=0.5)

    def plot(self, scan):
        """
        Отрисовка скана в 3D
        :param scan: скан который будет отрисовываться
        :return: None
        """
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection="3d")
        plot_data = self.get_plot_data(scan)
        self.set_plot_limits(self.calk_plot_limits(scan))
        self.ax.scatter(plot_data["x"],
                        plot_data["y"],
                        plot_data["z"],
                        marker="+",
                        s=self.point_size,
                        )
        self._plot_plane(scan, scan.base_plane)
        if scan.sub_plane is not None:
            self._plot_plane(scan, scan.sub_plane)
        plt.show()

