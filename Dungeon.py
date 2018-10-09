from Room import Room
from Hallway import Hallway
from collections import deque
from random import randint

class Dungeon:
    def __init__(self):
        self.rooms = []
        self.hallways = []
        self.width = 0
        self.height = 0

    def generateRooms(self, width, height):
        self.width = width
        self.height = height

        for y in range(height):
            for x in range(width):
                self.rooms.append(Room(x, y))

        for x in range(width):
            for y in range(height):
                if x + 1 < width:
                    room = next(room 
                        for room in self.rooms if room.x == x and room.y == y)

                    adjacent = next(room 
                        for room in self.rooms if room.x == x + 1 and room.y == y)
                    
                    room.add_neighbours(
                        [adjacent]
                    )

                    self.hallways.append(Hallway(room, adjacent))

                if y + 1 < height:
                    room = next(room 
                        for room in self.rooms if room.x == x and room.y == y)

                    adjacent = next(room 
                        for room in self.rooms if room.x == x and room.y == y + 1)

                    room.add_neighbours(
                        [adjacent]
                    )

                    self.hallways.append(Hallway(room, adjacent))

                if x - 1 >= 0:
                    room = next(room 
                        for room in self.rooms if room.x == x and room.y == y)

                    adjacent = next(room 
                        for room in self.rooms if room.x == x - 1 and room.y == y)
                    
                    room.add_neighbours(
                        [adjacent]
                    )

                if y - 1 >= 0:
                    room = next(room 
                        for room in self.rooms if room.x == x and room.y == y)

                    adjacent = next(room 
                        for room in self.rooms if room.x == x  and room.y == y - 1)
                    
                    room.add_neighbours(
                        [adjacent]
                    )

    def getRoom(self, x, y):
        return next(room
            for room in self.rooms if room.x == x and room.y == y)

    def generateExits(self):
        startx, starty = randint(0, self.width - 1), randint(0, self.height - 1)
        endx, endy = randint(0, self.width - 1), randint(0, self.height - 1)

        startRoom = next(room
            for room in self.rooms if room.x == startx and room.y == starty)

        endRoom = next(room
            for room in self.rooms if room.x == endx and room.y == endy)

        return (startRoom, endRoom)


    def bfs(self, startRoom, endRoom):
        visited = {startRoom: None}
        queue = deque([startRoom])

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
    
