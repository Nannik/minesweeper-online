from app.Cell import Cell, MINE, RevealMineException
import random


class GameException(Exception):
    pass


class Board:
    _board: list[list[Cell]] = None
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
            [Cell() for j in range(size_x)]
            for i in range(size_y)
        ]

    def _fill_mines(self, count, exclude_x, exclude_y):
        i = 0
        while i < count:
            pos = random.randint(0, (self._size_x * self._size_y) - 1)
            y = int(pos / self._size_x)
            x = pos % self._size_y
            if (
                not self._board[y][x].is_mine() and
                (exclude_x != x and exclude_y != y)
            ):
                i += 1
                self._board[y][x].value = MINE
                self._increment_neighbors(x, y)

    def _get_neighbors_coord(self, x, y):
        px = max(0, min(self._size_x - 1, x - 1))
        nx = max(0, min(self._size_x - 1, x + 1))
        py = max(0, min(self._size_y - 1, y - 1))
        ny = max(0, min(self._size_y - 1, y + 1))

        yield (px, py)
        yield (x, py)
        yield (nx, py)

        yield (px, y)
        yield (nx, y)

        yield (px, ny)
        yield (x, ny)
        yield (nx, ny)

    def _increment_neighbors(self, x, y):
        for (nx, ny) in self._get_neighbors_coord(x, y):
            if (not self._board[ny][nx].is_mine()):
                self._board[ny][nx].value += 1

    def _reveal_mines(self):
        for y in range(self._size_y):
            for x in range(self._size_x):
                if self._board[y][x].is_mine():
                    try:
                        self._board[y][x].reveal()
                    except RevealMineException:
                        pass

    def reveal(self, x, y):
        def reveal_recursivelly(x, y, is_target_cell=False):
            if x < 0 or x >= self._size_x:
                return
            if y < 0 or y >= self._size_y:
                return
            if self._board[y][x].is_flagged():
                return

            was_visible = self._board[y][x].is_visible()
            try:
                self._board[y][x].reveal()
            except RevealMineException:
                self.is_game_over = True
                self._reveal_mines()

            neighbor_flags_count = 0
            for (nx, ny) in self._get_neighbors_coord(x, y):
                if self._board[ny][nx].is_flagged():
                    neighbor_flags_count += 1

            if (
                (
                    was_visible and
                    is_target_cell and
                    neighbor_flags_count == self._board[y][x].value
                ) or
                (
                    not was_visible and
                    self._board[y][x].value == 0
                )
            ):
                for (nx, ny) in self._get_neighbors_coord(x, y):
                    reveal_recursivelly(nx, ny)

        if not self._is_generated:
            self._fill_mines(self._mines_count, x, y)
            self._is_generated = True

        reveal_recursivelly(x, y, True)

    def flag(self, x, y):
        if x < 0 or x >= self._size_x:
            return
        if y < 0 or y >= self._size_y:
            return

        self._board[y][x].toggle_flag()

    def get(self):
        return [
            [
                self._board[y][x].get_public_value()
                for x in range(self._size_x)
            ] for y in range(self._size_y)
        ]
