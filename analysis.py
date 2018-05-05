"""
Copyright (C) 2017 Shane Steinert-Threlkeld

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
import matplotlib 
matplotlib.use('Agg')

import itertools as it
import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt
import util
import argparse

# COLORS = ["blue", "red", "green", "brown", "purple", "orange"]
COLORS = ["#377eb8", "#ff7f00", "#4daf4a", "#f781bf", "#a65628", "#984ea3", "#999999", "#e41a1c", "#dede00"]
linestyles = ["-", "-.", "--", ":"]

# Conservative quantifiers
quants_c = ["all", "not_all", "most_AB", "most_not_AB", "exactly_half_AB"]

# Non-conservative quantifiers
quants_nc = ["only", "not_only", "most_BA", "most_not_BA", "exactly_half_BA"]

# Test quantifiers
quants_test = ["all", "only"]


def experiment_analysis(path, quants, path_tosave, title, trials=range(30), plots=True):
    """Prints statistical tests and makes plots for experiment one.

    Args:
        path: where the trials in CSV are
        plots: whether to make plots or not
    """
    print(path.split("/")[-1], path.split("/")[1])

    # read the data in
    data = util.read_trials_from_csv(path, trials)
    # print("Data read!")
    # FILTER OUT TRIALS WHERE RNN DID NOT LEARN
    remove_bad_trials(data)
    # get convergence points per quantifier
    convergence_points = get_convergence_points(data, quants)

    if plots:
        # make plots
        # make_boxplots(convergence_points, quants)
        # make_barplots(convergence_points, quants)
        make_plot(data, quants, path_tosave, title, ylim=(0.4, 1))

    print(stats.ttest_rel(convergence_points[quants[0]],
                          convergence_points[quants[1]]))
    print()


def experiment_one_a_10k_analysis():
    experiment_analysis("results/10k/exp-1-a/run_2", ["all", "only", "not_all", "most_AB", "most_not_AB", "exactly_half_AB"], "plots_training/10k/run_2/run_2.4c_0nc_10k.png", "4c:0nc")


def experiment_one_b_10k_analysis():
    experiment_analysis("results/10k/exp-1-b/run_3", ["all", "only", "not_all", "most_AB", "most_not_AB", "not_only"], "plots_training/10k/run_2/run_2.3c_1nc_10k.png", "3c:1nc")


def experiment_one_c_10k_analysis():
    experiment_analysis("results/10k/exp-1-c/run_2", ["all", "only", "not_all", "most_AB", "not_only", "most_BA"], "plots_training/10k/run_2/run_2.2c_2nc_10k.png", "2c:2nc")


def experiment_one_d_10k_analysis():
    experiment_analysis("results/10k/exp-1-d/run_2", ["all", "only", "not_all", "not_only", "most_BA", "most_not_BA"], "plots_training/10k/run_2/run_2.1c_3nc_10k.png", "1c:3nc")


def experiment_one_e_10k_analysis():
    experiment_analysis("results/10k/exp-1-e/run_2", ["all", "only", "not_only", "most_BA", "most_not_BA", "exactly_half_BA"], "plots_training/10k/run_2/run_2.0c_4nc_10k.png", "0c:4nc")


def experiment_one_a_30k_analysis():
    experiment_analysis("results/30k/exp-1-a/run_2", ["all", "only", "not_all", "most_AB", "most_not_AB", "exactly_half_AB"], "plots_training/30k/run_2/run_2.4c_0nc_30k.png", "4c:0nc")


def experiment_one_b_30k_analysis():
    experiment_analysis("results/30k/exp-1-b/run_3", ["all", "only", "not_all", "most_AB", "most_not_AB", "not_only"], "plots_training/30k/run_2/run_2.3c_1nc_30k.png", "3c:1nc")


def experiment_one_c_30k_analysis():
    experiment_analysis("results/30k/exp-1-c/run_2", ["all", "only", "not_all", "most_AB", "not_only", "most_BA"], "plots_training/30k/run_2/run_2.2c_2nc_30k.png", "2c:2nc")


def experiment_one_d_30k_analysis():
    experiment_analysis("results/30k/exp-1-d/run_2", ["all", "only", "not_all", "not_only", "most_BA", "most_not_BA"], "plots_training/30k/run_2/run_2.1c_3nc_30k.png", "1c:3nc")


def experiment_one_e_30k_analysis():
    experiment_analysis("results/30k/exp-1-e/run_2", ["all", "only", "not_only", "most_BA", "most_not_BA", "exactly_half_BA"], "plots_training/30k/run_2/run_2.0c_4nc_30k.png", "0c:4nc")


def remove_bad_trials(data, threshold=0.60):
    """Remove "bad" trials from a data set.  A trial is bad if the total
    accuracy never converged to a value close to 1.  The bad trials are
    deleted from data, but nothing is returned.
    """
    accuracies = [data[key]["total_accuracy"].values for key in data.keys()]
    forward_accs = [forward_means(accs) for accs in accuracies]
    threshold_pos = [first_above_threshold(accs, threshold)
                     for accs in forward_accs]
    # a trial is bad if the forward mean never hit 0.99
    bad_trials = [idx for idx, thresh in enumerate(threshold_pos)
                  if thresh is None]
    print("Number of bad trials: {}".format(len(bad_trials)))
    for trial in bad_trials:
        del data[trial]


def get_convergence_points(data, quants):
    """Get convergence points by quantifier for the data.

    Args:
        data: a dictionary, intended to be made by util.read_trials_from_csv
        quants: list of quantifier names

    Returns:
        a dictionary, with keys the quantifier names, and values the list of
        the step at which accuracy on that quantifier converged on each trial.
    """
    convergence_points = {q: [] for q in quants}
    for trial in data.keys():
        for quant in quants:
            convergence_points[quant].append(
                data[trial]["global_step"][
                    convergence_point(
                        data[trial][quant + "_accuracy"].values)])
    return convergence_points


def diff(ls1, ls2):
    """List difference function.

    Args:
        ls1: first list
        ls2: second list

    Returns:
        pointwise difference ls1 - ls2
    """
    assert len(ls1) == len(ls2)
    return [ls1[i] - ls2[i] for i in range(len(ls1))]


def forward_means(arr, window_size=250):
    """Get the forward means of a list. The forward mean at index i is
    the sum of all the elements from i until i+window_size, divided
    by the number of such elements. If there are not window_size elements
    after index i, the forward mean is the mean of all elements from i
    until the end of the list.

    Args:
        arr: the list to get means of
        window_size: the size of the forward window for the mean

    Returns:
        a list, of same length as arr, with the forward means
    """
    return [(sum(arr[idx:min(idx + window_size, len(arr))]) /
             min(window_size, len(arr) - idx))
            for idx in range(len(arr))]


def first_above_threshold(arr, threshold):
    """Return the point at which a list value is above a threshold.

    Args:
        arr: the list
        threshold: the threshold

    Returns:
        the first i such that arr[i] > threshold, or None if there is not one
    """
    means = forward_means(arr)
    for idx in range(len(arr)):
        if arr[idx] > threshold and means[idx] > threshold:
            return idx
    return None


def convergence_point(arr, threshold=0.50):
    """Get the point at which a list converges above a threshold.

    Args:
        arr: the list
        threshold: the threshold

    Returns:
        the first i such that forward_means(arr)[i] is above threshold
    """
    return first_above_threshold(arr, threshold)


def get_max_steps(data):
    """Gets the longest `global_step` column from a data set.

    Args:
        data: a dictionary, whose values are pandas.DataFrame, which have a
        column named `global_step`

    Returns:
        the values for the longest `global_step` column in data
    """
    max_val = None
    max_len = 0
    for key in data.keys():
        new_len = len(data[key]["global_step"].values)
        if new_len > max_len:
            max_len = new_len
            max_val = data[key]["global_step"].values
    return max_val


def make_plot(data, quants, path_tosave, title, ylim=None, threshold=0.95):
    """Makes a line plot of the accuracy of trials by quantifier, color coded,
    and with the medians also plotted.

    Args:
        data: the data
        quants: list of quantifier names
        ylim: y-axis boundaries
    """
    assert len(quants) <= len(COLORS)

    """
    Plot training
    """
    print("Generating plot: {0}".format(path_tosave))
    trials_by_quant = [[] for _ in range(len(quants))]
    for trial in data.keys():
        for idx in range(len(quants)):
            trials_by_quant[idx].append(smooth_data(
                data[trial][quants[idx] + "_accuracy"].values))

    # plot median lines
    medians_by_quant = [get_median_diff_lengths(trials_by_quant[idx])
                        for idx in range(len(trials_by_quant))]
    # get x-axis of longest trial
    longest_x = get_max_steps(data)
    for idx in range(len(quants)):

        # C style
        if quants[idx] in quants_c[1:]:
            lines = "-"
            color = COLORS[idx]
        # NC style
        if quants[idx] in quants_nc[1:]:
            lines = "-."
            color = COLORS[idx]
        # Test style
        if quants[idx] == "all":
            lines = ":"
            color = "#377eb8"
        if quants[idx] == "only":
            lines = ":"
            color = "#ff7f00"

        plt.plot(longest_x,
                 smooth_data(medians_by_quant[idx]),
                 color,
                 label=quants[idx],
                 linewidth=1.5,
                 linestyle=lines)

    # max_x = max([len(ls) for ls in medians_by_quant])
    # plt.plot(longest_x, [threshold for _ in range(max_x)],
    #          linestyle="dashed", color="#4daf4a")
    if ylim:
        plt.ylim(ylim)
    plt.title(title)
    plt.legend(loc=4)
    plt.xlabel("Global step")
    plt.ylabel("Accuracy")
    plt.savefig(path_tosave, dpi=500)
    plt.close()

    """
    Plot testing
    """
    # First 2 are test quantifiers
    quants = quants[:2]
    colors = ["#377eb8", "#e41a1c"]

    # Change output file path
    path_tosave = "plots_testing/" + "/".join(path_tosave.split("/")[1:])
    print("Generating plot: {0}".format(path_tosave))

    trials_by_quant = [[] for _ in range(len(quants))]
    for i, trial in enumerate(data.keys()):
        steps = data[trial]["global_step"].values
        for idx in range(len(quants)):
            trials_by_quant[idx].append(
                smooth_data(data[trial][quants[idx] + "_accuracy"].values)
            )
            plt.plot(
                steps,
                trials_by_quant[idx][-1],
                colors[idx],
                # label=quants[idx] if i == 0 else "",
                alpha=0.4,
                linewidth=1,
            )

    # plot median lines
    medians_by_quant = [get_median_diff_lengths(trials_by_quant[idx])
                        for idx in range(len(trials_by_quant))]
    # get x-axis of longest trial
    longest_x = get_max_steps(data)

    for idx in range(len(quants)):
        plt.plot(
            longest_x,
            smooth_data(medians_by_quant[idx]),
            color=colors[idx],
            label=quants[idx],
            linewidth=2,
        )

    plt.title(title)
    plt.legend(loc=4)
    plt.xlabel("Global step")
    plt.ylabel("Accuracy")
    plt.savefig(path_tosave, dpi=500)
    plt.close()


def get_median_diff_lengths(trials):
    """Get the point-wise median of a list of lists of possibly
    different lengths.

    Args:
        trials: a list of lists, corresponding to trials

    Returns:
        a list, of the same length as the longest list in trials,
        where the list at index i contains the median of all of the
        lists in trials that are at least i long
    """
    max_len = np.max([len(trial) for trial in trials])
    # pad trials with NaN values to length of longest trial
    trials = np.asarray(
        [np.pad(trial, (0, max_len - len(trial)),
                "constant", constant_values=np.nan)
         for trial in trials])
    return np.nanmedian(trials, axis=0)


# def make_boxplots(convergence_points, quants):
#     """Makes box plots of some data.

