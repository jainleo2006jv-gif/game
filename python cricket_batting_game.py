import pygame
import random
import sys

# ================= SAFE INIT =================
pygame.init()

try:
    pygame.mixer.init(44100, -16, 2)
except pygame.error:
    print("Audio disabled")

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

hit_sound = load_sound("hit.wav")
out_sound = load_sound("out.wav")

# ================= SCREEN =================
WIDTH, HEIGHT = 900, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cricket Batting Game – 1 Over")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 60)

# ================= COLORS =================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (50, 100, 255)

# ================= MATCH SETTINGS =================
MAX_OVERS = 1        # 🔥 ONE OVER ONLY
TARGET = 20          # You can change target

# ================= RESET GAME =================
def reset_game():
    global score, wickets, balls, power, charging
    global ball_x, ball_y, ball_state, swing_dir, game_over

    score = 0
    wickets = 0
    balls = 0
    power = 0
    charging = False
    game_over = False

    ball_x = WIDTH - 50
    ball_y = HEIGHT // 2
    ball_state = "bowling"
    swing_dir = random.choice([-1, 1])

# ================= GAME STATE =================
game_over = False
reset_game()

# ================= BAT =================
bat_zone = pygame.Rect(140, 150, 70, 120)

# ================= BOWLERS =================
BOWLERS = [
    {"name": "Fast Bowler", "speed": 10, "swing": 0.3},
    {"name": "Swing Bowler", "speed": 7, "swing": 1.0},
    {"name": "Spin Bowler", "speed": 5, "swing": 1.5},
]

# ================= DRAW TEXT =================
def draw_text(text, x, y, big=False):
    f = big_font if big else font
    screen.blit(f.render(text, True, BLACK), (x, y))

# ================= MAIN LOOP =================
while True:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------- GAME OVER MENU --------
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            continue

        # -------- INPUT --------
        if event.type == pygame.MOUSEBUTTONDOWN:
            charging = True
            power = 0

        if event.type == pygame.MOUSEBUTTONUP:
            charging = False
            if ball_state == "bowling" and bat_zone.collidepoint(ball_x, ball_y):
                if hit_sound:
                    hit_sound.play()
                ball_state = "air" if power > 60 else "ground"
            else:
                wickets += 1
                balls += 1
                if out_sound:
                    out_sound.play()
                ball_state = "bowling"

    # -------- GAME OVER SCREEN --------
    if game_over:
        draw_text("GAME OVER", 330, 140, big=True)
        draw_text(f"Final Score: {score}", 350, 210)
        draw_text("Press R to Restart", 330, 260)
        draw_text("Press Q to Quit", 350, 300)
        pygame.display.update()
        continue

    # -------- POWER --------
    if charging and power < 100:
        power += 2

    bowler = BOWLERS[(balls // 6) % len(BOWLERS)]

    # -------- BALL LOGIC --------
    if ball_state == "bowling":
        ball_x -= bowler["speed"]
        ball_y += bowler["swing"] * swing_dir

        if ball_x < 0:
            wickets += 1
            balls += 1
            ball_state = "bowling"

    elif ball_state == "air":
        ball_x += 6
        ball_y -= 4
        if ball_x > WIDTH:
            score += 6 if power > 80 else 4
            balls += 1
            ball_state = "bowling"

    elif ball_state == "ground":
        ball_x += 4
        if ball_x > WIDTH:
            score += 2 if power > 50 else 1
            balls += 1
            ball_state = "bowling"

    # -------- RESET BALL --------
    if ball_state == "bowling":
        ball_x = WIDTH - 50
        ball_y = random.randint(160, 260)
        swing_dir = random.choice([-1, 1])

    overs = balls // 6
    current_ball = balls % 6
    balls_left = max(0, 6 - balls)

    # -------- END CONDITION --------
    if overs >= MAX_OVERS:
        game_over = True

    # -------- DRAW --------
    pygame.draw.rect(screen, GREEN, bat_zone)
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), 8)

    pygame.draw.rect(screen, BLACK, (140, 310, 100, 12), 2)
    pygame.draw.rect(screen, BLUE, (142, 312, power, 8))

    draw_text(f"Score: {score}", 20, 20)
    draw_text(f"Wickets: {wickets}", 20, 50)
    draw_text(f"Overs: 0.{current_ball}", 20, 80)
    draw_text(f"Balls Left: {balls_left}", 20, 110)
    draw_text(f"Target: {TARGET}", 20, 140)
    draw_text(f"Bowler: {bowler['name']}", 20, 170)
    draw_text("Hold mouse = power | Release = hit", 420, 20)

    pygame.display.update()
