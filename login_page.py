import customtkinter as ctk
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

#card width and height
card_width=80
card_height=160
screen=pygame.display.set_mode((600,400))
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
       screen.fill((0,255,0))
       font=pygame.font.Font(None,24)
       screen.blit(image,(120,75))
       rect=pygame.draw.rect(screen, (255,0,0), (125,225,350,100))
       text=font.render("WELCOME TO MONOPOLY: PLAY A GAME", True, (255,255,255))
       text_rect=text.get_rect(center=rect.center)
       screen.blit(text,text_rect)
       pygame.display.update()

mainscreen()
pygame.quit()
    

