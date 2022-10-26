from typing import List
import random
from score import TeamMember, TeamSet, Priority, Team

ATTRIBUTES = {
    1: ('gender', ['male', 'female', 'non-binary', 'other']),
    2: ('race', ['black', 'caucasian', 'asian', 'indigenous']),
    3: ('gpa', ['90+', '80+', '70+', 'other']),
    4: ('drinks', ['tea', 'coffee', 'bubble tea'])
}


def generate_random_person() -> TeamMember:
    attributes = {}
    for attr_id, (_, values) in ATTRIBUTES.items():
        attributes[attr_id] = random.choice(values)
    return TeamMember(attributes)


def generate_random_class(class_size: int) -> List[TeamMember]:
    return [generate_random_person() for _ in range(class_size)]


def generate_random_start_teamset(class_size: int, team_size: int) -> TeamSet:
    # TODO: handle when class size is not equally divisible by team size
    class_list = generate_random_class(class_size)
    num_teams = int(len(class_list) / team_size)
    teams = [Team(class_list[i * team_size: (i + 1) * team_size])
             for i in range(num_teams)]
    return TeamSet(teams)


def generate_random_priority(attribute: int, team_size: int) -> Priority:
    return Priority(
        Priority.TYPE_DIVERSIFY,
        attribute, Priority.MIN_OF,
        random.randint(1, team_size),
        random.choice(ATTRIBUTES[attribute][1])
    )


def generate_random_ordered_priorities(num_priorities: int, team_size: int) -> List[Priority]:
    chosen_priorities = [i for i in range(len(ATTRIBUTES))]
    random.shuffle(chosen_priorities)
    chosen_priorities = chosen_priorities[:num_priorities]
    return [generate_random_priority(i + 1, team_size) for i in chosen_priorities]