#     Args:
#         convergence_points: dictionary of quantifier convergence points
#         quants: names of quantifiers
#     """
#     plt.boxplot([convergence_points[quant] for quant in quants])
#     plt.xticks(range(1, len(quants) + 1), quants)
#     plt.show()


# def make_barplots(convergence_points, quants):
#     """Makes bar plots, with confidence intervals, of some data.

#     Args:
#         convergence_points: dictionary of quantifier convergence points
#         quants: names of quantifiers
#     """
#     pairs = list(it.combinations(quants, 2))
#     assert len(pairs) <= len(COLORS)

#     diffs = {pair: diff(convergence_points[pair[0]],
#                         convergence_points[pair[1]])
#              for pair in pairs}
#     means = {pair: np.mean(diffs[pair]) for pair in pairs}
#     stds = {pair: np.std(diffs[pair]) for pair in pairs}
#     intervals = {pair: stats.norm.interval(
#         0.95, loc=means[pair],
#         scale=stds[pair] / np.sqrt(len(diffs[pair])))
#         for pair in pairs}

#     # plotting info
#     index = np.arange(len(pairs))
#     bar_width = 0.75
#     # reshape intervals to be fed to pyplot
#     yerrs = [[means[pair] - intervals[pair][0] for pair in pairs],
#              [intervals[pair][1] - means[pair] for pair in pairs]]

