from Room import Room
from Dungeon import Dungeon
import pygame

pygame.init()

font = pygame.font.Font(None, 24)

white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((800, 800))
gameDisplay.fill(black)

room_width = None
room_height = None
room_size = None
margin = None

currentRoom = None
startRoom = None
endRoom = None
shortestPath = []

def render(dungeon):
    gameDisplay.fill(black)
    for hallway in dungeon.hallways:
        start_x = hallway.start.x * (room_width + margin) + margin/2
        start_y = hallway.start.y * (room_height + margin) + margin/2
        start_line = (start_x + room_size/2, start_y + room_size/2)

        end_x = hallway.end.x * (room_width + margin) + margin/2
        end_y = hallway.end.y * (room_height + margin) + margin/2
        end_line = (end_x + room_size/2, end_y + room_size/2)

        pygame.draw.line(gameDisplay, 
            red if hallway.isCollapsed else white,
            start_line,
            end_line,
            5
        )

        text = font.render(str(hallway.cost), True, white)
        textrect = text.get_rect()
        # horizontal line
        if start_x == end_x:
            textrect.centerx = start_line[0] + 10
            textrect.centery = (start_line[1] + end_line[1])/2
        # vertical line
        else:
            textrect.centerx = (start_line[0] + end_line[0])/2
            textrect.centery = start_line[1] + 10

        gameDisplay.blit(text, textrect)


    for room in dungeon.rooms:
        color = None
        if room.isEnd:
            color = green
        elif room.isStart:
            color = blue
        elif room.isPlayer:
            color = red
        elif room.isRoute:
            color = red
        else:
            color = white

        pygame.draw.rect(gameDisplay, color, 
            (room.x * (room_width + margin) + margin/2,
             room.y * (room_height + margin) + margin/2,
             room_size,
             room_size))

def user_input(dungeon):
    global currentRoom
    global startRoom
    global endRoom
    global shortestPath

    print("up|down|left|right")
    print("talisman")
    print("")

    choise = input()

    currentRoom.isPlayer = False
    if choise == "up":
        if currentRoom.y - 1 >= 0:
            currentRoom = dungeon.getRoom(currentRoom.x, currentRoom.y - 1)
    elif choise == "down":
        if currentRoom.y + 1 < dungeon.height:
            currentRoom = dungeon.getRoom(currentRoom.x, currentRoom.y + 1)
    elif choise == "left":
        if currentRoom.x - 1 >= 0:
            currentRoom = dungeon.getRoom(currentRoom.x - 1, currentRoom.y)
    elif choise == "right":
        if currentRoom.x + 1 < dungeon.width:
            currentRoom = dungeon.getRoom(currentRoom.x + 1, currentRoom.y)
    elif choise == "talisman":
        rooms = dungeon.bfs(currentRoom, endRoom)
        for room in rooms:
            print(room)
        print("{} steps left till the exit!".format(len(rooms) - 1))
    elif choise == "boom":
        mst = dungeon.mst()
        collapsedHalls = set(dungeon.hallways).difference(set(mst))
        for hall in collapsedHalls:
            hall.isCollapsed = True
    elif choise == "dijkstra":
        shortestPath = dungeon.dijkstra(startRoom, endRoom)
        for room in shortestPath:
            room.isRoute = True
    elif choise == "reset":
        for room in dungeon.rooms:
            room.isRoute = False
        dungeon.hallways.clear()
        dungeon.hallways_double.clear()
        dungeon.generateHallways()
    elif choise == "hard":
        for room in dungeon.rooms:
            room.isRoute = False

        for i in range(len(shortestPath) - 1):
            hall = next((hall
                for hall in dungeon.hallways if hall.start == shortestPath[i] and hall.end == shortestPath[i+1]), None)
            if hall is not None:
                hall.cost = 10
            hall = next((hall
                for hall in dungeon.hallways if hall.start == shortestPath[i + 1] and hall.end == shortestPath[i]), None)
            if hall is not None:
                hall.cost = 10
            hall = next((hall
                for hall in dungeon.hallways_double if hall.start == shortestPath[i] and hall.end == shortestPath[i+1]), None)
            if hall is not None:
                hall.cost = 10
            hall = next((hall
                for hall in dungeon.hallways_double if hall.start == shortestPath[i + 1] and hall.end == shortestPath[i]), None)
            if hall is not None:
                hall.cost = 10

    currentRoom.isPlayer = True

if __name__ == '__main__':
    dungeon = Dungeon()

    rooms_x = int(input("Room width: "))
    rooms_y = int(input("Room height: "))

    margin = rooms_x * 10
    room_width = (800 / rooms_x) - (margin)
    room_height = (800 / rooms_y) - (margin)
    room_size = min([200, room_width, room_height])

    (start, end) = dungeon.generate(rooms_x, rooms_y)
    start.isStart = True
    end.isEnd = True

    currentRoom = start
    startRoom = start
    endRoom = end

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        render(dungeon)
        pygame.display.update()

        user_input(dungeon)


