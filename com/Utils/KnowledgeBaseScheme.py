from collections import namedtuple

fact = namedtuple('fact', 'relation x y')


class Fact:
    def __init__(self, relation: str, x: str, y: str = None):
        self.relation = relation
        self.x = x
        self.y = y

    def __str__(self):
        if self.y is not None:
            return self.relation + '(' + self.x + ', ' + self.y + ')'
        else:
            return self.relation + '(' + self.x + ')'


class Rule:
    def __init__(self):
