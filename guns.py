import pygame as pg


class MachineGun:
    def __init__(self):
        self.firerate = 5
        self.cooldown = 0
        self.bullet = MachineGunBullet
        self.bullets = []

    def shoot(self, direction, position):
        """ Actually fire the gun"""
        self.cooldown = self.firerate
        # gun probably shouldn't keep track of it's own bullets. probably a world thing.
        self.bullets.append(self.bullet(direction, position))
        print("BANG!")

    def update(self):
        for bullet in self.bullets:
            bullet.update()

    def draw(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)


class MachineGunBullet:
    velocity = 10

    def __init__(self, direction, position):
        self.direction = direction
        self.position = position
        self.image = pg.Surface((5, 5)).convert()
        self.image.fill(pg.Color("red"))
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self):
        # Make this work properly with direction. Trigonometry and shit.
        self.rect[0] += self.velocity

    def draw(self, surface):
        surface.blit(self.image, self.rect)
