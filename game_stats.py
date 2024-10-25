class GameStats(object):
    """跟踪游戏的统计信息"""

    def __init__(self,St):
        """初始化统计信息"""
        self.St=St
        self.reset_stats()
        # 让游戏刚启动时处于非活动状态
        self.game_active=False
        # 最高得分，不能重置
        self.high_score=0
        # 显示等级
        self.level=1

    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.game_active = False
        self.ships_left=self.St.ship_limit
        self.score=0
        self.level=1
