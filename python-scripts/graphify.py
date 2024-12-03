#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

import os
import pprint
from collections import namedtuple


def trimCSV(filename):
    """
    trims comment and file name from CSV
    """
    with open(filename, "r") as f:
        return [x.split(",")[0:2] for x in f.readlines()]


def getBranchStats(filename):
    """
    searches for bpred add index 0 as the key and index 1 as value
    """
    branchstats = dict()
    with open(filename, "r") as f:
        for l in f:
            split_line = l.split(",")
            if split_line[0].find("bpred") != -1:
                metric = "".join(split_line[0].split(".")[1:])
                branchstats[metric] = float(split_line[1])
    return branchstats


def benchMarkBranchMethodValueMap(fn):
    """
    ("Bench Mark", "Branching Method",  {Metrics: })
    """

    return (fn.split("_")[-2], fn.split("_")[-1].split(".")[0], getBranchStats(fn))


result = namedtuple("result", "metric, benchmark, method, value")


def ToMetricBenchMarkMethod(valueMap):
    all_result = []

    methods = set()
    benchmarks = set()
    metrics = set()

    for method in valueMap:
        methods.add(method)
        for benchmark in valueMap[method]:
            benchmarks.add(benchmark)
            for metric in valueMap[method][benchmark]:
                metrics.add(metric)
                value = valueMap[method][benchmark][metric]
                all_result.append(result(metric, benchmark, method, value))

    return methods, benchmarks, metrics, all_result


def getAllBenchMarks(directory):
    allBenchMarks = dict()
    for csv in os.listdir(directory):
        curBench = benchMarkBranchMethodValueMap(directory + "/" + csv)
        if curBench[1] in allBenchMarks:
            allBenchMarks[curBench[1]].update({curBench[0]: curBench[2]})
        else:
            allBenchMarks.update({curBench[1]: {curBench[0]: curBench[2]}})

    return allBenchMarks


def makeGraph(ax, metric, method, benchmark, data):
    graphables = [x for x in data if x.metric == metric]
    pprint.pprint(graphables)
    # species
    group = dict.fromkeys(method)
    for able in graphables:
        if group[able.method] is None:
            group[able.method] = [able]
        else:
            group[able.method].append(able)

    multiplier = 0

    colorSelection = ["r", "b", "g", "y", "k", "m"]
    for meth, data in group.items():

        print(meth)
        if data is not None:
            graphdata = [d.value for d in sorted(data, key=lambda x: x.benchmark)]
            graphlabels = [d.benchmark for d in sorted(data, key=lambda x: x.benchmark)]
            print(graphdata)
            print(graphlabels)
            x = np.arange(0, len(graphdata))
            offset = 1 * multiplier
            rects = ax.bar(
                x + offset,
                graphdata,
                align="edge",
                color=colorSelection,
            )
            ax.bar_label(rects, padding=3)
            ax.legend(rects, graphlabels)
        multiplier += 6
    ax.set_title(metric)
    ax.set_xticks(np.arange(0, len(method) * len(benchmark), len(benchmark)), method)
    pprint.pprint(group)


if __name__ == "__main__":
    allBenchMarks = getAllBenchMarks("results")
    methods, benchmarks, metrics, all_result = ToMetricBenchMarkMethod(allBenchMarks)
    for tric in metrics:
        fig, ax = plt.subplots(layout="constrained")
        makeGraph(ax, tric, methods, benchmarks, all_result)
        plt.show()
        break
