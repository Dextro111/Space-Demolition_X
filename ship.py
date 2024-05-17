import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, df_settings,screen):
        """Initialize The Ship And Set Its Starting Position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.df_settings = df_settings

        #   Load the ship image and get its rect.
        self.image = pygame.image.load("Images/spaceship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        #   Start Each New Ship At The Bottom Center Of the Screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #   Store A Decimal value For The Ships Center.
        self.center = float(self.rect.centerx)
        #   Movemment Flag,,,,,,,,,,,,
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ships position based on the movement flag."""
        #   Update the ships center value, not the rect. 
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.df_settings.ship_speed_factor
            self.rect.centerx += 6
        if self.moving_left and self.rect.left > 0:
            self.center -= self.df_settings.ship_speed_factor
            self.rect.centerx -= 6

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image.convert_alpha(), self.rect)
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx