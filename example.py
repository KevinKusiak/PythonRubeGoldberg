"""A basic playground. Most interesting function is draw a shape, basically
move the mouse as you want and pymunk will approximate a Poly shape from the
drawing.
"""
__docformat__ = "reStructuredText"

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk as pm
from pymunk import Vec2d
import pymunk.util as u
import pymunk.pygame_util

# TODO: Clean up code

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

size_factor = .5;


class PhysicsDemo:
   def flipyv(self, v):
       return int(v.x), int(-v.y + self.h)

   def __init__(self):
       self.running = True
       ### Init pygame and create screen
       pygame.init()
       self.w, self.h = 800, 800
       self.screen = pygame.display.set_mode((self.w, self.h))
       self.clock = pygame.time.Clock()

       ### Init pymunk and create space
       self.space = pm.Space()
       self.space.gravity = (0.0, -990.0)

       draw_options = pm.pygame_util.DrawOptions(self.screen)
       # disable the build in debug draw of collision point since we use our own code.
       draw_options.flags = draw_options.flags ^ pymunk.pygame_util.DrawOptions.DRAW_COLLISION_POINTS

       lines = self.add_L_pulley(self.space)

       ### Walls
       self.walls = []
       self.create_wall_segments([(100, 50), (500, 50)])

       ## Balls
       # balls = [createBall(space, (100,300))]
       self.balls = []

       ### Polys
       self.polys = []
       h = 6

       lines = self.add_L_pulley(self.space)
       lines2 = self.add_L(self.space)
       for y in range(1, h):
           # for x in range(1, y):
           x = 0
           s = 10  # the reason for the bottom line is the when we divide 50/4 it truncates, but for 50/5 it is a good number
           p = Vec2d( (y * s * 1.5 ) + (20/y)/5, 25) + Vec2d(250, 20 + 40/y)
           self.polys.append(self.create_box(p, size=10/y, mass=5))

       p = Vec2d((100 * 2) -40 , 20) + Vec2d(80, 80)
       self.polys.append(self.create_box(p, size=12, mass=5))

       p1 = Vec2d((100 * 2)-40, 20+50) + Vec2d(80, 80 +40)
       self.polys.append(self.create_box(p1, size=12, mass=5))

       p2 = Vec2d(10, 650)


       # self.balls.append(self.create_ball(p2, .5, 7.0))
       #
       # p2 = Vec2d(400, 650)
       moment = pm.moment_for_circle(1, 0.0, 7)
       ball_body = pm.Body(3, moment)
       ball_body.position = Vec2d(p2)
       ball_body.mass = 1

       ball_shape = pm.Circle(ball_body, 7)
       ball_shape.friction = 1.5
       ball_shape.collision_type = COLLTYPE_DEFAULT
       # ball_shape.elasticity = 0.0001
       self.space.add(ball_body, ball_shape)
       self.balls.append(ball_shape)

       p2 = Vec2d(250, 160)
       # self.balls.append(self.create_ball(p2, .5, 7.0))
       #
       # p2 = Vec2d(400, 650)
       moment = pm.moment_for_circle(1, 0.0, 7)
       ball_body = pm.Body(3, moment)
       ball_body.position = Vec2d(p2)
       ball_body.mass = 1

       ball_shape = pm.Circle(ball_body, 7)
       ball_shape.friction = 1.5
       ball_shape.collision_type = COLLTYPE_DEFAULT
       # ball_shape.elasticity = 0.0001
       self.space.add(ball_body, ball_shape)
       self.balls.append(ball_shape)
       #  ramp # 2
       points = [(430, 50), (600, 80)]
       points = list(map(Vec2d, points))
       for i in range(len(points) - 1):
           v1 = Vec2d(points[i].x - 50, points[i].y)
           v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
           wall_body = pm.Body(body_type=pm.Body.STATIC)
           wall_shape = pm.Segment(wall_body, v1, v2, .0)
           wall_shape.friction = 7
           wall_shape.collision_type = COLLTYPE_DEFAULT
           self.space.add(wall_shape)
           self.walls.append(wall_shape)

       # ramp # 1
       points = [(50, 550), (70, 500)]
       points = list(map(Vec2d, points))
       for i in range(len(points) - 1):
           v1 = Vec2d(points[i].x - 50, points[i].y)
           v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
           wall_body = pm.Body(body_type=pm.Body.STATIC)
           wall_shape = pm.Segment(wall_body, v1, v2, .0)
           wall_shape.friction = 7
           wall_shape.collision_type = COLLTYPE_DEFAULT
           self.space.add(wall_shape)
           self.walls.append(wall_shape)

       points = [(299, 155), (300, 200)]
       points = list(map(Vec2d, points))
       for i in range(len(points) - 1):
           v1 = Vec2d(points[i].x - 50, points[i].y)
           v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
           wall_body = pm.Body(body_type=pm.Body.STATIC)
           wall_shape = pm.Segment(wall_body, v1, v2, .0)

           wall_shape.friction = 7
           wall_shape.collision_type = COLLTYPE_DEFAULT
           self.space.add(wall_shape)
           self.walls.append(wall_shape)

       #  Rohan's Part (just static segments)
       points = [(600, 400), (450, 300)]
       self.create_wall_segments(points)

       points = [(630, 400), (480, 300)]
       self.create_wall_segments(points)
       #
       points = [(480+150, 300), (510, 250)]
       self.create_wall_segments(points)
       #
       points = [(450+150, 300), (420, 250)]
       self.create_wall_segments(points)
       # Kevin's Part
       ### walls
       print("it works nunu")
       self.run_physics = True

       ### Wall under construction
       self.wall_points = []
       ### Poly under construction
       self.poly_points = []
       self.shape_to_remove = None
       self.mouse_contact = None

   def draw_helptext(self):
       font = pygame.font.Font(None, 16)
       text = ["Rube Goldberg Team Python A"
               ]
       y = 5
       for line in text:
           text = font.render(line, 1, THECOLORS["black"])
           self.screen.blit(text, (5, y))
           y += 10

   def create_ball(self, point, mass=1.0, radius=15.0):
       moment = pm.moment_for_circle(mass, 0.0, radius)
       ball_body = pm.Body(3, moment)
       ball_body.position = Vec2d(point)
       ball_body.mass = 2

       ball_shape = pm.Circle(ball_body, radius)
       ball_shape.friction = 1.5
       ball_shape.collision_type = COLLTYPE_DEFAULT
       #ball_shape.elasticity = 0.0001
       self.space.add(ball_body, ball_shape)
       return ball_shape

   def create_box(self, pos, size, mass=5.0):
       sizex = 3
       if size == 12:
           sizex = 7
       box_points = [(-sizex, -size*4), (-sizex, size*4), (sizex, size*4), (sizex, -size*4)]
       return self.create_poly(box_points, mass=mass, pos=pos)

   def create_poly(self, points, mass=5.0, pos=(0, 0)):

       moment = pm.moment_for_poly(mass, points)
       # moment = 1000
       body = pm.Body(mass, moment)
       body.position = Vec2d(pos)
       shape = pm.Poly(body, points)
       shape.friction = 0.5
       shape.collision_type = COLLTYPE_DEFAULT
       self.space.add(body, shape)
       return shape

   def create_wall_segments(self, points):
       """Create a number of wall segments connecting the points"""
       if len(points) < 2:
           return []
       points = list(map(Vec2d, points))
       for i in range(len(points) - 1):
           v1 = Vec2d(points[i].x-50, points[i].y)
           v2 = Vec2d(points[i + 1].x + 100, points[i + 1].y)
           wall_body = pm.Body(body_type=pm.Body.STATIC)
           wall_shape = pm.Segment(wall_body, v1, v2, .0)
           wall_shape.friction = 7.0
           wall_shape.collision_type = COLLTYPE_DEFAULT
           self.space.add(wall_shape)
           self.walls.append(wall_shape)

   def run(self):
       while self.running:
           self.loop()

   def draw_ball(self, ball):

       body = ball.body
       v = body.position + ball.offset.cpvrotate(body.rotation_vector)
       p = self.flipyv(v)
       r = ball.radius
       pygame.draw.circle(self.screen, THECOLORS["blue"], p, int(r), 2)

   def draw_wall(self, wall):
       body = wall.body
       pv1 = self.flipyv(body.position + wall.a.cpvrotate(body.rotation_vector))
       pv2 = self.flipyv(body.position + wall.b.cpvrotate(body.rotation_vector))
       pygame.draw.lines(self.screen, THECOLORS["lightgray"], False, [pv1, pv2])

   def draw_poly(self, poly):
       body = poly.body
       ps = [p.rotated(body.angle) + body.position for p in poly.get_vertices()]
       ps.append(ps[0])
       ps = list(map(self.flipyv, ps))
       if u.is_clockwise(ps):
           color = THECOLORS["green"]
       else:
           color = THECOLORS["red"]
       pygame.draw.lines(self.screen, color, False, ps)

   def draw(self):

       ### Clear the screen
       self.screen.fill(THECOLORS["white"])

       ### Display some text
       self.draw_helptext()

       ### Draw balls
       for ball in self.balls:
           self.draw_ball(ball)

       ### Draw walls
       for wall in self.walls:
           self.draw_wall(wall)

       ### Draw polys
       for poly in self.polys:
           self.draw_poly(poly)

       ### Draw Uncompleted walls
       if len(self.wall_points) > 1:
           ps = [self.flipyv(Vec2d(p)) for p in self.wall_points]
           pygame.draw.lines(self.screen, THECOLORS["gray"], False, ps, 2)

       ### Uncompleted poly
       if len(self.poly_points) > 1:
           ps = [self.flipyv(Vec2d(p)) for p in self.poly_points]
           pygame.draw.lines(self.screen, THECOLORS["red"], False, ps, 2)

       ### Mouse Contact
       if self.mouse_contact is not None:
           p = self.flipyv(self.mouse_contact)
           pygame.draw.circle(self.screen, THECOLORS["red"], p, 3)
       ### All done, lets flip the display
       draw_options = pm.pygame_util.DrawOptions(self.screen)
       self.space.debug_draw(draw_options)
       pygame.display.flip()

   def loop(self):
       for event in pygame.event.get():
           if event.type == QUIT:
               self.running = False


       mpos = pygame.mouse.get_pos()

       if pygame.key.get_mods() & KMOD_SHIFT and pygame.mouse.get_pressed()[2]:
           p = self.flipyv(Vec2d(mpos))
           self.poly_points.append(p)
       hit = self.space.point_query_nearest(self.flipyv(Vec2d(mpos)), 0, pm.ShapeFilter())
       if hit != None:
           self.shape_to_remove = hit.shape
       else:
           self.shape_to_remove = None

       ### Update physics
       if self.run_physics:
           x = 1
           dt = 1.0 / 60.0 / x
           for x in range(x):
               self.space.step(dt)
               for ball in self.balls:
                   # ball.body.reset_forces()
                   pass
               for poly in self.polys:
                   # poly.body.reset_forces()
                   pass

       ### Draw stuff
       self.draw()

       ### Check for objects outside of the screen, we can remove those
       # Balls
       xs = []
       for ball in self.balls:
           if ball.body.position.x < -1000 or ball.body.position.x > 1000 \
                   or ball.body.position.y < -1000 or ball.body.position.y > 1000:
               xs.append(ball)
       for ball in xs:
           self.space.remove(ball, ball.body)
           self.balls.remove(ball)

       # Polys
       xs = []
       for poly in self.polys:
           if poly.body.position.x < -1000 or poly.body.position.x > 1000 \
                   or poly.body.position.y < -1000 or poly.body.position.y > 1000:
               xs.append(poly)

       for poly in xs:
           self.space.remove(poly, poly.body)
           self.polys.remove(poly)

       ### Tick clock and update fps in title
       self.clock.tick(50)
       pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

   def add_L(self, space):
       """Add a inverted L shape with two joints"""
       rotation_center_body = pm.Body(body_type=pm.Body.STATIC)
       rotation_center_body.position = (300, 300)

       rotation_limit_body = pm.Body(body_type=pm.Body.STATIC)
       rotation_limit_body.position = (300, 300)
       body = pm.Body(650, 650)
       body.position = (300, 600)
       l1 = pm.Segment(rotation_limit_body, (25, -20), (25, 200.0), 1.0)
       l2 = pm.Segment(rotation_limit_body, (-25, -20), (-25, 200.0), 1.0)

       l3 = pm.Segment(rotation_limit_body, (25, -20), (85.0, -90.0), 1.3)
       l4 = pm.Segment(rotation_limit_body, (-25, -20), (-85.0, -90.0), 1.3)
       l8 = pm.Segment(body, (-250, -200), (200.0, -200.0), 5.0)

       rotation_center_joint = pm.PinJoint(body, rotation_center_body, (0, -200), (0, -200))
       joint_limit = .03
       rotation_limit_joint = pm.SlideJoint(body, rotation_limit_body, (-20, -200), (0, -200), 0, joint_limit)

       space.add(l1, l2, l3, l4, l8, rotation_limit_body, rotation_center_body, body, rotation_center_joint,
                 rotation_limit_joint)
       return l8

   def add_L_pulley(self, space):

       rotation_center_body = pm.Body(body_type=pm.Body.STATIC)
       rotation_center_body.position = (300, 300)

       rotation_limit_body = pm.Body(body_type=pm.Body.STATIC)
       rotation_limit_body.position = (200, 300)

       body1 = pm.Body(10, 10000)
       body1.position = (300, 300)
       l1 = pm.Segment(body1, (-100, 125), (100.0, 125.0), 1)
       l2 = pm.Segment(body1, (100.0, 125), (100.0, 150.0), 1)

       rotation_center_joint = pm.PinJoint(body1, rotation_center_body, (0, 25), (0, 25))
       joint_limit = 200
       rotation_limit_joint = pm.SlideJoint(body1, rotation_limit_body, (-150, 125), (0, 125), 0, joint_limit)

       self.space.add(l1, l2, body1, rotation_center_joint, rotation_limit_joint)
       return l1, l2

def main():
   demo = PhysicsDemo()
   demo.run()

main()
