import pygame
import random
import time
import sys,subprocess
from login_page import w
print(w)
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
<<<<<<< HEAD
        
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
=======
       
main_board()
    
>>>>>>> edcf2c86f49ce4befd9747d2423019ea9ae8f586
