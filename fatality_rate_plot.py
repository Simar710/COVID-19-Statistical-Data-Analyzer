import sys
import pandas as pd 
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

def main(argv):
  if len(argv) != 3:
        print("Usage: fatality_plot.py <file name> <graphics filename>")
        sys.exit(1)
      
  csv_filename = argv[1]
  graphics_filename = argv[2]

  try:
    csv_df = pd.read_csv(csv_filename)

  except IOError as err:
        print("Unable to open source file",csv_filename,
                ": {}".format(err), file=sys.stderr)
        sys.exit(-1)

  fig = plt.figure()

  ax = sns.lineplot(x = "Date", y = "Count", hue="Outcome", data=csv_df)
  ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
  plt.xticks(rotation = 40, ha = 'right')
  ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))

  fig.savefig(graphics_filename, bbox_inches="tight")

main(sys.argv)