import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard(object):
    """显示得分信息，记分板"""

    def __init__(self, St, screen, stats):
        self.screen = screen
        self.St = St
        self.stats = stats
        self.rect_screen = self.screen.get_rect()

        # 记分板字体颜色大小的设置
        self.score_color = (30, 30, 30)
        self.font = pygame.font.SysFont('华文宋体', 28)

        self.prep_score()
        self.prep_high_score_most()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        """将记分板转换为图像"""
        round_score = int(round(self.stats.score, -1))
        self.score_str = '得分:' + '{:,}'.format(round_score)
        # print(pygame.font.get_fonts())
        # 上面这步是为了查看pygame支持什么字体，第一次写的时候’得分‘那两个字是乱码，就调用了这个函数
        self.score_image = self.font.render(self.score_str, True, self.score_color, self.St.bg_color)

        # 将记分板放在屏幕右上角
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.rect_screen.right
        self.score_image_rect.top = 20

    def prep_high_score_most(self):
        """将最高得分转换为图像并放在屏幕顶部中央"""
        # 将最高得分渲染为图像
        high_score = int(round(self.stats.high_score, -1))
        self.high_score_str = '最高记录:' + '{:,}'.format(high_score)
        self.high_score_image = self.font.render(self.high_score_str, True, self.score_color, self.St.bg_color)

        # 将最高得分图像放在屏幕顶部中央
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.rect_screen.centerx
        self.high_score_image_rect.top = self.rect_screen.top

    def prep_level(self):
        """显示目前等级"""
        # 将等级显示渲染为图像
        level = self.stats.level
        self.level_str = '难度:' + str(level)
        self.level_image = self.font.render(self.level_str, True, self.score_color, self.St.bg_color)

        # 将等级显示图像放在记分板下方
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.rect_screen.right
        self.level_image_rect.top = self.score_image_rect.bottom + 10

    def prep_ship(self):
        """显示剩余战斗机数量，即玩家还有几条命"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.screen, self.St)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_scoreboard(self):
        """将记分板显示在屏幕上"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)
