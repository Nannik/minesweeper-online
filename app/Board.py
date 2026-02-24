from enum import IntEnum
import random


class GameException(Exception):
    pass


class BoardMask(IntEnum):
    HIDDEN = 0
    VISIBLE = 1
    FLAG = 2


class PublicBoardSpecialCell(IntEnum):
    MINE = -1
    HIDDEN = -2
    FLAG = -3


class Board:
    _board = None
    _board_mask = None
    _size_x = None
    _size_y = None
    _mines_count = None
    _is_generated = False
    is_game_over = False

    def __init__(self, size_x, size_y, mines_count):
        self._size_x = size_x
        self._size_y = size_y
        self._mines_count = mines_count

        if (mines_count >= size_x * size_y):
            raise GameException('too many mines')

        self._board = [
            [0 for j in range(size_x)]
            for i in range(size_y)
        ]
        self._board_mask = [
            [BoardMask.HIDDEN for j in range(size_x)]
            for i in range(size_y)
        ]

    def _fill_mines(self, count, exclude_x, exclude_y):
        i = 0
        while i < count:
            pos = random.randint(0, (self._size_x * self._size_y) - 1)
            y = int(pos / self._size_x)
            x = pos % self._size_y
            if (
                self._board[y][x] != PublicBoardSpecialCell.MINE and
                (exclude_x != x and exclude_y != y)
            ):
                i += 1
                self._board[y][x] = PublicBoardSpecialCell.MINE
                self._increment_neighbors(x, y)

    def _increment_neighbors(self, cell_x, cell_y):
        for y in range(max(0, cell_y - 1), min(self._size_y, cell_y + 2)):
            for x in range(max(0, cell_x - 1), min(self._size_x, cell_x + 2)):
                if (self._board[y][x] != PublicBoardSpecialCell.MINE):
                    self._board[y][x] += 1

    def _reveal_mines(self):
        for y in range(self._size_y):
            for x in range(self._size_x):
                if self._board[y][x] == PublicBoardSpecialCell.MINE:
                    self._board_mask[y][x] = BoardMask.VISIBLE

    def reveal(self, x, y):
        def reveal_recursivelly(x, y, ignore_value=False):
            if x < 0 or x >= self._size_x:
                return
            if y < 0 or y >= self._size_y:
                return
            if (self._board_mask[y][x] == BoardMask.FLAG):
                return
            if (
                (self._board_mask[y][x] == BoardMask.VISIBLE) and
                (not ignore_value)
            ):
                return

            self._board_mask[y][x] = BoardMask.VISIBLE

            if self._board[y][x] == PublicBoardSpecialCell.MINE:
                self.is_game_over = True
                self._reveal_mines()

            if self._board[y][x] == 0 or ignore_value:
                reveal_recursivelly(x - 1, y - 1)
                reveal_recursivelly(x, y - 1)
                reveal_recursivelly(x + 1, y - 1)

                reveal_recursivelly(x - 1, y)
                reveal_recursivelly(x + 1, y)

                reveal_recursivelly(x - 1, y + 1)
                reveal_recursivelly(x, y + 1)
                reveal_recursivelly(x + 1, y + 1)

        if not self._is_generated:
            self._fill_mines(self._mines_count, x, y)
            self._is_generated = True

        if self._board_mask[y][x] == BoardMask.HIDDEN:
            reveal_recursivelly(x, y)
        elif self._board_mask[y][x] == BoardMask.VISIBLE:
            reveal_recursivelly(x, y, True)

    def flag(self, x, y):
        if x < 0 or x >= self._size_x:
            return
        if y < 0 or y >= self._size_y:
            return

        if self._board_mask[y][x] == BoardMask.VISIBLE:
            return

        if self._board_mask[y][x] == BoardMask.HIDDEN:
            self._board_mask[y][x] = BoardMask.FLAG
        else:
            self._board_mask[y][x] = BoardMask.HIDDEN

    def get(self):
        def map(x, y):
            if self._board_mask[y][x] == BoardMask.HIDDEN:
                return PublicBoardSpecialCell.HIDDEN
            if self._board_mask[y][x] == BoardMask.FLAG:
                return PublicBoardSpecialCell.FLAG
            if self._board_mask[y][x] == BoardMask.VISIBLE:
                return self._board[y][x]
        return [
            [
                map(x, y)
                for x in range(self._size_x)
            ] for y in range(self._size_y)
        ]

    def _get_neighbours(self, x, y):
        yield self._board[y][x]
