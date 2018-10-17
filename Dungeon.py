from Room import Room
from Hallway import Hallway
from collections import deque
from random import randint
import queue

class Dungeon:
    def __init__(self):
        self.rooms = []
        self.hallways = []
        self.hallways_double = []
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
                    adjacent.add_neighbours(
                        [room]
                    )

                    cost = randint(1,10)
                    self.hallways.append(Hallway(room, adjacent, cost))
                    self.hallways_double.append(Hallway(room, adjacent, cost))
                    self.hallways_double.append(Hallway(adjacent, room, cost))

                if y + 1 < self.height:
                    room = next(room 
                        for room in self.rooms if room.x == x and room.y == y)

                    adjacent = next(room 
                        for room in self.rooms if room.x == x and room.y == y + 1)

                    room.add_neighbours(
                        [adjacent]
                    )
                    adjacent.add_neighbours(
                        [room]
                    )

                    cost = randint(1,10)
                    self.hallways.append(Hallway(room, adjacent, cost))
                    self.hallways_double.append(Hallway(room, adjacent, cost))
                    self.hallways_double.append(Hallway(adjacent, room, cost))


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
            # Iterate over visited rooms
            for room in visited:
                # Look for lowest cost edge ...
                for edge in hallways:
                    # ... that contains the visited room
                    # if the neighbour has not been visited yet,
                    # append it to the list to visit
                    # and save this edge
                    if edge.start == room and edge.end not in visited:
                        visited.append(edge.end)
                        edges.append(edge)
                        break
        
        return edges

    def dijkstra(self, startRoom, endRoom):
        inf = float('inf')

        unvisited = set(self.rooms)
        prev_rooms = {room: None for room in self.rooms}
        room_costs = {}
        for room in self.rooms:
                room_costs[room] = inf
        room_costs[startRoom] = 0

        while len(unvisited) != 0:
            current_room = min(unvisited,
                key=lambda room: room_costs[room])
            unvisited.remove(current_room)

            if room_costs[current_room] == inf:
                break

            for neighbour in current_room.adjacentRooms:
                hall = next(hall 
                    for hall in self.hallways_double if hall.start == current_room and hall.end == neighbour)
                alt_cost = hall.cost + room_costs[current_room]

                if room_costs[neighbour] > alt_cost:
                    room_costs[neighbour] = alt_cost
                    prev_rooms[neighbour] = current_room
        
        path, current_room = deque(), endRoom
        while prev_rooms[current_room] is not None:
            path.appendleft(current_room)
            current_room = prev_rooms[current_room]

        if path:
            path.appendleft(current_room)
        return path