#     plt.bar(index, [means[pair] for pair in pairs], bar_width, yerr=yerrs,
#             color=[COLORS[idx] for idx in range(len(pairs))],
#             ecolor="black", align="center")
#     plt.xticks(index, pairs)
#     plt.show()


def smooth_data(data, smooth_weight=0.9):
    """Smooths out a series of data which might otherwise be choppy.

    Args:
        data: a line to smooth out
        smooth_weight: between 0 and 1, for 0 being no change and
            1 a flat line.  Higher values are smoother curves.

    Returns:
        a list of the same length as data, containing the smooth version.
    """
    prev = data[0]
    smoothed = []
    for point in data:
        smoothed.append(prev * smooth_weight + point * (1 - smooth_weight))
        prev = smoothed[-1]
    return smoothed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp", help="which experiment to run", type=str)
    args = parser.parse_args()
    func_map = {
        "one_a": experiment_one_a_10k_analysis,
        "one_b": experiment_one_b_10k_analysis,
        "one_c": experiment_one_c_10k_analysis,
        "one_d": experiment_one_d_10k_analysis,
        "one_e": experiment_one_e_10k_analysis,
        "two_a": experiment_one_a_30k_analysis,
        "two_b": experiment_one_b_30k_analysis,
        "two_c": experiment_one_c_30k_analysis,
        "two_d": experiment_one_d_30k_analysis,
        "two_e": experiment_one_e_30k_analysis,
    }

    func = func_map[args.exp]
    func()
