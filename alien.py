import pygame
import random
from pygame.sprite import Sprite

class Alien(Sprite):
    """单个外星人"""
    def __init__(self,screen,St):
        super(Alien,self).__init__()
        self.screen=screen
        self.St=St
        self.count=0
        # 加载外星人战斗机图片
        self.image=pygame.image.load('外星人战斗机.png')
        self.rect=self.image.get_rect()

        # 设置外星人战斗机的初始位置,放在屏幕左上角
        self.rect.x=random.randint(0,1100)
        self.rect.y=random.randint(0,10)

    def blitme(self):
        """将外星人战斗机放在屏幕指定位置"""
        self.screen.blit(self.image,self.rect)


