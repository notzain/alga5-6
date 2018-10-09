class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.isStart = False
        self.isEnd = False
        self.isVisited = False

        self.isRoute = False

        self.adjacentRooms = set()

    def __repr__(self):
        return "({},{}) : ({})".format(
           self.x,
           self.y,
           ','.join(["({},{})".format(room.x, room.y) for room in self.adjacentRooms])
        )

    def add_neighbours(self, rooms):
        for room in rooms:
            self.adjacentRooms.add(room)


