import random

import seaborn as sns

from Comparator import Comparator
from DATA import DATA_CONCRETE, DATA_STEEL, DATA_BRICK, DATA_PAINTED_STEEL
from Plane import Plane
from SSMCForManyScans import SSMCForManyScans
from Scan import Scan
from ScanSamplerMonteCarlo import ScanSamplerMonteCarlo

scan = Scan.load_scan_from_file(scan_name="0", filepath="src/dry_concrete/Бетон85-exported.txt")

# scan.plot()
comparator = Comparator("dry_concrete", DATA_CONCRETE,
                        DATA_STEEL,)
                        # DATA_PAINTED_STEEL, DATA_BRICK)


# sub_scan = scan.get_sub_scan(4)
# sub_scan.plot()

# comparator.plot_mse()

# comparator.plot_with_variance()
# comparator.plot_mse()


# comparator.plot_points_distributions()
print(scan)

# ssmc = ScanSamplerMonteCarlo(scan=scan,
#                              # point_count_tuple=tuple(range(100, 106)),
#                              # point_count_tuple=(5, 7, 10, 15, 20, 30, 40, 50, 70, 100),
#                              point_count_tuple=(5, 10, 40, 50, 100),
#                              n_iteration=1_000,
#                              )
#
# ssmc.plot_mse_graphic()
# # #
# ssmc.plot_distribution()


ssmcfms = SSMCForManyScans(comparator,
                           # scans_angles_tuple=tuple([0, 20, 30, 40, 50, 55, 60, 70, 75, 80, 85]),
                           scans_angles_tuple=tuple([0, 30, 50, 70]),
                           point_count_tuple=(5, 10, 20, 30, 40, 50, 60, 100),
                           n_iteration=1_000,)

ssmcfms.plot_mse_graphic()