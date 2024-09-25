#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

from boardgame import BoardGame, console_play
from boardgamegui import gui_play
from random import shuffle
from copy import deepcopy

delta = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

class Othello(BoardGame):
    def __init__(self, w: int, h: int):
        self._w, self._h = w, h
        self._board = b = [0] * (w * h)
        center = (h // 2) * w + (w // 2)
        b[center] =  b[center - w - 1] = 1
        b[center - 1] = b[center - w] = -1
        self._move = None
        self._turn = 1  # 1: MAX plr; -1: MIN plr

    def _get(self, x, y) -> int:
        if 0 <= x < self._w and 0 <= y < self._h:
            return self._board[y * self._w + x]  # otherwise, None
    
    def _flip(self, x, y, plr):
        for dx, dy in delta:
            for i in range(1, 1 + self._count(x, y, dx, dy, plr)):
                self._board[(y + i * dy) * self._w + (x + i * dx)] = plr

    def _count(self, x, y, dx, dy, plr) -> int:
        x, y, count = x + dx, y + dy, 0
        while v := self._get(x, y):
            if v == plr:
                return count
            x, y, count = x + dx, y + dy, count + 1
        return 0

    def _legit(self, x, y, plr) -> bool:
        return self._get(x, y) == 0 and any(self._count(x, y, dx, dy, plr) for dx, dy in delta)

    def _find_moves(self, plr) -> list:
        return [(x, y) for y in range(self._h) for x in range(self._w) if self._legit(x, y, plr)]

    def cols(self) -> int:
        return self._w

    def rows(self) -> int:
        return self._h

    def message(self) -> str:
        countO, countX = self._board.count(1), self._board.count(-1)
        if countO > countX:
            return f"The winner is O \n {countO} vs {countX}"
        if countX > countO:
            return f"The winner is X \n {countX} vs {countO}"
        return f"No winner \n {countO} vs {countX}"

    def value_at(self, x: int, y: int) -> str:
        val = self._get(x, y)
        txt = "O" if val == 1 else "X" if val == -1 else ""
        return f"·{txt}·" if self._move and self._move == (x, y) else txt

    def play_at(self, x: int, y: int):
        b, w, h = self._board, self._w, self._h
        if self._get(x, y) == 0 and self._legit(x, y, self._turn):
            b[y * w + x] = self._turn
            self._flip(x, y, self._turn)
            self._move = x, y
            self._turn *= -1
            if not self._find_moves(self._turn):
                self._turn *= -1

    def flag_at(self, x: int, y: int):
        return

    def finished(self) -> bool:
        return not self._find_moves(1) and not self._find_moves(-1)

if __name__ == "__main__":
    gui_play(Othello(8, 8))
