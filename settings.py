class Settings():
    """A Class To Store All Settings For Space Demolition"""

    def __init__(self):
        """Initialize The Game Static Settings."""
        #  Screen Settings
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        #  Ship Settings
        self.ship_limit = 3
        
        #  Bullet Settings
        self.bullet_speed = 10
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3

        #  Alien Settings
        self.fleet_drop_speed = 13

        #  How quickly the game speeds up
        self.speedup_scale = 1.1
        #  How quickly the alien points values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 5
        
        #  fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #  Scoring
        self.alien_points = 50
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        