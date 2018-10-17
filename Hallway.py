from random import randint
class Hallway:
    def __init__(self, start, end, cost):
        self.start = start
        self.end = end
        self.cost = cost

        self.isCollapsed = False

    def __repr__(self):
        return "({},{}) : {}".format(
            (self.start.x, self.start.y),
            (self.end.x, self.end.y),
            self.cost)
