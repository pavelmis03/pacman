class DrawableObject:

    def __init__(self, game_object):
        self.game_object = game_object

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def process_draw(self):
        pass


class FieldObject(DrawableObject):
    def __init__(self, game_object, ch, x=0, y=0):
        self.super().__init__(game_object)
        # x, y позиция в таблице
        self.index = ch
        self.x, self. y = x, y

    def pos(self):
        return self.game_object.field.get_cell_pos(self.x, self.y)

    def remove_self(self):
        self.game_object.field.cells[self.x][self.y] = ' '
