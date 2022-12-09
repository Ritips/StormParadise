import pygame


def draw_polygon():
    white = pygame.Color('white')
    w, h = screen.get_size()
    pos = center_x, center_y = w // 2, h // 2
    rad, s1 = 10, 70
    s2 = s1 * (2 - 3 ** 0.5) ** 0.5
    pygame.draw.circle(screen, white, pos, rad)
    height2 = (s1 ** 2 - s2 ** 2 / 4) ** 0.5

    pygame.draw.polygon(screen, white, [
        pos, (center_x - s2 / 2, center_y - height2), (center_x + s2 / 2, center_y - height2)
    ])

    s3 = s1 * 3 ** 0.5
    h3 = (s1 ** 2 - s3 ** 2) ** 0.5
    
    print(height2, s2, s1)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('pygame')
    size = width, height = 201, 201
    screen = pygame.display.set_mode(size)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_polygon()
        pygame.display.flip()

