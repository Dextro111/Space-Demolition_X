import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A Class To Represent a single alien in the fleet."""

    def __init__(self, df_settings, screen):
        """Initialize the alien and its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.df_settings = df_settings
        
        #   Load Alien Image and set its rect attribute
        self.image = pygame.image.load("Images/ufo.png").convert_alpha()
        
        self.rect = self.image.get_rect()

        #   Start each alien at top left of screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #   Store the alien position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draws the alien at its current location"""
        self.screen.blit(self.image, self)
    
    def check_edges(self):
        """Return True if if alien at rdgr of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the alien right or left"""
        self.x += (self.df_settings.alien_speed_factor * self.df_settings.fleet_direction)
        self.rect.x = self.x
    