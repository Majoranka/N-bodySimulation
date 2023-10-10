import pygame
import random
import numpy as np
import math
import os

#init pygame
pygame.init()

#define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
orange = (255,165,0)

game_display = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #(0, 0), pygame.FULLSCREEN
pygame.display.set_caption("Physics Simulator")

width, height = game_display.get_size()

#surface = pygame.Surface((width, height), pygame.SRCALPHA)

clock = pygame.time.Clock()

pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

#set icon and other assets
#img = pygame.image.load('C:/Users/Lenovo/Desktop/Ucebne_materialy/Python programs/data/3body.png')
def open_img(name):
    script_dir = os.path.dirname(os.path.abspath(name))
    relative_image_path = os.path.join(script_dir, 'data', name)
    return pygame.image.load(relative_image_path)

img = open_img('3body.png')
pygame.display.set_icon(img) 
#start = pygame.image.load('C:/Users/Lenovo/Desktop/Ucebne_materialy/Python programs/data/Start.png')
#cont = pygame.image.load('C:/Users/Lenovo/Desktop/Ucebne_materialy/Python programs/data/Continue.png')
#qit = pygame.image.load('C:/Users/Lenovo/Desktop/Ucebne_materialy/Python programs/data/Quit.png')
#physim = pygame.image.load('C:/Users/Lenovo/Desktop/Ucebne_materialy/Python programs/data/phys_sim.png')
start = open_img('Start.png')
cont = open_img('Continue.png')
qit = open_img('Quit.png')
physim = open_img('phys_sim.png')

def abs(x):
    sum = 0
    for i in x:
        sum += i**2
    return sum**0.5

random.seed(0)
star_pos_x = [random.randint(-1.5*width,1.5*width) for i in range(1000)]
star_pos_y = [random.randint(-1.5*height,1.5*height) for i in range(1000)]

def draw_stars(displacement = np.array([0.0,0.0])):
    random.seed(0)
    for i in range(1000):
        pygame.draw.circle(center = [star_pos_x[i], star_pos_y[i]]-displacement, radius = 1, color = white, surface = game_display)
     

def main_menu(camera_position = np.array([0.0,0.0]), m = np.ones(0), R = np.ones(0), pos = np.zeros((0,2)), v = np.zeros((0,2)), N = 0):
    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
    while True:
        game_display.fill(black)
        draw_stars()
        game_display.blit(physim, (width/2 - 290, height/2 - 160))
        game_display.blit(start, (width/2 - 65, height/2 - 60))
        game_display.blit(cont, (width/2 - 100, height/2))
        game_display.blit(qit, (width/2 - 47, height/2 + 60))
        #pygame.draw.rect(game_display, white, (width/2,0,1,height))

        if width/2 - 65 < pygame.mouse.get_pos()[0] < width/2 + 60 and height/2 - 60 < pygame.mouse.get_pos()[1] < height/2 - 15:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif width/2 - 100 < pygame.mouse.get_pos()[0] < width/2 + 100 and height/2 - 10 < pygame.mouse.get_pos()[1] < height/2 + 35:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif width/2 - 52 < pygame.mouse.get_pos()[0] < width/2 + 48 and height/2 + 50 < pygame.mouse.get_pos()[1] < height/2 + 100:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if width/2 - 65 < pygame.mouse.get_pos()[0] < width/2 + 60 and height/2 - 60 < pygame.mouse.get_pos()[1] < height/2 - 15:
                    run_simulation()
                if width/2 - 100 < pygame.mouse.get_pos()[0] < width/2 + 100 and height/2 - 10 < pygame.mouse.get_pos()[1] < height/2 + 35:
                    run_simulation(camera_position, m, R, pos, v, N)
                if width/2 - 52 < pygame.mouse.get_pos()[0] < width/2 + 48 and height/2 + 50 < pygame.mouse.get_pos()[1] < height/2 + 100:
                    quit()
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                    
                

        pygame.display.update()
        

