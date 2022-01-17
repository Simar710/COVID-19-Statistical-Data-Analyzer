import csv
import io
import sys
from collections import defaultdict, OrderedDict
import pandas
import matplotlib.pyplot as plt
from datetime import datetime


def preprocess(argv):
    icu_file = argv[2]

    icu_cases_by_date = defaultdict(lambda: [0, 0])
    with open(icu_file, encoding="utf-8-sig"):
        icu_file = open(icu_file, encoding="utf-8-sig")
        csv_reader = csv.reader(icu_file)
        next(csv_reader, None)
        for row in csv_reader:
            icu_cases_by_date[datetime.strptime(row[0], "%Y-%m-%d")][0] += int(row[2]) + int(row[3])
            icu_cases_by_date[datetime.strptime(row[0], "%Y-%m-%d")][1] += int(row[4])

    with open("data/icu_preprocessed.csv", "w") as preprocessed:
        csv_writer = csv.writer(preprocessed)
        csv_writer.writerow(["date", "ICU", "hospitalizations"])
        for elem in sorted(icu_cases_by_date.items()):
            csv_writer.writerow([elem[0], elem[1][0], elem[1][1]])


def graph(argv):
    date_begin = datetime.strptime(argv[2], "%Y-%m-%d")
    date_end = datetime.strptime(argv[3], "%Y-%m-%d")
    re_file = argv[4]
    preprocessed_icu_file = argv[5]
    out_file = argv[6]

    with open(re_file, encoding="utf-8-sig") as re_file, open(preprocessed_icu_file,
                                                              encoding="utf-8-sig") as preprocessed_icu_file:
        re_reader = csv.reader(re_file)
        icu_reader = csv.reader(preprocessed_icu_file)
        next(re_reader, None)
        next(icu_reader, None)
        icu_stats = OrderedDict()
        re_stats = OrderedDict()

        # read ICU csv file as as a map from date -> (#icu_vented, #hospitalizations) provided that the date is within
        # our desired range
        for row in icu_reader:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            icu_vented = int(row[1])
            hospitalizations = int(row[2])
            if date_begin <= date <= date_end:
                icu_stats[date] = (icu_vented, hospitalizations)

        # read re csv file as as a map from date -> (re ,lower re CI, higher re CI)  provided that the date is within our
        # desired range
        for row in re_reader:
            re_date_start = datetime.strptime(row[1], "%Y-%m-%d")
            re_date_end = datetime.strptime(row[2], "%Y-%m-%d")
            re = float(row[3])
            re_lower = float(row[4])
            re_higher = float(row[5])

            if date_begin <= re_date_start and re_date_end <= date_end:
                re_stats[re_date_start] = (re, re_lower, re_higher)

        icu_graph_csv = io.StringIO()
        csv_writer = csv.writer(icu_graph_csv)
        csv_writer.writerow(["date", "ICU", "hospitalizations"])
        for date, icu_and_hospitalizations in icu_stats.items():
            csv_writer.writerow([date.strftime("%Y-%m-%d"), icu_and_hospitalizations[0], icu_and_hospitalizations[1]])
        icu_graph_csv.seek(0)

        re_graph_csv = io.StringIO()
        csv_writer = csv.writer(re_graph_csv)
        csv_writer.writerow(["date", "re", "lower re CI", "higher re CI"])
        for date, re_numbers in re_stats.items():
            csv_writer.writerow([date.strftime("%Y-%m-%d"), re_numbers[0], re_numbers[1], re_numbers[2]])
        re_graph_csv.seek(0)

        icu_graph_dataframe = pandas.read_csv(icu_graph_csv)
        re_graph_dataframe = pandas.read_csv(re_graph_csv)

        # the magic graphing bit
        ax1 = re_graph_dataframe.plot(x="date", y="re", legend=False)
        ax1.set_ylabel("Re number")
        plt.xticks(rotation=45, ha='right')
        ax2 = ax1.twinx()
        icu_graph_dataframe.plot(x="date", y="ICU", ax=ax2, color="red", legend=False)
        icu_graph_dataframe.plot(x="date", y="hospitalizations", ax=ax2, color="purple", legend=False)
        ax2.set_ylabel("# patients")
        ax1.figure.legend()
        plt.savefig(out_file, bbox_inches="tight")


if __name__ == '__main__':
    if sys.argv[1] == "p":
        preprocess(sys.argv)
    elif sys.argv[1] == 'g':
        graph(sys.argv)
