import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random
import math
from FlappyBird_Gym.objects import Grumpy, Pipe, Base, Score

class FlappyBirdEnv(gym.Env):
    def __init__(self):
        # For Gymnasium Compatibility
        super(FlappyBirdEnv, self).__init__()
        # Spazio delle azioni: 0 = niente, 1 = flap
        self.action_space = spaces.Discrete(2)
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
        self.FPS = 30

        # COLORS
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Backgrounds
        self.bg1 = pygame.image.load('./FlappyBird_Gym/Assets/background-day.png')
        self.bg2 = pygame.image.load('./FlappyBird_Gym/Assets/background-night.png')

        self.bg = random.choice([self.bg1, self.bg2])

        self.im_list = [pygame.image.load('./FlappyBird_Gym/Assets/pipe-green.png'), pygame.image.load('./FlappyBird_Gym/Assets/pipe-red.png')]
        self.pipe_img = random.choice(self.im_list)

        self.gameover_img = pygame.image.load('./FlappyBird_Gym/Assets/gameover.png')
        self.flappybird_img = pygame.image.load('./FlappyBird_Gym/Assets/flappybird.png')
        self.flappybird_img = pygame.transform.scale(self.flappybird_img, (200, 80))

        # Sounds & fx
        self.die_fx = pygame.mixer.Sound('./FlappyBird_Gym/Sounds/die.wav')
        self.hit_fx = pygame.mixer.Sound('./FlappyBird_Gym/Sounds/hit.wav')
        self.point_fx = pygame.mixer.Sound('./FlappyBird_Gym/Sounds/point.wav')
        self.swoosh_fx = pygame.mixer.Sound('./FlappyBird_Gym/Sounds/swoosh.wav')
        self.wing_fx = pygame.mixer.Sound('./FlappyBird_Gym/Sounds/wing.wav')

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
        self.pipe_frequency = 0 

        # Dimensioni dell'osservazione (ad esempio, posizione, velocità, ecc.)
        self.observation_space = spaces.Box(
             low=np.array([0,-5,-6,0,-5,0]),  # Limiti inferiori
             high=np.array([340,self.HEIGHT,8,340,self.HEIGHT,340]),  # Limiti superiori
            dtype=np.float32
        )      

    def step(self, action):
        self.win.blit(self.bg, (0,0))
        
        reward = 0

        if self.start_screen:
            self.speed = 0
            self.grumpy.draw_flap()
            self.base.update(self.speed)
            self.win.blit(self.flappybird_img, (40, 50))

        else:
            
            self.pipe_group.update(self.speed)
            self.base.update(self.speed)	
            self.grumpy.update(action)
            self.score_img.update(self.score)
            
            if pygame.sprite.spritecollide(self.grumpy, self.pipe_group, False) or self.grumpy.rect.top <= 0:
                self.game_started = False
                if self.grumpy.alive:
                    self.hit_fx.play()
                    self.die_fx.play()
                    self.game_over = True
                self.grumpy.alive = False
                self.grumpy.theta = self.grumpy.vel * -2
        
            if self.grumpy.rect.bottom >= self.display_height:
                self.speed = 0
                self.game_over = True
                
            
            # Definizione della ricompensa
            if self.game_over:
                reward = -10
        
            if len(self.pipe_group) > 0:
                self.p = self.pipe_group.sprites()[0]
                if self.grumpy.rect.left > self.p.rect.left and self.grumpy.rect.right < self.p.rect.right and not self.pipe_pass and self.grumpy.alive:
                    self.pipe_pass = True
        
                if self.pipe_pass:
                    if self.grumpy.rect.left > self.p.rect.right:
                        self.pipe_pass = False
                        self.score += 1
                        self.point_fx.play()
                        reward = 1
                        #genero la pipe nuova
                        self.y = self.display_height // 2
                        self.pipe_pos = random.choice(range(-100,100,4))
                        self.height = self.y + self.pipe_pos
                        self.top = Pipe(self.win, self.pipe_img, self.height, 1)
                        self.bottom = Pipe(self.win, self.pipe_img, self.height, -1)
                        self.pipe_group.add(self.top)
                        self.pipe_group.add(self.bottom)
                        self.last_pipe = self.next_pipe
                        
        if not self.grumpy.alive:
            self.win.blit(self.gameover_img, (50,200))
            
        # Definizione della ricompensa
        if self.game_over:
            reward = -1

        pipes = self.pipe_group.sprites()
        if len(pipes) == 4: #nel caso sono state generate nuove pipe e le prime non sono ancora scomparse
            top_pipe = pipes[2]    # Primo tubo (superiore)
            bottom_pipe = pipes[3] # Secondo tubo (inferiore)
            # Calcola il centro del gap in termini di y
            gap_center_y = (top_pipe.rect.bottom + bottom_pipe.rect.top) / 2
            # print(top_pipe.rect.bottom - bottom_pipe.rect.top) Distanza spazio tra le coppie di pipe
            gap_center_x = top_pipe.rect.right
        elif len(pipes) == 2: #nel caso sono state generate nuove pipe e le prime non sono ancora scomparse
            top_pipe = pipes[0]    # Primo tubo (superiore)
            bottom_pipe = pipes[1] # Secondo tubo (inferiore)
            # Calcola il centro del gap in termini di y
            gap_center_y = (top_pipe.rect.bottom + bottom_pipe.rect.top) / 2
            # print(top_pipe.rect.bottom - bottom_pipe.rect.top) Distanza spazio tra le coppie di pipe
            gap_center_x = top_pipe.rect.right

        pygame.draw.line(self.win, (0, 255, 0), 
                 (int(self.grumpy.rect.centerx), int(self.grumpy.rect.centery)),
                 (int(gap_center_x), int(gap_center_y)), 2)  # Linea verde di spessore 2
        
        if self.grumpy.rect.y <= 15 and reward == 0:
            reward = -0.5
        elif ((self.grumpy.rect.centery - gap_center_y) < 13  and (self.grumpy.rect.centery - gap_center_y) > -13) and reward == 0:
            reward = 0.4
        elif ((self.grumpy.rect.centery - gap_center_y) < 25  and (self.grumpy.rect.centery - gap_center_y) > -25) and reward == 0:
            reward = 0.3
        elif ((self.grumpy.rect.centery - gap_center_y) < 50  and (self.grumpy.rect.centery - gap_center_y) > -50) and reward == 0:
            reward = 0.2
        elif reward == 0:
            reward = 0.1
        
        
        distance = math.sqrt((gap_center_x - self.grumpy.rect.centerx)**2 + (gap_center_y - self.grumpy.rect.centery)**2)

        # Stato di osservazione
        obs = np.array([
            self.grumpy.rect.centerx,
            self.grumpy.rect.centery,
            self.grumpy.vel, #VELOCITA CON CUI SALTA
            gap_center_x,
            gap_center_y,
            distance
        ], dtype=np.float32)
        
        # Stato del gioco
        done = self.game_over

        #Info Ulteriori
        info = {}
        
        # Valore aggiuntivo richiesto per Gymnasium
        truncated = False
        print('ACTION',action)
        print('REWARD',reward)
        print('OBS',obs)
        self.render()
        return obs, reward, done, truncated, info

    def render(self):
        self.clock.tick(self.FPS)
        pygame.display.update()

    def reset(self, seed=None, options=None):
        # Imposta il seme per la riproducibilità
        if seed is not None:
            self.np_random, seed = gym.utils.seeding.np_random(seed)
            random.seed(seed)
            np.random.seed(seed)
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
        self.game_started = True
        self.game_over = False
        self.score = 0
        self.start_screen = False
        self.pipe_pass = False
        self.pipe_frequency = 0
        distance = 0
        #gen next pipe
        self.last_pipe = 0
        self.next_pipe = 0
        self.pipe_group.empty()
        self.speed = 2
        self.score = 0
        #generazione nuova pipe
        self.y = self.display_height // 2
        self.pipe_pos = random.choice(range(-100,100,4))
        self.height = self.y + self.pipe_pos
        self.top = Pipe(self.win, self.pipe_img, self.height, 1)
        self.bottom = Pipe(self.win, self.pipe_img, self.height, -1)
        self.pipe_group.add(self.top)
        self.pipe_group.add(self.bottom)
        self.last_pipe = self.next_pipe
        # Osservazione iniziale

        pipes = self.pipe_group.sprites()
        if len(pipes) == 4: #nel caso sono state generate nuove pipe e le prime non sono ancora scomparse
            top_pipe = pipes[2]    # Primo tubo (superiore)
            bottom_pipe = pipes[3] # Secondo tubo (inferiore)
            # Calcola il centro del gap in termini di y
            gap_center_y = (top_pipe.rect.bottom + bottom_pipe.rect.top) / 2
            # print(top_pipe.rect.bottom - bottom_pipe.rect.top) Distanza spazio tra le coppie di pipe
            gap_center_x = top_pipe.rect.right
        elif len(pipes) == 2: #nel caso sono state generate nuove pipe e le prime non sono ancora scomparse
            top_pipe = pipes[0]    # Primo tubo (superiore)
            bottom_pipe = pipes[1] # Secondo tubo (inferiore)
            # Calcola il centro del gap in termini di y
            gap_center_y = (top_pipe.rect.bottom + bottom_pipe.rect.top) / 2
            # print(top_pipe.rect.bottom - bottom_pipe.rect.top) Distanza spazio tra le coppie di pipe
            gap_center_x = top_pipe.rect.right

        distance = math.sqrt((gap_center_x - self.grumpy.rect.centerx)**2 + (gap_center_y - self.grumpy.rect.centery)**2)

        observation = np.array([
            self.grumpy.rect.centerx,
            self.grumpy.rect.centery,
            self.grumpy.vel, #VELOCITA CON CUI SALTA
            gap_center_x,
            gap_center_y,
            distance
        ], dtype=np.float32)

        
        
        # Controlla se il chiamante si aspetta una tupla o solo l'osservazione
        if "stable_baselines3" in str(self.__class__):
            return observation
        
        return observation, {}

    def close(self):
        pygame.quit()