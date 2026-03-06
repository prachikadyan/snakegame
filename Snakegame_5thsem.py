import turtle
import time
import random

# ─── GAME SETTINGS ───────────────────────────────────────────
delay      = 0.12
score      = 0
high_score = 0
level      = 1
paused     = False
game_over  = False

# ─── SCREEN SETUP ────────────────────────────────────────────
wn = turtle.Screen()
wn.title("🐍 Snake Game")
wn.bgcolor("black")
wn.setup(width=700, height=700)
wn.tracer(0)

# ─── DRAW BORDER ─────────────────────────────────────────────
border = turtle.Turtle()
border.speed(0)
border.color("lime")
border.penup()
border.goto(-305, 285)
border.pendown()
border.pensize(4)
for _ in range(4):
    border.forward(610)
    border.right(90)
border.hideturtle()

# ─── SNAKE HEAD ──────────────────────────────────────────────
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ─── FOOD ────────────────────────────────────────────────────
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(random.randint(-13, 13) * 20, random.randint(-13, 13) * 20)

# ─── BONUS FOOD ──────────────────────────────────────────────
bonus = turtle.Turtle()
bonus.speed(0)
bonus.shape("triangle")
bonus.color("gold")
bonus.penup()
bonus.hideturtle()
bonus_active  = False
bonus_timer   = 0
bonus_limit   = 80

# ─── SCORE PEN ───────────────────────────────────────────────
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 310)

def update_score():
    pen.clear()
    pen.write(
        "Score: {}   High Score: {}   Level: {}".format(score, high_score, level),
        align="center",
        font=("Courier", 16, "bold")
    )

update_score()

# ─── MESSAGE PEN ─────────────────────────────────────────────
msg = turtle.Turtle()
msg.speed(0)
msg.color("yellow")
msg.penup()
msg.hideturtle()
msg.goto(0, 0)

def show_message(text):
    msg.clear()
    msg.write(text, align="center", font=("Courier", 22, "bold"))

def clear_message():
    msg.clear()

# ─── LEVEL UP PEN ────────────────────────────────────────────
lvl_pen = turtle.Turtle()
lvl_pen.speed(0)
lvl_pen.color("cyan")
lvl_pen.penup()
lvl_pen.hideturtle()
lvl_pen.goto(0, -50)
lvl_flash      = 0
lvl_flash_on   = False

# ─── CONTROLS ────────────────────────────────────────────────
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def toggle_pause():
    global paused
    if game_over:
        return
    paused = not paused
    if paused:
        show_message("⏸  PAUSED  —  Press P to Resume")
    else:
        clear_message()

def restart():
    global score, delay, level, paused, game_over, bonus_active, bonus_timer
    paused     = False
    game_over  = False
    score      = 0
    delay      = 0.12
    level      = 1
    bonus_active = False
    bonus_timer  = 0
    bonus.hideturtle()
    head.goto(0, 0)
    head.direction = "stop"
    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()
    clear_message()
    lvl_pen.clear()
    update_score()

wn.listen()
wn.onkeypress(go_up,       "Up")
wn.onkeypress(go_down,     "Down")
wn.onkeypress(go_left,     "Left")
wn.onkeypress(go_right,    "Right")
wn.onkeypress(go_up,       "w")
wn.onkeypress(go_down,     "s")
wn.onkeypress(go_left,     "a")
wn.onkeypress(go_right,    "d")
wn.onkeypress(toggle_pause,"p")
wn.onkeypress(restart,     "r")

# ─── MOVE FUNCTION ───────────────────────────────────────────
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# ─── SPAWN FOOD AT RANDOM GRID POSITION ──────────────────────
def spawn_food():
    x = random.randint(-13, 13) * 20
    y = random.randint(-13, 13) * 20
    food.goto(x, y)

def spawn_bonus():
    x = random.randint(-13, 13) * 20
    y = random.randint(-13, 13) * 20
    bonus.goto(x, y)
    bonus.showturtle()

