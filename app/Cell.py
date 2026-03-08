from enum import IntEnum

MINE = -1
FLAG = -2
HIDDEN = -3


class RevealMineException(Exception):
    pass


class CellState(IntEnum):
    VISIBLE = 0
    HIDDEN = 1
    FLAGGED = 2


class Cell:
    value: int
    _state: CellState = CellState.HIDDEN

    def __init__(self):
        self.value = 0

    def is_mine(self):
        return self.value == MINE

    def reveal(self):
        self.is_hidden = False
        if self.is_mine():
            raise RevealMineException()

    def is_visible(self):
        return self._state == CellState.VISIBLE

    def is_hidden(self):
        return (
            self._state == CellState.HIDDEN or
            self._state == CellState.FLAGGED
        )

    def is_flagged(self):
        return self._state == CellState.FLAGGED

    def toggle_flag(self):
        if self.is_visible():
            return
        if self.is_flagged():
            self._state = CellState.HIDDEN
        else:
            self._state = CellState.FLAGGED

    def get_public_value(self):
        if self.is_flagged():
            return FLAG
        if self.is_hidden():
            return HIDDEN
        if self.is_mine():
            return MINE

        return self.value
