import pygame

pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound("hit.wav")
sound.play()

input("Press Enter to exit...")
