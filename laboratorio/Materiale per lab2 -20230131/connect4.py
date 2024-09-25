#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

from boardgame import BoardGame
from boardgamegui import gui_play

class Connect4(BoardGame):
    def __init__(self, w: int, h: int):
        self._w, self._h = w, h
        self._board = [0] * (w * h)
        self._move = None
        self._turn = 1  # 1: MAX plr; -1: MIN plr
        self._winner = 0

    def _get(self, x, y):
        if 0 <= y < self._h and 0 <= x < self._w:
            return self._board[y * self._w + x]  # otherwise, None
        
    def _lined(self, x, y, dx, dy, v):
        if self._get(x, y) != v:
            return 0
        return 1 + self._lined(x + dx, y + dy, dx, dy, v)

    def _around(self, x, y, v):
        '''Max line length of `v`s around `(x, y)`'''
        n = max(self._lined(x + dx, y + dy, dx, dy, v) +
                self._lined(x - dx, y - dy, -dx, -dy, v)
                for dx, dy in [(0, -1), (1, -1), (1, 0), (1, 1)])
        return n + (1 if self._get(x, y) == v else 0)

    def cols(self) -> int:
        return self._w

    def rows(self) -> int:
        return self._h

    def message(self) -> str:
        win = self._winner
        return "O wins" if win == 1 else "X wins" if win == -1 else "Draw"

    def value_at(self, x: int, y: int) -> str:
        v = self._get(x, y)
        p = "O" if v == 1 else "X" if v == -1 else ""
        return f"·{p}·" if self._move == (x, y) else p

    def play_at(self, x: int, y: int):
        y = self._lined(x, 0, 0, 1, 0) - 1
        if y >= 0:
            self._board[y * self._w + x] = self._turn
            self._move = x, y
            if self._around(x, y, self._turn) >= 4:
                self._winner = self._turn
            self._turn *= -1

    def flag_at(self, x: int, y: int):
        return

    def finished(self) -> bool:
        return self._winner or all(self._board)

if __name__ == "__main__":
    gui_play(Connect4(7, 6))
