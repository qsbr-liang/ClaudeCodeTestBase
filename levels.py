# 游戏关卡系统
# Game Level System

class GameLevel:
    def __init__(self, level_number, speed, obstacles=None):
        self.level_number = level_number
        self.speed = speed
        self.obstacles = obstacles or []
        
    def get_speed(self):
        return self.speed
        
    def get_obstacles(self):
        return self.obstacles

# 预定义关卡
LEVELS = {
    1: GameLevel(1, 3, []),  # 简单关卡
    2: GameLevel(2, 5, []),  # 中等关卡  
    3: GameLevel(3, 8, []),  # 困难关卡
}

print("关卡系统模块已加载")