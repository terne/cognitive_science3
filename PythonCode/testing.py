import sys
import pygame as pg


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    # A pygame.Rect to define the area.
    area = pg.Rect(100, 150, 200, 124)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button.
                    # Check if the rect collides with the mouse pos.
                    if area.collidepoint(event.pos):
                        print('Area clicked.')
                        print(event.pos)

        screen.fill((30, 30, 30))
        pg.draw.rect(screen, (100, 200, 70), area)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
