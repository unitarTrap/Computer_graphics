import os
import sys
from time import sleep
import pygame
import pickle
import random

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from bonus import Bonus


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            (self.settings.screen_width, self.settings.screen_height)))
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики и панели результата
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bonus = Bonus(self)
        self.bonus = None
        self._create_fleet()

        self._sound_initialize()

        # Создание кнопки Играть
        self.play_button = Button(self, "Играть")


    def run_game(self):
        """Запуск основноего цикла игры."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                if self.bonus:
                    self.bonus.update()

            self._update_screen()

    def _sound_initialize(self):
        self.shot_sound = pygame.mixer.Sound("resources/sounds/Shot_sound.wav")
        self.gameover_sound = pygame.mixer.Sound("resources/sounds/gameover_sound.wav")
        self.damage_sound = pygame.mixer.Sound("resources/sounds/damage_sound.wav")
        self.alien_dies_sound = pygame.mixer.Sound("resources/sounds/alien_dies_sound.wav")
        self.bonus_sound = pygame.mixer.Sound("resources/sounds/bonus_sound.wav")

    def _check_events(self):
        """Обрабатывает нажатия клавиатуры и мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Играть"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровых настроек
            self.settings.initialize_dynamic_settings()
 
            # Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:
            self._save_game()
        elif event.key == pygame.K_d:
            self._load_game()    

    def _check_keyup_events(self, event):
        """реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.shot_sound.play()
    
    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиции снарядов
        self.bullets.update()
  
        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами"""
        # удалить снаряд и пришельца, участвующих в коллизях
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        
        if not self.aliens:
            # Уничтожение всех существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb. check_high_score()
            self.alien_dies_sound.play()
            self._bonus_spawn()
            
    def _check_bonus_ship_collisions(self):
        """Обработка коллизий бонусов с кораблем"""
        # удалить бонус и добавить очко здоровья
        if self.bonus:
            if pygame.sprite.collide_rect(self.bonus, self.ship):
                self.bonus_sound.play()
                self.stats.ships_left += 1
                self.sb.prep_ships()
                self.bonus = None
            
    def _bonus_spawn(self):
        r = random.randint(1, 100)
        if r >= 90:
            self.bonus = Bonus(self)
            self.bonus.blitme()
            self.bonus.update()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            
            self.damage_sound.play()

            # Уменьшение ships_left и обновление счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.gameover_sound.play()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что и при столкновении с кораблем
                self._ship_hit()
                break

    def _create_fleet(self):
        """Создание флота вторжения"""
        # Создание пришельца и вычисление количсетва пришельцев в одном ряду
        # Интервал между соседними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Создание пришельца и размещение его в ряду.
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self._check_bonus_ship_collisions()
          
        # Вывод информации о счете
        self.sb.show_score()

        if self.bonus:
            self.bonus.blitme()
        
        # Кнопка Играть отображаетя в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _save_game(self):
        with open("resources/saves/savefile.pkl", "wb") as f:
            data = {"level": self.stats.level, "score": self.stats.score, "lives": self.stats.ships_left}
            pickle.dump(data, f)

    def _load_game(self):
        with open("resources/saves/savefile.pkl", "rb") as f:
            data = pickle.load(f)
            self.stats.level = data['level']
            self.stats.score = data['score']
            self.stats.ships_left = data['lives']

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # восстановление интерфейса
            self.sb.prep_ships()
            self.sb.prep_score()
            self.sb.prep_level()

            # Пауза
            sleep(0.5)



if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()