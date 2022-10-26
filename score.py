from typing import List


class PriorityException(Exception):
    pass


class UnImplementedException(Exception):
    pass


class TeamMember:
    attributes: dict 
    """
    {
        attribute_1_id: attribute_1_value,
        attribute_2_id: attribute_2_value,
        ...
        attribute_n_id: attribute_n_value,
    }
    """

    def __init__(self, attributes: dict):
        self.attributes = attributes

    def get_attribute_value(self, attribute_id: int) -> str:
        # TODO: try-except
        return self.attributes[attribute_id]


class Team:
    members: List[TeamMember] 

    def __init__(self, members=None):
        self.members = members

    def __len__(self):
        return len(self.members)


class Priority:
    # Represents the following
    # e.g. "diversify gender with min of 2 females"
    #       (p_type) (attribute) with (constraint) (k) (x)
    #       (diversify) (gender) with (min of) (2) (female)
    TYPE_DIVERSIFY = 'diversify'
    TYPE_CONCENTRATE = 'concentrate'

    MIN_OF = 'min_of'
    MAX_OF = 'max_of'

    p_type: str 
    constraint: str 
    attribute: int   # number representing attribute
    limit: int   # number representing k
    value: str   # string representing x

    def __init__(self, p_type: str, attribute: int, constraint: str, limit: int, value: str):
        self.p_type = p_type
        self.attribute = attribute
        self.constraint = constraint
        self.limit = limit
        self.value = value
        self.validate()

    def validate(self):
        # TODO: finish
        pass

    def satisfied_by(self, team: Team) -> bool:
        if self.p_type == Priority.TYPE_DIVERSIFY and self.constraint == Priority.MIN_OF:
            count = 0
            for member in team.members:
                # TODO: try-except
                if member.get_attribute_value(self.attribute) == self.value:
                    count += 1
            return count == 0 or count >= self.limit

        # TODO: add more cases
        return False

    def satisfied_detail(self, team: Team) -> int:
        if self.p_type == Priority.TYPE_DIVERSIFY and self.constraint == Priority.MIN_OF:
            count = 0
            for member in team.members:
                if member.get_attribute_value(self.attribute) == self.value:
                    count += 1
            return count
        else:
            raise UnImplementedException('Unhandle exception')


class TeamSet:
    teams: List[Team] 

    def __init__(self, teams: List[Team]):
        self.teams = teams

    def __len__(self):
        return len(self.teams)

    def abundance_score(self, priorities: List[Priority], num_buckets: int) -> List[int]:
        multipliers: List[int] = TeamSet.get_multipliers(
            priorities, num_buckets)
        max_score = self.get_max_score(multipliers, num_buckets)
        raw_score: List[List[int]] = [
            self.raw_satisfaction(pri) for pri in priorities]
        abundance_arr = []
        for i, pri in enumerate(priorities):
            abundance_arr.append(sum(
                [raw_score[i][j] - pri.limit if raw_score[i][j] != 0 else 0 for j in range(len(raw_score[i]))]))

        return sum([abundance_val * multiplier for abundance_val, multiplier in zip(abundance_arr, multipliers)]) / max_score

    def score(self, priorities: List[Priority], num_buckets: int) -> float:
        multipliers: List[int] = TeamSet.get_multipliers(
            priorities, num_buckets)
        satisfaction_values: List[int] = [
            self.get_satisfaction_value(pri, num_buckets) for pri in priorities]

        raw_score = sum([multiplier * value for multiplier,
                        value in zip(multipliers, satisfaction_values)])
        max_score = self.get_max_score(multipliers, num_buckets)

        # TODO: check normalization approach
        return raw_score / max_score

    def get_num_satisfied_team(self, priorities: List[Priority]) -> int:
        cnt = 0
        for pri in priorities:
            cnt += self.satisfaction_ratio(pri) == 1
        return cnt

    def get_max_score(self, multipliers: List[int], num_buckets: int) -> int:
        max_score = sum([m * (num_buckets - 1) for m in multipliers])
        return max_score

    def get_satisfaction_value(self, priority: Priority, num_buckets: int) -> int:
        satisfaction_ratio = self.satisfaction_ratio(priority)
        if satisfaction_ratio == 1:
            return num_buckets - 1

        gap = 1 / (num_buckets - 1)
        curr_bucket = 0
        low_bound = 0
        while curr_bucket < num_buckets - 1:
            upper_bound = low_bound + gap  # 0.2
            if low_bound <= satisfaction_ratio < upper_bound:
                return curr_bucket
            curr_bucket += 1
            low_bound = upper_bound

        print(satisfaction_ratio)

    def satisfaction_ratio(self, priority: Priority) -> float:
        # returns value in [0, 1] IMPORTANT that it does this, satisfaction value relies on it
        count = 0
        for team in self.teams:
            count += priority.satisfied_by(team)
        return count / len(self.teams)

    def raw_satisfaction(self, priority: Priority) -> List[int]:
        raw_satis = []
        for team in self.teams:
            raw_satis.append(priority.satisfied_detail(team))
        return raw_satis

    @staticmethod
    def get_multipliers(priorities: List[Priority], num_buckets: int) -> List[int]:
        # with 2 buckets and [C1, C2, C3], returns [4, 2, 1]
        multipliers = [num_buckets ** (n - 1)
                       for n in range(1, len(priorities) + 1)]
        return multipliers[::-1]

def team_score(team: Team, priorities: List[Priority]) -> float:
    satisfies: List[bool] = []
    for priority in priorities:
        satisfies.append(priority.satisfied_by(team))
    multiplier = TeamSet.get_multipliers(priorities, 2)
    NORMALIZED_CONST = sum(multiplier)
    return sum([s * m for s, m in zip(satisfies, multiplier)]) / NORMALIZED_CONST