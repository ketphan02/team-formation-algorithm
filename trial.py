from typing import List
from matplotlib import pyplot as plt
from matplotlib.collections import PathCollection
from matplotlib.container import ErrorbarContainer
import seaborn as sns
from copy import deepcopy
from random import randint
import time

from mutate.local_max import mutate_local_max
from mutate.random import mutate_random_b, mutate_random_b_family
from generate import generate_random_ordered_priorities, generate_random_start_teamset
from visualize import visualize, visualize_multiple_times
from tree import Generation


def one_trail():
    Q = 50 + randint(0, 150)
    class_size = 100
    team_size = 4
    plots: List[ErrorbarContainer] = []
    
    time_random_b: List[float] = []
    time_random_b_family: List[float] = []
    time_local_max: List[float] = []
    times: List[float] = []
    cul_times: List[float] = []

    plt.subplots(figsize=(40, 10))
    priorities = generate_random_ordered_priorities(3, team_size)
    teamset = generate_random_start_teamset(class_size, team_size)

    visualize(mutate_random_b(deepcopy(teamset), b=3,
              priorities=priorities, num_buckets=10, Q=Q, times=time_random_b), 'Random B', plots)
    visualize(mutate_random_b_family(deepcopy(teamset), b=3,
              priorities=priorities, num_buckets=10, Q=Q, times=time_random_b_family), 'Random Family B', plots)
    visualize(mutate_local_max(deepcopy(teamset),
              priorities=priorities, num_buckets=10, Q=Q, times=time_local_max), 'Local Max', plots)

    for i in range(len(time_random_b)):
        times.append(time_random_b[i] + time_random_b_family[i] + time_local_max[i])
        cul_times.append((cul_times[-1] if len(cul_times) > 0 else 0) + times[-1])

    # set title
    plt.title(
        f'Graph of score of 1 trial run for Random B, Random Family B, and Local Max run in {Q} times', fontsize=20)
    plt.xlabel('Generation', fontsize=15)
    plt.ylabel('Average score of 1 generation', fontsize=15)
    plt.xlim(left=-1, right=Q + 1)
    plt.ylim(bottom=-0.01, top=1.01)
    plt.legend(loc='lower right', fontsize=15)
    plt.show()

    plt.subplots(figsize=(40, 10))
    # plot times and Q
    plt.plot(range(Q), time_random_b, label='Random B')
    plt.plot(range(Q), time_random_b_family, label='Random Family B')
    plt.plot(range(Q), time_local_max, label='Local Max')
    plt.plot(range(Q), times, label='Total TIME')
    plt.title(
        f'Graph of time of 1 trail run for Random B, Random Family B, and Local Max run in {Q} times', fontsize=20)
    plt.xlabel('Generation', fontsize=15)
    plt.ylabel('Time (in seconds)', fontsize=15)
    plt.xlim(left=-1, right=Q + 1)
    plt.legend(loc='lower right', fontsize=15)
    plt.show()

    plt.subplots(figsize=(40, 10))
    # plot cul_times and Q
    plt.plot(range(Q), cul_times, label='Total TIME')
    plt.title(
        f'Graph of cul_time of 1 trail run for Random B, Random Family B, and Local Max run in {Q} times', fontsize=20)
    plt.xlabel('Generation', fontsize=15)
    plt.ylabel('Cul_time (in seconds)', fontsize=15)
    plt.xlim(left=-1, right=Q + 1)
    plt.legend(loc='lower right', fontsize=15)
    plt.show()




def multiple_trials():
    Q = 100
    num_trials = 200
    plots: List[PathCollection] = []

    plt.subplots(figsize=(40, 10))
    generations_list_1: List[List[Generation]] = []
    generations_list_2: List[List[Generation]] = []
    generations_list_3: List[List[Generation]] = []

    time_mutate_random_b: List[float] = []
    time_mutate_random_b_family: List[float] = []
    time_mutate_local_max: List[float] = []
    times: List[float] = []
    cul_times: List[float] = []

    for i in range(num_trials):
        # Q = 50 + randint(0, 150)
        class_size = 100  # TODO: Vary this
        team_size = 4  # TODO: Vary this
        priorities = generate_random_ordered_priorities(4, team_size)
        teamset = generate_random_start_teamset(class_size, team_size)
        
        start_time = time.time()
        generations_list_1.append(mutate_random_b(
            deepcopy(teamset), b=3, priorities=priorities, num_buckets=10, Q=Q))
        time_mutate_random_b.append(time.time() - start_time)

        start_time = time.time()
        generations_list_2.append(mutate_random_b_family(
            deepcopy(teamset), b=3, priorities=priorities, num_buckets=10, Q=Q))
        time_mutate_random_b_family.append(time.time() - start_time)

        start_time = time.time()
        generations_list_3.append(mutate_local_max(
            deepcopy(teamset), priorities=priorities, num_buckets=10, Q=Q))
        time_mutate_local_max.append(time.time() - start_time)

        times.append(time_mutate_random_b[-1] + time_mutate_random_b_family[-1] + time_mutate_local_max[-1])
        cul_times.append((cul_times[-1] if len(cul_times) > 0 else 0) + times[-1])

        print(f'Done {i} in {times[-1]} seconds')

    plt.title(
        f'Graph of the average score of {num_trials} trials run for Random B, Random Family B, and Local Max run in {Q} times', fontsize=20)
    plt.xlabel('Generation', fontsize=15)
    plt.ylabel('Average score of 1 generation', fontsize=15)
    visualize_multiple_times(generations_list_1, 'Random B', plots)
    visualize_multiple_times(generations_list_2, 'Random B Family', plots)
    visualize_multiple_times(generations_list_3, 'Local Max', plots)
    plt.xlim(left=-1, right=Q + 1)
    plt.ylim(bottom=-0.01, top=1.01)
    plt.legend(loc='lower right')
    plt.show()

    plt.subplots(figsize=(40, 10))
    # plot times and Q
    plt.plot(range(num_trials), time_mutate_random_b, label='Time of Random B')
    plt.plot(range(num_trials), time_mutate_random_b_family, label='Time of Random Family B')
    plt.plot(range(num_trials), time_mutate_local_max, label='Time of Local Max')
    plt.plot(range(num_trials), times, label='Total time')
    plt.title(
        f'Graph of time of {num_trials} trials run for Random B, Random Family B, and Local Max run in {Q} times', fontsize=20)
    plt.xlabel('Generation', fontsize=15)
    plt.ylabel('Time (in seconds)', fontsize=15)
    plt.xlim(left=-1, right=num_trials + 1)
    plt.legend(loc='lower right', fontsize=15)
    plt.show()

    plt.subplots(figsize=(40, 10))
    # plot cul_times and Q
    plt.plot(range(num_trials), cul_times, label='Culmulated time')
    plt.title(
        f'Graph of Culmulated time of {num_trials} trials run for Random B, Random Family B, and Local Max run in {Q} times', fontsize=20)
    plt.xlabel('Generation', fontsize=15)
    plt.ylabel('Cul_time (in seconds)', fontsize=15)
    plt.xlim(left=-1, right=num_trials + 1)
    plt.legend(loc='lower right', fontsize=15)
    plt.show()



if __name__ == '__main__':
    sns.set_palette('Set2')
    plt.style.use('ggplot')

    one_trail()
    # multiple_trials()

# add label plz 🙏🏻

# create 2 graphs of time
# vary Q <- cant vary time in multiple trials since it is a fixed number of generations to plot the score
# one graph of time vs. Q (time per step)
# one graph of cummulative time vs. Q
