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


if __name__ == '__main__':
    dungeon = Dungeon()

    rooms_x = int(input("Room width: "))
    rooms_y = int(input("Room height: "))

    margin = rooms_x * 10
    room_width = (800 / rooms_x) - (margin)
    room_height = (800 / rooms_y) - (margin)
    room_size = min([200, room_width, room_height])

    dungeon.generate(rooms_x, rooms_y)

    dungeon.rooms[0].isStart = True
    dungeon.rooms[-1].isEnd = True

    print(dungeon.rooms[2])
    dungeon.bfs(dungeon.rooms[2])

    print(len(dungeon.hallways))
    for hallway in dungeon.hallways:
        start_left = hallway.start.x * (room_width + margin) + margin/2
        start_top = hallway.start.y * (room_height + margin) + margin/2
        start_line = (start_left + room_size/2, start_top + room_size/2)

        end_left = hallway.end.x * (room_width + margin) + margin/2
        end_top = hallway.end.y * (room_height + margin) + margin/2
        end_line = (end_left + room_size/2, end_top + room_size/2)

        pygame.draw.line(gameDisplay, (128, 128, 128), 
            start_line,
            end_line,
            5
        )

        text = font.render(str(hallway.cost), True, white)
        textrect = text.get_rect()
        if start_left == end_left:
            textrect.centerx = start_line[0] + end_line[0]/2
            textrect.centery = start_line[1]
        else:
            textrect.centerx = start_line[1] + end_line[1]/2
            textrect.centery = start_line[0]

        gameDisplay.blit(text, textrect)


    for room in dungeon.rooms:
        color = None
        if room.isVisited:
            color = red
        elif room.isEnd:
            color = green
        elif room.isStart:
            color = blue
        elif room.isRoute:
            color = red
        else:
            color = white

        #pygame.draw.rect(gameDisplay, color, 
        #    (room.x * (room_width + margin) + margin/2,
        #     room.y * (room_height + margin) + margin/2,
        #     room_size,
        #     room_size))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()

