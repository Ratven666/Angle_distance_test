import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from Scan import Scan


class Comparator:

    def __init__(self, surface_type, data_dict):
        self.surface_type = surface_type
        self.data_dict = data_dict
        self.scans = []
        self.points_df = None
        self.scans_df = None
        self._init_comparator()

    def __iter__(self):
        return iter(self.scans)

    def _init_comparator(self):
        for data in self.data_dict:
            scan_name = f"{data['type_']}_{data['material']}_{data['angle']}"
            self.scans.append(Scan.load_scan_from_file(scan_name=scan_name,
                                                       filepath=data["filepath"],
                                                       type_=data['type_'],
                                                       material=data['material'],
                                                       angle=data['angle']
                                                       ))
        scans_data = {"material": [],
                       "type_": [],
                       "angle": [],
                       "mse": [],
                       "mse_type": [],
                      }
        for scan in self.scans:
            scans_data["material"].append(scan.material)
            scans_data["type_"].append(scan.type_)
            scans_data["angle"].append(scan.angle)
            scans_data["mse"].append(scan.mse_y)
            scans_data["mse_type"].append("mse_y")

            scans_data["material"].append(scan.material)
            scans_data["type_"].append(scan.type_)
            scans_data["angle"].append(scan.angle)
            scans_data["mse"].append(scan.mse_d)
            scans_data["mse_type"].append("mse_d")
        self.scans_df = pd.DataFrame(scans_data)

    def plot_mse(self):
        sns.set_style("darkgrid")
        ax = sns.lmplot(data=self.scans_df,
                        x="angle",
                        y="mse",
                        hue="mse_type",
                        col="type_",
                        fit_reg=False,
                        )
        plt.show()

    def plot_with_variance(self):
        data = {"angle": [],
                "v_points": [],
                "mse_type": [],
                "material": [],
                "type_": [],
                }
        for scan in self.scans:
            for point in scan:
                v_y = point.v_y + scan.mse_y
                v_d = point.v_d + scan.mse_d
                data["material"].append(scan.material)
                data["type_"].append(scan.type_)
                data["angle"].append(scan.angle)
                data["v_points"].append(v_y)
                data["mse_type"].append("mse_y")
                data["material"].append(scan.material)
                data["type_"].append(scan.type_)
                data["angle"].append(scan.angle)
                data["v_points"].append(v_d)
                data["mse_type"].append("mse_d")

        df = pd.DataFrame(data)
        sns.set_style("darkgrid")
        ax = sns.relplot(data=df,
                         x="angle",
                         y="v_points",
                         style="mse_type",
                         hue="mse_type",
                         col="type_",
                         kind="line",
                         markers=True,
                         errorbar=("se", 3),
                         )
        plt.show()

    def plot_points_distributions(self):
        sns.set_style("darkgrid")
        angles = sorted(list({scan.angle for scan in self.scans}))
        print(angles)
        for angle in angles:
            scans = [scan for scan in self.scans if scan.angle == angle]
            points_data = {"material": [],
                           "type_": [],
                           "angle": [],
                           "mse_type": [],
                           "deviation": [],
                           }
            for scan in scans:
                for point in scan:
                    points_data["angle"].append(scan.angle)
                    points_data["type_"].append(scan.type_)
                    points_data["material"].append(scan.material)
                    points_data["deviation"].append(point.v_y)
                    points_data["mse_type"].append("mse_y")

                    points_data["angle"].append(scan.angle)
                    points_data["type_"].append(scan.type_)
                    points_data["material"].append(scan.material)
                    points_data["deviation"].append(point.v_d)
                    points_data["mse_type"].append("mse_d")
            df = pd.DataFrame(points_data)
            ax = sns.displot(data=df,
                             x="deviation",
                             hue="mse_type",
                             col="type_",
                             row="angle",
                             kde=True,
                             )
            plt.show()
