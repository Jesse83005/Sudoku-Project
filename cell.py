class Cell:
    def __init__(self, value):
        self.value = value
        if self.value == 0:
            self.is_mutable = True
        else:
            self.is_mutable = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

