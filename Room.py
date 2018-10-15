from collections import deque

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.isStart = False
        self.isEnd = False
        self.isVisited = False
        self.isPlayer = False

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

    def bfs(self, endRoom):
        visited = {self: None}
        queue = deque([self])

        while queue:
            room = queue.popleft()
            if room == endRoom:
                path = []
                while room is not None:
                    path.append(room)
                    room = visited[room]
                return path[::-1]

            for adjacent in room.adjacentRooms:
                if not adjacent in visited:
                    visited[adjacent] = room
                    queue.append(adjacent)

        return None

    def isCyclic(self):
        visited = set()
        queue = [self]

        while queue:
            room = queue.pop()
            visited.add(room)
            room.isRoute = True

            for adjacent in room.adjacentRooms:
                if not adjacent in visited and not adjacent in queue:
                    queue.append(adjacent)
                else:
                    return True
                
        return False