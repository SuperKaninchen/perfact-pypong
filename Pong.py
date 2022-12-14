import sys, math, random, pygame
from mpnUtils.Vector import Vector


SIZE = WIDTH, HEIGHT = 1366, 720


class Ball(object):
    def __init__(self, size):
        self.reset()
        self.size = size
        self.surface = pygame.Surface((size*2, size*2))
        self.surface.fill((0, 0, 0))
        pygame.draw.circle(self.surface, (255, 255, 255), (size, size), size)

    def reset(self):
        self.pos = Vector(WIDTH/2, HEIGHT/2)
        self.vel = Vector.random() * 25
        self.speed = 25

    def move(self, delta):
        self.vel = self.vel.setMagnitude(self.speed)
        self.pos += self.vel * delta / 100

    def incSpeed(self, delta):
        self.speed += delta / 1000

    def checkRightColl(self, paddle):
        if self.center().x+self.size > paddle.pos.x:
            if not self.center().y+self.size > paddle.pos.y:
                return False
            if not self.center().y-self.size < paddle.pos.y+paddle.size.y:
                return False
            return True
        return False

    def checkLeftColl(self, paddle):
        if self.center().x-self.size < paddle.pos.x+paddle.size.x:
            if not self.center().y+self.size > paddle.pos.y:
                return False
            if not self.center().y-self.size < paddle.pos.y+paddle.size.y:
                return False
            return True
        return False

    def checkVertColl(self):
        if self.pos.y < 0 or self.pos.y+(self.size*2) > HEIGHT:
            self.vel.y *= -1
            return True
        return False

    def doCollide(self, paddle):
        #diff = paddle.center().y - self.pos.y
        self.vel.x *= -1
        #self.vel.y = diff * -1

    def center(self):
        x = self.pos.x + self.size
        y = self.pos.y + self.size
        return Vector(x, y)


class Paddle(object):
    def __init__(self, x, size):
        self.pos = Vector(x, HEIGHT/2-size.y/2)
        self.size = size
        self.surface = pygame.Surface((size.x, size.y))
        self.surface.fill((0, 0, 0))
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0, 0, size.x, size.y))

    def move(self, direction):
        self.pos.y += direction*10
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y+self.size.y > HEIGHT:
            self.pos.y = HEIGHT-self.size.y

    def center(self):
        x = self.pos.x + self.size.x/2
        y = self.pos.y + self.size.y/2
        return Vector(x, y)


class Game(object):

    def __init__(self):
        self.ball = Ball(10)
        p1 = Paddle(0, Vector(20, 150))
        p2 = Paddle(WIDTH-20, Vector(20, 150))
        self.paddles = (p1, p2)
        self.scores = Vector(0, 0)
        self.wall_sound = pygame.mixer.Sound("wall_hit.wav")
        self.paddle_sound = pygame.mixer.Sound("paddle_hit.wav")
        self.point_sound = pygame.mixer.Sound("point.wav")

    def update(self, delta):
        self.ball.incSpeed(delta)
        self.ball.move(delta)

        if self.ball.pos.x > WIDTH/2:
            if self.ball.checkRightColl(self.paddles[1]):
                self.ball.doCollide(self.paddles[1])
                self.paddle_sound.play()
            else:
                if self.ball.pos.x >= WIDTH:
                    self.scores.y += 1
                    self.point_sound.play()
                    self.ball.reset()
        else:
            if self.ball.checkLeftColl(self.paddles[0]):
                self.ball.doCollide(self.paddles[0])
                self.paddle_sound.play()
            else:
                if self.ball.pos.x <= 0:
                    self.scores.x += 1
                    self.point_sound.play()
                    self.ball.reset()

        if self.ball.checkVertColl():
            self.wall_sound.play()


def handlePlayerInput(game):
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        game.paddles[1].move(-1)
    if pressed[pygame.K_DOWN]:
        game.paddles[1].move(1)

    if pressed[pygame.K_w]:
        game.paddles[0].move(-1)
    if pressed[pygame.K_s]:
        game.paddles[0].move(1)


def show(screen, game, score):
    screen.fill((0, 0, 0))
    screen.blit(game.ball.surface, game.ball.pos.tuple())
    for paddle in game.paddles:
        screen.blit(paddle.surface, paddle.pos.tuple())
    screen.blit(score, (WIDTH/2-50, 50))
    pygame.display.flip()


def main():

    # Initialize pygame modules
    pygame.init()

    # Set window title
    pygame.display.set_caption("pongCEED")

    # Get display surface
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Instantiate clock for delta
    clock = pygame.time.Clock()

    # Initialize font object for rendering text
    font = pygame.font.Font(None, 32)

    # Initialize Game object
    game = Game()

    running = True
    while running:
        # Calculate delta and restrict fps to 60
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Game()
                elif event.key == pygame.K_ESCAPE:
                    running = False


        handlePlayerInput(game)

        # Time since last frame
        delta = clock.get_time()


        game.update(delta)
        score_surface = font.render(f"{game.scores.x} : {game.scores.y}", True, (255, 255, 255))
        show(screen, game, score_surface)


if __name__ == "__main__":
    main()
