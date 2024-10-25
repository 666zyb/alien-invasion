import pygame
import game_function as g_f
from clock import Clocks
from pygame.sprite import Group
from setting import Setting
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from alien import Alien


def run_game():
    # 初始化游戏窗口
    pygame.init()
    Cl=Clocks()
    # 设置游戏窗口的大小
    St = Setting()
    screen = pygame.display.set_mode((St.screen_width, St.screen_height))
    # 设置游戏背景
    background_image=pygame.image.load('外太空（游戏背景图）.png')
    # 设置游戏窗口的名字
    pygame.display.set_caption('外星人入侵')
    # 设置游戏背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load('背景音乐（Endless_Storys_战斗5）.mp3')
    # 子弹发射声音
    shoot_b=pygame.mixer.Sound('射击音效.mp3')
    pygame.mixer.music.set_volume(0.5)
    # 播放背景音乐，设置为无限循环
    pygame.mixer.music.play(-1)
    # 创建一个能够存储游戏统计信息的实例
    stats=GameStats(St)
    # 创建一个战斗机
    Sp = Ship(screen, St)
    Al=Alien(screen,St)
    # 创建一个可以存储子弹和外星人战斗机,爆炸效果的编组
    bullets = Group()
    aliens=Group()
    # 创建一个play按钮
    play_bt=Button(screen,'play')
    # 创建一个记分板
    Sb=Scoreboard(St,screen,stats)
    # 主事件循环
    while True:
        # 鼠标和键盘事件
        g_f.check_events(screen, St, Sp, bullets,stats,play_bt,aliens,Sb,Cl,Al,shoot_b)
        # 更新屏幕
        g_f.update_screen(screen, Sp, bullets, aliens,play_bt,stats,Sb)
        # 游戏背景图
        screen.blit(background_image,(0,0))
        # 玩家未死亡的时候运行
        if stats.game_active:
            # 战斗机位置的更新
            Sp.update()
            g_f.update_alien(aliens,St,Sp,stats,screen,bullets,Sb)
            # 更新子弹并删除屏幕之外的子弹
            g_f.update_bullets(bullets, aliens, St,stats,Sb,Al)



run_game()
