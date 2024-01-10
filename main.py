import random

import seaborn as sns

from Comparator import Comparator
from DATA import DATA_CONCRETE, DATA_STEEL, DATA_BRICK, DATA_PAINTED_STEEL
from Plane import Plane
from Scan import Scan
from ScanSamplerMonteCarlo import ScanSamplerMonteCarlo

scan = Scan.load_scan_from_file(scan_name="0", filepath="src/dry_concrete/Бетон85-exported.txt")

scan.plot()
comparator = Comparator("dry_concrete", DATA_CONCRETE, DATA_STEEL,
                        DATA_PAINTED_STEEL, DATA_BRICK)


# sub_scan = scan.get_sub_scan(4)
# sub_scan.plot()

# comparator.plot_mse()

comparator.plot_with_variance()
# comparator.plot_mse()


# comparator.plot_points_distributions()
print(scan)
#
# ssmc = ScanSamplerMonteCarlo(scan=scan,
#                              # point_count_tuple=tuple(range(100, 106)),
#                              point_count_tuple=(5, 7, 10, 15, 20, 30, 40, 50, 70, 100),
#                              n_iteration=1_000,
#                              )
#
# ssmc.plot_mse_graphic()
# #
# ssmc.plot_distribution()
