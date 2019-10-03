from random import choice
import logging
import kivy
import sys
kivy.require('1.11.0')

from os.path import join
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
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
        * bombnum         - Number of bombnum in the board
        * _board        - The board as a 2D list
        Magic Methods:
        __init__        - Sets up the object and generates a randomized board
        __str__         - Prints a string version of the board's values
        __len__         - The number of rows in the board
        __getitem__     - Accesses the list at Board()._board[index]
        __iter__        - Allows iteration over the board using 'for i in Board()'
        __contains__    - States if the board contains the item
    """
    def __init__(self, rows=8, cols=8, bombnum=None, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise ValueError("Rows and cols have to be integers!")
        self.flagged = set()
        self.bombs = set()
        self.rownum = rows
        self.cols = cols
        if not bombnum:
            bombnum = int((rows * cols) ** 0.5)
        self._bombnum = bombnum
        self.board_gen()
        self.__label1 = Label(text='Total bombs: %d' % bombnum, font_size='20sp', color=(1, 0, 0, 1))
        self.add_widget(self.__label1)
        logging.info('New board object initialized')
    
    '''
    def __str__(self):
        out = ''
        for i in self:
            line = '{}\t' * len(i) + '\n'
            i = [x.val for x in i]
            out += line.format(*i)
        return out
    '''

    def __len__(self):
        return len(self._board)
    
    def __getitem__(self, index):
        return self._board[index]
    
    def __iter__(self):
        yield from self._board
    
    def __contains__(self, item):
        for i in self._board:
            if item in i:
                return True
        return False

    def board_gen(self):
        self.__board_init()
        self.__set_mines()
        self.__set_nums()
        logging.info('Board generated.')

    def __board_init(self):
        self._board = [[Cell(self, x, y) for y in range(self.cols)] for x in range(self.rownum)]
        for i in self._board:
            for j in i:
                self.add_widget(j)
        logging.debug('Board initialized.')
    
    def __set_mines(self):
        mines = self.bombnum
        while mines > 0:
            next_bomb = choice(choice(self))
            if next_bomb.val == Cell.BOMB:
                continue
            next_bomb.val = Cell.BOMB
            self.bombs.add(next_bomb)
            mines -= 1
        logging.debug('Mines set.')

    def __set_nums(self):
        for i in range(len(self)):
            for j in range(len(self[i])):
                if self[i][j].val == Cell.BOMB:
                    continue
                self[i][j].val = self.__bomb_counter(self[i][j])
        logging.debug('Cell values set.')
    
    def __bomb_counter(self, cell):
        bombnum = 0
        for neighbour in cell.neighbours():
            if neighbour.val == Cell.BOMB:
                bombnum += 1
        return bombnum
    
    def in_range_x(self, i):
        return 0 <= i < self.rownum

    def in_range_y(self, j):
        return 0 <= j < self.cols
    
    @property
    def bombnum(self):
        return self._bombnum
    
    def open_zeros(self, cell):
        if not isinstance(cell, Cell):
            raise TypeError('cell needs to be a Cell object!')
        if cell.is_open:
            return
        cell.open()
        if cell.val != 0:
            return
        for neighbour in cell.neighbours():
            self.open_zeros(neighbour)
    
    def done(self):
        for i in self:
            for j in i:
                if not j.is_open or not j.is_flag:
                    return False
        return True

    def lose(self):
        popup = Popup(title='Game Over!', content=Label(text='Click outside to end game.'), size_hint=(None, None), size=(400, 400))
        popup.bind(on_dismiss=sys.exit)
        self.disabled = True
        popup.open()
    
    def win(self):
        popup = Popup(title='You Win!', content=Label(text='Click outside to end game.'), size_hint=(None, None), size=(400, 400))
        popup.bind(on_dismiss=sys.exit)
        self.disabled = True
        popup.open()



class Cell(ButtonBehavior, Image):
    """
    class Cell:
        Constants:
        BLANK   - Default value assigned to a cell if no other value is specified, Displayed before cell is  ed
        BOMB    - The value used to represent a bomb
        FLAG    - The displayed value when a flag has been placed on the cell
        Properties:
        val     - The number of bombnum around the cell
        is_open - If the tile has been opened or not
        is_flag - If the user has placed a flag or not
    """

    BLANK = 'blank'
    BOMB = 9
    DEFAULT = -1
    FLAG = 'flag'

    def __init__(self, board, i, j, val=DEFAULT, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(val, int):
            raise ValueError('val needs to be an integer!')
        self.__board = board
        self._val = val
        self._i = i
        self._j = j
        self.source = Cell.img_path(Cell.BLANK)
        self._is_open = False
        self._is_flag = False
        self._board = None
        self.bind(on_release=self.push)
    
    @staticmethod
    def img_path(source):
        return join('images', '{}.png'.format(source))

    '''
    def __str__(self):
        return self.val
    '''

    def push(self, touch):
        if self.last_touch.button == 'left':
            if self.is_flag:
                return
            if self.val == 0:
                self.__board.open_zeros(self)
            elif self.val == Cell.BOMB:
                self.__board.lose()
            else:
                self.open()
        elif self.last_touch.button == 'right':
            self.flag()
    
    def neighbours(self):
        out = []
        for k in range(-1, 2):
            if not self.__board.in_range_x(self.i + k):
                continue
            for l in range(-1, 2):
                if k == l == 0 or not self.__board.in_range_y(self.j + l):
                    continue
                out.append(self.__board[self.i + k][self.j + l])
        return out
    
    @property
    def i(self):
        return self._i
    
    @property
    def j(self):
        return self._j

    @property
    def val(self):
        return self._val
    
    @val.setter
    def val(self, val):
        if not isinstance(val, int):
            raise ValueError('val needs to be an integer!')
        self._val = val
    
    @property
    def is_open(self):
        return self._is_open
    
    def open(self):
        self._is_open = True
        self.source = Cell.img_path(self.val)
        self.funbind('on_release', self.push)
    
    @property
    def is_flag(self):
        return self._is_flag
    
    def flag(self):
        self._is_flag = not self._is_flag
        src = Cell.FLAG if self._is_flag else Cell.BLANK
        self.source = Cell.img_path(src)
        if self._is_flag:
            self.source = Cell.img_path(Cell.FLAG)
            self.__board.flagged.add(self)
            if self.__board.flagged == self.__board.bombs and self.__board.done():
                self.__board.win()
        else:
            self.source = Cell.img_path(Cell.BLANK)
            self.__board.flagged.discard(self)


class MinesweeperApp(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        self.title = 'MinesweeperPy'
        # self.icon = Cell.img_path(Cell.BOMB)
        return Board()


if __name__ == "__main__":
   MinesweeperApp().run()