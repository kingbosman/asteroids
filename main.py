import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot
import os


def main():
    if not os.path.exists("current_highscore.txt"):
        with open("current_highscore.txt", "w") as file:
            file.write("0")

    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updateable, drawable)

    AsteroidField.containers = updateable
    AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, updateable, drawable)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updateable.update(dt)
        for v in asteroids:
            if player.collide(v):
                print("Game over!")
                print(f"final score: {player.score}")
                with open("current_highscore.txt", "r+") as file:
                    current = file.read()
                    if player.score <= int(current):
                        print(f"current highscore: {current}")
                    else:
                        file.seek(0)
                        file.write(str(player.score))
                        file.truncate()
                        print("You have a new Highscore!")
                exit()

            for shot in shots:
                if shot.collide(v):
                    player.score += 1
                    v.split()
                    shot.kill()

        screen.fill("black")

        # Set score
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render(f"Score:{player.score}", True, (0, 255, 0))
        screen.blit(text, pygame.Vector2(0, 0))

        pygame.display.set_caption("Asteroid Game")

        # player.draw(screen)
        for v in drawable:
            v.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
