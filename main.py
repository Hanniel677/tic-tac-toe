import pygame
import math

pygame.init()
screen = pygame.display.set_mode((640, 640))
clk = pygame.time.Clock()
running = True
xImg = pygame.image.load("Assets/X.png")
oImg = pygame.image.load("Assets/O.png")
xImg = pygame.transform.scale(xImg, (100, 100))
oImg = pygame.transform.scale(oImg, (100, 100))
board = [0, 0, 0,
         0, 0, 0,
         0, 0, 0]
positions = {
    0: (50, 50),
    1: (270, 50),
    2: (490, 50),
    3: (50, 270),
    4: (270, 270),
    5: (490, 270),
    6: (50, 490),
    7: (270, 490),
    8: (490, 490)
}

lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
playerTurn = False
gameOver = False
winner = ""
font = pygame.font.SysFont(None, 60)
def checkWin(b, player):
    for ln in lines:
        if b[ln[0]] == player and b[ln[1]] == player and b[ln[2]] == player:
            return True
    return False

def minimax(b, isAI):
    if checkWin(b, 2):
        return 10
    if checkWin(b, 1):
        return -10
    if 0 not in b:
        return 0

    if isAI:
        best = -math.inf
        for i in range(9):
            if b[i] == 0:
                b[i] = 2
                score = minimax(b, False)
                b[i] = 0
                if score > best:
                    best = score
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == 0:
                b[i] = 1
                score = minimax(b, True)
                b[i] = 0
                if score < best:
                    best = score
        return best
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and playerTurn and not gameOver:
            mx, my = pygame.mouse.get_pos()

            col = 0
            if mx > 220 and mx < 440:
                col = 1
            elif mx > 440:
                col = 2
            row = 0
            if my > 220 and my < 440:
                row = 1
            elif my > 440:
                row = 2

            cell = row * 3 + col

            if board[cell] == 0:
                board[cell] = 1
                playerTurn = False

    if not playerTurn and not gameOver:
        bestScore = -math.inf
        bestMove = -1

        for i in range(9):
            if board[i] == 0:
                board[i] = 2
                score = minimax(board, False)
                board[i] = 0
                if score > bestScore:
                    bestScore = score
                    bestMove = i

        if bestMove != -1:
            board[bestMove] = 2

        playerTurn = True

    if checkWin(board, 2):
        gameOver = True
        winner = "AI Wins!"
    if 0 not in board and not gameOver:
        gameOver = True
        winner = "Draw!"
    screen.fill("white")
    pygame.draw.rect(screen, (0, 0, 0), (200, 0, 20, 640))
    pygame.draw.rect(screen, (0, 0, 0), (420, 0, 20, 640))
    pygame.draw.rect(screen, (0, 0, 0), (0, 200, 640, 20))
    pygame.draw.rect(screen, (0, 0, 0), (0, 420, 640, 20))

    for i in range(9):
        if board[i] == 1:
            screen.blit(xImg, positions[i])
        elif board[i] == 2:
            screen.blit(oImg, positions[i])
    if gameOver:
        txt = font.render(winner, True, (255, 0, 0))
        screen.blit(txt, (200, 300))

    pygame.display.flip()
    clk.tick(60)

pygame.quit()