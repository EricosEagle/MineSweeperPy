from random import choice
import logging
import kivy
kivy.require('1.11.0')

from os.path import join
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.app import App

logging.basicConfig(filename='log.txt',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class Board(GridLayout):
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
    def __init__(self, rows=8, cols=8, bombs=None, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise ValueError("Rows and cols have to be integers!")
        self._rows = rows
        self.cols = cols
        if not bombs:
            bombs = int((rows * cols) ** 0.5)
        self._bombs = bombs
        self.__board_gen()
        self.__label1 = Label(text='Total bombs: %d' % bombs, font_size='20sp', color=(1, 0, 0, 1))
        self.add_widget(self.__label1)
        logging.info('New board object initialized')
    
    '''
    def __str__(self):
        out = ''
        line = '{}\t' * self.cols + '\n'
        for i in self:
            i = [str(x) for x in i]
            out += line.format(*i)
        return out
    '''

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
        self._board = [[Cell() for _ in range(self.cols)] for _ in range(self._rows)]
        for i in self._board:
            for j in i:
                self.add_widget(j)
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
                if self[i][j].val != Cell.BLANK:
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
        return 0 < i < self._rows

    def in_range_y(self, j):
        return 0 < j < self.cols
    
    @property
    def bombs(self):
        return self._bombs


class Cell(ButtonBehavior, Image):
    """
    class Cell:
        Constants:
        BLANK   - Default value assigned to a cell if no other value is specified, Displayed before cell is opened
        BOMB    - The value used to represent a bomb
        FLAG    - The displayed value when a flag has been placed on the cell
        Properties:
        val     - The number of bombs around the cell
        is_open - If the tile has been opened or not
        is_flag - If the user has placed a flag or not
    """

    BLANK = 'blank'
    BOMB = 9
    FLAG = 'flag'

    def __init__(self, val=-1, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(val, int):
            raise ValueError('val needs to be an integer!')
        self._val = str(val)
        self.source = Cell.get_source(Cell.BLANK)
        self._is_open = False
        self._is_flag = False
        self.bind(on_release=self.push)
    
    @staticmethod
    def get_source(source):
        if isinstance(source, int):
            return join('images', '%d.jpg' % source)
        return join('images', '%s.jpg' % source)

    '''
    def __str__(self):
        return self.val
    '''

    def push(self, touch):
        if self.last_touch.button == 'left':
            if self.is_flag:
                return
            self.open()
        else:
            self.flag()
    
    @property
    def val(self):
        return self._val
    
    @val.setter
    def val(self, val):
        if not isinstance(val, (int, str)):
            raise ValueError('val needs to be an integer!')
        self._val = str(val)
    
    @property
    def is_open(self):
        return self._is_open
    
    def open(self):
        self._is_open = True
        self._display = self.val
        self.bind(on_release=lambda *args: None)
    
    @property
    def is_flag(self):
        return self._is_flag
    
    def flag(self):
        self._flag = not self._is_flag
        self.text = Cell.FLAG if self._flag else Cell.BLANK


class MinesweeperApp(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        self.title = 'MinesweeperPy'
        return Board()

if __name__ == "__main__":
    # Testing
   MinesweeperApp().run()