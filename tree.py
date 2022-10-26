# Child node
from typing import List

from score import TeamSet, Priority


class Child:
    score: int
    teamset: TeamSet

    def __init__(self, teamset: TeamSet, prorities: List[Priority], num_buckets: int):
        self.teamset = teamset
        self.score = self.teamset.score(prorities, num_buckets)

    def __len__(self):
        return len(self.teamset)

    def __lt__(self, comp: TeamSet):
        return self.score < comp.score

# set of child nodes that are kept


class Generation:
    Min: float = float('inf')
    min_child: Child
    Max: float = float('-inf')
    max_child: Child
    Avg: float
    num_satisfied: int
    children: List[Child]

    def __init__(self, children: List[Child], prorities: List[Priority]):
        self.children = children
        self.Avg = self.get_score_average()
        self.get_score_max_min()
        self.get_num_statisfied(prorities)

    def get_score_average(self):
        return sum([child.score for child in self.children]) / len(self.children)

    def get_score_max_min(self):
        for child in self.children:
            if (self.Min > child.score):
                self.Min = child.score
                self.min_child = child
            if (self.Max < child.score):
                self.Max = child.score
                self.max_child = child

    def get_num_statisfied(self, prorities: List[Priority]):
        self.num_satisfied = self.max_child.teamset.get_num_satisfied_team(prorities)
