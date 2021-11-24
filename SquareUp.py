import pygame
import os
from random import randint

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Intialisation
pygame.init()
icon = pygame.image.load('Assets\RedSquare.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 700), pygame.RESIZABLE)
screen.fill("white")
pygame.display.set_caption('Square Up')
clock = pygame.time.Clock()
Font = pygame.font.Font('Assets\PixelatedFont1.ttf', 50)
FontRestart = pygame.font.Font('Assets\PixelatedFont1.ttf', 45)
ScoreFont = pygame.font.Font('Assets\PixelatedFont1.ttf', 45)
fullscreen = 'notsussy'
groundheight = 200
groundwidth = 800
w, h = pygame.display.get_surface().get_size()
print('e')

StarCollection = 0
GameActive = True
Intro = True


# Introduction
def ScorePrint():
    global Current_time
    Current_time = int((pygame.time.get_ticks() - StartTime)/90)

    scoresurf = ScoreFont.render(f"{Current_time}", False, (64, 64, 64))

    score_rect = scoresurf.get_rect(midtop=(400, 50))

    screen.blit(scoresurf, score_rect)

    # surface, color, start_pos, end_pos, width


ButtonLength = 150
ButtonHeight = 80
PlayButton = pygame.Surface((ButtonLength, ButtonHeight))
PlayRect = PlayButton.get_rect(center=(400, 450))

RestartButton = FontRestart.render('Restart?', False, 'Black')
RestartRect = RestartButton.get_rect(midtop=(800/2, 50))

# TextBoxes
# This has the size down conveniently despite not used
text1 = Font.render('My game', False, 'Black')
TextRect = text1.get_rect(midtop=(800/2, 50))

TitleFont = pygame.font.Font('Assets\PixelatedFont1.ttf', 100)
TitleCard = TitleFont.render('Square Up', False, '#FFC400')
#TitleCard = pygame.transform.rotate(TitleCard, -5)
TitleCardRect = TitleCard.get_rect(midtop=(800/2, 200))

ControlFonts = pygame.font.Font('Assets\PixelatedFont1.ttf', 20)
Controls = ControlFonts.render(
    "Press Space and Arrow Keys", False, (64, 64, 64))
ControlRect = Controls.get_rect(midtop=(400, 100))

IntroPlayer = pygame.Surface((175, 175))
IntroPlayerRect = IntroPlayer.get_rect(center=(400, 500))
IntroPlayer.fill('Black')

IntroPlayerRed = pygame.Surface((150, 150))
IntroPlayerRedRect = IntroPlayerRed.get_rect(bottomright=(400, 500))
IntroPlayerRed.fill((160, 0, 0))

IntroPlayerBlue = pygame.Surface((150, 150))
IntroPlayerBlueRect = IntroPlayerBlue.get_rect(topleft=(400, 500))
IntroPlayerBlue.fill((0, 0, 160))

# Player
Player = pygame.Surface((50, 50))
Player.fill("black")
PlayerRect = Player.get_rect(midbottom=(400, 500))
Player_GravityX = 0
Jump, Left, Right = False, False, False
JumpRecord = PlayerRect.y
StartTime = 0
playerX_change = 0


def Gravity(Xvalue, JumpRecord):  # f: y = -0.08 (x - 50)² + 200
    # (700-JumpRecord)
    return (JumpRecord - (-0.08 * float((Xvalue-50)**2) + 200))


# Enemies
Enemy1_Surf = pygame.Surface((100, 100))
Enemy1_Surf.fill((160, 0, 0))

Enemy2_Surf = pygame.Surface((500, 20))
Enemy2_Surf.fill((0, 0, 160))
#Enemy2Rect = Enemy2_Surf.get_rect(midbottom=(800, 300))


# Obstacle timer
Enemy1_Timer = pygame.USEREVENT + 0
pygame.time.set_timer(Enemy1_Timer, 900)
Enemy1List = []


def Enemy1_Movement():  # Enemy1List #Automatically uses the global function
    global Enemy1List
    if Enemy1List:
        for Enemy1 in Enemy1List:
            Enemy1.x -= 5

            screen.blit(Enemy1_Surf, Enemy1)
        Enemy1List = [obstacle for obstacle in Enemy1List if obstacle.x > -100]


def Enemy1_Collisions():
    global GameActive
    global RoundEndTime
    for enemy1 in Enemy1List:
        if PlayerRect.colliderect(enemy1):
            GameActive = False
            RoundEndTime = pygame.time.get_ticks()
            global ENDscoresurf
            global ENDscoreRect
            ENDscoresurf = ScoreFont.render(
                f"Score: {Current_time}", False, (64, 64, 64))
            ENDscoreRect = ENDscoresurf.get_rect(center=(400, 20))
            break


# Stars

Stars = pygame.Surface((20, 20))
Stars.fill("Yellow")
# Use random module to get from x(20 to 780), y(20 to 580)

# Ground
Ground = pygame.Surface((800, 200))
GroundRect = Ground.get_rect(bottomleft=(0, 700))
Ground.fill((60, 35, 20))

# GameLoop
while True:

    if Intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.FULLSCREEN:
                pygame.display.toggle_fullscreen
                w, h = pygame.display.get_surface().get_size()
                if fullscreen == 'sussy':
                    fulscreen = 'notsussy'
                elif fulscreen == 'notsussy':
                    fulscreen = 'sussy'
                else:
                    print('iamneilandmyvariablesmakenosense2:)')
                # Ground
                if fullscreen == 'sussy':
                    groundheight = 35/100
                    groundheight = groundheight * h
                    groundwidth = 69000
                    print(w, groundheight, h)

                else:
                    groundheight = 200
                    groundwidth = 800
                Ground = pygame.Surface((groundwidth, groundheight))
                GroundRect = Ground.get_rect(bottomleft=(0, 700))
                Ground.fill((60, 35, 20))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                StartTime = pygame.time.get_ticks()
                Intro = False

        screen.blit(TitleCard, TitleCardRect)
        screen.blit(Controls, ControlRect)
        screen.blit(IntroPlayerRed, IntroPlayerRedRect)
        screen.blit(IntroPlayerBlue, IntroPlayerBlueRect)
        screen.blit(IntroPlayer, IntroPlayerRect)

        pygame.display.update()
        continue

    if GameActive:
        screen.fill("white")
        ### Floor ###
        screen.blit(Ground, GroundRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == Enemy1_Timer:
                Enemy1List.append(Enemy1_Surf.get_rect(
                    midbottom=(randint(900, 1200), 500)))
                Enemy1List.append(
                    Enemy1_Surf.get_rect(midbottom=(randint(900, 1200), randint(0, 300))))  # Flying Enemy 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    Jump = True
                    JumpRecord = PlayerRect.y
                    JumpRecordTime = pygame.time.get_ticks()
                    Player_GravityX = 0

                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                    Left = True
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                    Right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Left = False
                    if Right == True:
                        playerX_change = 5
                if event.key == pygame.K_RIGHT:
                    Right = False
                    if Left == True:
                        playerX_change = -5

            if not any((Left, Right)):  # if anything tru return false
                playerX_change = 0

        ### Player ###
        PlayerRect.x += playerX_change
        if PlayerRect.x <= 0:
            PlayerRect.x = 0
        if PlayerRect.x >= 750:
            PlayerRect.x = 750

        # Jumping
        if Jump == True:
            Player_GravityX += 1.5
            PlayerRect.y = Gravity(Player_GravityX, JumpRecord)

        if PlayerRect.y <= -50:
            PlayerRect.y = -50

        if GroundRect.colliderect(PlayerRect):
            Jump = False
            Player_GravityX = 0
            PlayerRect.y = 450

        ### Text ###
        pygame.draw.rect(screen, 'pink', TextRect)
        pygame.draw.rect(screen, 'pink', TextRect, 10)
        ScorePrint()

        Enemy1_Movement()  # Enemy1List
        Enemy1_Collisions()

        screen.blit(Player, PlayerRect)

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if pygame.time.get_ticks() - RoundEndTime >= 500:
                    GameActive = True
                    PlayerRect.midbottom = (400, 600)
                    playerX_change = 0
                    StarCollection = 0
                    StartTime = pygame.time.get_ticks()
                    Enemy1List = []
            #event.type == pygame.MOUSEBUTTONDOWN and RestartRect.collidepoint(event.pos)

        pygame.draw.rect(screen, 'pink', RestartRect)
        pygame.draw.rect(screen, 'pink', RestartRect, 10)
        screen.blit(TitleCard, TitleCardRect)
        screen.blit(RestartButton, TextRect)
        screen.blit(Controls, ControlRect)

        screen.blit(ENDscoresurf, ENDscoreRect)

        # screen.blit(, GroundRect)
    pygame.display.update()

    clock.tick(80)  # Can't run faster than 60 times a second
