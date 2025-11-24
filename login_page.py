'''import customtkinter as ctk'''
import random
import pygame
import tkinter as tk
import time
import os
pygame.init()
property_brown=['OLD KENT ROAD','WHITECHAPEL ROAD']
property_light_blue=['THE ANGEL ISLINGTON','EUSTON ROAD','PENTONVILLE ROAD']
property_pink=['PALL MALL','WHITEHALL','NORTHUMBERLAND AVENUE']
property_orange=['BOW STREET','MARLBOROUGH STREET','VINE STREET']
property_red=['STRAND','FLEET STREET','TRAFALGAR SQUARE']
property_yellow=['LEICESTER SQUARE','COVENTRY STREET','PICCADILLY']
property_green=['REGENT STREET','OXFORD STREET','BOND STREET']
property_dark_blue=['PARK LANE','MAYFAIR']
property_railway=['KINGS CROSS STATION','MARYLEBONE STATION','FENCHURCH ST. STATION','LIVERPOOL ST. STATION']
property_utilities=['ELECTRIC COMPANY','WATER WORKS']
chance_community=['CHANCE','COMMUNITY CHEST']
free_parking=['FREE PARKING']
jail=['GO TO JAIL']
go=['GO']
visit=['JUST VISITING']
income_tax=['INCOME TAX']
super_tax=['SUPER TAX']


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


import random
import pygame
import tkinter as tk
import time
import os
pygame.init()
property_brown=['OLD KENT ROAD','WHITECHAPEL ROAD']
property_light_blue=['THE ANGEL ISLINGTON','EUSTON ROAD','PENTONVILLE ROAD']
property_pink=['PALL MALL','WHITEHALL','NORTHUMBERLAND AVENUE']
property_orange=['BOW STREET','MARLBOROUGH STREET','VINE STREET']
property_red=['STRAND','FLEET STREET','TRAFALGAR SQUARE']
property_yellow=['LEICESTER SQUARE','COVENTRY STREET','PICCADILLY']
property_green=['REGENT STREET','OXFORD STREET','BOND STREET']
property_dark_blue=['PARK LANE','MAYFAIR']
property_railway=['KINGS CROSS STATION','MARYLEBONE STATION','FENCHURCH ST. STATION','LIVERPOOL ST. STATION']
property_utilities=['ELECTRIC COMPANY','WATER WORKS']
chance_community=['CHANCE','COMMUNITY CHEST']
free_parking=['FREE PARKING']
jail=['GO TO JAIL']
go=['GO']
visit=['JUST VISITING']
income_tax=['INCOME TAX']
super_tax=['SUPER TAX']


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

main()
pygame.quit()
    

