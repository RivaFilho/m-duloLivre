import pygame
import sys
import time
import random
import json

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, game_window):
        raise NotImplementedError("This method should be overridden in child classes")

class Snake(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.body = [[x, y], [x - 10, y], [x - 20, y]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def move(self):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.y -= 10
        if self.direction == 'DOWN':
            self.y += 10
        if self.direction == 'LEFT':
            self.x -= 10
        if self.direction == 'RIGHT':
            self.x += 10

        self.body.insert(0, [self.x, self.y])

    def grow(self):
        pass

    def shrink(self):
        self.body.pop()

    def render(self, game_window):
        for segment in self.body:
            pygame.draw.rect(game_window, pygame.Color(0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))

class Food(GameObject):
    def __init__(self, frame_size_x, frame_size_y):
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        super().__init__(
            random.randrange(1, (frame_size_x // 10)) * 10,
            random.randrange(1, (frame_size_y // 10)) * 10
        )

    def spawn(self):
        self.x = random.randrange(1, (self.frame_size_x // 10)) * 10
        self.y = random.randrange(1, (self.frame_size_y // 10)) * 10

    def render(self, game_window):
        pygame.draw.rect(game_window, pygame.Color(255, 255, 255), pygame.Rect(self.x, self.y, 10, 10))

class Player:
    def __init__(self, username):
        self.username = username
        self.scores = {"Fácil": 0, "Médio": 0, "Difícil": 0, "Impossível": 0}

    @staticmethod
    def load_data(file_path='players.json'):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_data(data, file_path='players.json'):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def update_score(self, score, difficulty):
        data = Player.load_data()
        if self.username in data:
            if score > data[self.username]['scores'][difficulty]:
                data[self.username]['scores'][difficulty] = score
        else:
            data[self.username] = {"scores": self.scores}
            data[self.username]['scores'][difficulty] = score
        Player.save_data(data)

    def get_scores(self):
        data = Player.load_data()
        return data.get(self.username, {}).get('scores', self.scores)

class Game:
    def __init__(self):
        pygame.init()
        self.difficulty = "Médio"
        self.frame_size_x = 720
        self.frame_size_y = 480

        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        pygame.display.set_caption('Snake Eater')

        self.snake = Snake(100, 50)
        self.food = Food(self.frame_size_x, self.frame_size_y)

        self.player = None
        self.score = 0
        self.fps_controller = pygame.time.Clock()
        self.difficulty_map = {"Fácil": 10, "Médio": 25, "Difícil": 40, "Impossível": 60}
        self.colors = {
            'black': pygame.Color(0, 0, 0),
            'red': pygame.Color(255, 0, 0),
            'white': pygame.Color(255, 255, 255)
        }

    def get_username(self):
        font = pygame.font.SysFont('times new roman', 40)
        header_font = pygame.font.SysFont('times new roman', 50)
        input_box = pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 3, 300, 50)
        color_active = pygame.Color('lightskyblue3')
        color_inactive = pygame.Color('gray15')
        color = color_inactive
        active = False
        text = ''

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.game_window.fill(self.colors['black'])
            header_surface = header_font.render("Registre um usuario", True, self.colors['white'])
            self.game_window.blit(header_surface, (self.frame_size_x / 3, self.frame_size_y / 3 - 70))
            txt_surface = font.render(text, True, self.colors['white'])
            self.game_window.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
            pygame.draw.rect(self.game_window, color, input_box, 2)
            pygame.display.flip()

    def select_difficulty(self):
        font = pygame.font.SysFont('times new roman', 30)
        difficulties = ["Fácil", "Médio", "Difícil", "Impossível"]
        buttons = []

        for i, difficulty in enumerate(difficulties):
            button = {
                'rect': pygame.Rect(self.frame_size_x / 4, self.frame_size_y / 3 + i * 60, 300, 50),
                'color': pygame.Color('lightskyblue3'),
                'text': difficulty,
                'font': font
            }
            buttons.append(button)

        while True:
            self.game_window.fill(self.colors['black'])
            header_surface = font.render("Selecione a dificuldade", True, self.colors['white'])
            self.game_window.blit(header_surface, (self.frame_size_x / 4, self.frame_size_y / 4 - 50))

            for button in buttons:
                pygame.draw.rect(self.game_window, button['color'], button['rect'])
                text_surface = button['font'].render(button['text'], True, self.colors['white'])
                text_rect = text_surface.get_rect(center=button['rect'].center)
                self.game_window.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button['rect'].collidepoint(event.pos):
                            self.difficulty = button['text']
                            return

    def show_scores(self):
        scores = self.player.get_scores()
        font = pygame.font.SysFont('times new roman', 30)
        self.game_window.fill(self.colors['black'])

        y_offset = self.frame_size_y / 4
        for difficulty, score in scores.items():
            text = f'{difficulty}: {score}'
            text_surface = font.render(text, True, self.colors['white'])
            self.game_window.blit(text_surface, (self.frame_size_x / 4, y_offset))
            y_offset += 40

        pygame.display.flip()
        time.sleep(3)

    def game_over_screen(self):
        self.player.update_score(self.score, self.difficulty)
        font = pygame.font.SysFont('times new roman', 40)

        retry_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 - 50, 200, 50),
            'color': pygame.Color('green'),
            'text': 'Retry',
            'font': font
        }
        logout_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 + 20, 200, 50),
            'color': pygame.Color('blue'),
            'text': 'Logout',
            'font': font
        }
        exit_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 + 90, 200, 50),
            'color': pygame.Color('red'),
            'text': 'Exit',
            'font': font
        }
        scores_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 + 160, 200, 50),
            'color': pygame.Color('yellow'),
            'text': 'Scores',
            'font': font
        }
        difficulty_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 + 230, 200, 50),
            'color': pygame.Color('orange'),
            'text': 'Change Difficulty',
            'font': font
        }

        buttons = [retry_button, logout_button, exit_button, scores_button, difficulty_button]

        while True:
            self.game_window.fill(self.colors['black'])
            game_over_text = font.render('GAME OVER', True, self.colors['red'])
            self.game_window.blit(game_over_text, (self.frame_size_x / 3, self.frame_size_y / 3 - 50))

            for button in buttons:
                pygame.draw.rect(self.game_window, button['color'], button['rect'])
                text_surface = button['font'].render(button['text'], True, self.colors['white'])
                text_rect = text_surface.get_rect(center=button['rect'].center)
                self.game_window.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button['rect'].collidepoint(event.pos):
                        self.snake = Snake(100, 50)
                        self.food = Food(self.frame_size_x, self.frame_size_y)
                        self.score = 0
                        
    def game_over_screen(self):
        self.player.update_score(self.score, self.difficulty)
        font = pygame.font.SysFont('times new roman', 30)

        retry_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 - 80, 200, 50),
            'color': pygame.Color('blue'),
            'text': 'Tentar nov',
            'font': font
        }
        logout_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 - 10, 200, 50),
            'color': pygame.Color('blue'),
            'text': 'Logout',
            'font': font
        }
        exit_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 + 60, 200, 50),
            'color': pygame.Color('red'),
            'text': 'Sair',
            'font': font
        }
        scores_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 + 130, 200, 50),
            'color': pygame.Color('blue'),
            'text': 'Scores',
            'font': font
        }
        difficulty_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y / 2 + 200, 200, 50),
            'color': pygame.Color('blue'),
            'text': 'Dificuldade',
            'font': font
        }

        buttons = [retry_button, logout_button, exit_button, scores_button, difficulty_button]

        while True:
            self.game_window.fill(self.colors['black'])
            game_over_text = font.render('GAME OVER', True, self.colors['red'])
            self.game_window.blit(game_over_text, (self.frame_size_x / 3, self.frame_size_y / 3 - 50))

            for button in buttons:
                pygame.draw.rect(self.game_window, button['color'], button['rect'])
                text_surface = button['font'].render(button['text'], True, self.colors['white'])
                text_rect = text_surface.get_rect(center=button['rect'].center)
                self.game_window.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button['rect'].collidepoint(event.pos):
                        self.snake = Snake(100, 50)
                        self.food = Food(self.frame_size_x, self.frame_size_y)
                        self.score = 0
                        return
                    if logout_button['rect'].collidepoint(event.pos):
                        self.__init__()  # Restart the game to allow username input
                        self.run()
                    if exit_button['rect'].collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if scores_button['rect'].collidepoint(event.pos):
                        self.show_scores_screen()
                    if difficulty_button['rect'].collidepoint(event.pos):
                        self.select_difficulty()
                        self.snake = Snake(100, 50)
                        self.food = Food(self.frame_size_x, self.frame_size_y)
                        self.score = 0
                        return

    def show_scores_screen(self):
        scores = self.player.get_scores()
        font = pygame.font.SysFont('times new roman', 30)
        self.game_window.fill(self.colors['black'])

        y_offset = self.frame_size_y / 4
        for difficulty, score in scores.items():
            text = f'{difficulty}: {score}'
            text_surface = font.render(text, True, self.colors['white'])
            self.game_window.blit(text_surface, (self.frame_size_x / 4, y_offset))
            y_offset += 40

        back_button = {
            'rect': pygame.Rect(self.frame_size_x / 3, self.frame_size_y - 100, 200, 50),
            'color': pygame.Color('green'),
            'text': 'Back',
            'font': font
        }
        pygame.draw.rect(self.game_window, back_button['color'], back_button['rect'])
        text_surface = back_button['font'].render(back_button['text'], True, self.colors['white'])
        text_rect = text_surface.get_rect(center=back_button['rect'].center)
        self.game_window.blit(text_surface, text_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button['rect'].collidepoint(event.pos):
                        return

    def run(self):
        username = self.get_username()
        self.player = Player(username)
        self.select_difficulty()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.snake.change_to = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.snake.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.snake.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.snake.change_to = 'RIGHT'

            self.snake.move()

            # Check if snake eats food
            if self.snake.x == self.food.x and self.snake.y == self.food.y:
                self.score += 1
                self.food.spawn()
            else:
                self.snake.shrink()

            # Check game over conditions
            if (
                self.snake.x < 0 or self.snake.x >= self.frame_size_x or
                self.snake.y < 0 or self.snake.y >= self.frame_size_y
            ):
                self.game_over_screen()

            for block in self.snake.body[1:]:
                if self.snake.x == block[0] and self.snake.y == block[1]:
                    self.game_over_screen()

            self.game_window.fill(self.colors['black'])
            self.snake.render(self.game_window)
            self.food.render(self.game_window)
            score_font = pygame.font.SysFont('consolas', 20)
            score_surface = score_font.render(f'Score: {self.score}', True, self.colors['white'])
            self.game_window.blit(score_surface, (10, 10))
            pygame.display.update()
            self.fps_controller.tick(self.difficulty_map[self.difficulty])

if __name__ == '__main__':
    Game().run()
