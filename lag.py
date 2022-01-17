import sys
import csv
import io
from collections import defaultdict
from datetime import datetime
import pandas
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from termcolor import colored


def preprocess(argv):
    if len(argv) < 3:
        print("Usage <mode> <data file>")
        return
    filepath = argv[2]
    with open(filepath) as data_file:
        reader = csv.reader(data_file)
        writer = csv.writer(open("data/lag_preprocessed.csv", "w"))
        writer.writerow(["PHU", "Test Report Date", "Specimen Date"])
        next(reader, None)
        for row in reader:
            writer.writerow([row[10], row[2], row[4]])


def graph(argv):
    if len(argv) < 5:
        print("Incomplete parameters, require <mode> <out file>  <2 or more PHU id and the data file>")

    out_file = argv[2]
    PHUs = list()
    for i in range(3, len(argv)):
        PHUs.append(argv[i])

    cases_by_PHU_date = defaultdict(lambda: list())
    with open("data/lag_preprocessed.csv") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            for PHU in PHUs:
                if row[0] == PHU:
                    if row[1] != '' and row[2] != '':
                        lag = datetime.strptime(row[1], "%Y-%m-%d") - datetime.strptime(row[2], "%Y-%m-%d")
                        if lag.days >= 14:
                            continue
                        else:
                            cases_by_PHU_date[(row[0], row[2])].append(lag.days)
                    else:
                        print(
                            colored(
                                "WARNING: this case is missing crucial information " + "{ " + ', '.join(row) + " }",
                                "red"))

    csv_file = io.StringIO()

    writer = csv.writer(csv_file)
    writer.writerow(["PHU", "date", "average_lag"])
    for key, value in cases_by_PHU_date.items():
        sum = 0.0
        for cases in cases_by_PHU_date[key]:
            sum += cases
        cases_by_PHU_date[key] = [sum / len(cases_by_PHU_date[key])]
        writer.writerow([key[0], key[1], cases_by_PHU_date[key][0]])

    csv_file.seek(0)
    lag_dataset = pandas.read_csv(csv_file)
    fig = plt.figure()
    ax = sns.lineplot(data=lag_dataset, x="date", hue="PHU", y="average_lag")
    ax.set_ylabel("average lag in days")
    plt.xticks(rotation=45, ha='right')
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=25))
    fig.savefig(out_file, bbox_inches="tight")


if __name__ == '__main__':
    if sys.argv[1] == 'p':
        preprocess(sys.argv)
    elif sys.argv[1] == 'g':
        graph(sys.argv)
