import math, sys, random

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk import Vec2d
import pymunk.pygame_util


def draw_collision(arbiter, space, data):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)

        p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
        pygame.draw.circle(data["surface"], THECOLORS["black"], p, r, 1)


def main():
    global contact
    global shape_to_remove

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # disable the build in debug draw of collision point since we use our own code.
    draw_options.flags = draw_options.flags ^ pymunk.pygame_util.DrawOptions.DRAW_COLLISION_POINTS
    ## Balls
    balls = []

    ### walls
    static_lines = [pymunk.Segment(space.static_body, (10.0, 400.0), (150.0, 350.0), 5)]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

    ticks_to_next_ball = 1

    ch = space.add_collision_handler(0, 0)
    ch.data["surface"] = screen
    ch.post_solve = draw_collision

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "contact_with_friction.png")

        ticks_to_next_ball -= 1
        if ticks_to_next_ball == 0:
            ticks_to_next_ball = 100
            mass = 1
            radius = 15
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            # x = random.randint(50, 200)
            body.position = 30, 413
            shape = pymunk.Circle(body, radius, (0, 0))
            shape.friction = 0.5
            space.add(body, shape)
            balls.append(shape)

        ### Clear screen
        screen.fill(THECOLORS["white"])

        ### Draw stuff
        space.debug_draw(draw_options)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        # Make body for pulley

        # Update physics

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("Rube Goldberg")



if __name__ == '__main__':
    sys.exit(main())