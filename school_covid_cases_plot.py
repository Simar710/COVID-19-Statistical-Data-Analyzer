import sys
import pandas as pd 
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

def main(argv):
  if len(argv) != 3:
        print("Usage: school_covid_cases_plot.py <file name> <graphics filename>")
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

  ax = sns.lineplot(x = "School", y = "Total_Cases", data=csv_df)
    
  #give better names to x and y axis
  plt.xlabel('School Names')
  plt.ylabel('Total no. of Cases')
  
  #rotate the names to left by 45 degrees  
  plt.xticks(rotation = 45, ha = 'right')
  
  fig.savefig(graphics_filename, bbox_inches="tight")

main(sys.argv)