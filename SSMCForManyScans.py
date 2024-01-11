import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from Comparator import Comparator
from ScanSamplerMonteCarlo import ScanSamplerMonteCarlo


class SSMCForManyScans:
    def __init__(self, comparator: Comparator, scans_angles_tuple=tuple([0, 20, 30, 40, 50, 55, 60, 70, 75, 80, 85]),
                 point_count_tuple=tuple(range(3, 20)), n_iteration=1_000):
        self.comparator = comparator
        self.scans = self.comparator.scans
        self.point_count_tuple = point_count_tuple
        self.scans_angles_tuple = scans_angles_tuple
        self.n_iteration = n_iteration
        self.deviation_df = pd.DataFrame()
        self.mse_df = pd.DataFrame()
        self._init()

    def _init(self):
        for scan in self.scans:
            try:
                if scan.angle not in self.scans_angles_tuple:
                    continue
                ssmc = ScanSamplerMonteCarlo(scan,
                                             point_count_tuple=self.point_count_tuple,
                                             n_iteration=self.n_iteration)
                ssmc.mse_df["angle"] = scan.angle
                ssmc.mse_df["type_"] = scan.type_
                ssmc.mse_df["material"] = scan.material
                ssmc.deviation_df["angle"] = scan.angle
                ssmc.deviation_df["type_"] = scan.type_
                ssmc.deviation_df["material"] = scan.material
                self.deviation_df = pd.concat([self.deviation_df, ssmc.deviation_df]).fillna(0)
                self.mse_df = pd.concat([self.mse_df, ssmc.mse_df]).fillna(0)
                print(f"Закончен расчет для угла {scan.angle} скана {scan}")
            except ValueError:
                continue

    def plot_mse_graphic(self):
        sns.set_style("darkgrid")
        ax = sns.relplot(data=self.mse_df,
                         x="point_count",
                         y="mse",
                         hue="angle",
                         col="type_",
                         row="material",
                         kind="line",
                         markers=True,
                         palette="tab10",
                         )
        plt.show()
