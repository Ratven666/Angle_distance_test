import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from Scan import Scan


class Comparator:

    def __init__(self, surface_type, data_dict):
        self.surface_type = surface_type
        self.data_dict = data_dict
        self.scans = {}
        self.df = None
        self._init_comparator()

    def __iter__(self):
        return iter(self.scans.items())

    def _init_comparator(self):
        for angle, data in self.data_dict.items():
            self.scans[angle] = Scan.load_scan_from_file(scan_name=data["name"], filepath=data["filepath"])
        data = {"angle": [],
                "mse": [],
                "type": [],
                }
        for angle, scan in self.scans.items():
            data["mse"].append(scan.mse_y)
            data["angle"].append(angle)
            data["type"].append("mse_y")
            data["mse"].append(scan.mse_d)
            data["angle"].append(angle)
            data["type"].append("mse_d")
        self.df = pd.DataFrame(data)

    def plot_mse(self):
        sns.set_style("darkgrid")
        # g = sns.lmplot()
        ax = sns.lmplot(data=self.df, x="angle", y="mse", hue="type", fit_reg=False)
        # ax.scatter(data=self.df, x="angle", y="mse_y", color="b", label="mse_y")
        # ax.scatter(data=self.df, x="angle", y="mse_d", color="r", label="mse_d")
        # ax.set_title(self.surface_type)
        # ax.set(xlabel="angle_deg", ylabel="MSE")
        # plt.legend(loc="upper left")
        plt.show()

    # def plot_mse(self):
    #     sns.set_style("darkgrid")
    #     ax = plt.subplot()
    #     ax.scatter(data=self.df, x="angle", y="mse_y", color="b", label="mse_y")
    #     ax.scatter(data=self.df, x="angle", y="mse_d", color="r", label="mse_d")
    #     ax.set_title(self.surface_type)
    #     ax.set(xlabel="angle_deg", ylabel="MSE")
    #     plt.legend(loc="upper left")
    #     plt.show()

    def plot_points_distributions(self):
        sns.set_style("darkgrid")
        for angle, scan in self:
            data = {"deviation": [],
                    "type": []}
            for point in scan:
                data["deviation"].append(point.v_y)
                data["type"].append("v_y")
                data["deviation"].append(point.v_d)
                data["type"].append("v_d")

            data = pd.DataFrame(data)
            ax = sns.displot(data=data, x="deviation", hue="type", kde=True)
            ax.fig.suptitle(f"{self.surface_type} angle: {angle}")
            ax.set(xlabel="point_deviation", ylabel="count")
            plt.show()
