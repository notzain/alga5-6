from Room import Room
from Hallway import Hallway

class Dungeon:
    def __init__(self):
        self.rooms = []
        self.hallways = []

    def generate(self, width, height):
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


        

    def bfs(self, startRoom):
        visited = set()
        queue = [startRoom]

        while queue:
            room = queue.pop()
            visited.add(room)
            room.isRoute = True

            for adjacent in room.adjacentRooms:
                if not adjacent in visited and not adjacent in queue:
                    queue.append(adjacent)

        return visited
    
