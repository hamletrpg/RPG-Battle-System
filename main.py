import pygame
import os
import random
import time
pygame.font.init()

WIDTH, HEIGTH = 500, 700
WINDOWS = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("RPG Battle System")

default = []
archer_idle = []
archer_attack = []
orc_idle = []
orc_attack = []

BG = pygame.transform.scale(pygame.image.load(os.path.join("background.jpg")), (WIDTH, HEIGTH))

def load_image(dirr=None, name="None"):
    if dirr == None:
        image = pygame.image.load(name)
        return image
    else:
        image = pygame.image.load(dirr + "/" + name)
        return image

def filled_up(dirr, var):
    character_quantity = [name for name in os.listdir(dirr)]
    for name in character_quantity:
        var.append(name)

class Label:
    def __init__(self, x, y, text=''):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, window):
        window.blit(self.text, (self.x, self.y))

    def __repr__(self):
        return self.text

class Pointer:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.image = load_image(None, 'arrow.png')

    def flipping(self):
        arrow_copy = self.image.copy()
        arrow_copy = pygame.transform.flip(arrow_copy, True, False)
        self.image = arrow_copy

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class Character:
    def __init__(self, x, y, name, atk, deffense, hp, mana, speed):
        self.x = x
        self.y = y
        self.name = name
        self.atk = atk
        self.deffense = deffense
        self.hp = hp
        self.mana = mana
        self.speed = speed
        self.elapsed = 0
        self.images = []
        self.turn = False
        self.attacking = False

        self.itterate(default, "Default")
        self.index = 0
        self.image = self.images[self.index]

    def itterate(self, lists, folder):
        for image in lists:
            self.images.append(load_image(folder, image))

    def update(self):
        self.elapsed = pygame.time.get_ticks() - self.elapsed
        if self.elapsed % 5 == 0:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.images.clear()

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def attack(self, target):
        damage = self.atk - target.deffense
        damage_taken = target.hp - damage
        target.hp = damage_taken

filled_up("Archer", archer_idle)
filled_up("ArcherAttack", archer_attack)
filled_up("Orc", orc_idle)
filled_up("OrcAttack", orc_attack)
filled_up("Default", default)

def main():
    gameOn = True
    player = Character(300, 300, "Roy", 30,20, 100, 30, 10)
    enemy = Character(100, 300, "Kirby", 30, 20, 100, 30, 4)
    text_attack = Label(200, 520, "Attack")
    arrow = Pointer(text_attack.x - 20, text_attack.y)
    clock = pygame.time.Clock()
    max_enemy_num = 4
    min_enemy_num = 3
    enemies = []
    padding = 300
    health_font = pygame.font.SysFont("comicsans", 20)
    FPS = 60
    index = 0

    def redraw_window():
        WINDOWS.blit(BG, (0, 0))
        player.itterate(archer_idle, "Archer")
        player.draw(WINDOWS)
        player.update()

        for enemy in enemies:
            enemy.update()
            enemy.itterate(orc_idle, "Orc")
            enemy_dmg_show = health_font.render(f"{enemy.hp}", 1, (255, 255, 255))
            WINDOWS.blit(enemy_dmg_show, (enemy.x, enemy.y - 15))
            enemy.draw(WINDOWS)

        player_dmg_show = health_font.render(f"{player.hp}", 1, (255, 255, 255))
        WINDOWS.blit(player_dmg_show, (player.x, player.y - 15))

        attack_label = health_font.render(f"{text_attack}", 1, (0, 0, 0))
        WINDOWS.blit(attack_label, (text_attack.x, text_attack.y))

        arrow.draw(WINDOWS)

        pygame.display.update()

    while gameOn:
        clock.tick(FPS)

        if len(enemies) == 0:
            for _ in range(random.randrange(min_enemy_num, max_enemy_num)):
                enemy = Character(random.randrange(50, 100), padding, "Kirby", 30, 20, 100, 30, 4)
                padding += 75
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False

        keys = pygame.key.get_pressed()

        if player.turn:

            arrow.x = enemies[index].x + 20
            arrow.y = enemies[index].y
            if keys[pygame.K_s]:
                try:
                    time.sleep(.1)
                    index += 1
                    arrow.y = enemies[index].y
                    arrow.x = enemies[index].x + 20
                except IndexError:
                    index -= 1
            elif keys[pygame.K_w]:
                try:
                    time.sleep(.1)
                    index -= 1
                    arrow.y = enemies[index].y
                    arrow.x = enemies[index].x + 20
                except IndexError:
                    index += 1
            elif keys[pygame.K_j]:
                time.sleep(.3)
                t_end = time.time() + .5
                while time.time() < t_end:
                    player.itterate(archer_attack, "ArcherAttack")
                    redraw_window()
                player.attack(enemies[index])
                arrow.flipping()
                arrow.x = text_attack.x - 20
                arrow.y = text_attack.y
                enemy.turn = True
                player.turn = False
        elif enemy.turn:
            for enemy in enemies:
                t_end = time.time() + .50
                while time.time() < t_end:
                    enemy.itterate(orc_attack, "OrcAttack")
                    redraw_window()
                enemy.attack(player)
                enemy.turn = False
        else:
            if keys[pygame.K_j] and arrow.y == text_attack.y:
                time.sleep(.1)
                arrow.flipping()
                arrow.x = enemies[0].x + 20
                arrow.y = enemies[0].y
                player.turn = True

        redraw_window()

main()