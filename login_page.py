import pygame
import random
import sys,subprocess,os,pathlib
current_dir = pathlib.Path(__file__).parent.resolve()
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
            choice_screen()
            return 'play'
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
            player_game(2)
        if button("3 Player", w//2 - 50, 225, 100, 75, RED, BLUE):
            player_game(3)
        if button("4 Player", 3*w//4 - 50, 225, 100, 75, RED, BLUE):
            player_game(4)
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
                subprocess.Popen(['python',os.path.join(current_dir,'main.py')])
        else:
            pygame.draw.rect(screen,(0,150,0),play_button_rect)
        play_text=font.render('PLAY',True,(255,255,255))
        play_text_rect=play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text,play_text_rect)
        pygame.display.update()
        clock.tick(60)
mainscreen()
	
