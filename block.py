import pygame
import time
import board

pygame.init()
red = (255,0,0)

class Block(board.Board):
    def __init__(self, display_rows, display_columns, block_size):
        self.display_rows = display_rows
        self.display_columns = display_columns
        self.display_height = display_columns * block_size
        self.display_width = display_rows * block_size

    def move_down(self, y_coord):
        return y_coord + 1

    def move_left(self, board, selectBox, x_coord, y_coord, box_x_size, box_y_size):
        if x_coord == 0:
            return x_coord
        for i in range(box_y_size):
            if selectBox[i][0] == 'X':
                if board.checkPositionSide(y_coord + i, x_coord-1):
                    return x_coord
        return x_coord -1

    def move_right(self, board, selectBox, x_coord, y_coord, box_x_size, box_y_size):
        if x_coord == self.display_columns - box_x_size :
            return x_coord
        for i in range(box_y_size):
            if selectBox[i][box_x_size-1] == 'X':
                if board.checkPositionSide(y_coord + i, x_coord + box_x_size):
                    return x_coord
        return x_coord + 1

    def rotate(self, oldBox):
        newBox = zip(*oldBox[::-1])
        newBox = [list(a) for a in newBox]
        return newBox
