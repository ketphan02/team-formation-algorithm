import random
import time
from copy import deepcopy
from heapq import heappush, nlargest
from typing import List
from tree import Child, Generation
from score import TeamSet, Team, Priority


def mutate_random(teamset: TeamSet) -> TeamSet:
    num1: int = random.randint(0, len(teamset) - 1)
    num2: int = num1
    while num2 == num1:
        num2 = random.randint(0, len(teamset) - 1)

    team1: Team = teamset.teams[num1]
    team2: Team = teamset.teams[num2]

    i = random.randint(0, len(team1) - 1)
    j = random.randint(0, len(team2) - 1)
    teamset.teams[num1].members[i], teamset.teams[num2].members[j] = teamset.teams[num2].members[j], teamset.teams[num1].members[i]
    return teamset


def mutate_random_b(teamset: TeamSet, b: int, priorities: List[Priority], num_buckets: int, Q: int, times: List[float] = None) -> List[Generation]:
    generations = []

    m: int = 3  # keep m nodes

    tree = [Child(teamset, priorities, num_buckets)]  # the tree
    generations.append(Generation(tree, priorities))
    for _ in range(Q):
        if times is not None:
            start_time = time.time()

        children = []
        for node in tree:
            for _ in range(b):
                # randomly choose 2 teams and swap 2 people in the 2 teams
                generated_team = mutate_random(node.teamset)
                heappush(children, Child(
                    generated_team, priorities, num_buckets))

        tree = nlargest(m, children)
        generations.append(Generation(tree, priorities))

        if times is not None:
            times.append(time.time() - start_time)

    return generations


def mutate_random_b_family(teamset: TeamSet, b: int, priorities: List[Priority], num_buckets: int, Q: int, times: List[float] = None) -> List[Generation]:
    generations = []

    m: int = 3  # keep m nodes

    tree = [Child(teamset, priorities, num_buckets)]  # the tree
    generations.append(Generation(tree, priorities))
    for _ in range(Q):
        if times is not None:
            start_time = time.time()

        children = deepcopy(tree)
        for node in tree:
            for _ in range(b):
                # randomly choose 2 teams and swap 2 people in the 2 teams
                generated_team = mutate_random(node.teamset)
                heappush(children, Child(
                    generated_team, priorities, num_buckets))

        tree = nlargest(m, children)
        generations.append(Generation(tree, priorities))

        if times is not None:
            times.append(time.time() - start_time)

    return generations
