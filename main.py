from Comparator import Comparator
from Plane import Plane
from Scan import Scan

scan = Scan.load_scan_from_file(scan_name="0", filepath="src/dry_concrete/Бетон85-exported.txt")

data_dict = {0: {"name": "dry_concrete_0",
                 "filepath": "src/dry_concrete/Бетон0-exported.txt",
                 },
             20: {"name": "dry_concrete_20",
                  "filepath": "src/dry_concrete/Бетон20-exported.txt",
                  },
             30: {"name": "dry_concrete_30",
                  "filepath": "src/dry_concrete/Бетон30-exported.txt",
                  },
             40: {"name": "dry_concrete_40",
                  "filepath": "src/dry_concrete/Бетон40-exported.txt",
                  },
             50: {"name": "dry_concrete_50",
                  "filepath": "src/dry_concrete/Бетон50-exported.txt",
                  },
             55: {"name": "dry_concrete_55",
                  "filepath": "src/dry_concrete/Бетон55-exported.txt",
                  },
             60: {"name": "dry_concrete_60",
                  "filepath": "src/dry_concrete/Бетон60-exported.txt",
                  },
             65: {"name": "dry_concrete_65",
                  "filepath": "src/dry_concrete/Бетон65-exported.txt",
                  },
             70: {"name": "dry_concrete_70",
                  "filepath": "src/dry_concrete/Бетон70-exported.txt",
                  },
             75: {"name": "dry_concrete_75",
                  "filepath": "src/dry_concrete/Бетон75-exported.txt",
                  },
             80: {"name": "dry_concrete_80",
                  "filepath": "src/dry_concrete/Бетон80-exported.txt",
                  },
             85: {"name": "dry_concrete_85",
                  "filepath": "src/dry_concrete/Бетон85-exported.txt",
                  },
             }

comparator = Comparator("dry_concrete", data_dict)

comparator.plot_mse()

comparator.plot_points_distributions()
print(scan)
