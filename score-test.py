import copy
import itertools
import random
from typing import List

from matplotlib import pyplot as plt

from score import Priority, Team, TeamMember, PriorityException, TeamSet

ATTRIBUTES = {
    1: ('gender', ['male', 'female', 'non-binary', 'other']),
    2: ('race', ['black', 'caucasian', 'asian', 'indigenous']),
    3: ('gpa', ['90+', '80+', '70+', 'other']),
    4: ('drinks', ['tea', 'coffee', 'bubble tea'])
}

NUM_STUDENTS = 20
NUM_TEAMS = 5
TEAM_SIZE = int(NUM_STUDENTS / NUM_TEAMS)
NUM_BUCKETS = 12


def generate_bool_combinations(size: int) -> List:
    options = [False, True]
    return [list(i) for i in itertools.product(options, repeat=size)]


def test_with_priority_combination(priorities: List[Priority], satisfies: List[bool]):
    num_teams_satisfying = []
    scores = []

    for i in range(0, NUM_TEAMS + 1):
        # make a teamset where "i" teams satisfy constraint and other teams satisfy none of the constraints
        pass_team = create_dummy_team(priorities, TEAM_SIZE, satisfies)
        fail_team = create_dummy_team(priorities, TEAM_SIZE, [
                                      [False] for _ in range(len(priorities))])

        pass_teams = [copy.deepcopy(pass_team) for _ in range(0, i)]
        fail_teams = [copy.deepcopy(fail_team)
                      for _ in range(0, NUM_TEAMS - i)]
        teams = pass_teams + fail_teams
        team_set = TeamSet(teams)

        num_teams_satisfying.append(i)
        scores.append(team_set.score(priorities, num_buckets=NUM_BUCKETS))

    # TODO: plot graph
    print(num_teams_satisfying)
    print(scores)
    plt.plot(num_teams_satisfying, scores)


def create_dummy_team(priorities: List[Priority], num_members: int, satisfies: List[bool]) -> Team:
    # 0 or >=2 members female, 0 or >=3 members asian => [ [true, true], [true, true], [false, true], [false, false] ]
    # 0 or >=2 members female, 0 or >=3 members asian => [ [false, true], [false, true], [false, true], [false, false] ]
    default = [False for _ in range(0, len(satisfies))]
    member_satisfaction_list = [default[:] for _ in range(0, num_members)]
    for pri_index, priority in enumerate(priorities):
        if satisfies[pri_index]:
            is_empty_case = random.random() < 0.2
            limit = 0 if is_empty_case else priority.limit
        else:
            # priority.limit is >= 2 by definition
            limit = random.randint(1, priority.limit - 1)

        count = 0
        for member in member_satisfaction_list:
            member[pri_index] = True if count < limit else False
            count += 1

    members = []
    for member_satisfaction in member_satisfaction_list:
        members.append(create_dummy_student(priorities, member_satisfaction))
    return Team(members)


def create_dummy_student(priorities: List[Priority], satisfies: List[bool]) -> TeamMember:
    if len(priorities) != len(satisfies):
        raise PriorityException('Should be the same length.')

    attribute_dict = {}
    for attr_id, (_, values) in ATTRIBUTES.items():
        attribute_dict[attr_id] = random.choice(values)

    for priority, should_satisfy in zip(priorities, satisfies):
        if should_satisfy:
            attribute_dict[priority.attribute] = priority.value
        else:
            _, raw_values = ATTRIBUTES.get(priority.attribute)
            attr_values = raw_values[:]
            attr_values.remove(priority.value)
            attribute_dict[priority.attribute] = random.choice(attr_values)

    team_member = TeamMember(attribute_dict)
    return team_member


if __name__ == '__main__':
    gender_priority = Priority(
        Priority.TYPE_DIVERSIFY, 1, Priority.MIN_OF, 2, 'female')
    race_priority = Priority(Priority.TYPE_DIVERSIFY,
                             2, Priority.MIN_OF, 3, 'asian')
    gpa_priority = Priority(Priority.TYPE_DIVERSIFY, 3,
                            Priority.MIN_OF, 2, '80+')
    drinks_priority = Priority(
        Priority.TYPE_DIVERSIFY, 4, Priority.MIN_OF, 3, 'coffee')

    # priorities = [gender_priority, race_priority, gpa_priority, drinks_priority]

    # TODO: add legend to displayed graphs that articulates which combination of constraints are being satisfied
    for combination in generate_bool_combinations(1):
        test_with_priority_combination([gender_priority], combination)
    plt.show()

    for combination in generate_bool_combinations(2):
        test_with_priority_combination(
            [gender_priority, race_priority], combination)
    plt.show()

    for combination in generate_bool_combinations(3):
        test_with_priority_combination(
            [gender_priority, race_priority, gpa_priority], combination)
    plt.show()

    for combination in generate_bool_combinations(4):
        test_with_priority_combination(
            [gender_priority, race_priority, gpa_priority, drinks_priority], combination)
    plt.show()
