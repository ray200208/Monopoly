'''import pygame
import random
import math
import time
import os

pygame.init()

card_width=80
card_height=160
screen=pygame.display.set_mode((600,400))
font=pygame.font.Font(None,24)

try:
    image = pygame.image.load("monopoly_logo.jpeg").convert_alpha()
    print("Image loaded successfully!")
    
except Exception as e:
    print("Image loading failed:", e)
    image = None
    
def mainscreen():
   global screen
   while True:
       for event in pygame.event.get():
           if event.type==pygame.QUIT:
               pygame.quit()
               exit()
       screen.fill((0,200,0))
       screen.blit(image,(120,75))
       if button('PLAY A GAME',125,225,350,100,(255,0,0),(0,0,255)):
           return 'play'
       pygame.display.update()
       
def button(text,x,y,width,height,colour,hover_colour):
    global screen
    mouse_pos=pygame.mouse.get_pos()
    click=False
    if x<mouse_pos[0]<x+width and y<mouse_pos[1]<y+height:
        pygame.draw.rect(screen,hover_colour, (x,y,width,height))
        if pygame.mouse.get_pressed()[0]:
            click=True
    else:
        pygame.draw.rect(screen,colour, (x,y,width,height))
    text=font.render(text,True,(255,255,255))
    text_rect=text.get_rect(center=(x+width//2,y+height//2))
    screen.blit(text,text_rect)
    return click
            
def choice_screen():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0,200,0))
        if button('2 Player',100,225,100,75,(255,0,0),(0,0,255)):
            return 2
        elif button('3 Player',225,225,100,75,(255,0,0),(0,0,255)):
            return 3
        elif button('4 Player',350,225,100,75,(255,0,0),(0,0,255)):
            return 4
        elif button('BACK',475,225,100,70,(255,0,0),(0,0,255)):
            return 'back'
        pygame.display.update()

def player_game(n):
    list_colours=['Blue','Yellow','Red','Green']
    colour_players=[]
    for i in range(n):
        colour_players.append(random.choice(list_colours))
        list_colours.remove(colour_players[i])
        print("The colour generated for player", i+1, 'is', colour_players[i])
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_m]:
            running=False
        screen.fill((0,0,250))
        y=100
        for i in range(n):
            text=font.render(f"The colour assigned to player {i+1} is {colour_players[i]}",True, (255,255,255))
            screen.blit(text, (100,y))
            y+=75
        instruction_text=font.render("Press M to return to Main Menu",True,(255,255,255))
        text_rect=instruction_text.get_rect(center=(screen.get_width()//2, 50))
        screen.blit(instruction_text,text_rect)
        pygame.display.update()
        
def main():
    while True:
        result=mainscreen()
        if result=='play':
            choice=choice_screen()
            if choice!='back':
                player_game(choice)

class Space:
    def __init__(self,name,type,price=0,rent=0):
        self.name=name
        self.type=type
        self.price=price
        self.rent=rent
        self.owner=None

board=[
    Space("Go",'go'),
    Space('Old Kent Road','property',60,2),
    Space("Community Chest","community"),
    Space("Whitechapel Road","property",60,4),
    Space("Income Tax","tax"),
    Space("King's Cross Station","station",200,25),
    Space("The Angel Islington","property",100,6),
    Space("Chance","chance"),
    Space("Euston Road","property",100,6),
    Space("Pentonville Road","property",120,8),
    Space("Jail/Just Visiting","jail"),
    Space("Pall Mall","property",140,10),
    Space("Electric Company","utility",150),
    Space("Whitehall","property",140,10),
    Space("Northumberland Avenue","property",160,12),
    Space("Marylebone Station","station",200,25),
    Space("Bow Street","property",180,14),
    Space("Community Chest","community"),
    Space("Marlborough Street","property",180,14),
    Space("Vine Street","property",200,16),
    Space("Free Parking","parking"),
    Space("Strand","property",220,18),
    Space("Chance","chance"),
    Space("Fleet Street","property",220,18),
    Space("Trafalgar Square","property",240,20),
    Space("Fenchurch Street Station","station",200,25),
    Space("Leicester Square","property",260,22),
    Space("Coventry Street","property",260,22),
    Space("Water Works","utility",150),
    Space("Piccadilly","property",280,24),
    Space("Go To Jail","gotojail"),
    Space("Regent Street","property",300,26),
    Space("Oxford Street","property",300,26),
    Space("Community Chest","community"),
    Space("Bond Street","property",320,28),
    Space("Liverpool Street Station","station",200,25),
    Space("Chance","chance"),
    Space("Park Lane","property",350,35),
    Space("Super Tax","tax"),
    Space("Mayfair","property",400,50)
    ]

property_colours={"brown": (152,75,44),
    "lightblue": (173,216,230),
    "pink": (216,112,147),
    "orange": (255,165,0),
    "red":  (220,20,60),
    "yellow": (255,255,0),
    "green": (34,139,34),
    "darkblue": (25,25,112),
    "station": (0,0,0),
    "utility": (200,200,200),
    "chance": (255,140,0),
    "community": (0,120,255),
    "special": (240,240,240)
    }
    
pygame.init()
fullscreen=True
if fullscreen:
    screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    w,h=screen.get_size()
else:
    w,h=1200,1200
    screen=pygame.display.set_mode((w,h))
pygame.display.set_caption('MONOPOLY BOARD')
font=pygame.font.Font(None,14)
clock=pygame.time.Clock()
tile_width=w//10.8
tile_height=h//11
tile_positions=[]
for i in range(11): #Bottom row cards
    x=w-(i+1)*tile_width
    y=h-tile_height
    tile_positions.append((x,y))
    
for i in range(1,10): #Left column cards
    x=0
    y=h-(i+1)*tile_height
    tile_positions.append((x,y))

for i in range(11): #Top row cards
    x=i*tile_width
    y=0
    tile_positions.append((x,y))

for i in range(1,10): #Right column cards
    x=w-tile_width
    y=i*tile_height
    tile_positions.append((x,y))

def draw_text_custom(text,font,color,surface,x,y):
    words=text.split()
    line_height=font.size("Tg")[1]
    if len(words)==2:
        lines=[words[0],words[1]]
    elif len(words)==3:
        lines=[" ".join(words[:2]),words[2]]
    else:
        lines=[text]
    for i, line in enumerate(lines):
        surface.blit(font.render(line, True, color), (x, y + i * line_height))

def draw_tile(index,x,y):
    global lines
    space=board[index]
    name=space.name
    ttype=space.type
    colour_key='special'
    if name in ("Old Kent Road","Whitechapel Road"):
        colour_key="brown"
    elif name in ("The Angel Islington","Euston Road","Pentonville Road"):
        colour_key="lightblue"
    elif name in ("Pall Mall","Whitehall","Northumberland Avenue"):
        colour_key="pink"
    elif name in ("Bow Street","Marlborough Street","Vine Street"):
        colour_key="orange"
    elif name in ("Strand","Fleet Street","Trafalgar Square"):
        colour_key="red"
    elif name in ("Leicester Square","Coventry Street","Piccadilly"):
        colour_key="yellow"
    elif name in ("Regent Street","Oxford Street","Bond Street"):
        colour_key="green"
    elif name in ("Park Lane","Mayfair"):
        colour_key="darkblue"
    elif ttype=="station":
        colour_key="station"
    elif ttype=="utility":
        colour_key="utility"
    colour=property_colours[colour_key]
    pygame.draw.rect(screen,(255,255,255),(x,y,tile_width,tile_height))
    pygame.draw.rect(screen,(0,0,0),(x,y,tile_width,tile_height),2)
    if ttype in ('property','station','utility'):
        pygame.draw.rect(screen,colour,(x,y,tile_width,tile_height//6))

    words=name.split()
    line_height=font.size("Tg")[1]
    if len(words)==2:
        lines=[words[0],words[1]]
    elif len(words)==3:
        lines=[" ".join(words[:2]),words[2]]
    else:
        lines=[name]
    total_text_height=len(lines)*line_height
    if ttype not in('chance','community'):
        y_starting=y+tile_height//5+2
    else:
        y_starting=y+4

    for i,line in enumerate(lines):
            text=font.render(line,True,(0,0,0))
            text_x=x+(tile_width-text.get_width())//2
            text_y=y_starting+i*line_height
            screen.blit(text,(text_x,text_y))
    if ttype in ('chance','community'):
        icon_y=y_starting+total_text_height+14
    else:
        icon_y=y_starting+total_text_height+4
    icon_x=x+tile_width//2

    if ttype=="station":
        pygame.draw.rect(screen,(0,0,0),
                         (icon_x-18,icon_y,36,18),2)
        pygame.draw.circle(screen, (0,0,0),
                           (icon_x-10,icon_y+18),6,2)
        pygame.draw.circle(screen,(0,0,0),
                           (icon_x+10,icon_y+18),6,2)
    elif ttype=="utility":
        if "Electric" in name:
            points = [(icon_x-6,icon_y-9), (icon_x+1,icon_y-3),
                (icon_x-2,icon_y-3), (icon_x+6,icon_y-6),
                (icon_x-1,icon_y), (icon_x+2, icon_y)]
            
            pygame.draw.polygon(screen,(255,215,0),points)

        else:
            pygame.draw.circle(screen,(0,0,255),
                               (icon_x,icon_y+8),10)
            pygame.draw.polygon(screen,(0,0,255),
                                [(icon_x-10,icon_y+6),
                                 (icon_x+10,icon_y+6),
                                 (icon_x,icon_y+25)])
    elif ttype=="chance":
        pygame.draw.circle(screen,(255,140,0), (icon_x,icon_y+10),5)
        pygame.draw.lines(screen,(255,140,0),False,[(icon_x-10,icon_y-10),
                                    (icon_x+10,icon_y-10), (icon_x+10,icon_y),
                                    (icon_x,icon_y)],4)

    elif ttype=="community":
        pygame.draw.rect(screen,(0,120,255),
                         (icon_x-15,icon_y,30,20),2)
        pygame.draw.rect(screen,(0,120,255),
                         (icon_x-15,icon_y-8,30,10),2)
        pygame.draw.rect(screen,(0,120,255),
                         (icon_x-4,icon_y+10,8,8))
            


def draw_board():
    for i,(x,y) in enumerate(tile_positions):
        draw_tile(i,x,y)

logo_image=pygame.image.load('monopoly_logo.jpeg')
logo_width,logo_height=350,175
logo_image=pygame.transform.scale(logo_image,(logo_width,logo_height))
logo_rect=logo_image.get_rect(center=(w//2,h//2))

button_font=pygame.font.Font(None,25)
back_text=button_font.render('Back',True,(255,255,255))
back_rect=pygame.Rect(w//2,h//4,100,40)
back_colour=(0,0,0)

def main_board():
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    choice_screen()
        screen.fill((255,255,255))
        draw_board()
        screen.blit(logo_image,logo_rect)
        pygame.draw.rect(screen,back_colour,back_rect)
        screen.blit(back_text,(back_rect.x+(back_rect.width-back_text.get_width())//2,
                            back_rect.y+(back_rect.height-back_text.get_height())//2))
        pygame.display.flip()
    pygame.quit()
main()
main_board()'''


