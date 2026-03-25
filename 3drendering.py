import math
import pygame

origin = (0, 0)

class datacalculation:
    def __init__(self):
        self.origin = (0, 0)

    def convert_to_2d_matrix(self, matrix):
        self.X = matrix[0]
        self.Y = matrix[1]
        self.Z = matrix[2]
        return self.X, self.Y, self.Z 

    def calc2ddistance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def calculate_COP(self, array):
        if len(array) < 1:
            return (0, 0)
        sumvaluex = 0
        sumvaluey = 0
        for i in array:
            sumvaluex += (i[0] - self.origin[0])
            sumvaluey += (i[1] - self.origin[1])
        return (sumvaluex / len(array), sumvaluey / len(array))

    def update_points(self, pointsarray, delta, camera, rotation, speed=0.1):
        self.updated_points_array = []
        self.cache_points = pointsarray.copy()

        self.Xrotation = rotation[0]
        self.Yrotation = rotation[1]
        self.Zrotation = rotation[2]

        COP = self.calculate_COP(pointsarray)
        lam = delta[2] * speed   

        for i in self.cache_points:
            newpoint = [i[0], i[1]]

           
            newpoint[0] += delta[0]
            newpoint[1] += delta[1]

          
            if delta[2] != 0:
                newpoint[0] = (lam * COP[0] + newpoint[0]) / (lam + 1)
                newpoint[1] = (lam * COP[1] + newpoint[1]) / (lam + 1)

            #the reason we use new values is because if we dont shift the origin the rotation axis is preliminariliy set at the initla origin not COP
            if self.Zrotation != 0:
                x = newpoint[0] - COP[0]
                y = newpoint[1] - COP[1]

                rx = x * math.cos(self.Zrotation) - y * math.sin(self.Zrotation)
                ry = x * math.sin(self.Zrotation) + y * math.cos(self.Zrotation)

                newpoint[0] = rx + COP[0]
                newpoint[1] = ry + COP[1]

            self.updated_points_array.append(newpoint)

        return self.updated_points_array


pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

dc = datacalculation()
#ok i  did ask ai for these points cuz yk i wont waste much time on this bs but trust me i coded the algo if u want u can question me on the shit
points = [
    [200, 200],
    [300, 200],
    [300, 300],
    [200, 300],

    [240, 240],
    [340, 240],
    [340, 340],
    [240, 340],
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

camera = (400, 300)

def joinpoints(surface, colour, start_pos, end_pos):
    pygame.draw.line(surface, colour, start_pos, end_pos, width=1)



running = True
while running:
    clock.tick(60)
    win.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    dx = dy = dz = 0
    dxT = dyT = dzT = 0

    if keys[pygame.K_LEFT]:
        dx = -2
    if keys[pygame.K_RIGHT]:
        dx = 2
    if keys[pygame.K_UP]:
        dy = -2
    if keys[pygame.K_DOWN]:
        dy = 2
    if keys[pygame.K_q]:
        dz = -1
    if keys[pygame.K_e]:
        dz = 1

    # Smooth rotation speed
    if keys[pygame.K_z]:
        dzT = 0.05
    if keys[pygame.K_x]:
        dzT = -0.05

    points = dc.update_points(points, (dx, dy, dz), camera, (dxT, dyT, dzT))

 
    for value in points:
        pygame.draw.circle(win, (255, 255, 255), (int(value[0]), int(value[1])), 5)

  
    for i in edges:
        joinpoints(
            win,
            (255, 255, 255),
            (int(points[i[0]][0]), int(points[i[0]][1])),
            (int(points[i[1]][0]), int(points[i[1]][1]))
        )

    pygame.display.update()

pygame.quit()