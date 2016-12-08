import pygame
from random import randint
pygame.init()
font = pygame.font.SysFont(None, 50)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
random = (122,122,122)
random1 = (25,122,180)

class Board:
    def __init__(self, display_rows, display_columns, block_size):
        self.blockPresent = [[0 for i in range(display_columns)] for j in range(display_rows)]
        self.display_rows = display_rows
        self.display_columns = display_columns
        self.display_width = self.display_rows*block_size
        self.display_height = self.display_columns*block_size
        self.block_size = block_size
        self.gameDisplay = pygame.display.set_mode((self.display_height, self.display_width))

    def checkPositionBelow(self, selectBox, x_coord, y_coord, box_x_size, box_y_size):
        for j in range(box_y_size):
            for i in range(box_x_size):
                if selectBox[j][i] == 'X':
                    if (y_coord + box_y_size)==self.display_rows:
                        return True
                    elif self.blockPresent[y_coord + j + 1][x_coord + i] == 1:
                        return True
        return False

    def checkPositionSide(self, y, x):
        if self.blockPresent[y][x] == 1:
            return True
        else:
            return False

    def checkIfCanRotate(self, oldBox, x_coord, y_coord, box_x_size, box_y_size):
        newBox = zip(*oldBox[::-1])
        newBox = [list(a) for a in newBox]
        box_x_size, box_y_size = box_y_size, box_x_size
        if x_coord + box_x_size -1 >= self.display_columns:
            return False
        if y_coord + box_y_size -1 >= self.display_rows:
            return False
        for i in range(box_y_size):
            for j in range(box_x_size):
                if newBox[i][j] == 'X':
                    if self.blockPresent[y_coord + i][x_coord + j] == 1:
                        return False
        return True

    def checkCoincide(self,selectBox, x_coord, y_coord , box_x_size, box_y_size):
        for i in range(box_y_size):
            for j in range(box_x_size):
                if selectBox[i][j] == 'X':
                    if self.blockPresent[y_coord + i][x_coord + j] == 1:
                        return True
        return False

    def randomBlocks(self,level):
        for i in range(level*2):
            x = randint(0,29)
            y = randint(16,25)
            self.blockPresent[y][x] = 1

    def pushRandomRow(self):
        newRow = []
        for i in range(self.display_columns):
            if i%2 == 0:
                randomNumber = randint(i,i+1)
                for j in range(i,i+2):
                    if j==randomNumber:
                        newRow.append(1)
                    else:
                        newRow.append(0)
        for i in range(self.display_rows - 1):
            self.blockPresent[i] = self.blockPresent[i+1]
        self.blockPresent[self.display_rows-1] = newRow


    def draw(self, selectBox, x_coord, y_coord, box_x_size, box_y_size, score, level):
        # self.gameDisplay.fill((255,255,255))
        bg = pygame.image.load('background.jpg')
        self.gameDisplay.blit(bg, (0,0))
        pygame.display.set_caption('Tetris')
        msg = "Score: " + str(score)
        levelScore = "Level: " + str(level)
        self.message_to_screen(msg, blue, 0, 0)
        self.message_to_screen(levelScore, blue, (7*self.display_width)/10, 0)
        for i in range(self.display_rows):
            for j in range(self.display_columns):
                if self.blockPresent[i][j] == 1:
                    img = pygame.image.load('green.png')
                    self.gameDisplay.blit(img, (self.block_size*j, self.block_size*i))
                    #pygame.draw.rect(self.gameDisplay, (255,0,0), [self.block_size*j,self.block_size*i,self.block_size, self.block_size])
        for i in range(box_y_size):
            for j in range(box_x_size):
                if selectBox[i][j] == 'X':
                    img = pygame.image.load('purple.png')
                    self.gameDisplay.blit(img, (self.block_size*(j + x_coord), self.block_size*(i + y_coord)))
                    # pygame.draw.rect(self.gameDisplay, (0,0,0), [self.block_size*(j+x_coord), self.block_size*(i + y_coord), self.block_size, self.block_size])
        pygame.display.update()

    def drawStart(self):
        bg = pygame.image.load('background.jpg')
        self.gameDisplay.blit(bg, (0,0))
        pygame.display.set_caption('Tetris')
        instructions = "Press i for instructions"
        start = "Press Space to start the game"
        mainMenu = "Press Esc to come to main menu"
        restart = "Press r to restart anytime"
        pause = "Press p to pause anytime"
        self.message_to_screen(instructions, green, self.display_width/13, (3*self.display_height)/9)
        self.message_to_screen(start, red, self.display_width/13, (4*self.display_height)/9)
        self.message_to_screen(mainMenu, blue, self.display_width/13, (5*self.display_height)/9)
        self.message_to_screen(restart, black, self.display_width/13, (6*self.display_height)/9)
        self.message_to_screen(pause, random1, self.display_width/13, (7*self.display_height)/9)
        pygame.display.update()

    def drawGameOver(self, score, level):
        score = score - 10
        bg = pygame.image.load('background.jpg')
        self.gameDisplay.blit(bg, (0,0))
        pygame.display.set_caption('Tetris')
        gameOver = "Game Over"
        yourScore = "Your Score: " + str(score)
        levelReached = "Level Reached: " + str(level)
        restart = "Press r to restart game"
        mainMenu = "Press Esc to go to main menu"
        self.message_to_screen(gameOver, green, self.display_width/8, (3*self.display_height)/10)
        self.message_to_screen(yourScore, red, self.display_width/8, (4*self.display_height)/10)
        self.message_to_screen(levelReached, random, self.display_width/8, (5*self.display_height)/10)
        self.message_to_screen(mainMenu, blue, self.display_width/8, (6*self.display_height)/10)
        self.message_to_screen(restart, black, self.display_width/8, (7*self.display_height)/10)
        pygame.display.update()

    def showInstructions(self):
        goBack = False
        bg = pygame.image.load('background.jpg')
        self.gameDisplay.blit(bg, (0,0))
        pygame.display.set_caption('Tetris')
        left = "Press a to go left"
        right = "Press d to go right"
        rotate = "Press s to rotate"
        goBackText = "Press b to go back"
        self.message_to_screen(left, black, self.display_width/5, (2*self.display_height)/9)
        self.message_to_screen(right, black, self.display_width/5, (3*self.display_height)/9)
        self.message_to_screen(rotate, black, self.display_width/5, (4*self.display_height)/9)
        self.message_to_screen(goBackText, black, self.display_width/5, (8*self.display_height)/9)
        pygame.display.update()
        while not goBack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    goBack = True


    def update_table(self,selectBox, x_coord, y_coord, box_x_size, box_y_size):
        for i in range(box_y_size):
            for j in range(box_x_size):
                if selectBox[i][j]=='X':
                    self.blockPresent[y_coord + i][x_coord + j] = 1

    def clearRows(self):
        row = self.display_rows - 1
        counter = 0
        while row > 0:
            countof1 = 0
            for i in range(self.display_columns):
                if self.blockPresent[row][i] == 1:
                    countof1 += 1
            if countof1 == self.display_columns:
                counter+=1
                for x in range(row, 0, -1):
                    self.blockPresent[x] = self.blockPresent[x-1]
            else:
                row -= 1
        return counter

    def cleanSingleRow(self, row):
        for x in range(row, 0, -1):
            self.blockPresent[x] = self.blockPresent[x-1]

    def message_to_screen(self, msg, color, x, y):
        screen_text = font.render(msg, True, color)
        self.gameDisplay.blit(screen_text, [x, y])
