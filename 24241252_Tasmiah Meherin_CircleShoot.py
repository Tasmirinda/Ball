from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

gameover = False
pause = False
score = 0
lives = 3
miss = 0

shooter_x, shooter_y, shooter_r, shooter_h = 225, 20, 20, 40

circle_speed = 0.2
circles_no = random.randint(1, 5)

class Circle:
    global circle_speed

    def __init__(self):
        self.x = random.randrange(20, 425, 2)
        self.y = 423
        self.r = random.randint(15, 30)
        self.speed = circle_speed

class Fire:
    global shooter_x, shooter_y, shooter_r, shooter_h, circle_speed

    def __init__(self):
        self.x = shooter_x
        self.y = shooter_y + (shooter_h/2)
        self.r = 5
        self.fired = False
        self.speed = 1.5

circle_list = [Circle() for count in range(circles_no)]

fire_list = []


def draw_shooter(): #rocket
    glColor3f(1.0, 0.0, 0.0) 
    glBegin(GL_POLYGON)
    glVertex2f(shooter_x, shooter_y + shooter_h)  
    glVertex2f(shooter_x + shooter_r / 2, shooter_y + shooter_h * 1.5)  
    glVertex2f(shooter_x + shooter_r, shooter_y + shooter_h) 
    glEnd()
    
    glColor3f(0.3, 0.3, 0.3) 
    glBegin(GL_POLYGON)
    glVertex2f(shooter_x + 2, shooter_y)  
    glVertex2f(shooter_x + shooter_r - 2, shooter_y)  
    glVertex2f(shooter_x + shooter_r - 2, shooter_y + shooter_h) 
    glVertex2f(shooter_x + 2, shooter_y + shooter_h) 
    glEnd()


def draw_circle():
    global circle_list, gameover

    if gameover == False:
        for circles in circle_list:
            mcl(circles.x, circles.y, circles.r)

def draw_fire():
    global fire_list, gameover

    if gameover == False:
        for fires in fire_list:
            fires.fired = True

            if fires.fired == True:
                mcl(fires.x, fires.y, fires.r)

def circle_hit():
    global circle_list, fire_list, score

    for circles in circle_list:
        for fires in fire_list:
            x0_dist = abs(circles.x - fires.x)
            y0_dist = abs(circles.y - fires.y)

            rad_dist = circles.r + fires.r

            center_dist = math.sqrt((x0_dist ** 2) + (y0_dist ** 2))

            if center_dist <= rad_dist:
                score += 1
                fires.fired = False
                circle_list.remove(circles)
                fire_list.remove(fires)
                print('Score:', score)

    glutPostRedisplay()

def game_overs():
    global circle_list, shooter_x, shooter_y, shooter_r, shooter_h, gameover, lives, fire_list, miss

    for circles in circle_list:
        if (circles.y - circles.r) <= (shooter_y + shooter_h):
            if (((circles.x - circles.r) <= (shooter_x + shooter_r)) and (
                    (circles.x + circles.r) >= (shooter_x))):
                gameover = True
                print('Goodbye! Final Score:', score)
                
            elif ((circles.x + circles.r) >= (shooter_x)) and (
                    (circles.x - circles.r) <= (shooter_x + shooter_r)):
                gameover = True
                print('Goodbye! Final Score:', score)

        if (circles.y + circles.r) <= 0:
            circle_list.remove(circles)
            lives -= 1
            print('Lives left:', lives)

    if lives == 0:
        gameover = True
        print('Goodbye! Final Score:', score)
        print('Lives left:', lives)

    for fires in fire_list:
        if (fires.y + fires.r) >= 450:
            fire_list.remove(fires)
            miss += 1
            print('Misses:', miss)

    if miss == 3:
        gameover = True
        print('Game Over! Final Score:', score)
        print('Misses:', miss)

    glutPostRedisplay()

