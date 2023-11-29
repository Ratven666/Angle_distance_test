import random

import seaborn as sns

from Comparator import Comparator
from DATA import DATA_LIST
from Plane import Plane
from Scan import Scan

scan = Scan.load_scan_from_file(scan_name="0", filepath="src/dry_concrete/Бетон85-exported.txt")


comparator = Comparator("dry_concrete", DATA_LIST)

# comparator.plot_mse()

# comparator.plot_with_variance()


# comparator.plot_points_distributions()
print(scan)

lst = list(range(20))
print(lst)
r_lst = random.sample(lst, 3)
print(r_lst)

sub_scan = scan.get_sub_scan(10, random_seed=2)
sub_scan.plot()