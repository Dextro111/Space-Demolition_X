class GameStats():
    """Track Statistics for alien Invasion."""

    def __init__(self, df_settings):
        """Initialize statistics"""
        self.df_settings = df_settings
        self.reset_stats()

        # Start alien invasion in an active state
        self.game_active = False

        #  High Score should never reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.df_settings.ship_limit
        self.score = 0
        self.level = 1