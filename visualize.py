
from typing import List
import matplotlib.pyplot as plt
from tree import Generation
from matplotlib.container import ErrorbarContainer
from matplotlib.collections import PathCollection


def visualize(generations: List[Generation], legend: str, plots: List[ErrorbarContainer]):
    q = [i for i in range(len(generations))]
    mins = [abs(generation.Min - generation.Avg) for generation in generations]
    avgs = [generation.Avg for generation in generations]
    maxs = [abs(generation.Max - generation.Avg) for generation in generations]
    errors = [mins, maxs]
    plot = plt.errorbar(q, avgs, yerr=errors, capsize=3,
                        fmt='o', ecolor='black', capthick=2, markersize=5)
    plot.set_label(legend)
    plots.append(plot)


def get_culmulative_average(generations_list: List[List[Generation]]) -> List[float]:
    cul_avg = []
    for i in range(len(generations_list[0])):
        Sum = 0
        for j in range(len(generations_list)):
            preSum = generations_list[j]
            Sum += preSum[i].Max
        cul_avg.append(Sum / len(generations_list))
    return cul_avg


def visualize_multiple_times(generations_list: List[List[Generation]], legend: str, plots: List[PathCollection]):
    data_points = get_culmulative_average(generations_list)
    q = [i for i in range(len(data_points))]
    plot = plt.scatter(q, data_points)
    plot.set_label(legend)
    plots.append(plot)

