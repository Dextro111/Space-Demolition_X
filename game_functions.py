import sys
from time import sleep
import pygame


from bullet import Bullet
from alien import Alien

def check_events(df_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond To Keypresses And Mouse Events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
        #    check_keydown_events(event, ship)
            check_keydown_events(event, df_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(df_settings, screen, stats, sb, play_button , ship, 
                aliens, bullets, mouse_x, mouse_y)

def check_play_button(df_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start A New game when The Button is clicked"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #  Reset the game settings.
        df_settings.initialize_dynamic_settings()
        
        #  Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        #  Reset The Game stats
        stats.reset_stats()
        stats.game_active = True

        #  Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #  Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #  Create a new fleet amd center the ship
        create_fleet(df_settings, screen, ship, aliens)
        ship.center_ship()

def df_settings(df_settings):
    return df_settings

def check_keydown_events(event, df_settings, screen, ship, bullets):
    """Respond To Keypresses."""
    if event.key == pygame.K_RIGHT:
    #   Moves The Ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(df_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, ship):
    """Responds To Key Releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_bullets(df_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullet and remove old bullets."""
    #   Update bullet positions.
    bullets.update()
    #   Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(df_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collision(df_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet alien collision"""
    #   Remove any bullets and aliens that collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += df_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #   If the entire fleet is destroyed, start a new level
        bullets.empty()
        df_settings.increase_speed()

        #  Increase Level
        stats.level += 1
        sb.prep_level()

        create_fleet(df_settings, screen, ship, aliens)
    
        if stats.level == 5 or stats.level == 10 or stats.level == 15 or stats.level == 20 :  
            df_settings.bullet_width = 100
        elif stats.level > 20:
            df_settings.bullet_width = 250
        else:
            df_settings.bullet_width = 5
        
def fire_bullet(df_settings, screen, ship, bullets):
    """Fire a bullet if limit has not been reached"""
    # Create A New bullet and add to the group.
    if len(bullets) < df_settings.bullets_allowed:
        new_bullet = Bullet(df_settings, screen, ship,)
        bullets.add(new_bullet)

def get_number_aliens_x(df_settings, alien_width):
    """Determine the nymber of akiens in a row"""
    available_space_x = df_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(df_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row"""
    alien = Alien(df_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(df_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    #   Create an alien and find the numb of aliens
    alien = Alien(df_settings, screen)
    number_aliens_x = get_number_aliens_x(df_settings, alien.rect.width)
    number_rows = get_number_rows(df_settings, ship.rect.height, alien.rect.height)

    #   Create the fleet of aliens.
    for row_number in range(number_rows):
        #   Create an alien and put in row
        for alien_number in range(number_aliens_x):
            create_alien(df_settings, screen, aliens, alien_number, row_number)

def get_number_rows(df_settings, ship_height, alien_height):
    """Determine the number of rows of aliens fitting on screen."""
    available_space_y = (df_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(df_settings, aliens):
    """Respond appropriately if aliens have reached edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(df_settings, aliens)
            break

def change_fleet_direction(df_settings, aliens):
    """Drop the fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += df_settings.fleet_drop_speed
    df_settings.fleet_direction *= -1

def ship_hit(df_settings, stats, screen, sb, ship, aliens, bullets):
    """ Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        #   decrement ships_left
        stats.ships_left -= 1

        # Update Scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #   Creaate new fleet and center ship
        create_fleet(df_settings, screen, ship, aliens)
        ship.center_ship()

        #   Pause
        sleep(1.5)
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(df_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any alien have reached the bottom screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #   Treat this same as ship got hit
            ship_hit(df_settings, stats, screen, sb, ship, aliens, bullets)
            break
def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_aliens(df_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if fleet is at edge and Updaate position of aliens"""
    check_fleet_edges(df_settings, aliens)
    aliens.update()
    #   Look for alien ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(df_settings, stats, screen, sb, ship, aliens, bullets)
        print("ship Hit")
    #   Look for aliens hitting bottom of screen
    check_aliens_bottom(df_settings, stats, screen, sb, ship, aliens, bullets)
    
def update_screen(df_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Updates Images On The Screen And Flip To A New Screen."""
    #  Draws Screen Color During each pass.
    screen.fill(df_settings.bg_color)
    # Background Image
    background = pygame.image.load("Images/bg.png").convert_alpha()
    screen.blit(background, (0, 0))
    #  Redraws all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    aliens.draw(screen)

    #  Draw the score info
    sb.show_score()

    #  Draw the Play Button If Game Is Inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make The Most Recently Drawn Screen Visible.
    pygame.display.flip()