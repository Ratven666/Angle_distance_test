import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


from Point import Point


class ScanSamplerMonteCarlo:

    def __init__(self, scan, point_count_tuple=tuple(range(3, 20)), n_iteration=1_000):
        self.scan = scan
        self.point_count_tuple = point_count_tuple
        self.n_iteration = n_iteration
        self.x0 = (scan.max_x - scan.min_x) / 2
        self.z0 = (scan.max_z - scan.min_z) / 2
        self.deviation_df = self._calk_stat_data()
        self.mse_df = self._calk_mse()

    def _calk_stat_data(self):
        data = {"point_count": [],
                "deviation": [],
                }
        for point_count in self.point_count_tuple:
            for iteration in range(self.n_iteration):
                sub_scan = self.scan.get_sub_scan(point_count=point_count, random_seed=iteration)
                point_y = sub_scan.sub_plane.get_y_from_x_z(self.x0, self.z0)
                deviation = sub_scan.base_plane.get_distance_from_point(Point(x=self.x0,
                                                                              y=point_y,
                                                                              z=self.z0,
                                                                              ))
                if abs(deviation) > 1:
                    continue
                data["point_count"].append(point_count)
                data["deviation"].append(deviation)
        deviation_df = pd.DataFrame(data)
        return deviation_df

    def _calk_mse(self):
        mse_data = {"mse": [],
                    "point_count": []}
        for point_count in self.point_count_tuple:
            deviation_df = self.deviation_df[self.deviation_df["point_count"] == point_count]
            mse = deviation_df["deviation"].std()
            mse_data["mse"].append(mse)
            mse_data["point_count"].append(point_count)
        mse_df = pd.DataFrame(mse_data)
        return mse_df

    def plot_distribution(self):
        ax = sns.displot(data=self.deviation_df,
                         x="deviation",
                         col="point_count",
                         kde=True,
                         )
        plt.show()

    def plot_mse_graphic(self):
        sns.set_style("darkgrid")
        # ax = sns.lmplot(data=self.mse_df,
        #                 x="point_count",
        #                 y="mse",
        #                 fit_reg=True,
        #                 order=2,
        #                 ci=None
        #                 )
        ax = sns.lineplot(data=self.mse_df,
                          x="point_count",
                          y="mse",
                          marker=True,
                          )
        plt.show()
