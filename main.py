import pygame as pg, sys
import pygame.event
from pygame.locals import *
import time

#initialize global variable
XO = 'x'
winner = None
draw = False
width = 400
height = 400
white = (255,255,255)
line_color = (10,10,10)

#Jogo da velha 3x3 board
TTT = [[None]*3,[None]*3,[None]*3]

#Initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100), 0, 32)
pg.display.set_caption("Jogo da Velha")

#Loading images
abertura = pg.image.load('tic tac opening.jpg')
xis = pg.image.load('X.png')
circulo = pg.image.load('O.png')

#Resizing images
abertura = pg.transform.scale(abertura, (width, height+100))
xis = pg.transform.scale(xis, (80,80))
circulo = pg.transform.scale(circulo, (80,80))

#Mostra a abertura do jogo e desenha as linhas
def abertura_func():
    screen.blit(abertura, (0,0))
    pg.display.update()
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    time.sleep(1)
    pygame.event.clear()
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    screen.fill(white)

    #Draw vertical lines
    pg.draw.line(screen,line_color,(width/3, 0),(width/3, height),7)
    pg.draw.line(screen,line_color, (width/3 * 2, 0),(width/3 * 2, height),7)
    #Draw horizontal lines
    pg.draw.line(screen, line_color, (0, height/3), (width, height/3), 7)
    pg.draw.line(screen, line_color, (0, height/3 * 2), (width, height/3 * 2), 7)
    draw_status()

#Define um retangulo preto no fundo da tela com informações do jogo
def draw_status():
    global draw

    if winner is None:
        message = "Vez do " + XO.upper()
    else:
        message = winner.upper() + " venceu!"
    if draw:
        message = "Empate"

    font = pg.font.Font(None,30)
    text = font.render(message, 1, white)

    # Copy the rendered message onto de board
    screen.fill((0,0,0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    global TTT, winner, draw

    #check for winning rows
    for row in range (0,3):
        if (TTT[row][0] == TTT[row][1] == TTT[row][2]) and (TTT[row][0] is not None):
            #this row won
            winner = TTT[row][0]
            #draw winning line
            pg.draw.line(screen, (250,0, 0), (0, (row + 1) * height/3 - height/6),\
                         (width, (row + 1) * height/3 - height/6), 4)
            break

    #checks for winning columns
    for col in range (0,3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            #this column won
            winner = TTT[0][col]
            #draw winning line
            pg.draw.line(screen, (250,0,0), ((col+1) * width/3 - width/6, 0),\
                         ((col+1) * width/3 - width/6, width), 4)
            break

    #checks for diagonal lines
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        #game won diagonal left
        winner = TTT[0][0]
        pg.draw.line(screen, (250,70,70), (50,50), (350,350), 4)
    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        #game won diagonal right
        winner = TTT[0][2]
        pg.draw.line(screen, (250,70,70), (350,50), (50,350),4)
    if(all([all(row) for row in TTT]) and winner is None):
        draw = True
    draw_status()

def drawXO(row,col):
    global TTT, XO
    if row == 1:
        posx = 30
    if row == 2:
        posx = width/3 + 30
    if row == 3:
        posx = width/3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height/3 + 30
    if col == 3:
        posy = height/3 * 2 + 30
    TTT[row-1][col-1] = XO
    if XO == 'x':
        screen.blit(xis, (posy,posx))
        XO = 'o'
    else:
        screen.blit(circulo, (posy,posx))
        XO = 'x'
    pg.display.update()
    print(posx,posy)
    print(TTT)

def userClick():
    #get coords of mouse click
    x, y = pg.mouse.get_pos()
    #Equate the column of mouse click
    if x<width/3:
        col = 1
    elif x<width/3*2:
        col = 2
    elif x<width:
        col = 3
    else:
        col = None

    #Equate row of mouse click
    if y<height/3:
        row = 1
    elif y<width/3*2:
        row = 2
    elif y<width:
        row = 3
    else:
        row = None
    print(row,col)

    if row and col and TTT[row-1][col-1] is None:
        global XO
        #Draw X or O on the screen
        drawXO(row,col)
        check_win()

def reset_game():
    global TTT, winner,XO,draw
    pygame.event.set_blocked(MOUSEBUTTONDOWN)
    time.sleep(3)
    pygame.event.clear()
    pygame.event.set_allowed(MOUSEBUTTONDOWN)
    XO = 'x'
    draw = False
    winner=None
    abertura_func()
    TTT = [[None]*3, [None]*3,[None]*3]

abertura_func()

#Run the game FOREVER
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            #The user clicked, pull the lever, Kronk
            userClick()
            if winner or draw:
                reset_game()
    pg.display.update()
    CLOCK.tick(fps)