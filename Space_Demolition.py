import sys
import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf



def run_space_game():
    #   Initialize pygame,settings And Create A Screen Object.
    pygame.init()
    df_settings = Settings()
    
    screen = pygame.display.set_mode(
        (df_settings.screen_width, df_settings.screen_height))
    pygame.display.set_caption("Space Demolition")
    #  Make the Icon
    icon = pygame.image.load("Images/icon.png")
    pygame.display.set_icon(icon)
   
    #  Make The Play Button
    play_button = Button(df_settings, screen, "PLAY ME")

    #  create an instance to store game statistics and create scoreboard
    stats = GameStats(df_settings)
    sb = Scoreboard(df_settings, screen, stats)

    #   Make A Ship
    ship = Ship(df_settings, screen) 
    #   Make a group to store all bullets and aliens
    bullets = Group()
    aliens = Group()
    #   Create a fleet of aliens
    gf.create_fleet(df_settings, screen, ship, aliens)
    #   make an Alien
    alien = Alien(df_settings, screen)

    # Starting The Main Loop For The Game.
    while True:
        #   Watch For Keyboard And Mosue Events.
        gf.check_events(df_settings, screen,stats, sb,play_button, ship, aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(df_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(df_settings, stats, screen, sb, ship, aliens, bullets)

            #   Set Color, Draw The Ship,alien, makes most recently screen visible during each pass through the loop.
        gf.update_screen(df_settings, screen, stats, sb, ship, aliens, bullets, play_button)
                
run_space_game()

