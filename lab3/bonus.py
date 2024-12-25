import pygame
from pygame.sprite import Sprite

class Bonus(Sprite):
    """Класс, представляющий бонус"""

    def __init__(self, ai_game):
        """Инициализирует бонус и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загрузка изображения пришельца и назнаение атрибута rect
        self.image = pygame.image.load('resources/images/bonus.bmp')
        self.rect = self.image.get_rect()
        self.y = self.rect.y
        # Каждый новый пришелец появляется в левом верхнем углу экрана.
        self.rect.midtop = self.screen_rect.midtop
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Перемещает пришельца вправо или влево"""
        self.rect.y += 1

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)