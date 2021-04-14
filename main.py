import pygame
import time
import random
from pygame.locals import *

# Define constants
BACKGROUND_COLOR = (52, 195, 235)
SIZE_X = 1000
SIZE_Y = 500
SIZE = 20


class Rabbit:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/rabbit.png").convert()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    # Print rabbit
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # Move new rabbit
    def move(self):
        cant_x = (SIZE_X / SIZE)-1
        cant_y = (SIZE_Y / SIZE)-1
        self.x = random.randint(0, cant_x) * SIZE
        self.y = random.randint(0, cant_y) * SIZE
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/Snake/point.png").convert()
        self.block = pygame.transform.scale(self.block, (20, 20))
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    # Increase longitude snake
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    # Print snake
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    # Move directions
    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Change direction walk
        if self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        elif self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE

        # Print new position
        self.draw()


class Game:
    def __init__(self):
        # Init pygame
        pygame.init()
        pygame.display.set_caption("Snake and rabbit")

        # Init music reproducer
        pygame.mixer.init()

        # Play sound background
        music("background2", "mp3")

        # Print snake and rabbit
        self.surface = pygame.display.set_mode((SIZE_X, SIZE_Y))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.rabbit = Rabbit(self.surface)
        self.rabbit.draw()

    # Init game
    def play(self):
        # Draw the elements
        render_background(self)
        self.snake.walk()
        self.rabbit.draw()
        self.display_Score()
        pygame.display.flip()

        # Collision with rabbit
        if is_collision(self.snake.x[0], self.snake.y[0], self.rabbit.x, self.rabbit.y):
            sound("eat", "wav")
            self.snake.increase_length()
            self.rabbit.move()

        # Collision with snake
        for i in range(1, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound("crash", "wav")
                raise Exception("Game Over")

        # Collision with borders and game over
        # for i in range(0, SIZE_X):
        #     if is_collision(self.snake.x[0], self.snake.y[0], 0, i):
        #         sound("crash", "wav")
        #         raise Exception("Game Over")
        #
        # for i in range(0, SIZE_X):
        #     if is_collision(self.snake.x[0], self.snake.y[0], i, SIZE_Y):
        #         sound("crash", "wav")
        #         raise Exception("Game Over")
        #
        # for i in range(0, SIZE_Y):
        #     if is_collision(self.snake.x[0], self.snake.y[0], i, 0):
        #         sound("crash", "wav")
        #         raise Exception("Game Over")
        #
        # for i in range(0, SIZE_Y):
        #     if is_collision(self.snake.x[0], self.snake.y[0], SIZE_X, i):
        #         sound("crash", "wav")
        #         raise Exception("Game Over")

        # Collision with borders and teleport snake
        for i in range(0, SIZE_X):
            if is_collision(self.snake.x[0], self.snake.y[0], -20, i):
                self.snake.x[0] = SIZE_X
                self.snake.y[0] = i
            if is_collision(self.snake.x[0], self.snake.y[0], i, SIZE_Y+20):
                self.snake.x[0] = i
                self.snake.y[0] = 0

        for i in range(0, SIZE_Y):
            if is_collision(self.snake.x[0], self.snake.y[0], i, -20):
                self.snake.x[0] = i
                self.snake.y[0] = SIZE_Y
            if is_collision(self.snake.x[0], self.snake.y[0], SIZE_X+20, i):
                self.snake.x[0] = 0
                self.snake.y[0] = i

        # Print new position
        self.snake.draw()

    # Show game over when collision
    def show_game_over(self):
        # Init surface and font
        render_background(self)
        font = pygame.font.SysFont('arial', 30)

        # Calculated score
        score = (self.snake.length - 2) * 100

        # Print the message
        line = font.render(f"Game is over! Your score is: {score}", True, (255, 255, 255))
        self.surface.blit(line, (250, 200))
        line2 = font.render("To play again press Enter. To exit press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (250, 250))

        # Update screen
        pygame.display.flip()

        # Pause music background
        pygame.mixer.music.pause()

    # Print score
    def display_Score(self):
        score = (self.snake.length-3)*100
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {score}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))

    # Reset all the game
    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.rabbit = Rabbit(self.surface)

    # Execute game
    def run(self):
        if menu(self):
            running = True
            pause = False
            i = 0

            while running:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = checkout(self)

                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause()
                            pause = False

                        if not pause:
                            if event.key == K_UP:
                                self.snake.move_up()
                            if event.key == K_DOWN:
                                self.snake.move_down()
                            if event.key == K_LEFT:
                                self.snake.move_left()
                            if event.key == K_RIGHT:
                                self.snake.move_right()

                    elif event.type == QUIT:
                        running = checkout(self)

                    if i == 25:
                        i = 0
                        sound("snake", "wav")
                    else:
                        i += 1
                try:
                    if not pause:
                        self.play()
                except Exception as e:
                    self.show_game_over()
                    pause = True
                    self.reset()

                time.sleep(.3)


# Menu principal
def menu(self):
    # Clear screen
    render_background(self)

    # Init variables
    running = False
    font = pygame.font.SysFont('arial', 30)

    # Print the message
    line2 = font.render("To play press Enter. To exit press Escape", True, (255, 255, 255))
    self.surface.blit(line2, (250, 250))

    # Update screen
    pygame.display.flip()

    # Listen the event type == KEY_DOWN
    while not running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_RETURN:
                    return True


# Check if secure to exit
def checkout(self):
    # Pause music
    pygame.mixer.music.pause()

    # Clear screen
    render_background(self)

    # Init variables
    running = True
    font = pygame.font.SysFont('arial', 30)

    # Print the message
    line2 = font.render("To play again press Enter. To exit press Escape", True, (255, 255, 255))
    self.surface.blit(line2, (250, 250))

    # Update screen
    pygame.display.flip()

    # Listen the event type == KEY_DOWN
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_RETURN:
                    # Unpause music
                    pygame.mixer.music.unpause()
                    return True


# Check is collision
def is_collision(x1, y1, x2, y2):
    if x1 >= x2 >= x1:
        if y1 >= y2 >= y1:
            return True

    return False


# Play sound
def sound(name, extension):
    file_sound = pygame.mixer.Sound(f"resources/Music/{name}.{extension}")
    pygame.mixer.Sound.play(file_sound)


# Play music
def music(name, extension):
    pygame.mixer.music.load(f"resources/Music/{name}.{extension}")
    pygame.mixer.music.play()


# Render background
def render_background(self):
    # Load the image
    bg = pygame.image.load("resources/grass-texture.jpg")

    # Transform the image for better view
    bg = pygame.transform.scale(bg, (1000, 500))
    self.surface.blit(bg, (0, 0))


if __name__ == '__main__':
    game = Game()
    game.run()
