#!/usr/bin/env python
import sys
import csv
import io
from collections import defaultdict, OrderedDict
from datetime import datetime
import pandas
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from functools import cmp_to_key


def dist_cmp(lhs, rhs):
    order = ["<20", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90+"]
    return order.index(lhs[0]) - order.index(rhs[0])


def trend_cmp(lhs, rhs):
    order = ["<20", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90+"]
    return order.index(lhs[0][1]) - order.index(rhs[0][1])


def preprocess(argv):
    if len(argv) < 3:
        print("Incomplete parameters: <mode> <data file>")
        return

    file_path = argv[2]

    age_distribution = defaultdict(lambda: 0)
    total_cases_by_PHU = defaultdict(lambda: 0)

    with open(file_path, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        # skip the header
        next(reader, None)

        for row in reader:
            age_group = row[5]
            episode_date = datetime.strptime(row[1], "%Y-%m-%d")
            PHU = row[10]

            total_cases_by_PHU[PHU, str(episode_date)] += 1
            age_distribution[(PHU, str(episode_date), age_group)] += 1

    for key, value in age_distribution.items():
        PHU = key[0]
        episode_date = key[1]
        age_distribution[key] /= total_cases_by_PHU[PHU, episode_date]

    out = OrderedDict(sorted(age_distribution.items(), key=lambda x: (x[0], x[1])))

    with open('data/age_dist_trend_preprocessed.csv', "w") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["PHU ID", "EPISODE DATE", "AGE_GROUP", "PROBABILITY MASS"])
        for key, value in out.items():
            writer.writerow([key[0], key[1], key[2], value])


def graph(argv):
    if len(argv) < 5:
        print("require: <mode> <dist out file> <trend out file> <begin date> <end date> <PHU id>")
    dist_out_file = argv[2]
    trend_out_file = argv[3]
    begin_date = datetime.strptime(argv[4], "%Y-%m-%d")
    end_date = datetime.strptime(argv[5], "%Y-%m-%d")
    PHU_ID = int(argv[6])

    data = list()
    with open("data/age_dist_trend_preprocessed.csv") as data_file:
        reader = csv.reader(data_file)
        next(reader, None)
        for row in reader:
            phu = int(row[0])
            episode_date = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            age_group = row[2]
            probability_mass = float(row[3])
            data.append((phu, episode_date, age_group, probability_mass))

    age_distribution = defaultdict(lambda: 0.0)
    age_trend = defaultdict(lambda: 0.0)
    sum = 0.0
    for elem in data:
        if begin_date <= elem[1] <= end_date and PHU_ID == elem[0]:
            sum += float(elem[3])
            age_distribution[elem[2]] += float(elem[3])
            age_trend[(elem[1].strftime("%Y-%m-%d"), elem[2])] = float(elem[3])

    for key, value in age_distribution.items():
        age_distribution[key] /= sum

    age_distribution = OrderedDict(sorted(age_distribution.items(), key=cmp_to_key(dist_cmp)))
    age_trend = OrderedDict(sorted(age_trend.items(), key=cmp_to_key(trend_cmp)))

    age_distribution_csv = io.StringIO()
    writer = csv.writer(age_distribution_csv)
    writer.writerow(["age_group", "probability_mass"])
    for age_group, probability_mass in age_distribution.items():
        writer.writerow([age_group, probability_mass])

    age_distribution_csv.seek(0)
    age_distribution_dataset = pandas.read_csv(age_distribution_csv)

    fig = plt.figure()
    plt.xticks(rotation=45, ha='right')
    sns.barplot(data=age_distribution_dataset, x="age_group", y="probability_mass")
    fig.savefig(dist_out_file, bbox_inches="tight")

    age_trend_csv = io.StringIO()
    writer = csv.writer(age_trend_csv)
    writer.writerow(["date", "age_group", "probability_mass"])
    for date_and_age_group, probability_mass in age_trend.items():
        writer.writerow([date_and_age_group[0], date_and_age_group[1], probability_mass])

    age_trend_csv.seek(0)
    age_trend_dataset = pandas.read_csv(age_trend_csv)

    fig = plt.figure()
    plt.xticks(rotation=45, ha='right')

    ax = sns.lineplot(data=age_trend_dataset, x="date", hue="age_group", y="probability_mass")
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=25))
    fig.savefig(trend_out_file, bbox_inches="tight")


if __name__ == '__main__':
    if sys.argv[1] == 'p':
        preprocess(sys.argv)
    elif sys.argv[1] == 'g':
        graph(sys.argv)
    else:
        print("Unrecognized mode")
