import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A Class To Manage Bullets Fired"""

    def __init__(self, df_settings, screen, ship):
        """Create A Bullet Object At The Ship Current Position."""
        super(Bullet, self).__init__()
        self.screen = screen

        #   Create a bullet rect at (0,0) and then set correct position.
        self.rect = pygame.Rect(0, 0, df_settings.bullet_width, 
                    df_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #   Store the bullets position as a decimal value
        self.y = float(self.rect.y)

        self.color = df_settings.bullet_color
        self.bullet_speed = df_settings.bullet_speed

    def update(self):
        """Move thebullet up the screen."""
        #   Update the decimal position of the bullet.
        self.y -= self.bullet_speed
        #   Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw The Bullet To The Screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)