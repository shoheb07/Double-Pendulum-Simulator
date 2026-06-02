import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Pendulum Simulator")

clock = pygame.time.Clock()

# Pendulum Parameters
g = 9.81

m1 = 20
m2 = 20

L1 = 150
L2 = 150

a1 = np.pi / 2
a2 = np.pi / 2

a1_v = 0
a2_v = 0

origin_x = WIDTH // 2
origin_y = 150

trail = []

running = True

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Double Pendulum Equations
    num1 = -g * (2 * m1 + m2) * np.sin(a1)
    num2 = -m2 * g * np.sin(a1 - 2 * a2)
    num3 = -2 * np.sin(a1 - a2) * m2
    num4 = a2_v**2 * L2 + a1_v**2 * L1 * np.cos(a1 - a2)

    den = L1 * (
        2 * m1 + m2 -
        m2 * np.cos(2 * a1 - 2 * a2)
    )

    a1_a = (num1 + num2 + num3 * num4) / den

    num1 = 2 * np.sin(a1 - a2)

    num2 = (
        a1_v**2 * L1 * (m1 + m2)
        + g * (m1 + m2) * np.cos(a1)
        + a2_v**2 * L2 * m2 * np.cos(a1 - a2)
    )

    den = L2 * (
        2 * m1 + m2 -
        m2 * np.cos(2 * a1 - 2 * a2)
    )

    a2_a = (num1 * num2) / den

    a1_v += a1_a * 0.05
    a2_v += a2_a * 0.05

    a1 += a1_v
    a2 += a2_v

    # Coordinates
    x1 = origin_x + L1 * np.sin(a1)
    y1 = origin_y + L1 * np.cos(a1)

    x2 = x1 + L2 * np.sin(a2)
    y2 = y1 + L2 * np.cos(a2)

    trail.append((int(x2), int(y2)))

    if len(trail) > 500:
        trail.pop(0)

    # Draw Trail
    for point in trail:
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            point,
            2
        )

    # Draw Rods
    pygame.draw.line(
        screen,
        (0, 0, 0),
        (origin_x, origin_y),
        (x1, y1),
        3
    )

    pygame.draw.line(
        screen,
        (0, 0, 0),
        (x1, y1),
        (x2, y2),
        3
    )

    # Draw Masses
    pygame.draw.circle(
        screen,
        (0, 0, 255),
        (int(x1), int(y1)),
        15
    )

    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (int(x2), int(y2)),
        15
    )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
