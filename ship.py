import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, screen, St):
        """初始化战斗机并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.St=St
        # 加载战斗机图片，并获取其外接矩形
        self.image = pygame.image.load('战斗机.png')
        self.rect = self.image.get_rect()
        self.rect_screen = screen.get_rect()
        # 将每艘战斗机放在屏幕底部中央位置
        self.rect.centerx = self.rect_screen.centerx
        self.rect.bottom = self.rect_screen.bottom
        # 战斗机是否向右运动
        self.moving_right = False
        # 战斗机是否向左运动
        self.moving_left = False

        self.center = float(self.rect.centerx)

    def blitme(self):
        """指定位置加载战斗机图像"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right<self.rect_screen.right:
            self.center += self.St.ship_speed
        if self.moving_left and self.rect.left>self.rect_screen.left:
            self.center -= self.St.ship_speed
        self.rect.centerx = self.center

    def ship_center(self):
        """让玩家战斗机在屏幕上居中"""
        self.center=self.rect_screen.centerx
