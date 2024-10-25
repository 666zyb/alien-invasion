import pygame

class Clocks(object):
    def __init__(self):
        self.ALIEN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ALIEN_EVENT, 1000)  # 每500毫秒生成一个外星人
        self.ALIEN_EVENT_1 = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ALIEN_EVENT_1, 150)