#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

from connect4 import Connect4, gui_play
from copy import deepcopy
from math import inf
from random import sample, shuffle

class Connect4AI(Connect4):
    def _value(self):
        if self._winner:
            return self._winner * (1000 + self._board.count(0))
        count = 0
        for y in range(self._h):
            for x in range(self._w):
                for v in (1, -1):
                    if self._get(x, y) == 0 and self._around(x, y, v) >= 3:
                        count += v * (10 + y)
                    if x == self._w // 2 and self._get(x, y) == v:
                        count += v
        return count

    def _negamax(self, depth, alpha=-inf, beta=+inf):
        if depth == 0 or self.finished():
            return self._turn * self._value(), self._move
        value, move = -inf, None
        for x in sample(range(self._w), self._w):
            if self._get(x, 0) == 0:
                child = deepcopy(self)
                child.play_at(x, 0)
                v, m = child._negamax(depth - 1, -beta, -alpha)
                v *= -1
                if v > value:
                    value, move = v, (x, 0)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break # α-β cutoff
        return value, move

    def flag_at(self, x: int, y: int):
        v, move = self._negamax(6)
        print(v, move)
        self.play_at(*move)

if __name__ == "__main__":
    gui_play(Connect4AI(7, 6))
