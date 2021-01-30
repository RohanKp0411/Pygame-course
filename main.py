import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First game")


# Defining the image of the player walking left, right and standing still.
walkRight = (
    pygame.image.load("Images/R1.png"),
    pygame.image.load("Images/R2.png"),
    pygame.image.load("Images/R3.png"),
    pygame.image.load("Images/R4.png"),
    pygame.image.load("Images/R5.png"),
    pygame.image.load("Images/R6.png"),
    pygame.image.load("Images/R7.png"),
    pygame.image.load("Images/R8.png"),
    pygame.image.load("Images/R9.png"),
)
walkLeft = (
    pygame.image.load("Images/L1.png"),
    pygame.image.load("Images/L2.png"),
    pygame.image.load("Images/L3.png"),
    pygame.image.load("Images/L4.png"),
    pygame.image.load("Images/L5.png"),
    pygame.image.load("Images/L6.png"),
    pygame.image.load("Images/L7.png"),
    pygame.image.load("Images/L8.png"),
    pygame.image.load("Images/L9.png"),
)
bg = pygame.image.load("Images/bg.jpg")
char = pygame.image.load("Images/standing.png")

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound("Sound/bullet.mp3")
hitSound = pygame.mixer.Sound("Sound/hit.mp3")

music = pygame.mixer.music.load("Sound/music.mp3")
pygame.mixer.music.play(-1)
score = 0


sc_s = 500
x = 50
y = 430
width = 64
height = 64
vel = 5
isJump = False
jumpCount = 10
left = False
right = False
walkcount = 0


# ************* Player class ****************
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 10, 30, 58)

    def draw(self, win):
        if self.walkcount + 1 > 27:
            self.walkcount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            elif self.right:
                win.blit(walkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 20, self.y + 10, 30, 58)
        # pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-5", 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


# ************* Projectile class ****************
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# ************* Enemy class ****************
class enemy(object):
    # Defining the image of the enemy walking left and right.
    walkRight = [
        pygame.image.load("Images/R1E.png"),
        pygame.image.load("Images/R2E.png"),
        pygame.image.load("Images/R3E.png"),
        pygame.image.load("Images/R4E.png"),
        pygame.image.load("Images/R5E.png"),
        pygame.image.load("Images/R6E.png"),
        pygame.image.load("Images/R7E.png"),
        pygame.image.load("Images/R8E.png"),
        pygame.image.load("Images/R9E.png"),
        pygame.image.load("Images/R10E.png"),
        pygame.image.load("Images/R11E.png"),
    ]
    walkLeft = [
        pygame.image.load("Images/L1E.png"),
        pygame.image.load("Images/L2E.png"),
        pygame.image.load("Images/L3E.png"),
        pygame.image.load("Images/L4E.png"),
        pygame.image.load("Images/L5E.png"),
        pygame.image.load("Images/L6E.png"),
        pygame.image.load("Images/L7E.png"),
        pygame.image.load("Images/L8E.png"),
        pygame.image.load("Images/L9E.png"),
        pygame.image.load("Images/L10E.png"),
        pygame.image.load("Images/L11E.png"),
    ]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible == True:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(
                win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)
            )
            pygame.draw.rect(
                win,
                (0, 128, 0),
                (
                    self.hitbox[0],
                    self.hitbox[1] - 20,
                    50 - (5 * (10 - self.health)),
                    10,
                ),
            )
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

            pass

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        pass

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("HIT")


def redrawGameWindow():

    win.blit(bg, (0, 0))
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (390, 10))
    Lamba.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# ************* Main Loop ****************

font = pygame.font.SysFont("comicsans", 30, True, True)
Lamba = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []


run = True
while run:
    clock.tick(27)
    if goblin.visible == True:
        if (
            Lamba.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3]
            and Lamba.hitbox[1] + Lamba.hitbox[3] > goblin.hitbox[1]
        ):
            if (
                Lamba.hitbox[0] + Lamba.hitbox[2] > goblin.hitbox[0]
                and Lamba.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]
            ):
                Lamba.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # ************* for loop for shooting bullets ****************
    for bullet in bullets:
        if (
            bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3]
            and bullet.y + bullet.radius > goblin.hitbox[1]
        ):
            if (
                bullet.x + bullet.radius > goblin.hitbox[0]
                and bullet.x - bullet.radius < goblin.hitbox[1] + goblin.hitbox[2]
            ):
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if Lamba.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(
                projectile(
                    round(Lamba.x + Lamba.width // 2),
                    round(Lamba.y + Lamba.height // 2),
                    6,
                    (255, 167, 0),
                    facing,
                )
            )

        shootLoop = 1
    # ************* Player movement ****************
    if keys[pygame.K_LEFT] and Lamba.x > Lamba.vel:
        Lamba.x -= Lamba.vel
        Lamba.left = True
        Lamba.right = False
        Lamba.standing = False

    elif keys[pygame.K_RIGHT] and Lamba.x < sc_s - Lamba.width - Lamba.vel:
        Lamba.x += Lamba.vel
        Lamba.right = True
        Lamba.left = False
        Lamba.standing = False
    else:
        Lamba.standing = True
        Lamba.walkcount = 0

    if not (Lamba.isJump):
        if keys[pygame.K_UP]:
            Lamba.isJump = True
            Lamba.right = False
            Lamba.left = False
            Lamba.walkcount = 0
    else:
        if Lamba.jumpCount >= -10:
            neg = 1
            if Lamba.jumpCount < 0:
                neg = -1
            Lamba.y -= (Lamba.jumpCount ** 2) * 0.5 * neg
            Lamba.jumpCount -= 1

        else:
            Lamba.isJump = False
            Lamba.jumpCount = 10

    redrawGameWindow()


pygame.quit()
