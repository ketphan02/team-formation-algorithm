import time
from copy import deepcopy
from heapq import heappush, nlargest
from typing import List
from score import Priority, TeamSet, team_score
from tree import Child, Generation


def generate_all_possible_mutations(teamset: TeamSet, x: int, y: int):
    teamX = teamset.teams[x]
    teamY = teamset.teams[y]
    team_x, team_y = teamX[:], teamY[:]
    team_x[x], team_y[y] = team_y[y], team_x[x]
    return team_x, team_y


def get_lowest_team_scores(teamset: TeamSet, priorities: List[Priority]):
    min_est = float('inf')
    min_est_loc = -1
    min_er = float('inf')
    min_er_loc = -1
    for i, team in enumerate(teamset.teams):
        s = team_score(team, priorities)
        if (min_est > s):
            min_est = s
            min_est_loc = i
        elif (min_er >= s):
            min_er = s
            min_er_loc = i
    return min_est_loc, min_er_loc


def mutate_local_max(teamset: TeamSet, priorities: List[Priority], num_buckets: int, Q: int, times: List[float] = None) -> List[Generation]:
    generations = []

    m = 3  # keep m branches

    tree = [Child(teamset, priorities, num_buckets)]
    generations.append(Generation(tree, priorities))
    for _ in range(Q):
        if times is not None:
            start_time = time.time()

        children = deepcopy(tree)
        for node in tree:
            x, y = get_lowest_team_scores(node.teamset, priorities)
            for i in range(len(node.teamset.teams[x])):
                for j in range(len(node.teamset.teams[y])):
                    new_node = deepcopy(node)
                    new_node.teamset.teams[x].members[i], new_node.teamset.teams[y].members[j] = \
                        new_node.teamset.teams[y].members[j], new_node.teamset.teams[x].members[i]
                    heappush(children, Child(
                        new_node.teamset, priorities, num_buckets))

        tree = nlargest(m, children)
        generations.append(Generation(tree, priorities))

        if times is not None:
            times.append(time.time() - start_time)

    return generations
