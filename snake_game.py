import pygame
import random
import sys
import os

# 初始化pygame
pygame.init()

# 游戏配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def get_chinese_font(size):
    """获取支持中文的字体"""
    # 尝试常见的中文字体
    chinese_fonts = [
        'simhei.ttf',  # 黑体
        'simsun.ttc',  # 宋体
        'msyh.ttc',    # 微软雅黑
        'NotoSansCJK-Regular.ttc',  # 思源黑体
        'DejaVuSans.ttf'  # 备用字体
    ]
    
    # Windows系统字体路径
    windows_font_paths = [
        'C:/Windows/Fonts/',
        'C:/Windows/System32/Fonts/'
    ]
    
    # 尝试系统字体
    for font_path in windows_font_paths:
        for font_name in chinese_fonts:
            full_path = os.path.join(font_path, font_name)
            if os.path.exists(full_path):
                try:
                    return pygame.font.Font(full_path, size)
                except:
                    continue
    
    # 如果找不到系统字体，尝试使用pygame内置字体
    try:
        return pygame.font.Font('simhei.ttf', size)
    except:
        # 最后的备用方案：使用系统默认字体
        return pygame.font.Font(None, size)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
        
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # 检查是否撞墙
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False
            
        # 检查是否撞到自己
        if new_head in self.body:
            return False
            
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
        return True
        
    def change_direction(self, direction):
        # 防止反向移动
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
            
    def grow_snake(self):
        self.grow = True
        
    def draw(self, screen):
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                             GRID_SIZE, GRID_SIZE)
            # 蛇头用不同颜色
            if i == 0:
                pygame.draw.rect(screen, (0, 200, 0), rect)
            else:
                pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = self.generate_position()
        
    def generate_position(self):
        return (random.randint(0, GRID_WIDTH - 1), 
                random.randint(0, GRID_HEIGHT - 1))
                
    def draw(self, screen):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, 
                          self.position[1] * GRID_SIZE, 
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏 - 等级版")
        self.clock = pygame.time.Clock()
        
        # 初始化字体
        self.font = get_chinese_font(24)
        self.big_font = get_chinese_font(48)
        self.medium_font = get_chinese_font(36)
        self.small_font = get_chinese_font(20)
        
        # 等级系统配置
        self.level_speeds = [4, 6, 8, 10, 12, 14, 16, 18, 20, 25]  # 每级对应的游戏速度
        self.level_thresholds = [0, 50, 120, 200, 300, 420, 560, 720, 900, 1100]  # 升级所需分数
        
        self.reset_game()
        
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.level = 1
        self.game_over = False
        
    def get_current_level(self):
        """根据分数计算当前等级"""
        for i in range(len(self.level_thresholds) - 1, -1, -1):
            if self.score >= self.level_thresholds[i]:
                return i + 1
        return 1
        
    def get_game_speed(self):
        """根据等级获取游戏速度"""
        level_index = self.level - 1
        if level_index < len(self.level_speeds):
            return self.level_speeds[level_index]
        else:
            return self.level_speeds[-1]  # 最高等级速度
            
    def get_next_level_score(self):
        """获取升级到下一级所需的分数"""
        if self.level <= len(self.level_thresholds):
            return self.level_thresholds[self.level - 1] if self.level < len(self.level_thresholds) else None
        return None
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return True
        
    def update(self):
        if not self.game_over:
            if not self.snake.move():
                self.game_over = True
                return
                
            # 检查是否吃到食物
            if self.snake.body[0] == self.food.position:
                self.snake.grow_snake()
                self.score += 10
                
                # 检查是否升级
                new_level = self.get_current_level()
                if new_level > self.level:
                    self.level = new_level
                
                # 生成新食物，确保不在蛇身上
                while self.food.position in self.snake.body:
                    self.food.position = self.food.generate_position()
                    
    def draw(self):
        self.screen.fill(BLACK)
        
        if not self.game_over:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
        # 绘制游戏信息面板
        self.draw_game_info()
        
        # 绘制游戏结束信息
        if self.game_over:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def draw_game_info(self):
        """绘制游戏信息面板"""
        # 分数
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 等级
        level_text = self.font.render(f"等级: {self.level}", True, YELLOW)
        self.screen.blit(level_text, (10, 40))
        
        # 游戏速度
        speed_text = self.font.render(f"速度: {self.get_game_speed()}", True, ORANGE)
        self.screen.blit(speed_text, (10, 70))
        
        # 升级进度
        next_level_score = self.get_next_level_score()
        if next_level_score:
            progress_text = self.font.render(f"升级还需: {next_level_score - self.score}", True, PURPLE)
            self.screen.blit(progress_text, (10, 100))
        else:
            max_level_text = self.font.render("已达最高等级!", True, PURPLE)
            self.screen.blit(max_level_text, (10, 100))
        
        # 绘制操作提示（仅在游戏进行中显示）
        if not self.game_over:
            help_text = self.small_font.render("方向键控制移动，ESC退出", True, WHITE)
            self.screen.blit(help_text, (10, WINDOW_HEIGHT - 30))
            
        # 绘制等级进度条
        if next_level_score:
            current_level_start = self.level_thresholds[self.level - 1] if self.level > 1 else 0
            progress = (self.score - current_level_start) / (next_level_score - current_level_start)
            
            # 进度条背景
            bar_width = 200
            bar_height = 10
            bar_x = WINDOW_WIDTH - bar_width - 10
            bar_y = 20
            
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, bar_width * progress, bar_height))
            
            # 进度条标签
            progress_label = self.small_font.render("升级进度", True, WHITE)
            self.screen.blit(progress_label, (bar_x, bar_y - 25))
        
    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 绘制半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文本
        game_over_text = self.big_font.render("游戏结束!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 120))
        
        # 最终分数
        final_score_text = self.medium_font.render(f"最终分数: {self.score}", True, YELLOW)
        score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60))
        
        # 最终等级
        final_level_text = self.medium_font.render(f"达到等级: {self.level}", True, ORANGE)
        level_rect = final_level_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20))
        
        # 重新开始提示
        restart_text = self.font.render("按空格键重新开始", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
        
        # 退出提示
        exit_text = self.font.render("按ESC键退出游戏", True, WHITE)
        exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80))
        
        # 绘制所有文本
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, score_rect)
        self.screen.blit(final_level_text, level_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(exit_text, exit_rect)
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.get_game_speed())  # 根据等级调整游戏速度
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()