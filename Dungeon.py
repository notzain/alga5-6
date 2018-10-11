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

    def generate(self, width, height):
        self.width = width
        self.height = height

        self.generateRooms()
        self.generateHallways()
        return self.generateExits()

    def generateRooms(self):
        for y in range(self.height):
            for x in range(self.width):
                self.rooms.append(Room(x, y))

    def generateHallways(self):
        for x in range(self.width):
            for y in range(self.height):
                if x + 1 < self.width:
                    room = next(room 
                        for room in self.rooms if room.x == x and room.y == y)

                    adjacent = next(room 
                        for room in self.rooms if room.x == x + 1 and room.y == y)
                    
                    room.add_neighbours(
                        [adjacent]
                    )

                    self.hallways.append(Hallway(room, adjacent))

                if y + 1 < self.height:
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
        return startRoom.bfs(endRoom)

    def mst(self):
        edges = []
        visited = []
        visited.append(self.rooms[0])

        hallways = list(self.hallways)
        hallways.sort(key=lambda hall: hall.cost)

        while len(visited) != len(self.rooms):
            for room in visited:
                for edge in hallways:
                    if edge.start == room and edge.end not in visited:
                        visited.append(edge.end)
                        edges.append(edge)
                        break
        
        return edges