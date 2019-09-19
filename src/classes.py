from random import choice
import logging

logging.basicConfig(filename='log.txt',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class Board:
    """
    class Board:
        Variables:
        * rows          - Number of rows in the board
        * cols          - Number of columns in the board
        * bombs         - Number of bombs in the board
        * _board        - The board as a 2D list
        Magic Methods:
        __init__        - Sets up the object and generates a randomized board
        __str__         - Prints a string version of the board's values
        __len__         - The number of rows in the board
        __getitem__     - Accesses the list at Board()._board[index]
        __iter__        - Allows iteration over the board using 'for i in Board()'
        __contains__    - States if the board contains the item
    """
    def __init__(self, rows=8, cols=8, bombs=None):
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise ValueError("Rows and cols have to be integers!")
        self._rows = rows
        self._cols = cols
        if not bombs:
            bombs = int((rows * cols) ** 0.5)
        self._bombs = bombs
        self.__board_gen()
        logging.info('New board object initialized')
    
    def __str__(self):
        out = ''
        line = '{}\t' * self.cols + '\n'
        for i in self:
            i = [str(x) for x in i]
            out += line.format(*i)
        return out

    def __len__(self):
        return len(self._board)
    
    def __getitem__(self, index):
        return self._board[index]
    
    def __iter__(self):
        return iter(self._board)
    
    def __contains__(self, item):
        for i in self._board:
            if item in i:
                return True
        return False

    def __board_gen(self):
        self.__board_init()
        self.__set_mines()
        self.__set_nums()
        logging.info('Board generated.')

    def __board_init(self):
        self._board = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        logging.debug('Board initialized.')
    
    def __set_mines(self):
        mines = self.bombs
        while mines > 0:
            next_bomb = choice(choice(self._board))
            if next_bomb.val == Cell.BOMB:
                continue
            next_bomb.val = Cell.BOMB
            mines -= 1
        logging.debug('Mines set.')

    def __set_nums(self):
        for i in range(len(self)):
            for j in range(len(self[i])):
                if self[i][j].val != Cell.DEFAULT:
                    continue
                self[i][j].val = self.__bomb_counter(i, j)
        logging.debug('Cell values set.')
    
    def __bomb_counter(self, i, j):
        bombs = 0
        for k in range(-1, 2):
            if not self.in_range_x(i + k):
                continue
            for l in range(-1, 2):
                if i == 0 and j == 0 or not self.in_range_y(j + l):
                    continue
                if self[i + k][j + l].val == Cell.BOMB:
                    bombs += 1
        return bombs
    
    def in_range_x(self, i):
        return 0 < i < self.rows

    def in_range_y(self, j):
        return 0 < j < self.cols

    @property
    def rows(self):
        return self._rows
    
    @property
    def cols(self):
        return self._cols
    
    @property
    def bombs(self):
        return self._bombs


class Cell:
    """
    class Cell:
        Constants:
        DEFAULT - Default value assigned to a cell if no other value is specified
        BOMB    - The value used to represent a bomb
        Properties:
        val     - The number of bombs around the cell
        is_open - If the tile has been opened or not
    """

    DEFAULT = -1
    BOMB = 9

    def __init__(self, val=DEFAULT):
        if not isinstance(val, int):
            raise ValueError('val needs to be an integer!')
        self._val = val
        self._is_open = False
    
    def __str__(self):
        return str(self._val)
    
    @property
    def val(self):
        return self._val
    
    @val.setter
    def val(self, val):
        self._val = val
    
    @property
    def is_open(self):
        return self._is_open
    
    def open(self):
        self._is_open = True


if __name__ == "__main__":
    # Testing
    board = Board()
    print(board)