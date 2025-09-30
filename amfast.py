import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 90
PIPE_GAP = 250
PIPE_SPEED = 3
FPS = 85

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (0, 255, 0)

# Layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird ")
clock = pygame.time.Clock()

# Font untuk skor
font = pygame.font.Font(None, 36)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = 20
        self.color = (255, 255, 0)  # Kuning untuk burung

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        # Pipa atas
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # Pipa bawah
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP))

    def get_rects(self):
        # Rect untuk pipa atas
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        # Rect untuk pipa bawah
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)
        return top_rect, bottom_rect

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()

        # Update
        bird.update()

        # Tambah pipa baru secara periodik
        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe(SCREEN_WIDTH))

        for pipe in pipes[:]:
            pipe.update()
            if pipe.off_screen():
                pipes.remove(pipe)
            # Cek tabrakan
            top_rect, bottom_rect = pipe.get_rects()
            if bird.get_rect().colliderect(top_rect) or bird.get_rect().colliderect(bottom_rect):
                running = False  # Game over
            # Cek jika burung lewat pipa
            if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                pipe.passed = True
                score += 1

        # Cek batas layar (tanah dan langit)
        if bird.y + bird.size > SCREEN_HEIGHT or bird.y - bird.size < 0:
            running = False

        # Gambar
        screen.fill(BLUE)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Gambar skor
        draw_text(screen, f"Score: {score}", font, BLACK, 10, 10)

        pygame.display.flip()
        clock.tick(FPS)

    # Game over screen
    screen.fill(BLUE)
    draw_text(screen, f"Game Over! Score: {score}", font, BLACK, SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2)
    draw_text(screen, "Tekan SPASI untuk main lagi atau tutup jendela", pygame.font.Font(None, 24), BLACK, SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 50)
    pygame.display.flip()

    # Tunggu input untuk restart atau keluar
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main()  # Restart
                waiting = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
