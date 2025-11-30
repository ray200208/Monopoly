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
button_font = pygame.font.Font(None, 30)
popup_font = pygame.font.Font(None, 40)        
normal_font = pygame.font.Font(None, 20)
big_font = pygame.font.Font(None, 48)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,200,0)

HOUSE_COSTS = {
    "brown": 50,
    "lightblue": 50,
    "pink": 100,
    "orange": 100,
    "red": 150,
    "yellow": 150,
    "green": 200,
    "darkblue": 200}

color_counts = {
    "brown": 2,
    "lightblue": 3,
    "pink": 3,
    "orange": 3,
    "red": 3,
    "yellow": 3,
    "green": 3,
    "darkblue": 2,
    "station": 4, 
    "utility": 2 
}
    
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

back_rect = pygame.Rect(w//2-50, h-180, 100,50)
back_button_rect = pygame.Rect(0,0,0,0)

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

def button(text, x, y, w_rect, h_rect, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    rect=pygame.Rect(x,y,w_rect,h_rect)
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

def name_entry_screen(num_players):
    names = [""]*num_players
    active_input=0
    input_rects = [pygame.Rect(w//2-100,150+i*70,200,50) for i in range(num_players)]

    start_button_rect=pygame.Rect(w//2-75, 150+num_players*70, 150,50)

    list_colours = ['Blue', "Yellow", 'Green', 'Red']
    assigned_colours=[]
    for i in range(num_players):
        color=random.choice(list_colours)
        list_colours.remove(color)
        assigned_colours.append(color)

    cursor_visible = True
    cursor_timer=0
    cursor_interval=500

    while True:
        screen.fill(GREEN)
        draw_text_centered("Enter Player Names", big_font, WHITE, screen, w//2,80)

        for i in range(num_players):
            if active_input ==i:
                color='#FFD700'
            else:
                color=WHITE
            pygame.draw.rect(screen, color, input_rects[i])
            pygame.draw.rect(screen, color, input_rects[i],2)
            draw_text(names[i], normal_font, BLACK, screen, input_rects[i].x+10, input_rects[i].y+10)
            draw_text_centered(f"Color: {assigned_colours[i]}", normal_font, WHITE, screen, input_rects[i].right+100, input_rects[i].centery)

            if active_input==i and cursor_visible:
                text_width= normal_font.size(names[i])[0]
                cursor_x=input_rects[i].x+10+text_width
                cursor_y=input_rects[i].y+5
                pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y+input_rects[i].height-10),2)
                
        pygame.draw.rect(screen, RED, start_button_rect)
        draw_text_centered("START", normal_font, WHITE, screen, start_button_rect.centerx, start_button_rect.centery)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                active_input = None
                for i, rect in enumerate(input_rects):
                    if rect.collidepoint(event.pos):
                        active_input=i
                        break
                    
                if start_button_rect.collidepoint(event.pos):
                    if all(name.strip()!="" for name in names):
                        return names, assigned_colours
                    
            elif event.type==pygame.KEYDOWN:
                if active_input is not None:
                    if event.key==pygame.K_BACKSPACE:
                        names[active_input]=names[active_input][:-1]
                    elif event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                        if active_input<num_players-1:
                            active_input+=1
                        else:
                            if all(name.strip()!= '' for name in names):
                                return names, assigned_colours
                    elif len(names[active_input])<18:
                        names[active_input]+=event.unicode

        cursor_timer+=clock.get_time()
        if cursor_timer>=cursor_interval:
            cursor_visible=not cursor_visible
            cursor_timer=0

        pygame.display.update()
        clock.tick(60)
                    
                                                            
def player_game(num_players):
    names, colors = name_entry_screen(num_players)
    start_game(num_players, names, colors)

class Space:
    def __init__(self, name, type, price=0, rent=0, rent_1=0, rent_2=0, rent_3=0,
                 rent_4=0, rent_hotel=0, house_price=0, hotel_price=0, color=None):
        self.name = name
        self.type = type
        self.price = price
        self.owner = None
        self.color = color
        self.houses = 0
        self.hotel = False
        self.is_mortgaged = False
        self.all_rents = {0: rent, 1:rent_1, 2:rent_2, 3:rent_3, 4:rent_4, 5:rent_hotel}
        self.house_price=house_price
        self.hotel_price=hotel_price
        self.mortgage_value=price//2 if price>0 else 0
        self.unmortgage_value=self.mortgage_value + self.mortgage_value*110/100

    def get_current_rent(self, owner_has_monopoly):
        if self.is_mortgaged:
            return 0
        rent_key = 5 if self.hotel else self.houses
        current_rent = self.all_rents.get(rent_key, 0)
        if rent_key == 0 and owner_has_monopoly:
            return current_rent*2

        return current_rent

board = [
    Space("Go",'go'),
    Space('Old Kent Road','property',60,2,4,10,30,90,160,250, color='brown'),
    Space("Community Chest","community"),
    Space("Whitechapel Road","property",60,4,8,20,60,180,320,450,color='brown'),
    Space("Income Tax","incometax"),
    Space("King's Cross Station","station",200,25, color='station'),
    Space("The Angel Islington","property",100,6,12,30,90,270,400,550,color='lightblue'),
    Space("Chance","chance"),
    Space("Euston Road","property",100,6,12,30,90,270,400,550,color='lightblue'),
    Space("Pentonville Road","property",120,8,16,40,100,300,450,600,color='lightblue'),
    Space("Jail/Just Visiting","jail"),
    Space("Pall Mall","property",140,10,20,50,150,450,625,750,color='pink'),
    Space("Electric Company","utility",150),
    Space("Whitehall","property",140,10,20,50,150,450,625,750,color='pink'),
    Space("Northumberland Avenue","property",160,12,24,60,180,500,700,900,color='pink'),
    Space("Marylebone Station","station",200,25,color='station'),
    Space("Bow Street","property",180,14,28,70,200,550,750,950,color='orange'),
    Space("Community Chest","community"),
    Space("Marlborough Street","property",180,14,28,70,200,550,750,950,color='orange'),
    Space("Vine Street","property",200,16,32,80,220,600,800,1000,color='orange'),
    Space("Free Parking","parking"),
    Space("Strand","property",220,18,36,90,250,700,875,1050,color='red'),
    Space("Chance","chance"),
    Space("Fleet Street","property",220,18,36,90,250,700,875,1050,color='red'),
    Space("Trafalgar Square","property",240,20,40,100,300,750,925,1100,color='red'),
    Space("Fenchurch Street Station","station",200,25,color='station'),
    Space("Leicester Square","property",260,22,44,110,330,800,975,1150,color='yellow'),
    Space("Coventry Street","property",260,22,44,110,330,800,975,1150,color='yellow'),
    Space("Water Works","utility",150),
    Space("Piccadilly","property",280,24,48,120,360,850,1025,1200,color='yellow'),
    Space("Go To Jail","gotojail"),
    Space("Regent Street","property",300,26,52,130,390,900,1100,1275,color='green'),
    Space("Oxford Street","property",300,26,52,130,390,900,1100,1275,color='green'),
    Space("Community Chest","community"),
    Space("Bond Street","property",320,28,56,150,450,1000,1200,1400,color='green'),
    Space("Liverpool Street Station","station",200,25,color='station'),
    Space("Chance","chance"),
    Space("Park Lane","property",350,35,70,175,500,1100,1300,1500, color='darkblue'),
    Space("Super Tax","supertax"),
    Space("Mayfair","property",400,50,100,200,600,1400,1700,2000,color='darkblue')
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

board_w= w*9//11
board_h=h
tile_width = board_w//11
tile_height = board_h//11
tile_positions = []
x_start = board_w - tile_width
y_start = board_h - tile_height

for i in range(11):
    x = board_w - (i+1)*tile_width
    y = board_h - tile_height
    tile_positions.append((x,y))

for i in range(1,10):
    x = 0
    y = board_h - (i+1)*tile_height
    tile_positions.append((x,y))

for i in range(11):
    x = i*tile_width
    y = 0
    tile_positions.append((x,y))

for i in range(1,10):
    x = board_w - tile_width
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
        
def draw_board(current_player_index):
    screen.fill((220.,220,220))
    for i,(x,y) in enumerate(tile_positions):
        draw_tile(i,x,y)
    if logo_image:
        screen.blit(logo_image, ((board_w-logo_image.get_width())//2, (board_h-logo_image.get_height())//2))

    for index, player in enumerate(players):
        px,py=tile_positions[player.position]
        offset_x=5+(index%2)*20
        offset_y=5+(index//2)*20
        colour_map = {"Blue": (0,0,255), "Red": (255,0,0), "Green": (0,200,0), "Yellow": (255,255,0)}
        pygame.draw.circle(screen, colour_map[player.colour],(px+offset_x+15, py+offset_y+15),10)

    properties_button_rect, build_bt_rect=main_panel(current_player_index)
    return properties_button_rect, build_bt_rect
    
def main_panel(current_player_index):
    fonts=(normal_font, normal_font)
    
    panel_width = w-board_w-40
    panel_height = 180
    panel_x = board_w+20
    panel_y = 20
    button_w=120
    button_h=30
    button_x=panel_x+(panel_width-button_w)//2
    button_y=panel_y+panel_height-35
    build_bt_w=120
    build_bt_h=30
    build_bt_x=panel_x+(panel_width-build_bt_w)//2
    build_bt_y=panel_y+panel_height-70
    build_bt_rect=pygame.Rect(build_bt_x, build_bt_y, build_bt_w, build_bt_h)

    pygame.draw.rect(screen, (220, 255, 220),
                     (panel_x, panel_y, panel_width, panel_height),
                     border_radius=12)
    pygame.draw.rect(screen, (0, 0, 0),
                     (panel_x, panel_y, panel_width, panel_height), 3,
                     border_radius=12)

    player = players[current_player_index]

    draw_text(f"Player: {player.name}", normal_font, (0, 0, 0),
              screen, panel_x + 15, panel_y + 10)

    pygame.draw.rect(screen, pygame.Color(player.colour),
                     (panel_x + 15, panel_y + 45, 30, 30))
    draw_text(f"Colour", normal_font, (0, 0, 0),
              screen, panel_x + 55, panel_y + 50)

    draw_text(f"Money: ${player.total_money()}", normal_font, (0, 0, 0),
              screen, panel_x + 15, panel_y + 90)

    
    properties_button_rect = pygame.Rect(button_x, button_y,button_w, button_h)
    pygame.draw.rect(screen, BLUE, properties_button_rect)

    draw_text_centered("PROPERTIES", normal_font, WHITE,
              screen, properties_button_rect.centerx, properties_button_rect.centery)
    pygame.draw.rect(screen, GREEN, build_bt_rect)
    draw_text_centered("BUILD", normal_font, WHITE, screen, build_bt_rect.centerx, build_bt_rect.centery)
    return properties_button_rect, build_bt_rect

def properties_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return

        prop_panel()
        pygame.display.update()
        clock.tick(60)

def prop_panel():
    screen.fill((210,210,210))
    draw_text_centered("All Player Properties", big_font, BLACK, screen, w//2, 40)
    x=50
    y=100
    for player in players:
        draw_text(player.name, big_font, BLACK, screen, x,y)
        y+=40

        if not player.properties:
            draw_text("-None-", normal_font, BLACK, screen, x+40, y)
            y+=25
        else:
            for p in player.properties:
                draw_text(f"{p.name}", normal_font, BLACK, screen, x+40,y)
                y+=25
        y+=25

    global back_button_rect
    back_button_rect=pygame.Rect(w-160, h-80, 140,50)
    pygame.draw.rect(screen, (255,180,180), back_button_rect)
    pygame.draw.rect(screen, BLACK, back_button_rect, 2)
    draw_text_centered("Back", normal_font, BLACK, screen, back_button_rect.centerx, back_button_rect.centery)
    return back_button_rect

def main_board():
    global properties_button_rect
    while True:
        properties_button_rect = draw_board(current_player_index)

        if logo_image:
            screen.blit(logo_image, ((board_w-logo_image.get_width())//2, (board_h-logo_image.get_height())//2))
        pygame.draw.rect(screen, BLACK, back_rect)
        draw_text_centered("BACK", button_font, WHITE, screen, back_rect.centerx, back_rect.centery)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return

                if properties_button_rect.collidepoint(event.pos):
                    properties_window()

                clock.tick(60)
    
class Bank:
    def __init__(self):
        self.total_money=5000000000
        self.notes={}
        self.denominations = [500,100,50,20,10,5,1]

    def deposit(self, amount):
        self.total_money+=amount

    def withdraw(self, amount):
        if amount<=0:
            return {}
        if self.total_money<amount:
            return None
        notes={}
        remaining=amount
        for d in self.denominations:
            count = remaining // d
            if count > 0:
                notes[d] = count
                remaining -= count * d
        
        self.total_money -= amount
        
        return notes
        
class Player:
    def __init__(self, name, colour, bank):
        self.name = name
        self.colour = colour
        self.properties = []
        self.money=bank.withdraw(2000)
        self.position = 0
        self.in_jail = False
        self.jail_turns = 0
        self.has_get_out_of_jail=0
        self.is_bankrupt = False
        self.houses=0
        self.hotel=False

    def total_money(self):
        total=0
        return sum(den * i for den, i in self.money.items())

    def receive_money(self, bank, amount):
        notes = bank.withdraw(amount)
        if notes is None:
            return False
        for den, i in notes.items():
            self.money[den] = self.money.get(den, 0) + i
        return True

    def pay_money(self, receiver, amount, bank):
        if self.total_money() < amount:
            return False
        remaining_amount = self.total_money() - amount
        self.money={}
        self.receive_money(bank, remaining_amount)
        if isinstance(receiver, Bank):
            receiver.deposit(amount)
        else:
            receiver.receive_money(bank, amount)
        return True
    
    def add_property(self, property_space):
        self.properties.append(property_space)

    def get_property_group(self, color):
        return [prop for prop in self.properties if prop.color == color]

    def has_monopoly(self, color):
        global color_counts
        if color in color_counts:
            owned_count=len(self.get_property_group(color))
            total_count=color_counts.get(color, 0)
            return owned_count == total_count
        
        return False

def draw_dice(die1,die2,x,y):
    if 1 <= die1 <= 6 and dice_images[die1 - 1]:
        screen.blit(dice_images[die1 - 1], (x, y))
    else:
        pygame.draw.rect(screen, WHITE, (x,y,50,50))
        draw_text(str(die1), normal_font, BLACK, screen, x+15, y+10)
            
    if 1 <= die2 <= 6 and dice_images[die2 - 1]:
        screen.blit(dice_images[die2 - 1], (x + 60, y))
    else:
        pygame.draw.rect(screen, WHITE, (x+60,y,50,50))
        draw_text(str(die2), normal_font, BLACK, screen, x+75, y+10)

def roll_dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    total = die1 + die2
    doubles = (die1 == die2)
    return (die1, die2, total, doubles)

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
    ('Pay 20 for birth of first child', -20),
    ('Go to jail', 'jail'),
    ('Advance to Go', 'go'),
    ('Get out of jail', 'free'),
    ('Pay 100 for each house you have as maintenance', -100)]

def overlay_message(message, duration=1200, wait_for_ok=False):
    overlay = pygame.Surface((w,h))
    overlay.set_alpha(200)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))
    draw_text_centered(message, popup_font, WHITE, screen, w//2, h//2-40)
    ok_button = pygame.Rect(w//2-40, h//2+20, 80, 40)

    if wait_for_ok:
        pygame.draw.rect(screen, GREEN, ok_button)
        draw_text_centered("OK", normal_font, WHITE, screen, ok_button.centerx, ok_button.centery)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if ok_button.collidepoint(event.pos):
                        return
            clock.tick(60)
    else:
        pygame.display.update()
        pygame.time.delay(duration)

def apply_card_effect(player, bank, card):    
    description = card[0]
    effect = card[1]
    overlay_message(f"Card: {description}", wait_for_ok=True) 

    if description == 'Pay 200 per hotel for maintenance': 
        cost = get_total_maintenance_cost(player, house_rate=0, hotel_rate=200)
        
        if cost > 0:
            overlay_message(f"{player.name} owes ${cost} for hotel maintenance.", duration=1200)
            
            if not player.pay_money(bank, cost, bank): 
                if handle_debt(player, bank, cost, bank):
                    overlay_message(f"{player.name} successfully paid maintenance after mortgaging.", duration=1200)
                else:
                    return 
        else:
            overlay_message(f"{player.name} has no hotels.", duration=1000)
    
    elif description == 'Pay 100 for each house you have as maintenance':
        cost = get_total_maintenance_cost(player, house_rate=100, hotel_rate=0)
        
        if cost > 0:
            overlay_message(f"{player.name} owes ${cost} for house maintenance.", duration=1200)
            
            if not player.pay_money(bank, cost, bank): 
                if handle_debt(player, bank, cost, bank):
                    overlay_message(f"{player.name} successfully paid maintenance after mortgaging.", duration=1200)
                else:
                    return 
        else:
            overlay_message(f"{player.name} has no houses.", duration=1000)

    elif effect == 'go':
        player.position = 0
        player.receive_money(bank, 200)
        overlay_message(f"{player.name} advances to GO! Collect $200", duration=1200)
            
    elif effect == 'jail':
        player.position = 10
        player.in_jail = True
        player.jail_turns = 0
        overlay_message(f"{player.name} goes to Jail!", duration=1200)
        
    elif effect == 'free':
        player.has_get_out_of_jail+=1
        overlay_message(f"{player.name} got a Get Out of Jail card", duration = 1200)

        
    elif isinstance(effect,int) and effect > 0:
        player.receive_money(bank, effect)
        overlay_message(f"{player.name} receives ${effect} due to the card", duration=1200)
            
    elif isinstance(effect,int) and effect < 0:
        cost = -effect
        overlay_message(f"{player.name} pays ${cost} due to the card", duration=1200)
        
        if not player.pay_money(bank, cost, bank):
            if handle_debt(player, bank, cost, bank):
                overlay_message(f"{player.name} successfully paid the fee after mortgaging.", duration=1200)
            else:
                return

def get_total_maintenance_cost(player, house_rate, hotel_rate):
    total_cost = 0
    for prop in player.properties:
        if prop.type == 'property':
            total_cost += prop.houses * house_rate
            if prop.hotel:
                total_cost += hotel_rate
    return total_cost
            
def draw_chance(player, bank):
    card = random.choice(chance_cards)
    overlay_message(f"Chance Card : {card[0]}", duration = 1200)
    apply_card_effect(player, bank, card)

def draw_community(player, bank):
    card = random.choice(community_chest_cards)
    overlay_message(f"Community Chest Card : {card[0]}", duration =1200)
    apply_card_effect(player, bank, card)

def calculate_utility_rent(owner, dice_roll):
    count = sum(1 for p in owner.properties if p.type == 'utility')
    return dice_roll*4 if count == 1 else dice_roll*10

def calculate_station_rent(owner):
    count = sum(1 for p in owner.properties if p.type == 'station')
    return 25*count

def handle_debt(debtor, receiver, amount, bank):
    while debtor.total_money()<amount:
        mortgageable_props=[p for p in debtor.properties if not p.is_mortgaged and p.houses==0 and not p.hotel]
        if not mortgageable_props:
            debtor.is_bankrupt=True
            overlay_message(f"{debtor.name} is bankrupt! ALL assets forfeited to {receiver.name}", duration = 2000, wait_for_ok=True)

            if not isinstance(receiver, Bank):
                for prop in debtor.properties:
                    prop.owner= receiver
            debtor.money={}
            return False
        overlay_message(f"{debtor.name}, you owe ${amount}, you must mortgage properties", wait_for_ok=True)
        mortgage_prop=min(mortgageable_props, key=lambda p: p.mortgage_value)
        mortgafe_prop.is_mortgaged=True
        debtor.receive_money(bank, mortgage_prop.mortgage_value)
        overlay_message(f"{debtor.name} has mortgaged {mortgage_prop.name} for ${mortgage_prop.mortgage_value}", duration=1500)

    debtor.pay_money(receiver, amount, bank)
    return True

def handle_space(player, space, bank, dice_roll = 0):
    if space.type == 'property':
        if space.owner is None:
            choice = player_choice(player, f"Buy {space.name} for ${space.price}?")
            if choice == 'yes':
                if player.total_money() < space.price:
                    overlay_message(f"Not enough money to buy {space.name}", duration=1200)
                elif player.pay_money(bank, space.price, bank):
                    player.add_property(space)
                    space.owner = player
                    overlay_message(f"{player.name} bought {space.name}", duration=1200)
                else:
                    overlay_message(f"{player.name} failed to complete transaction", duration=1200)
            else:
                overlay_message(f"{player.name} declined to buy {space.name}", duration=1200)
                
        elif space.owner!=player:
            rent = space.get_current_rent(space.owner.has_monopoly(space_color))
            overlay_message(f"{player.name} pays rent to {space.owner.name}", duration=1200)
            if player.pay_money(sapce.owner,rent, bank):
                pass
            else:
                if handle_debt(player, space.owner, rent, bank):
                    overlay_message(f"{player.name} has paid rent after liquidation of assets", duration = 1200)
                else:
                    return

    elif space.type == 'station':
        if space.owner is None:
            choice = player_choice(player, f"Buy {space.name} for {space.price}?")
            if choice == 'yes':
                if player.total_money() < space.price:
                    overlay_message(f"Not enough money to buy {space.name}", duration=1200)
                elif player.pay_money(bank, space.price, bank):
                    player.add_property(space)
                    space.owner = player
                    overlay_message(f"{player.name} bought {space.name}", duration=1200)
                else:
                    overlay_message(f"{player.name} failed to complete transaction", duration=1200)
            else:
                overlay_message(f"{player.name} declined to buy {space.name}", duration=1200)
        
        elif space.owner!=player:
            rent = space.get_current_rent(space.owner.has_monopoly(space_color))
            overlay_message(f"{player.name} pays rent to {space.owner.name}", duration=1200)
            if player.pay_money(sapce.owner,rent, bank):
                pass
            else:
                if handle_debt(player, space.owner, rent, bank):
                    overlay_message(f"{player.name} has paid rent after liquidation of assets", duration = 1200)
                else:
                    return
         
    elif space.type == 'utility':
        if space.owner is None:
            choice = player_choice(player, f"Buy {space.name} for {space.price}?")
            if choice=='yes':
                if player.total_money() < space.price:
                    overlay_message(f"Not enough money to buy {space.name}", duration=1200)
                elif player.pay_money(bank, space.price, bank):
                    player.add_property(space)
                    space.owner = player
                    overlay_message(f"{player.name} bought {space.name}", duration=1200)
                else:
                    overlay_message(f"{player.name} failed to complete transaction", duration=1200)
            else:
                overlay_message(f"{player.name} declined to buy {space.name}", duration=1200)
            
        elif space.owner!=player:
            rent = space.get_current_rent(space.owner.has_monopoly(space_color))
            overlay_message(f"{player.name} pays rent to {space.owner.name}", duration=1200)
            if player.pay_money(sapce.owner,rent, bank):
                pass
            else:
                if handle_debt(player, space.owner, rent, bank):
                    overlay_message(f"{player.name} has paid rent after liquidation of assets", duration = 1200)
                else:
                    return
        

    elif space.type == 'incometax':
        overlay_message(f"{player.name} pays tax of 200",duration=1200)
        if player.pay_money(bank, 200, bank):
            pass
        else:
            if handle_debt(player, bank, 200, bank):
                overlay_message(f"{player.name} has paid tax after liquidation of assets", duration = 1200)
            else:
                return

    elif space.type == 'supertax':
        overlay_message(f"{player.name} pays tax of 100", duration = 1200)
        if player.pay_money(bank, 100, bank):
            pass
        else:
            if handle_debt(player, bank, 100, bank):
                overlay_message(f"{player.name} has paid tax after liquidation of assets", duration = 1200)
            else:
                return

    elif space.type == 'chance':
        draw_chance(player, bank)

    elif space.type == 'community':
        draw_community(player, bank)

    elif space.type == 'jail':
        if not player.in_jail:
            overlay_message(f"{player.name} is just visiting jail", duration=1200)
        else:
            if player.has_get_out_of_jail>0:
                overlay_message(f"{player.name} has used one get out of jail free card")
                player.has_get_out_of_jail-=1

    elif space.type == 'parking':
        overlay_message(f"{player.name} has landed on Free Parking! Collect 100", duration=1200)
        player.receive_money(bank, 100)

def manage_property_development(player, bank):
    if open_development_window(player, bank):
        pass

def open_development_window(player, bank):
    global screen, w, h, clock, normal_font, popup_font, button_font
    win_w, win_h = w*0.7, h*0.7
    win_x, win_y= (w-win_w)//2, (h-win_h)//2
    win_rect=pygame.Rect(win_x, win_y, win_w, win_h)
    win_surf=pygame.Surface((win_w,win_h))

    monopolies = {}
    owned_colors={prop.color for prop in player.properties if prop.color}

    for color in owned_colors:
        if player.has_monopoly(color):
            monopolies[color]=player.get_property_group(color)
            
    if not monopolies:
        overlay_message(f"{player.name} does not own any monopolies to develop", duration=1200)
        return False

    running=True
    while running:
        win_surf.fill((240,240,240))
        pygame.draw.rect(win_surf, (200,200,200), (0,0,win_w,win_h),5)
        draw_text_centered("PROPERTY DEVELOPMENT", popup_font, BLACK,win_surf, win_w//2, 20)

        close_bt_rect=pygame.Rect(win_w-70,10,60,30)
        pygame.draw.rect(win_surf, RED, close_bt_rect)
        draw_text_centered("CLOSE", normal_font, WHITE, win_surf, close_bt_rect.centerx, close_bt_rect.centery)
        y_pos=60
        button_rects={}
        for color, props in monopolies.items():
            
            
            draw_text_centered(f"Group: {color.upper()} (House Cost: ${props[0].house_price})", 
                               button_font, BLACK, win_surf, win_w // 2, y_pos)
            y_pos += 30
            
            for prop in props:
                rent = prop.get_current_rent(True)
                status = f"{prop.houses} H / {'Htl' if prop.hotel else '0'}"
                mortgage_status = " (MORTGAGED)" if prop.is_mortgaged else ""
                
               
                min_houses = min(p.houses for p in props)
                can_build = prop.houses == min_houses and prop.houses < 4
                
                text_color = BLACK
                if not can_build and prop.houses < 4 and not prop.hotel:
                    text_color = (200, 0, 0) 
                if prop.hotel:
                    text_color = BLUE

                draw_text_centered(f"{prop.name}: Rent=${rent} Status: {status}{mortgage_status}", 
                                   normal_font, text_color, win_surf, win_w // 2 - 150, y_pos, align_left=True)
                
                
                house_btn_rect = pygame.Rect(win_w - 200, y_pos - 10, 80, 25)
                house_enabled = not prop.is_mortgaged and not prop.hotel and prop.houses < 4 and prop.houses == min_houses
                
                if house_enabled:
                    pygame.draw.rect(win_surf, GREEN, house_btn_rect)
                    draw_text_centered("Buy House", normal_font, WHITE, win_surf, house_btn_rect.centerx, house_btn_rect.centery)
                    button_rects[(prop.name, 'house')] = (house_btn_rect, prop, props)
                else:
                    pygame.draw.rect(win_surf, (150, 150, 150), house_btn_rect)
                    draw_text_centered("N/A", normal_font, BLACK, win_surf, house_btn_rect.centerx, house_btn_rect.centery)

            
                hotel_btn_rect = pygame.Rect(win_w - 110, y_pos - 10, 80, 25)
                hotel_enabled = not prop.is_mortgaged and prop.houses == 4 and not prop.hotel
                
                if hotel_enabled:
                    pygame.draw.rect(win_surf, BLUE, hotel_btn_rect)
                    draw_text_centered("Buy Hotel", normal_font, WHITE, win_surf, hotel_btn_rect.centerx, hotel_btn_rect.centery)
                    button_rects[(prop.name, 'hotel')] = (hotel_btn_rect, prop, props)
                else:
                    pygame.draw.rect(win_surf, (150, 150, 150), hotel_btn_rect)
                    draw_text_centered("N/A", normal_font, BLACK, win_surf, hotel_btn_rect.centerx, hotel_btn_rect.centery)
                
                y_pos += 40
            y_pos += 10 

     
        screen.blit(win_surf, (win_rect.x, win_rect.y))
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                
                if close_btn_rect.collidepoint(mx - win_x, my - win_y):
                    running = False
                    break
                
            
                for key, (rect, prop, group_props) in button_rects.items():
                    action = key[1]
                    
                    if rect.collidepoint(mx - win_x, my - win_y):
                        
                        if prop.is_mortgaged:
                             overlay_message("Cannot build on a mortgaged property.", duration=1500)
                             break
                        
                        success = False
                        message = ""

                        if action == 'house':
                            success, message = handle_buy_house(player, bank, prop, group_props)
                        
                        elif action == 'hotel':
                            success, message = handle_buy_hotel(player, bank, prop, group_props)
                        
                        if success:
                            running = False
                            overlay_message(message, duration=2000)
                            return True
                        else:
                            overlay_message(message, duration=2000)
                            break
                            
        clock.tick(60)
        
    return False

def handle_buy_house(player, bank, prop, group_props):
    cost = prop.house_price
    min_houses = min(p.houses for p in group_props)
    
    if prop.houses > min_houses:
         return False, "You must build houses evenly. Build on other properties first."
        
    if player.total_money() < cost:
        return False, f"Not enough money (${cost}) to buy a house."

    if player.pay_money(bank, cost, bank):
        prop.houses += 1
        return True, f"House purchased on {prop.name}. Total: {prop.houses}"
    
    return False, "Transaction failed for unknown reason."

def handle_buy_hotel(player, bank, prop, group_props):
    cost = prop.house_price
    
    if prop.houses != 4:
        return False, "This property must have 4 houses before buying a hotel."

    
    if any(p.houses < 4 for p in group_props):
         return False, "All properties in the group must have 4 houses before buying a hotel."

    
    if player.total_money() < cost:
        return False, f"Not enough money (${cost}) to buy a hotel."

   
    if player.pay_money(bank, cost, bank):
        
        player.receive_money(bank, 4 * cost // 2) 
        prop.houses = 0
        prop.hotel = True
        return True, f"Hotel purchased on {prop.name}! Houses sold back."
    
    return False, "Transaction failed for unknown reason."    

def player_choice(player, message):
    overlay = pygame.Surface((w,h))
    overlay.set_alpha(190)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))
    
    yes_button = pygame.Rect(w//2 - 100, h//2, 80,50)
    no_button = pygame.Rect(w//2 + 20, h//2, 80,50)
    draw_text_centered(message, popup_font, WHITE, screen, w//2, h//2-80)
    pygame.draw.rect(screen, GREEN, yes_button)
    pygame.draw.rect(screen, RED, no_button)
    draw_text_centered("YES", normal_font, WHITE, screen, yes_button.centerx, yes_button.centery)
    draw_text_centered("NO", normal_font, WHITE, screen, no_button.centerx, no_button.centery)
    pygame.display.update()

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
        clock.tick(60)

    return choice_made

def show_message(message):
    overlay_message(message, wait_for_ok=True)
    

def player_turn(player, bank, turn_index):

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
            overlay_message(f"{player.name} skips turn in Jail",duration=1200)
            return
        

    doubles_count = 0
    while True:
        roll_button = pygame.Rect(board_w//2 - 50, board_h - 200, 100,50)
        rolled = False
        while not rolled:
            screen.fill(WHITE)
            properties_button_rect, build_bt_rect = draw_board(turn_index)
            pygame.draw.rect(screen, GREEN, roll_button)
            draw_text_centered("ROLL DICE", normal_font, WHITE, screen, roll_button.centerx, roll_button.centery)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my= event.pos
                    if roll_button.collidepoint(mx,my):
                        rolled = True
            
                    elif properties_button_rect.collidepoint(mx,my):
                        open_properties_window(players)
                    
                        properties_button_rect, build_bt_rect = draw_board(turn_index)

                    elif build_bt_rect.collidepoint(mx,my):
                        current_player= players[turn_index]
                        manage_property_development(current_player, bank)
            
            clock.tick(60)

        
        dice_x=roll_button.x+roll_button.width//2-60
        dice_y=roll_button.y-80

        for i in range(10):
            temp1, temp2 = random.randint(1,6), random.randint(1,6)
            draw_board(turn_index)
            draw_dice(temp1, temp2, dice_x, dice_y)
            pygame.draw.rect(screen, GREEN, roll_button)
            draw_text_centered("ROLL DICE", normal_font, WHITE, screen, roll_button.centerx, roll_button.centery)
            pygame.display.update()
            pygame.time.delay(60)

        d1,d2,total,doubles=roll_dice()
        die1,die2=d1,d2
        
        previous_pos = player.position
        player.position = (player.position + total) % len(board)

    
        draw_board(turn_index)
        draw_dice(die1, die2,dice_x, dice_y)
        pygame.display.update()
        pygame.time.delay(500)
    
        if player.position < previous_pos:
            overlay_message(f"{player.name} has passed Go! Collect $200", duration=1200)
            player.receive_money(bank, 200)
        
        space = board[player.position]
        handle_space(player, space, bank, total) 

        if doubles:
            doubles_count+=1
            if doubles_count == 3:
                overlay_message(f"{player.name} has rolled 3 doubles, go to jail",duration=1200)
                player.position = 10
                player.in_jail = True
                player.jail_turns = 0
                break
            else:
                overlay_message(f"{player.name} rolled doubles! Roll again", duration=1000)
        else:
            break

def open_properties_window(players):
    running = True
    W = 550
    H = 500
    font_title = pygame.font.Font(None, 40)
    font_sub = pygame.font.Font(None, 28)
    win_surf = pygame.Surface((W, H))
    win_rect = pygame.Rect(
        screen.get_width()//2 - W//2, screen.get_height()//2 - H//2, W, H
    )

    back_bt_w=200
    back_bt_h=40
    back_bt_x=win_rect.width-back_bt_w-10
    back_bt_y=win_rect.height-back_bt_h-10

    back_bt=pygame.Rect(back_bt_x, back_bt_y, back_bt_w, back_bt_h)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                screen_button_rect = pygame.Rect(win_rect.x + back_bt.x, win_rect.y + back_bt.y,
                                                 back_bt.width, back_bt.height)
                if screen_button_rect.collidepoint(mx,my):
                    running=False
                    return
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
        win_surf.fill((245, 245, 245))
        pygame.draw.rect(win_surf, (0, 0, 0), (0, 0, W, H), 3)
        pygame.draw.rect(win_surf, (150,0,100), back_bt)
        text=button_font.render("BACK TO BOARD", True, WHITE)
        text_rect=text.get_rect(center=back_bt.center)
        win_surf.blit(text, text_rect)

        title = font_title.render("ALL PLAYERS' PROPERTIES", True, (0, 0, 0))
        win_surf.blit(title, (20, 15))

        y = 80
        for player in players:
            header = font_sub.render(f"{player.name} ({player.colour}) ({player.total_money()})", True, (0, 0, 0))
            win_surf.blit(header, (20, y))
            y += 30

            if len(player.properties) == 0:
                no_prop = font_sub.render("  - No properties", True, (100, 100, 100))
                win_surf.blit(no_prop, (30, y))
                y += 30
                
            else:
                for prop in player.properties:
                    item = font_sub.render("  - " + prop.name, True, (50, 50, 50))
                    win_surf.blit(item, (30, y))
                    y += 28
            y += 18
            
        screen.blit(win_surf, (win_rect.x, win_rect.y))
        pygame.display.flip()
        clock.tick(60)
    
def start_game(num_players, player_names, player_colors):
    global players
    bank = Bank()
    players=[]
    for i in range(num_players):
        player= Player(player_names[i], player_colors[i], bank)
        players.append(player)
        player.jail_turns = 0
        player.in_jail = False

    turn_index = 0
    
    while True:
        screen.fill((220,220,220))
        draw_board(turn_index)
        pygame.display.update()
        player_turn(players[turn_index], bank, turn_index)
        turn_index = (turn_index + 1) % num_players

def main():
    while True:
        result = mainscreen()
        if result == 'play':
            choice = choice_screen()
            if choice != 'back':
                player_game(choice)

            
if __name__ == "__main__":
    main()



