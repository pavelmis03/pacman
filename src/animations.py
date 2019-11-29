class Anim:
    def __init__(self, sprite_list, frame_ms=1):
        self.sprites = sprite_list
        self.frame_ms = frame_ms
        self.curr_sprite_num = 0
        self.curr_sprite = self.sprites[0]
        self.ticks = 0

    def add_tick(self):
        self.ticks += 1
        if self.ticks % self.frame_ms == 0:
            self.curr_sprite_num = (self.curr_sprite_num + 1) % len(self.sprites)
        self.curr_sprite = self.sprites[self.curr_sprite_num]