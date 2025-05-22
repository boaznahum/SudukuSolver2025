class Cell:
    value: int | None
    notes: list[int | None]

    def __init__(self, value: int | None = None):
        self.value = value
        self.notes = [None] * 10