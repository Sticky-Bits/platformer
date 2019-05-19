import pygame as pg

from blocks import Block, MovingBlock
from player import Player


class App:
    """Class for managing event loop and game states."""
    def __init__(self):
        """Initalize the display and prepare game objects."""
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.player = Player((50, 875), 4)
        self.viewport = self.screen.get_rect()
        self.level = pg.Surface((1000, 1000)).convert()
        self.level_rect = self.level.get_rect()
        self.win_text, self.win_rect = self.make_text()
        self.obstacles = self.make_obstacles()
        self.key_mapping = {
            pg.K_1: (self.player.switch_weapon, 1),
            pg.K_2: (self.player.switch_weapon, 2),
            pg.K_3: (self.player.switch_weapon, 3),
            pg.K_4: (self.player.switch_weapon, 4),
            pg.K_5: (self.player.switch_weapon, 5),
            pg.K_SPACE: (self.player.jump, self.obstacles),
        }

    def make_text(self):
        """Renders a text object. Text is only rendered once."""
        font = pg.font.Font(None, 100)
        message = "You win. Celebrate."
        text = font.render(message, True, (100, 100, 175))
        rect = text.get_rect(centerx=self.level_rect.centerx, y=100)
        return text, rect

    def make_obstacles(self):
        """Adds some arbitrarily placed obstacles to a sprite.Group."""
        walls = [Block(pg.Color("chocolate"), (0, 980, 1000, 20)),
                 Block(pg.Color("chocolate"), (0, 0, 20, 1000)),
                 Block(pg.Color("chocolate"), (980, 0, 20, 1000))]
        static = [Block(pg.Color("darkgreen"), (250, 780, 200, 100)),
                  Block(pg.Color("darkgreen"), (600, 880, 200, 100)),
                  Block(pg.Color("darkgreen"), (20, 360, 880, 40)),
                  Block(pg.Color("darkgreen"), (950, 400, 30, 20)),
                  Block(pg.Color("darkgreen"), (20, 630, 50, 20)),
                  Block(pg.Color("darkgreen"), (80, 530, 50, 20)),
                  Block(pg.Color("darkgreen"), (130, 470, 200, 215)),
                  Block(pg.Color("darkgreen"), (20, 760, 30, 20)),
                  Block(pg.Color("darkgreen"), (400, 740, 30, 40))]
        moving = [MovingBlock(pg.Color("olivedrab"), (20, 740, 75, 20), 325, 0),
                  MovingBlock(pg.Color("olivedrab"), (600, 500, 100, 20), 880, 0),
                  MovingBlock(pg.Color("olivedrab"),
                              (420, 430, 100, 20), 550, 1, speed=3, delay=200),
                  MovingBlock(pg.Color("olivedrab"),
                              (450, 700, 50, 20), 930, 1, start=930),
                  MovingBlock(pg.Color("olivedrab"),
                              (500, 700, 50, 20), 730, 0, start=730),
                  MovingBlock(pg.Color("olivedrab"),
                              (780, 700, 50, 20), 895, 0, speed=-1)]
        return pg.sprite.Group(walls, static, moving)

    def update_viewport(self):
        """
        The viewport will stay centered on the player unless the player
        approaches the edge of the map.
        """
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key in self.key_mapping.keys():
                    func = self.key_mapping[event.key]
                    func[0](func[1])
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
        self.player.shooting = bool(pg.mouse.get_pressed()[0])

    def update(self):
        """Update the player, obstacles, and current viewport."""
        self.keys = pg.key.get_pressed()
        self.player.pre_update(self.obstacles)
        self.obstacles.update(self.player, self.obstacles)
        self.player.update(self.obstacles, self.keys)
        self.update_viewport()

    def draw(self):
        """
        Draw all necessary objects to the level surface, and then draw
        the viewport section of the level to the display surface.
        """
        self.level.fill(pg.Color("lightblue"))
        self.obstacles.draw(self.level)
        self.level.blit(self.win_text, self.win_rect)
        self.player.draw(self.level)
        self.screen.blit(self.level, (0, 0), self.viewport)

    def main_loop(self):
        """As simple as it gets."""
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)
