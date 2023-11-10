import math
import pygame
import numpy as np

def translate(dx,dy,dz):
    return np.array([[1,0,0,dx],[0,1,0,dy],[0,0,1,dz],[0,0,0,1]])

def scale(sx,sy,sz):
    return np.array([[sx,0,0,0],[0,sy,0,0],[0,0,sz,0],[0,0,0,1]])

def rotateX(angle):
    angle = math.radians(angle)
    return np.array([[1,0,0,0],[0,math.cos(angle),-math.sin(angle),0],[0,math.sin(angle),math.cos(angle),0],[0,0,0,1]])

def rotateY(angle):
    angle = math.radians(angle)
    return np.array([[math.cos(angle),0,math.sin(angle),0],[0,1,0,0],[-math.sin(angle),0,math.cos(angle),0],[0,0,0,1]])

def rotateZ(angle):
    angle = math.radians(angle)
    return np.array([[math.cos(angle),-math.sin(angle),0,0],[math.sin(angle),math.cos(angle),0,0],[0,0,1,0],[0,0,0,1]])

def viewTransform(camX,camY,camZ, eye):
    return np.array([[camX[0],camX[1],camX[2],-np.dot(camX,eye)],[camY[0],camY[1],camY[2],-np.dot(camY,eye)],
                   [camZ[0],camZ[1],camZ[2],-np.dot(camZ,eye)],[0,0,0,1]])

def project(near, far, f):
    return np.array([[f,0,0,0],[0,f,0,0],[0,0,-(far+near)/(far-near),-(2*far*near)/(far-near)],[0,0,-1,0]])

def viewport(point, width, height):
    return ((width/2)*(point[0]+1),(height/2)*(point[1]+1),(1/2)*point[2]-(1/2))

def to3D(point):
    return (point[0]/point[3], point[1]/point[3], point[2]/point[3])

pygame.init()
height = 400
width = 400
near = 1
far = 100
angleX = 0
angleY = 0 
angleZ = 0 
eye = np.array([0,0,0])
center = np.array([0,0,1])
up = np.array([0,1,0])
camZ = (eye-center)/np.linalg.norm(eye-center)
camX = np.cross(up, camZ)/np.linalg.norm(np.cross(up, camZ))
camY = np.cross(camZ, camX)
f = 1/math.tan(math.radians(45))

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

cube = np.array([[(0,0,0,1),(1,0,0,1),(0,0,1,1)],[(1,0,0,1),(1,0,1,1),(0,0,1,1)],[(0,0,0,1),(1,0,0,1),(0,1,0,1)],[(1,0,0,1),(0,1,0,1),(1,1,0,1)],[(0,0,0,1),(0,1,0,1),(0,0,1,1)],[(0,1,0,1),(0,0,1,1),(0,1,1,1)],[(0,0,1,1),(0,1,1,1),(1,0,1,1)],[(0,1,1,1),(1,1,1,1),(1,0,1,1)],[(1,0,1,1),(1,0,0,1),(1,1,0,1)],[(1,0,1,1),(1,1,1,1),(1,1,0,1)],[(1,1,0,1),(0,1,0,1),(1,1,1,1)],[(1,1,1,1),(0,1,1,1),(0,1,0,1)]])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        eye[0] -= 1
    if keys[pygame.K_s]:
        eye[1] -= 1
    if keys[pygame.K_w]:
        eye[1] += 1
    if keys[pygame.K_d]:
        eye[0] += 1
    if keys[pygame.K_x]:
        eye[2] -= 1
    if keys[pygame.K_z]:
        eye[2] += 1
    if keys[pygame.K_q]:
        angleZ -= 3
    if keys[pygame.K_e]:
        angleZ += 3
    if keys[pygame.K_u]:
        angleY -= 3
    if keys[pygame.K_i]:
        angleY += 3
    if keys[pygame.K_j]:
        angleX -= 3
    if keys[pygame.K_k]:
        angleX += 3

    model = np.linalg.inv(translate(20,20,20)) @ scale(2,2,2) @ rotateZ(-angleZ) @ rotateY(-angleY) @ rotateX(-angleX) @ np.linalg.inv(translate(0,0,0))

    for i in range(len(cube)):
        display_points = []
        for point in cube[i]:
            model_point = np.dot(model, point)
            modelview_point = np.dot(viewTransform(camX,camY,camZ, eye), model_point)
            project_point = np.dot(project(near, far, f), modelview_point)
            pointin3D = to3D(project_point)
            display_point = viewport(pointin3D, width, height)
            display_points.append(display_point[:2])
        pygame.draw.polygon(screen, "green", display_points, width=1)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
