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
    
def mainscreen():
   global screen
   running=True
   while running:
       for event in pygame.event.get():
           if event.type==pygame.QUIT:
               running=False
       screen.fill((0,200,0))
       screen.blit(image,(120,75))
       if button('PLAY A GAME',125,225,350,100,(255,0,0),(0,0,255)):
           choice_screen()
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
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        screen.fill((0,200,0))
        if button('2 Player',125,225,100,75,(255,0,0),(0,0,255)):
            two_player_game()
        elif button('3 Player',175,225,100,75,(255,0,0),(0,0,255)):
            three_player_game()
        elif button('4 Player',225,225,100,75,(255,0,0),(0,0,255)):
            four_player_game()
        pygame.display.update()

def two_player_game():
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        screen.fill((0,200,0))
    
mainscreen()
pygame.quit()
        
    