def mcl(x0, y0, r):
    x, y = 0, r
    d = 1 - r

    draw_point(x + x0, y + y0)

    while x <= y:
        de = ((2 * x) + 3)
        dne = ((2 * x) - (2 * y) + 5)

        if d < 0:
            d += de
            x += 1
        else:
            d += dne
            x += 1
            y -= 1

        draw_point(x + x0, y + y0)
        draw_point(-x + x0, y + y0)
        draw_point(-x + x0, -y + y0)
        draw_point(x + x0, -y + y0)
        draw_point(y + x0, x + y0)
        draw_point(-y + x0, x + y0)
        draw_point(-y + x0, -x + y0)
        draw_point(y + x0, -x + y0)

def draw_point(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def pause_button():
    glColor3f(1.0, 1.0, 0.0)
    mpl(210, 450, 210, 490)
    mpl(240, 450, 240, 490)

def play_button():
    glColor3f(1.0, 1.0, 0.0)
    mpl(210, 450, 210, 490)
    mpl(210, 450, 240, 469)
    mpl(210, 491, 240, 471)

def cancel_button():
    glColor3f(1.0, 0.0, 0.0)
    mpl(400, 450, 435, 490)
    mpl(400, 490, 435, 450)

def restart_button():
    glColor3f(0.0, 0.75, 0.8)
    mpl(15, 470, 50, 470)
    mpl(15, 470, 32.5, 490)
    mpl(15, 470, 32.5, 450)

def mpl(x0, y0, x1, y1):
    zone = findzone(x0, y0, x1, y1)
    x0, y0 = converttozone0(zone, x0, y0)
    x1, y1 = converttozone0(zone, x1, y1)

    dx = x1 - x0
    dy = y1 - y0
    dne = 2 * dy - 2 * dx
    de = 2 * dy
    dinit = 2 * dy - dx

    while x0 <= x1:
        if dinit >= 0:
            dinit += dne
            x0 += 1
            y0 += 1
        else:
            dinit += de
            x0 += 1

        a, b = converttozoneM(zone, x0, y0)
        draw_point(a, b)



def findzone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6

    return zone

def converttozone0(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def converttozoneM(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def keyboardListener(key, x, y):
    global shooter_x, fires

    if gameover == False:
        if pause == False:
            if key == b'a':
                if shooter_x >= 16:
                    shooter_x -= 5
            elif key == b'd':
                if shooter_x <= 434:
                    shooter_x += 5
            elif key == b' ':
                fire_list.append(Fire())

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global pause, score, gameover, lives, miss, shooter_x, shooter_y, shooter_r, circle_speed, circle_list, fire_list

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 210 <= x <= 240 and 10 <= y <= 50:
            if gameover == False:
                if pause == False:
                    pause = True
                    print('Paused')
                else:
                    pause = False
        elif 15 <= x <= 50 and 10 <= y <= 50:
            if gameover == True:
                gameover = False

            print('Starting Over')

            score = 0
            lives = 3
            miss = 0

            shooter_x, shooter_y, shooter_r = 225, 20, 12

            circle_speed = 0.3
            circles_no = random.randint(1, 5)

            circle_list = [Circle() for count in range(circles_no)]
            fire_list = []

        elif 400 <= x <= 435 and 10 <= y <= 50:
            gameover = True
            print('Goodbye! Final Score:', score)
            glutLeaveMainLoop()

    glutPostRedisplay()

def animate():
    global fire_list

    if gameover == False:
        if pause == False:
            for fires in fire_list:
                if (fires.y - fires.r) <= 450:
                    fires.y += fires.speed

            for circles in circle_list:
                circles.y -= circles.speed

            circle_hit()

            if gameover == False:
                game_overs()

    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    animate()
    glColor3f(0.0, 0.0, 0.0)

    global fire_list, circle_list

    if pause == False:
        pause_button()
    else:
        play_button()

    cancel_button()
    restart_button()

    glColor3f(0.7, 0.6, 0.2)
    draw_shooter()

    if gameover == False:
        draw_fire()
        draw_circle()

    if circle_list == []:
        circle_list = [Circle() for count in range(circles_no)]

    draw_circle()

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(450, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Shoot The Circles")
glutDisplayFunc(showScreen)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()