import gymnasium
from gymnasium import spaces
import numpy as np
import pygame
import random
from objects import Grumpy, Pipe, Base, Score

class FlappyBirdEnv(gymnasium.Env):
    def __init__(self):
        # Setup del gioco
        pygame.init()
        self.SCREEN = self.WIDTH, self.HEIGHT = 288, 512
        self.display_height = 0.80 * self.HEIGHT
        self.info = pygame.display.Info()

        self.width = self.info.current_w
        self.height = self.info.current_h

        if self.width >= self.height:
            self.win = pygame.display.set_mode(self.SCREEN, pygame.NOFRAME)
        else:
            self.win = pygame.display.set_mode(self.SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        # COLORS
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Backgrounds
        self.bg1 = pygame.image.load('Assets/background-day.png')
        self.bg2 = pygame.image.load('Assets/background-night.png')

        self.bg = random.choice([self.bg1, self.bg2])

        self.im_list = [pygame.image.load('Assets/pipe-green.png'), pygame.image.load('Assets/pipe-red.png')]
        self.pipe_img = random.choice(self.im_list)

        self.gameover_img = pygame.image.load('Assets/gameover.png')
        self.flappybird_img = pygame.image.load('Assets/flappybird.png')
        self.flappybird_img = pygame.transform.scale(self.flappybird_img, (200, 80))

        # Sounds & fx
        self.die_fx = pygame.mixer.Sound('Sounds/die.wav')
        self.hit_fx = pygame.mixer.Sound('Sounds/hit.wav')
        self.point_fx = pygame.mixer.Sound('Sounds/point.wav')
        self.swoosh_fx = pygame.mixer.Sound('Sounds/swoosh.wav')
        self.wing_fx = pygame.mixer.Sound('Sounds/wing.wav')

        # Objects
        self.pipe_group = pygame.sprite.Group()
        self.base = Base(self.win)
        self.score_img = Score(self.WIDTH // 2, 50, self.win)
        self.grumpy = Grumpy(self.win)

        # Variables
        self.base_height = 0.80 * self.HEIGHT
        self.speed = 0
        self.game_started = False
        self.game_over = False
        self.score = 0
        self.start_screen = True
        self.pipe_pass = False
        self.pipe_frequency = 1600        

    def step(self, action):
        self.win.blit(self.bg, (0,0))
        
        if self.start_screen:
            self.speed = 0
            self.grumpy.draw_flap()
            self.base.update(self.speed)
            
            self.win.blit(self.flappybird_img, (40, 50))
        else:
            
            if self.game_started and not self.game_over:
                
                self.next_pipe = pygame.time.get_ticks()
                if self.next_pipe - self.last_pipe >= self.pipe_frequency:
                    self.y = self.display_height // 2
                    self.pipe_pos = random.choice(range(-100,100,4))
                    self.height = self.y + self.pipe_pos
                    
                    self.top = Pipe(self.win, self.pipe_img, self.height, 1)
                    self.bottom = Pipe(self.win, self.pipe_img, self.height, -1)
                    self.pipe_group.add(self.top)
                    self.pipe_group.add(self.bottom)
                    self.last_pipe = self.next_pipe
            
            self.pipe_group.update(self.speed)
            self.base.update(self.speed)	
            self.grumpy.update(action)
            self.score_img.update(self.score)
            
            if pygame.sprite.spritecollide(self.grumpy, self.pipe_group, False) or self.grumpy.rect.top <= 0:
                self.game_started = False
                if self.grumpy.alive:
                    self.hit_fx.play()
                    self.die_fx.play()
                self.grumpy.alive = False
                self.grumpy.theta = self.grumpy.vel * -2
        
            if self.grumpy.rect.bottom >= self.display_height:
                self.speed = 0
                self.game_over = True
        
            if len(self.pipe_group) > 0:
                self.p = self.pipe_group.sprites()[0]
                if self.grumpy.rect.left > self.p.rect.left and self.grumpy.rect.right < self.p.rect.right and not self.pipe_pass and self.grumpy.alive:
                    self.pipe_pass = True
        
                if self.pipe_pass:
                    if self.grumpy.rect.left > self.p.rect.right:
                        self.pipe_pass = False
                        self.score += 1
                        self.point_fx.play()
                        
        if not self.grumpy.alive:
            self.win.blit(self.gameover_img, (50,200))
            
        #for start game or restart game
        if action == 1:
            if self.start_screen:
                self.game_started = True
                self.speed = 2
                self.start_screen = False

                self.game_over = False
            #grumpy.reset()
                self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency
                self.next_pipe = 0
                self.pipe_group.empty()
                
                self.speed = 2
                self.score = 0
                
            if self.game_over:
                self.start_screen = True
                self.grumpy = Grumpy(self.win)
                self.pipe_img = random.choice(self.im_list)
                self.bg = random.choice([self.bg1, self.bg2])

    def render(self):
        self.clock.tick(self.FPS)
        pygame.display.update()

    def reset(self):
        # Backgrounds
        self.bg = random.choice([self.bg1, self.bg2])
        self.pipe_img = random.choice(self.im_list)
        # Objects
        self.pipe_group = pygame.sprite.Group()
        self.base = Base(self.win)
        self.score_img = Score(self.WIDTH // 2, 50, self.win)
        self.grumpy = Grumpy(self.win)
        # Variables
        self.base_height = 0.80 * self.HEIGHT
        self.speed = 0
        self.game_started = False
        self.game_over = False
        self.score = 0
        self.start_screen = True
        self.pipe_pass = False
        self.pipe_frequency = 1600

    def close(self):
        pygame.quit()