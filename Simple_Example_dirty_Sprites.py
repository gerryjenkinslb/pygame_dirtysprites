import pygame
from pygame.locals import KEYDOWN

# dirty sprite example

#   width and height of window
win_size = (900, 600)  # you may need to adjust this for windows, linux


class Face(pygame.sprite.DirtySprite):  # our DirtySprite class

    def __init__(self, center, dx, dy):
        pygame.sprite.DirtySprite.__init__(self) # always need to have this call to super constructor

        self.image = pygame.image.load("emoji_face.png")
        self.rect = self.image.get_rect(center=center)  # rect controls target place when copied to screen
        self.dx, self.dy = dx, dy # change to move every frame

    def update(self):  # make changes for this time tick
        x, y = self.rect.center  # move current center
        x = (x + self.dx) % win_size[0]  # move by dx,dy and wrap modulo window size
        y = (y + self.dy) % win_size[1]
        self.rect.center = (x, y)  # changes where sprite will be copied to buffer
        self.dirty = 1  # force redraw from image, since we moved the sprite rect


def is_exit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == KEYDOWN:
                return True
    return False


def main():
    # Initialize Everything
    pygame.init()
    draw_buffer = pygame.display.set_mode(win_size)
    pygame.display.set_caption('Balls Ahoy')

    # Create The Background used to restore sprite previous location
    background = pygame.Surface(draw_buffer.get_size()) # make a surface the size of display area
    background.blit(pygame.image.load("water.png"), (0, 0))  # draw image into sprite surface

    # Prepare Game Objects
    clock = pygame.time.Clock()  # Clock is object that will allow fairly exact frame rate

    cx, cy = win_size[0]//2, win_size[1]//2  # figure out middle of display area

    s1 = Face((cx+100, cy+100), 10, -5)   # add face 1 100 down and to right from center 10 -5 is movement
    s2 = Face((cx-100, cy-100), -16, -15) # add face 2 100 left and to up from center -16 -15 is movement

    my_sprites = pygame.sprite.LayeredDirty()  # holds sprites to be drawn
    my_sprites.add(s1, s2)  # add both to our group
    my_sprites.clear(draw_buffer, background) # copy background to screen

    # Main Loop:

    while True:
        if is_exit_event():
            break  # break out of loop and exit

        my_sprites.update()  # call update on all sprites

        # for each dirty sprint, erase previous rect with background copy
        # and then copy new sprite to buffer
        rects = my_sprites.draw(draw_buffer)

        clock.tick(18)  # times per second, delays for the time till next frame point
        pygame.display.update(rects)  # copy rects from buffer to screen

    pygame.quit()


if __name__ == '__main__':
    main()
