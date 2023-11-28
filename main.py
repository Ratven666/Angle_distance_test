import seaborn as sns

from Comparator import Comparator
from DATA import DATA_LIST
from Plane import Plane
from Scan import Scan

scan = Scan.load_scan_from_file(scan_name="0", filepath="src/dry_concrete/Бетон85-exported.txt")


comparator = Comparator("dry_concrete", DATA_LIST)

# comparator.plot_mse()


print(sns.load_dataset("fmri"))


# comparator.plot_points_distributions()
print(scan)
