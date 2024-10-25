import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(screen, St, Sp, bullets,stats,play_bt,aliens,Sb,Cl,Al,shoot_b):
    """鼠标和键盘事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果点击游戏窗口关闭按钮，则退出游戏
            pygame.mixer.music.stop()
            sys.exit()
        elif event.type == Cl.ALIEN_EVENT:
            # 定时器事件触发，创建一个新的外星人
            if stats.game_active:  # 只在游戏活动状态下生成外星人
                create_alien(St, screen, aliens,Al)
        elif event.type == Cl.ALIEN_EVENT_1:
            # 定时器事件触发，创建一个新的外星人
            if stats.game_active:  # 只在游戏活动状态下生成外星人
                change_fleet_direction(St, aliens)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(stats,play_bt,mouse_x,mouse_y,bullets,aliens,St,Sp,Sb)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                Sp.moving_right = True
            elif event.key == pygame.K_LEFT:
                Sp.moving_left = True
            elif event.key == pygame.K_SPACE:
                if stats.game_active:
                    new_bullet = Bullet(St, screen, Sp)
                    bullets.add(new_bullet)
                    shoot_b.play()
            elif event.key == pygame.K_q:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                Sp.moving_right = False
            elif event.key == pygame.K_LEFT:
                Sp.moving_left = False


def update_screen(screen, Sp, bullets, aliens,play_bt,stats,Sb):
    """更新屏幕"""
    # 每次循环绘制屏幕颜色
    for bt in bullets.sprites():
        bt.draw_b()
    Sp.blitme()
    aliens.draw(screen)
    Sb.show_scoreboard()
    # 如果游戏处于非活动状态，绘制play按钮
    if not stats.game_active:
        play_bt.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets, aliens, St,stats,Sb,Al):
    """更新子弹"""
    bullets.update()
    # 删除在屏幕之外的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom == 0:
            bullets.remove(bullet)
    # 子弹与外星人战斗机碰撞
    check_bullet_alien_collisions(aliens, bullets, St, stats,Sb,Al)


def create_alien(St, screen, aliens,Al):
    alien = Alien(screen, St)
    aliens.add(alien)
    Al.count+=1


def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    for alien in aliens.sprites():
        alien.rect.y += St.alien_speed


def update_alien(aliens, St, Sp,stats,screen,bullets,Sb):
    """检查外星人战斗机是否碰到边缘并更新战斗机的位置"""
    # 响应战斗机与外星人战斗机碰撞
    if pygame.sprite.spritecollideany(Sp, aliens):
        ship_hited(stats,aliens,bullets,Sp,Sb)

    # 检查是否有外星人战斗机到达屏幕底端
    check_alien_bottom(screen,stats,bullets,aliens,Sp,Sb)


def check_bullet_alien_collisions(aliens, bullets, St, stats,Sb,Al):
    """响应子弹和外星人战斗机的碰撞"""
    # 检查是否有子弹碰撞了外星人战斗机
    # 如果碰到了，则删除这颗子弹和被碰撞的外星人战斗机
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 如果子弹打到外星人战斗机，则分数加50
    if collisions:
        for alien in collisions.values():
            stats.score+=St.alien_score*len(alien)
            Sb.prep_score()
        check_high_score(stats,Sb)


    # 检查所有外星人战斗机是否被消灭
    if Al.count==24:
        # 删除现有的所有子弹，加快游戏速度，并重新创建一群外星人战斗机，并提高等级
        bullets.empty()
        St.increase_speed()
        Al.count=0

        # 提高等级
        stats.level+=1
        Sb.prep_level()


def ship_hited(stats,aliens,bullets,Sp,Sb):
    """响应被外星人战斗机撞到的战斗机"""
    # 将ship_left减1（即战斗机的数量减一）,相当于玩家的三条命
    if stats.ships_left>0:
        stats.ships_left-=1

        Sb.prep_ship()

        # 清空子弹和外星人战斗机列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人战斗机，并将玩家战斗机放置在屏幕底部中央
        # create_more_alien(St,screen,aliens,Sp)
        Sp.ship_center()

        # 暂停
        sleep(0.5)
    # 三条命用完则将游戏状态设置为false，代表玩家死亡
    else:
        stats.game_active=False
        # 游戏结束时让光标显示
        pygame.mouse.set_visible(True)

def check_alien_bottom(screen,stats,bullets,aliens,Sp,Sb):
    """检查外星人战斗机有没有到达屏幕底部，有则视为与玩家战斗机碰撞"""
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            # 像玩家战斗机被撞到一样处理
            ship_hited(stats,aliens,bullets,Sp,Sb)
            break

def check_play_button(stats,play_bt,mouse_x,mouse_y,bullets,aliens,St,Sp,Sb):
    """在玩家单击play的时候开始游戏"""
    if play_bt.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        # 在玩家点击play后，重置游戏信息，并开始游戏
        stats.reset_stats()
        stats.game_active=True
        St.initialize_setting()

        # 重置记分板和等级
        Sb.prep_level()
        Sb.prep_score()
        Sb.prep_ship()
        Sb.prep_high_score_most()

        # 清空子弹和外星人战斗机列表
        bullets.empty()
        aliens.empty()

        # 创建一群新的外星人并让玩家战斗机居中
        # create_more_alien(St,screen,aliens,Sp)
        Sp.ship_center()

        # 光标在游戏窗口内的时候隐藏光标
        pygame.mouse.set_visible(False)

def check_high_score(stats,Sb):
    """检查是否诞生了最高分"""
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        Sb.prep_high_score_most()