# ─── FLASH LEVEL UP MESSAGE ──────────────────────────────────
def flash_level(lv):
    lvl_pen.clear()
    lvl_pen.write(
        "  ★  LEVEL {}  ★  ".format(lv),
        align="center",
        font=("Courier", 20, "bold")
    )

# ─── GAME OVER SCREEN ────────────────────────────────────────
def show_game_over():
    msg.goto(0, 30)
    msg.color("red")
    msg.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
    msg.goto(0, -20)
    msg.color("white")
    msg.write(
        "Score: {}   Best: {}".format(score, high_score),
        align="center",
        font=("Courier", 18, "bold")
    )
    msg.goto(0, -70)
    msg.color("yellow")
    msg.write("Press  R  to Restart", align="center", font=("Courier", 16, "normal"))
    msg.goto(0, 0)

# ─── SEGMENTS LIST ───────────────────────────────────────────
segments = []

show_message("Press W A S D or Arrow Keys to Start!")

# ══════════════════════════════════════════════════════════════
#  MAIN GAME LOOP
# ══════════════════════════════════════════════════════════════
while True:
    wn.update()

    # ── Skip if paused or game over ──
    if paused or game_over:
        time.sleep(0.05)
        continue

    # ── Wall collision ───────────────────────────────────
    if (head.xcor() > 290 or head.xcor() < -290 or
            head.ycor() > 290 or head.ycor() < -290):
        game_over = True
        head.goto(1000, 1000)
        for seg in segments:
            seg.goto(1000, 1000)
        bonus.hideturtle()
        bonus_active = False
        show_game_over()
        continue

    # ── Eat apple ───────────────────────────────────────
    if head.distance(food) < 18:
        spawn_food()

        # Add new body segment
        new_seg = turtle.Turtle()
        new_seg.speed(0)
        new_seg.shape("square")
        # Colour changes with level
        seg_colors = ["orange", "yellow", "cyan", "magenta",
                      "pink", "lightblue", "white", "salmon",
                      "lime", "gold"]
        new_seg.color(seg_colors[(level - 1) % len(seg_colors)])
        new_seg.penup()
        segments.append(new_seg)

        score += 10
        if score > high_score:
            high_score = score

        # Speed up slightly
        delay = max(0.04, delay - 0.002)

        # Level up every 5 apples
        new_level = 1 + score // 50
        if new_level > level:
            level = new_level
            flash_level(level)
            lvl_flash    = 0
            lvl_flash_on = True

        # Spawn bonus every 3 apples
        if score % 30 == 0 and not bonus_active:
            spawn_bonus()
            bonus_active = True
            bonus_timer  = 0

        update_score()

    # ── Eat bonus ────────────────────────────────────────
    if bonus_active and head.distance(bonus) < 18:
        bonus.hideturtle()
        bonus_active = False
        bonus_timer  = 0
        score += 50
        if score > high_score:
            high_score = score
        update_score()

        # Flash bonus message briefly
        lvl_pen.clear()
        lvl_pen.color("gold")
        lvl_pen.write(
            "  ★  +50 BONUS!  ★  ",
            align="center",
            font=("Courier", 18, "bold")
        )
        lvl_pen.color("cyan")
        lvl_flash    = 0
        lvl_flash_on = True

    # ── Bonus food timeout ───────────────────────────────
    if bonus_active:
        bonus_timer += 1
        if bonus_timer >= bonus_limit:
            bonus.hideturtle()
            bonus_active = False
            bonus_timer  = 0

    # ── Clear level flash after 25 frames ────────────────
    if lvl_flash_on:
        lvl_flash += 1
        if lvl_flash > 25:
            lvl_pen.clear()
            lvl_flash_on = False
            lvl_flash    = 0

    # ── Move body segments ───────────────────────────────
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # ── Move head ────────────────────────────────────────
    move()

    # ── Self collision ───────────────────────────────────
    for seg in segments:
        if seg.distance(head) < 18:
            game_over = True
            head.goto(1000, 1000)
            for s in segments:
                s.goto(1000, 1000)
            bonus.hideturtle()
            bonus_active = False
            show_game_over()
            break

    time.sleep(delay)

wn.mainloop()