def run_simulation(camera_position = np.array([0.0,0.0]), m = np.ones(0), R = np.ones(0), pos = np.zeros((0,2)), v = np.zeros((0,2)), N = 0):

    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    #simulation parameters
    stars = True
    c_speed = 5
    #camera_position = np.array([0.0,0.0])
    lock = False
    lock_num = 0
    mass = 0.0
    creating_new_body = False
    mouse_drag = False

    #physics parameters
    G = 0.001
    exponent = 1
    #N = 0
    #m = np.ones(N)*10
    #R = np.ones(N)
    #pos = np.zeros((N,2))+[width/2, height/2]
    #for i in range(N):
    #    pos[i][0] += 400*math.cos(2*math.pi/N*i)
    #    pos[i][1] += 400*math.sin(2*math.pi/N*i)
    #v = np.zeros((N,2))
    close = False

    while not close:
        # displaying all the things
        game_display.fill(black)
        for i in range(N):
            pygame.draw.circle(center = pos[i], radius = R[i], color = white, surface = game_display)
        
        if stars:
            draw_stars(camera_position//20)

        #pygame.display.update()

        # Creating bodies
        #keys = pygame.key.get_pressed()
        #if keys[pygame.MOUSEBUTTONDOWN]:
        #    pos = np.vstack((pos, np.array(pygame.mouse.get_pos())))
        #    v = np.vstack((v, np.zeros(2)))
        #    N += 1

        # Camera movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pos += (0,c_speed)
            camera_position += (0,c_speed)
            lock = False
        if keys[pygame.K_DOWN]:
            pos += (0,-c_speed)
            camera_position += (0,-c_speed)
            lock = False
        if keys[pygame.K_LEFT]:
            pos += (c_speed,0)
            camera_position += (c_speed,0)
            lock = False
        if keys[pygame.K_RIGHT]:
            pos += (-c_speed,0)
            camera_position += (-c_speed,0)
            lock = False

        # Locked camera
        if lock:
            pos -= pos[lock_num] - np.array([width/2, height/2])
            camera_position = pos[(lock_num+1)%N] - np.array([width/2, height/2])
        

        # Escape + locked camera trigger
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(camera_position, m, R, pos, v, N)
                if event.key == pygame.K_SPACE and N > 0:
                    lock = True
                    lock_num = (lock_num + 1) % N
                if event.key == pygame.K_m:
                    main_menu(camera_position, m, R, pos, v, N)
            

        # Camera movement using mouse

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                lock = False
                mouse_drag = True
                starting_position = [pygame.mouse.get_pos(), None]

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                mouse_drag = False

        # Creating arbitrary bodies
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = np.vstack((pos, np.array(pygame.mouse.get_pos())))
                v = np.vstack((v, np.zeros(2)))
                m = np.append(m, [1.0])
                R = np.append(R, [10])
                N += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                creating_new_body = True
                mass += 0.01
            if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                pos = np.vstack((pos, np.array(pygame.mouse.get_pos())))
                v = np.vstack((v, np.zeros(2)))
                m = np.append(m, [mass])
                R = np.append(R, [10*mass**(1/2)])
                N += 1
                mass = 0.0
                creating_new_body = False

        if creating_new_body:    
            pygame.draw.circle(center = pygame.mouse.get_pos(), radius = 10*mass**(1/2), color = white, surface = game_display)
            mass += 0.1

        if mouse_drag:
            starting_position[1] = starting_position[0]
            starting_position[0] = pygame.mouse.get_pos()
            pos += starting_position[0]
            pos -= starting_position[1]
            camera_position += starting_position[0]
            camera_position -= starting_position[1]

        pygame.display.update()

        # Physics

        for i in range(N):
            r = pos - pos[i]
            r_size = [abs(r[j]) for j in range(N)]
            
            a = np.zeros(2)
            for j in range(N):
                if j == i:
                    continue
                #if r_size[j] <= 2*R:
                #    break
                if r_size[j] == 0:
                    break
                a += G*m[j]/(r_size[j]**exponent)*r[j]
            v[i] += a
            pos[i] += v[i]

        clock.tick()

    
    # Quit
    
    pygame.quit()
    

#run_simulation()
main_menu()