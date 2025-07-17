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
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GOLD = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)

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

class Obstacle:
    def __init__(self, obstacles_list=None):
        if obstacles_list is None:
            obstacles_list = []
        self.obstacles = obstacles_list
        
    def generate_level_obstacles(self, level):
        """根据等级生成障碍物"""
        self.obstacles = []
        
        # 基础障碍物数量随等级增加
        base_obstacles = min(level * 2, 15)  # 最多15个障碍物
        
        # 生成随机障碍物
        for _ in range(base_obstacles):
            # 确保障碍物不在游戏区域边缘和中心区域
            while True:
                x = random.randint(2, GRID_WIDTH - 3)
                y = random.randint(2, GRID_HEIGHT - 3)
                
                # 避免在蛇的初始位置周围生成障碍物
                snake_start_x = GRID_WIDTH // 2
                snake_start_y = GRID_HEIGHT // 2
                if abs(x - snake_start_x) > 3 or abs(y - snake_start_y) > 3:
                    if (x, y) not in self.obstacles:
                        self.obstacles.append((x, y))
                        break
        
        # 为高等级添加一些特殊形状的障碍物
        if level >= 3:
            self.add_wall_obstacles(level)
            
    def add_wall_obstacles(self, level):
        """添加墙壁型障碍物"""
        if level >= 3:
            # 添加一些短墙
            wall_length = min(level, 6)
            
            # 水平墙
            start_x = random.randint(5, GRID_WIDTH - wall_length - 5)
            start_y = random.randint(5, GRID_HEIGHT - 5)
            for i in range(wall_length):
                pos = (start_x + i, start_y)
                if pos not in self.obstacles:
                    self.obstacles.append(pos)
                    
            # 垂直墙
            start_x = random.randint(5, GRID_WIDTH - 5)
            start_y = random.randint(5, GRID_HEIGHT - wall_length - 5)
            for i in range(wall_length):
                pos = (start_x, start_y + i)
                if pos not in self.obstacles:
                    self.obstacles.append(pos)
                    
    def is_obstacle(self, position):
        """检查指定位置是否是障碍物"""
        return position in self.obstacles
        
    def draw(self, screen):
        """绘制障碍物"""
        for obstacle in self.obstacles:
            rect = pygame.Rect(obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, 
                             GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, DARK_GRAY, rect, 2)
            
            # 添加一些纹理效果
            inner_rect = pygame.Rect(obstacle[0] * GRID_SIZE + 2, obstacle[1] * GRID_SIZE + 2,
                                   GRID_SIZE - 4, GRID_SIZE - 4)
            pygame.draw.rect(screen, WHITE, inner_rect, 1)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
        
    def move(self, obstacles):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # 检查是否撞墙
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False
            
        # 检查是否撞到自己
        if new_head in self.body:
            return False
            
        # 检查是否撞到障碍物
        if obstacles.is_obstacle(new_head):
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
                # 给蛇头添加眼睛
                eye_size = 3
                left_eye = (segment[0] * GRID_SIZE + 4, segment[1] * GRID_SIZE + 4)
                right_eye = (segment[0] * GRID_SIZE + 12, segment[1] * GRID_SIZE + 4)
                pygame.draw.circle(screen, BLACK, left_eye, eye_size)
                pygame.draw.circle(screen, BLACK, right_eye, eye_size)
            else:
                pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.is_special = False
        self.special_timer = 0
        
    def generate_position(self, snake_body=None, obstacles=None):
        """生成食物位置，避免与蛇身和障碍物重叠"""
        if snake_body is None:
            snake_body = []
        if obstacles is None:
            obstacles = Obstacle()
            
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), 
                       random.randint(0, GRID_HEIGHT - 1))
            
            # 确保食物不在蛇身上和障碍物上
            if position not in snake_body and not obstacles.is_obstacle(position):
                return position
    
    def make_special(self):
        """将食物设为特殊食物"""
        self.is_special = True
        self.special_timer = 300  # 5秒钟特殊食物(60fps * 5)
    
    def update(self):
        """更新特殊食物状态"""
        if self.is_special:
            self.special_timer -= 1
            if self.special_timer <= 0:
                self.is_special = False
                
    def draw(self, screen):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, 
                          self.position[1] * GRID_SIZE, 
                          GRID_SIZE, GRID_SIZE)
        
        if self.is_special:
            # 特殊食物：金色闪烁效果
            color = GOLD if (self.special_timer // 10) % 2 == 0 else YELLOW
            pygame.draw.rect(screen, color, rect)
            
            # 特殊食物装饰
            center_x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
            center_y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 4)
            pygame.draw.circle(screen, color, (center_x, center_y), 2)
        else:
            # 普通食物
            pygame.draw.rect(screen, RED, rect)
            
            # 给食物添加一些装饰
            center_x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
            center_y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
            pygame.draw.circle(screen, (255, 100, 100), (center_x, center_y), 3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏 - 障碍物版")
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
        self.obstacles = Obstacle()
        self.obstacles.generate_level_obstacles(1)  # 初始等级为1
        self.food = Food()
        # 重新生成食物位置，避免与障碍物重叠
        self.food.position = self.food.generate_position(self.snake.body, self.obstacles)
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
            if not self.snake.move(self.obstacles):
                self.game_over = True
                return
                
            # 更新食物状态
            self.food.update()
                
            # 检查是否吃到食物
            if self.snake.body[0] == self.food.position:
                self.snake.grow_snake()
                
                # 根据食物类型给分
                if self.food.is_special:
                    self.score += 25  # 特殊食物更多分数
                else:
                    self.score += 10  # 普通食物
                
                # 检查是否升级
                new_level = self.get_current_level()
                if new_level > self.level:
                    self.level = new_level
                    # 升级时重新生成障碍物
                    self.obstacles.generate_level_obstacles(self.level)
                
                # 生成新食物，确保不在蛇身上和障碍物上
                self.food.position = self.food.generate_position(self.snake.body, self.obstacles)
                self.food.is_special = False
                
                # 10%概率生成特殊食物
                if random.random() < 0.1:
                    self.food.make_special()
                    
    def draw(self):
        self.screen.fill(BLACK)
        
        if not self.game_over:
            # 绘制顺序：障碍物 -> 食物 -> 蛇
            self.obstacles.draw(self.screen)
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            
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
        
        # 障碍物数量
        obstacle_count_text = self.font.render(f"障碍物: {len(self.obstacles.obstacles)}", True, GRAY)
        self.screen.blit(obstacle_count_text, (10, 100))
        
        # 升级进度
        next_level_score = self.get_next_level_score()
        if next_level_score:
            progress_text = self.font.render(f"升级还需: {next_level_score - self.score}", True, PURPLE)
            self.screen.blit(progress_text, (10, 130))
        else:
            max_level_text = self.font.render("已达最高等级!", True, PURPLE)
            self.screen.blit(max_level_text, (10, 130))
        
        # 绘制操作提示（仅在游戏进行中显示）
        if not self.game_over:
            help_text = self.small_font.render("方向键控制移动，ESC退出", True, WHITE)
            self.screen.blit(help_text, (10, WINDOW_HEIGHT - 70))
            
            help_text2 = self.small_font.render("灰色方块为障碍物，小心避开！", True, WHITE)
            self.screen.blit(help_text2, (10, WINDOW_HEIGHT - 50))
            
            # 特殊食物提示
            if self.food.is_special:
                special_text = self.small_font.render("✨ 金色食物出现！价值25分！", True, GOLD)
                self.screen.blit(special_text, (10, WINDOW_HEIGHT - 30))
            else:
                normal_text = self.small_font.render("红色食物：10分，金色食物：25分", True, LIGHT_BLUE)
                self.screen.blit(normal_text, (10, WINDOW_HEIGHT - 30))
            
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
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 140))
        
        # 最终分数
        final_score_text = self.medium_font.render(f"最终分数: {self.score}", True, YELLOW)
        score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 80))
        
        # 最终等级
        final_level_text = self.medium_font.render(f"达到等级: {self.level}", True, ORANGE)
        level_rect = final_level_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40))
        
        # 障碍物挑战
        obstacle_text = self.font.render(f"克服了 {len(self.obstacles.obstacles)} 个障碍物!", True, GRAY)
        obstacle_rect = obstacle_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        
        # 重新开始提示
        restart_text = self.font.render("按空格键重新开始", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        
        # 退出提示
        exit_text = self.font.render("按ESC键退出游戏", True, WHITE)
        exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 90))
        
        # 绘制所有文本
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, score_rect)
        self.screen.blit(final_level_text, level_rect)
        self.screen.blit(obstacle_text, obstacle_rect)
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