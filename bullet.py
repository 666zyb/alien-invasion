import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """对发射的子弹的管理"""

    def __init__(self, St, screen, Sp):
        super(Bullet, self).__init__()
        self.screen = screen
        # 在（0，0）处创建一个表示子弹的矩形，并调整子弹的位置
        self.bullet_image=pygame.image.load('导弹.png')
        self.rect = self.bullet_image.get_rect()
        self.rect.centerx = Sp.rect.centerx
        self.rect.top = Sp.rect.top

        self.center_y = float(self.rect.y)
        self.bullet_s = St.bullet_speed

        self.fire=False

    def update(self):
        """更新子弹的位置"""
        self.center_y -= self.bullet_s
        # 更新表示子弹的rect的位置
        self.rect.y = self.center_y

    def draw_b(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.bullet_image,self.rect)