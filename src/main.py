import kivy
kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from classes import Board, Cell

board = Board()

class GameLayout(GridLayout):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)
        self.cols = board.cols
        self.rows = board.rows
        pass


class MineSweeperApp(App):
    def build(self):
        self.title = 'MineSweeperPy'
        return GameLayout()


if __name__ == "__main__":
    MineSweeperApp().run()