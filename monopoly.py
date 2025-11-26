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
class Bank:
    def __init__(self):
        self.notes={500: 50, 100: 50, 50: 50, 20: 50, 10: 50, 1: 50}
        
    def total_money(self):
        return sum(den * i for den, i in self.notes.items())
    
    def withdraw(self, amount):
        result = {}
        for den in sorted(self.notes.keys(), reverse = True):
            if amount <= 0:
                break
            needed = amount // den
            take = min(needed, self.notes[den])
            if take > 0:
                result[den] = take
                self.notes[den] -= take
                amount -= take*den
            if amount>0:
                for den, i in result.items():
                    self.notes[den] += i
                return None
            return result
        
    def deposit(self, notes_dict):
        for den, i in notes_dict.items():
            self.notes[den] += i
            

        
class Player:
    def __init__(self, name, colour, bank):
        self.name = name
        self.colour = colour
        self.properties = []
        self.money = {}
        start_cash = 1500
        notes = bank.withdraw(start_cash)
        self.money = notes
        self.position = 0

    def total_money(self):
        return sum(den * i for den, i in self.money.items())

    def receive_money(self, bank, amount):
        notes = bank.withdraw(amount)
        if notes is None:
            print(f"{self.name} cannot receive exact amount from bank")
            return False
        for den, i in notes.items():
            self.money[den] = self.money.get(den, 0) + count
        return True

    def pay_money(self, bank, amount):
        if self.total_money() < amount:
            print(f"{self.name} does not have enough money")
            return False

        payment = {}
        remaining = amount
        for den, i in sorted(self.money.keys(), reverse = True):
            if remaining <=0:
                break
            available = self.money[den]
            needed = remaining // den
            take = min(needed, available)
            if take > 0:
                payment[den] = take
                self.money[den] -= take
                remaining -= take*den
        if remaining > 0:
            print(f"{self.name} cannot pay exact amount")
            for den, i in payment.items():
                self.money[den] += i
            return False
        
        bank.deposit(payment)
        return True
    
    def add_property(self, property_space):
        self.properties.append(property_space)

def roll_dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    total = die1 + die2
    doubles = (die1 == die2)
    return total, doubles

if __name__ == "__main__":
    main()



