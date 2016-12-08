import block
import board
import pygame
import random
import time

restartVar = True

class Gameplay(block.Block, board.Board):
    def __init__(self,display_rows,display_columns, block_size):
        self.score = 0
        self.display_rows = display_rows
        self.display_columns = display_columns
        self.block_size = block_size
        self.block = None
        self.board = None
        self.gameStart = True
        self.level = 1
        self.scoreToClearLevel = 0
        self.levelUp = False

    def gameLoop(self):
        self.scoreToClearLevel = 200*(2**(self.level-1))
        if self.levelUp == False:
            self.block = block.Block(self.display_rows, self.display_columns, self.block_size)
            self.board = board.Board(self.display_rows,self.display_columns, self.block_size)
            self.levelUp = False
        while self.gameStart == True :
            self.score = 0
            self.gameStartPrint()
        numberOfBlocksFell = 1
        clock = pygame.time.Clock()
        boxFalling = True
        gameExit = False
        restartVar = False
        gameOver = False
        if self.level >= 3:
            self.board.randomBlocks(self.level)
        while not gameExit:
            while gameOver:
                self.gameOverPrint()
            self.levelUp = False
            moveLeft = False
            moveRight = False
            randomNumber = random.randint(1,25)
            if randomNumber == 25:
                selectBox = ['X']
            else:
                selectBox = self.selectPiece(randomNumber%6)
            box_x_size = len(selectBox[0])
            box_y_size = len(selectBox)
            x_coord = self.display_columns/2 - box_y_size/2
            if randomNumber == 0:
                x_coord+=1
            y_coord = 0
            checkGameOver = self.board.checkCoincide(selectBox, x_coord, y_coord, box_x_size, box_y_size)
            if checkGameOver:
                gameOver = True
            boxFalling = True
            if self.level >=2:
                if numberOfBlocksFell % 15 ==0:
                    self.board.pushRandomRow()
            self.board.draw(selectBox,x_coord,y_coord,box_x_size, box_y_size, self.score, self.level)
            FPS = 10 + 2*(self.level - 1)
            flag = 0
            gamePause = False
            while boxFalling:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            if flag == 0:
                                moveLeft = True
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            if flag == 0:
                                moveRight = True
                        elif event.key == pygame.K_s:
                            if self.board.checkIfCanRotate(selectBox, x_coord, y_coord, box_x_size, box_y_size):
                                selectBox = self.block.rotate(selectBox)
                                box_x_size,box_y_size = box_y_size, box_x_size
                        elif event.key == pygame.K_p:
                            gamePause = True
                        elif event.key == pygame.K_r:
                            self.score = 0
                            self.level = 1
                            self.gameLoop()
                        elif event.key == pygame.K_ESCAPE:
                            self.gameStart = True
                            self.gameLoop()
                        elif event.key == pygame.K_SPACE:
                            flag = 1
                            FPS = 500
                            moveLeft = False
                            moveRight = False
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            moveLeft = False
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            moveRight = False
                while gamePause == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            gamePause = False
                toStop = self.board.checkPositionBelow(selectBox, x_coord, y_coord, box_x_size, box_y_size)
                if toStop:
                    numberOfBlocksFell += 1
                    self.updateScore(1,0,0)
                    self.board.update_table(selectBox, x_coord, y_coord, box_x_size, box_y_size)
                    if selectBox == ['X']:
                        self.board.cleanSingleRow(y_coord)
                    break
                else:
                    y_coord = self.block.move_down(y_coord)
                    if moveLeft:
                        x_coord = self.block.move_left(self.board, selectBox, x_coord, y_coord, box_x_size, box_y_size)
                    if moveRight:
                        x_coord = self.block.move_right(self.board, selectBox, x_coord, y_coord, box_x_size, box_y_size)
                countOfFullRows = self.board.clearRows()
                self.updateScore(0,1,countOfFullRows)
                if self.score >= self.scoreToClearLevel:
                    self.levelUp = True
                    self.level += 1
                    self.gameStart = False
                    self.gameLoop()
                self.board.draw(selectBox, x_coord, y_coord, box_x_size, box_y_size, self.score, self.level)
                clock.tick(FPS)

    def updateScore(self, blockDrop, cleanRow, countOfFullRows):
        if blockDrop == 1:
            self.score += 10
        elif cleanRow == 1:
            self.score += 100*countOfFullRows

    def gameOverPrint(self):
        self.board.drawGameOver(self.score, self.level)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.level = 1
                    self.score = 0
                    self.gameStart = False
                    self.gameLoop()
                elif event.key == pygame.K_ESCAPE:
                    self.gameStart = True
                    self.gameLoop()

    def gameStartPrint(self):
        self.level = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.gameStart = False
                    self.gameLoop()
                elif event.key == pygame.K_i:
                    self.board.showInstructions()
            self.board.drawStart()

    def selectPiece(self, index):
        if index == 0:
            return [['X','X','X','X']]
        elif index == 1:
            return [['X', 'X'], ['X', 'X']]
        elif index == 2:
            return [[' ', 'X', ' '],['X', 'X', 'X']]
        elif index == 3:
            return [['X', 'X', ' '],[' ', 'X', 'X']]
        elif index == 4:
            return [[' ','X','X'],['X','X',' ']]
        elif index == 5:
            return [['X','X','X'],[' ',' ','X']]
