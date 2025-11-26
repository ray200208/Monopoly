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

property_font = pygame.font.Font(None, 12)
menu_font = pygame.font.Font(None, 30)        
popup_font = pygame.font.Font(None, 40)        
normal_font = pygame.font.Font(None, 20)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,200,0)

dice_images = []
for i in range(1,7):
    try:
        img=pygame.image.load(f"dice{i}.png").convert()
        img = pygame.transform.scale(img, (50,50))
        dice_images.append(img)
    except Exception as e:
        print(f"Failed to load dice image dice{i}.png:",e)
        dice_images.append(None)
        
try:
    logo_image = pygame.image.load("monopoly_logo.jpeg").convert_alpha()
    logo_image = pygame.transform.scale(logo_image, (350, 175))
except Exception as e:
    print("Failed to load logo:", e)
    logo_image = None

def draw_text(text, font, color, surface, x, y, center = False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x,y)
    else:
        rect.topleft = (x,y)
    surface.blit(surf, rect)

def draw_text_centered(text, font, color, surface, x, y):
    draw_text(text, font, color, surface, x, y, center = True)

def button(text, x, y, w, h, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    rect=pygame.Rect(x,y,w,h)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, color, rect)

    text_surf = menu_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
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
    start_game(n)

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

    draw_text_centered(name, property_font, BLACK, screen, x + tile_width//2, name_y)


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
    if logo_image:
        screen.blit(logo_image, ((w-logo_image.get_width())//2, (h-logo_image.get_height())//2))

    for index, player in enumerate(players):
        px,py=tile_positions[player.position]
        offset_x=5+(index%2)*20
        offset_y=5+(index//2)*20
        pygame.draw.circle(screen, pygame.Color(player.colour),(px+offset_x+15, py+offset_y+15),10)

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
        

class Bank:
    def __init__(self):
        self.notes={500: 50, 100: 50, 50: 50, 20: 50, 10: 50, 1: 50}
        
    def total_money(self):
        return sum(den * i for den, i in self.notes.items())
    
    def withdraw(self, amount):
        result = {}
        original = self.notes.copy()
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
            self.notes = original
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
        self.in_jail = False
        self.jail_turns = 0

    def total_money(self):
        return sum(den * i for den, i in self.money.items())

    def receive_money(self, bank, amount):
        notes = bank.withdraw(amount)
        if notes is None:
            return False
        for den, i in notes.items():
            self.money[den] = self.money.get(den, 0) + i
        return True

    def pay_money(self, bank, amount):
        if self.total_money() < amount:
            return False

        payment = {}
        remaining = amount
        for den in sorted(self.money.keys(), reverse = True):
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
            for den, i in payment.items():
                self.money[den] += i
            return False
        
        bank.deposit(payment)
        return True
    
    def add_property(self, property_space):
        self.properties.append(property_space)

def draw_dice(die1,die2,x,y):
    if 1 <= die1 <= 6 and dice_images[die1 - 1]:
        screen.blit(dice_images[die1 - 1], (x, y))
    if 1 <= die2 <= 6 and dice_images[die2 - 1]:
        screen.blit(dice_images[die2 - 1], (x + 60, y))

def roll_dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    total = die1 + die2
    doubles = (die1 == die2)
    return total, doubles

chance_cards = [
    ('Bank pays you dividend', 50),
    ('Pay poor tax', -15),
    ('Pay 200 per hotel for maintenance', -200),
    ('Go to jail', 'jail'),
    ('Advance to Go', 'go'),
    ('School fees', -20),
    ('Get out of jail', 'free')]

community_chest_cards = [
    ('You inherit money', 100),
    ('You have been found convicted of felony', -50),
    ('Pay each player 20', -20),
    ('Go to jail', 'jail'),
    ('Advance to Go', 'go'),
    ('Get out of jail', 'free'),
    ('Pay 100 for each house you have as maintenance', -100)]

def apply_card_effect(player, bank, card):
    effect = card[1]
    if effect == 'go':
        player.position = 0
        player.receive_money(bank, 200)
        show_message(f"{player.name} advances to GO! Collect $200")
        
    elif effect == 'jail':
        player.position = 10
        player.in_jail = True
        player.jail_turns = 0
        if player.total_money()>=50:
            choice = player_choice(player, f"{player.name}, pay 50 to get out?")
            if choice == 'yes':
                player.pay_money(bank, 50)
                player.in_jail = False
                player.jail_turns = 0
            else:
                player.in_jail = True
                show_message(f"{player.name} goes to Jail!")

    elif effect > 0:
        player.receive_money(bank, effect)
        show_message(f"{player.name} receives ${effect} due to the card")

    elif effect < 0:
        player.pay_money(bank, -effect)
        show_message(f"{player.name} pays ${-effect} due to the card")

    elif effect == 'free':
        if player.position == 10:
            choice = player_choice(player, f"{player.name}, use your get out jail card?")
            if choice == 'yes':
                player.in_jail = False
                player.jail_turns = 0
            else:
                player.in_jail = True
        else:
            player.has_get_out_of_jail = True

def draw_chance(player, bank):
    card = random.choice(chance_cards)
    show_message(f"Chance Card : {card[0]}")
    apply_card_effect(player, bank, card)

def draw_community(player, bank):
    card = random.choice(community_chest_cards)
    show_message(f"Community Chest Card : {card[0]}")
    apply_card_effect(player, bank, card)

def calculate_utility_rent(owner, dice_roll):
    count = sum(1 for p in owner.properties if p.type == 'utility')
    return dice_roll*4 if count == 1 else dice_roll*10

def calculate_station_rent(owner):
    count = sum(1 for p in owner.properties if p.type == 'station')
    return 25*count

def handle_space(player, space, bank, dice_roll = 0):
    if space.type == 'property':
        if space.owner is None:
            choice = player_choice(player, f"Buy {space.name} for {space.price}?")
            if choice == 'yes' and player.total_money()>=space.price:
                player.pay_money(bank, space.price)
                player.add_property(space)
                space.owner = player
                print(f"{player.name} bought {space.name}")
                
        elif space.owner!=player:
            rent = space.rent
            print(f"{player.name} pays rent to {space.owner.name}")
            player.pay_money(bank,rent)
            space.owner.receive_money(bank, rent)

    elif space.type == 'station':
        if space.owner is None:
            choice = player_choice(player, f"Buy {space.name} for {space.price}?")
            if choice == 'yes' and player.total_money()>=space.price:
                player.pay_money(bank, space.price)
                player.add_property(space)
                space.owner = player
                print(f"{player.name} bought {space.name}")

        elif space.owner!=player:
            rent = calculate_station_rent(space.owner)
            print(f"{player.name} pays rent to {space.owner.name}")
            player.pay_money(bank, rent)
            space.owner.receive_money(bank, rent)

    elif space.type == 'utility':
        if space.owner is None:
            choice = player_choice(player, f"Buy {space.name} for {space.price}?")
            if choice == 'yes' and player.total_money()>=space.price:
                player.pay_money(bank, space.price)
                player.add_property(space)
                space.owner = player
                print(f"{player.name} bought {space.name}")

        elif space.owner!=player:
            rent = calculate_utility_rent(space.owner, dice_roll)
            print(f"{player.name} pays rent to {space.owner.name}")
            player.pay_money(bank, rent)
            space.owner.receive_money(bank, rent)

    elif space.type == 'tax':
        print(f"{player.name} pays tax of {space.rent}")
        player.pay_money(bank, space.rent)

    elif space.type == 'chance':
        draw_chance(player, bank)

    elif space.type == 'community':
        draw_community(player, bank)

    elif space.type == 'jail':
        if not player.in_jail:
            print(f"{player.name} is just visiting jail")

    elif space.type == 'parking':
        print(f"{player.name} has landed on Free Parking! Collect 100")
        player.receive_money(bank, 100)

def player_choice(player, message):
    yes_button = pygame.Rect(w//2 - 100, h//2, 80,50)
    no_button = pygame.Rect(w//2 + 20, h//2, 80,50)
    choice_made = None
    while choice_made is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    choice_made = 'yes'
                elif no_button.collidepoint(event.pos):
                    choice_made = 'no'

        overlay = pygame.Surface((w,h))
        overlay.set_alpha(200)
        overlay.fill((50,50,50))
        screen.blit(overlay, (0,0))

        draw_text_centered(message, popup_font, WHITE, screen, w//2, h//2-80)
        pygame.draw.rect(screen, GREEN, yes_button)
        pygame.draw.rect(screen, RED, no_button)
        draw_text("YES", normal_font, WHITE, screen, yes_button.centerx, yes_button.centery)
        draw_text("NO", normal_font, WHITE, screen, no_button.centerx, no_button.centery)

        pygame.display.update()
        clock.tick(60)

    return choice_made

def show_message(message):
    ok_button = pygame.Rect(w//2 - 40, h//2 + 30, 80,50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(event.pos):
                    return
                
        overlay = pygame.Surface((w,h))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))
        draw_text_centered(message, popup_font, WHITE, screen, w//2, h//2)
        pygame.draw.rect(screen, GREEN, ok_button)
        draw_text('OK', normal_font, WHITE, screen, ok_button.centerx, ok_button.centery)
        pygame.display.update()
        clock.tick(60)
        

def player_turn(player, bank):
    if player.in_jail:
        player.jail_turns+=1
        choice = player_choice(player, f"{player.name}, pay $50 to get out of jail?")
        if choice == 'yes' and player.total_money()>=50:
            player.pay_money(bank, 50)
            player.in_jail = False
            player.jail_turns = 0

        elif player.jail_turns >= 3:
            player.in_jail = False
            player.jail_turns = 0
        else:
            show_message(f"{player.name} skips turn in Jail")
            return
        
    doubles_count = 0
    while True:
        roll_button = pygame.Rect(w//2 - 50, h - 200, 100,50)
        rolled = False
        while not rolled:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if roll_button.collidepoint(event.pos):
                        rolled = True
            draw_board()
            pygame.draw.rect(screen, GREEN, roll_button)
            draw_text_centered("ROLL DICE", normal_font, WHITE, screen, roll_button.centerx, roll_button.centery)
            pygame.display.update()
            clock.tick(60)

        for i in range(10):
            temp1, temp2 = random.randint(1,6), random.randint(1,6)
            draw_board()
            draw_dice(temp1, temp2, w//2-50, h//2-50)
            pygame.draw.rect(screen, GREEN, roll_button)
            draw_text_centered("ROLL DICE", normal_font, WHITE, screen, roll_button.centerx, roll_button.centery)
            pygame.display.update()
            pygame.time.delay(30)

        die1, die2 = random.randint(1,6), random.randint(1,6)
        total = die1 + die2
        doubles = (die1==die2)
        
        previous_pos = player.position
        player.position = (player.position + total) % len(board)

        draw_board()
        draw_dice(die1, die2, w//2-50, h//2-50)
        pygame.display.update()
        pygame.time.delay(300)
    
        if player.position < previous_pos:
            show_message(f"{player.name} has passed Go! Collect 200")
            player.receive_money(bank, 200)
        
        space = board[player.position]
        handle_space(player, space, bank, total)

        if doubles:
            doubles_count+=1
            if doubles_count == 3:
                show_message(f"{player.name} has rolled 3 doubles, go to jail")
                player.position = 10
                player.in_jail = True
                player.jail_turns = 0
                break

            else:
                show_message(f"{player.name} rolled doubles! Roll again")

        else:
            break

def start_game(n):
    global players
    bank = Bank()
    list_colours = ['Blue', 'Yellow', 'Green', 'Red']
    players = []
    for i in range(n):
        colour = random.choice(list_colours)
        list_colours.remove(colour)
        player= Player(f"Player {i+1}", colour, bank)
        players.append(player)
        player.jail_turns = 0
        player.in_jail = False

    turn_index = 0
    while True:
        screen.fill(WHITE)
        draw_board()
        y = 170
        for p in players:
            draw_text_centered(f"{p.name} (${p.total_money()})", normal_font,
                               (0,0,0), screen, w//2, y)
            y+=30
        pygame.display.update()

        player_turn(players[turn_index], bank)
        turn_index = (turn_index + 1) % n

def main():
    while True:
        result = mainscreen()
        if result == 'play':
            choice = choice_screen()
            if choice != 'back':
                player_game(choice)

            
if __name__ == "__main__":
    main()