import pygame
import random
import sys

pygame.init()

fullscreen = True
if fullscreen:
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    w, h = screen.get_size()
else:
    w, h = 1200, 1200
    screen = pygame.display.set_mode((w,h))

pygame.display.set_caption("MONOPOLY")
clock = pygame.time.Clock()


font = pygame.font.Font(None, 14)
button_font = pygame.font.Font(None, 30)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,200,0)


try:
    logo_image = pygame.image.load("monopoly_logo.jpeg").convert_alpha()
    logo_image = pygame.transform.scale(logo_image, (350, 175))
except Exception as e:
    print("Failed to load logo:", e)
    logo_image = None


def button(text, x, y, w, h, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + w//2, y + h//2))
    screen.blit(text_surf, text_rect)
    return clicked

def mainscreen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(GREEN)
        if logo_image:
            screen.blit(logo_image, ((w-logo_image.get_width())//2, 75))
        if button("PLAY A GAME", w//2 - 175, 300, 350, 100, RED, BLUE):
            return "play"
        pygame.display.update()
        clock.tick(60)

def choice_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(GREEN)
        if button("2 Player", w//4 - 50, 225, 100, 75, RED, BLUE):
            return 2
        if button("3 Player", w//2 - 50, 225, 100, 75, RED, BLUE):
            return 3
        if button("4 Player", 3*w//4 - 50, 225, 100, 75, RED, BLUE):
            return 4
        if button("BACK", w - 120, h - 80, 100, 60, RED, BLUE):
            return "back"
        pygame.display.update()
        clock.tick(60)


def player_game(n):
    list_colours=['Blue','Yellow','Red','Green']
    colour_players=[]
    for i in range(n):
        colour_players.append(random.choice(list_colours))
        list_colours.remove(colour_players[i])
    play_button_rect=pygame.Rect(screen.get_width() // 2 - 75, screen.get_height() - 100, 100, 50)
    
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_m]:
            return 

        screen.fill((0,0,150))
        y = 100
        for i in range(n):
            text = font.render(f"Player {i+1} color: {colour_players[i]}", True, (255,255,255))
            screen.blit(text, (100, y))
            y += 75

        instr = font.render("Press M to return to Main Menu", True, (255,255,255))
        screen.blit(instr, (w//2 - instr.get_width()//2, 50))
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if play_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen,(0,200,0),play_button_rect)
            if click:
                main_board()
                return
        else:
            pygame.draw.rect(screen,(0,150,0),play_button_rect)
        play_text=font.render('PLAY',True,(255,255,255))
        play_text_rect=play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text,play_text_rect)
            

        pygame.display.update()
        clock.tick(60)


class Space:
    def __init__(self, name, type, price=0, rent=0):
        self.name = name
        self.type = type
        self.price = price
        self.rent = rent
        self.owner = None

board = [
    Space("Go",'go'),
    Space('Old Kent Road','property',60,2),
    Space("Community Chest","community"),
    Space("Whitechapel Road","property",60,4),
    Space("Income Tax","tax"),
    Space("King's Cross Station","station",200,25),
    Space("The Angel Islington","property",100,6),
    Space("Chance","chance"),
    Space("Euston Road","property",100,6),
    Space("Pentonville Road","property",120,8),
    Space("Jail/Just Visiting","jail"),
    Space("Pall Mall","property",140,10),
    Space("Electric Company","utility",150),
    Space("Whitehall","property",140,10),
    Space("Northumberland Avenue","property",160,12),
    Space("Marylebone Station","station",200,25),
    Space("Bow Street","property",180,14),
    Space("Community Chest","community"),
    Space("Marlborough Street","property",180,14),
    Space("Vine Street","property",200,16),
    Space("Free Parking","parking"),
    Space("Strand","property",220,18),
    Space("Chance","chance"),
    Space("Fleet Street","property",220,18),
    Space("Trafalgar Square","property",240,20),
    Space("Fenchurch Street Station","station",200,25),
    Space("Leicester Square","property",260,22),
    Space("Coventry Street","property",260,22),
    Space("Water Works","utility",150),
    Space("Piccadilly","property",280,24),
    Space("Go To Jail","gotojail"),
    Space("Regent Street","property",300,26),
    Space("Oxford Street","property",300,26),
    Space("Community Chest","community"),
    Space("Bond Street","property",320,28),
    Space("Liverpool Street Station","station",200,25),
    Space("Chance","chance"),
    Space("Park Lane","property",350,35),
    Space("Super Tax","tax"),
    Space("Mayfair","property",400,50)
]

property_colours = {
    "brown": (152,75,44),
    "lightblue": (173,216,230),
    "pink": (216,112,147),
    "orange": (255,165,0),
    "red":  (220,20,60),
    "yellow": (255,255,0),
    "green": (34,139,34),
    "darkblue": (25,25,112),
    "station": (0,0,0),
    "utility": (200,200,200),
    "chance": (255,140,0),
    "community": (0,120,255),
    "special": (240,240,240)
}


tile_width = w//11
tile_height = h//11
tile_positions = []


for i in range(11):
    x = w - (i+1)*tile_width
    y = h - tile_height
    tile_positions.append((x,y))

for i in range(1,10):
    x = 0
    y = h - (i+1)*tile_height
    tile_positions.append((x,y))

for i in range(11):
    x = i*tile_width
    y = 0
    tile_positions.append((x,y))

for i in range(1,10):
    x = w - tile_width
    y = i*tile_height
    tile_positions.append((x,y))

def draw_text_centered(text, font, color, surface, x, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x,y))
    surface.blit(surf, rect)

def draw_tile(index, x, y):
    space = board[index]
    ttype = space.type
    name = space.name
    color_key = "special"


    if name in ("Old Kent Road","Whitechapel Road"):
        color_key = "brown"
    elif name in ("The Angel Islington","Euston Road","Pentonville Road"):
        color_key = "lightblue"
    elif name in ("Pall Mall","Whitehall","Northumberland Avenue"):
        color_key = "pink"
    elif name in ("Bow Street","Marlborough Street","Vine Street"):
        color_key = "orange"
    elif name in ("Strand","Fleet Street","Trafalgar Square"):
        color_key = "red"
    elif name in ("Leicester Square","Coventry Street","Piccadilly"):
        color_key = "yellow"
    elif name in ("Regent Street","Oxford Street","Bond Street"):
        color_key = "green"
    elif name in ("Park Lane","Mayfair"):
        color_key = "darkblue"
    elif ttype == "station":
        color_key = "station"
    elif ttype == "utility":
        color_key = "utility"
    elif ttype == "chance":
        color_key = "chance"
    elif ttype == "community":
        color_key = "community"

    color = property_colours[color_key]


    pygame.draw.rect(screen, WHITE, (x,y,tile_width,tile_height))
    pygame.draw.rect(screen, BLACK, (x,y,tile_width,tile_height), 2)

 
    if ttype in ("property","station","utility"):
        pygame.draw.rect(screen, color, (x, y, tile_width, tile_height//6))


    if ttype in ("chance", "community"):
        name_y = y + 5
    else:
        name_y = y + tile_height//6 + 5

    draw_text_centered(name, font, BLACK, screen, x + tile_width//2, name_y)


    icon_x = x + tile_width//2
    icon_y = name_y + 25

  
    if ttype == "station":
        
        pygame.draw.rect(screen, BLACK, (icon_x-15, icon_y, 30, 15), 2)
        pygame.draw.circle(screen, BLACK, (icon_x-8, icon_y+18), 5, 2)
        pygame.draw.circle(screen, BLACK, (icon_x+8, icon_y+18), 5, 2)

    elif ttype == "utility":
        if "Electric" in name:
            points = [(icon_x-6,icon_y-6), (icon_x,icon_y-2),
                      (icon_x+6,icon_y-6), (icon_x,icon_y+8)]
            pygame.draw.polygon(screen,(255,215,0),points)
        else:
            pygame.draw.circle(screen,(0,0,255),(icon_x,icon_y),8)
            pygame.draw.polygon(screen,(0,0,255),
                                [(icon_x-8,icon_y),(icon_x+8,icon_y),(icon_x,icon_y+16)])

    elif ttype == "chance":
        pygame.draw.circle(screen,(255,140,0), (icon_x,icon_y+10),5)
        pygame.draw.lines(screen,(255,140,0),False,[(icon_x-10,icon_y-10),
                                    (icon_x+10,icon_y-10), (icon_x+10,icon_y),
                                    (icon_x,icon_y)],4)
    elif ttype == "community":
        pygame.draw.rect(screen,(0,120,255),
                         (icon_x-15,icon_y,30,20),2)
        pygame.draw.rect(screen,(0,120,255),
                         (icon_x-15,icon_y-8,30,10),2)
        pygame.draw.rect(screen,(0,120,255),
                         (icon_x-4,icon_y+10,8,8))
def draw_board():
    for i,(x,y) in enumerate(tile_positions):
        draw_tile(i,x,y)

back_rect = pygame.Rect(w//2 - 50, h - 180, 100, 50)

def main_board():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return  
        screen.fill(WHITE)
        draw_board()
        if logo_image:
            screen.blit(logo_image, ((w-logo_image.get_width())//2, (h-logo_image.get_height())//2))
        pygame.draw.rect(screen, BLACK, back_rect)
        draw_text_centered("BACK", button_font, WHITE, screen, back_rect.centerx, back_rect.centery)
        pygame.display.update()
        clock.tick(60)
        
def main():
    while True:
        result = mainscreen()
        if result == "play":
            choice = choice_screen()
            if choice != "back":
                player_game(choice)
                main_board()

if __name__ == "__main__":
    main()



