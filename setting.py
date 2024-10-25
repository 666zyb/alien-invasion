class Setting(object):
    def __init__(self):
        # 游戏窗口大小，背景颜色设置
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (255, 0, 0)

        # 战斗机的速度设置
        self.ship_speed = 0.1
        # 子弹的设置
        self.bullet_speed=1.5

        # 外星人战斗机的设置
        self.alien_speed=10

        # 刚开始的时候玩家拥有的战斗机数量
        self.ship_limit=3

        # 速度加快
        self.speed_up=1.1

        # 外星人战斗机的分数增大幅度
        self.alien_speed_score=1.5

        self.initialize_setting()

    def initialize_setting(self):
        """初始化游戏设置"""
        self.alien_speed=10
        self.ship_speed=1.1
        self.bullet_speed=1.5
        # 打中每个外星人战斗机的得分
        self.alien_score=50

    def increase_speed(self):
        """当游戏等级提升时，提高玩家，外星人战斗机"""
        self.alien_speed*=self.speed_up
        self.alien_score=int(self.alien_score*self.alien_speed_score)