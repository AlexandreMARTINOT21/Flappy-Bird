import brain
import random
import pygame
import config
import assets


class Player:
    """
    Représente un oiseau dans le jeu, contrôlé par son propre cerveau (IA).
    """
    def __init__(self, color=None):
        # Position et taille de l'oiseau
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 34, 24)
        
        # Couleur aléatoire pour distinguer les oiseaux
        if color is None:
            self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        else:
            self.color = color
            
        self.vel = 0         # Vitesse verticale (gravité)
        self.flap = False    # Si l'oiseau est en train d'appuyer pour monter
        self.alive = True    # Si l'oiseau est encore en jeu
        self.lifespan = 0    # Durée de vie (utilisée pour le score IA)
        
        # Gestion de l'animation
        self.img_count = 0
        self.img = None

        # Intelligence Artificielle (IA)
        self.decision = None
        self.vision = [0.5, 1, 0.5, 0, 0, 0] # Ce que l'oiseau 'voit'
        self.fitness = 0                     # Score de performance de l'IA
        self.inputs = 6                      # Nombre d'informations reçues par le cerveau
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def draw(self, window):
        """
        Gère l'affichage de l'oiseau, son animation et sa rotation.
        """
        self.img_count += 1

        # Cycle d'animation des ailes
        ANIMATION_SPEED = 5
        if self.img_count < ANIMATION_SPEED:
            self.img = assets.BIRD_IMGS[0]
        elif self.img_count < ANIMATION_SPEED * 2:
            self.img = assets.BIRD_IMGS[1]
        elif self.img_count < ANIMATION_SPEED * 3:
            self.img = assets.BIRD_IMGS[2]
        elif self.img_count < ANIMATION_SPEED * 4:
            self.img = assets.BIRD_IMGS[1]
        elif self.img_count == ANIMATION_SPEED * 4 + 1:
            self.img = assets.BIRD_IMGS[0]
            self.img_count = 0
            
        # Si l'oiseau tombe vite, on arrête de battre des ailes
        if self.vel >= 3:
            self.img = assets.BIRD_IMGS[1]
            self.img_count = ANIMATION_SPEED * 2

        # Rotation de l'image selon la vitesse (nez vers le haut ou bas)
        angle = -self.vel * 3
        rotated_image = pygame.transform.rotate(self.img, angle)
        # On rend les oiseaux un peu transparents pour mieux voir la masse
        rotated_image.set_alpha(150)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        
        window.blit(rotated_image, new_rect.topleft)

    def ground_collision(self, ground):
        """ Vérifie si l'oiseau touche le sol. """
        return pygame.Rect.colliderect(self.rect, ground.rect)

    def sky_collision(self):
        """ Vérifie si l'oiseau sort par le haut de l'écran. """
        return bool(self.rect.y < 0)

    def pipe_collision(self):
        """ Vérifie si l'oiseau percute un tuyau. """
        for p in config.pipes:
             if pygame.Rect.colliderect(self.rect, p.top_rect) or \
                   pygame.Rect.colliderect(self.rect, p.bottom_rect):
                return True
        return False

    def update(self, ground):
        """
        Met à jour la physique de l'oiseau (gravité et collisions).
        """
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Gravité : l'oiseau tombe de plus en plus vite
            self.vel += 0.25
            self.rect.y += self.vel
            # Vitesse maximale de chute
            if self.vel > 8:
                self.vel = 8
            self.lifespan += 4 # Plus il survit, plus son score augmente
        else:
            # Mort de l'oiseau
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        """ Fait sauter l'oiseau. """
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5 # Donne une vitesse vers le haut
        if self.vel >= 0:
            self.flap = False

    @staticmethod
    def closest_pipe():
        """ Trouve le prochain tuyau que l'oiseau va rencontrer. """
        for p in config.pipes:
            if not p.passed:
                return p

    def look(self):
        """
        Récupère les données de l'environnement pour nourrir l'IA.
        """
        if config.pipes:
            closest = self.closest_pipe()
            if closest:
                # 1. Distance verticale avec le tuyau du haut
                self.vision[0] = max(0, self.rect.center[1] - closest.top_rect.bottom) / 500
                # 2. Distance horizontale avec le tuyau
                self.vision[1] = max(0, closest.x - self.rect.center[0]) / 500
                # 3. Distance verticale avec le tuyau du bas
                self.vision[2] = max(0, closest.bottom_rect.top - self.rect.center[1]) / 500
                
                # 4 & 5. Info sur le mouvement si le tuyau est mobile
                if closest.type == 'moving':
                    self.vision[3] = closest.speed_direction
                    self.vision[4] = abs(closest.vel_y) / 5.0
                else:
                    self.vision[3] = 0
                    self.vision[4] = 0
                
                # 6. Distance par rapport au plafond
                self.vision[5] = self.rect.y / config.win_height

    def think(self):
        """
        L'IA décide de sauter ou non en fonction de sa vision.
        """
        self.decision = self.brain.feed_forward(self.vision)
        # Si la sortie du cerveau est supérieure à 0.6, l'oiseau saute
        if self.decision > 0.6:
            self.bird_flap()

    def calculate_fitness(self):
        """
        Calcule le score global de l'oiseau (mérite).
        """
        # La base est le temps de survie
        self.fitness = self.lifespan
        
        # On ajoute un bonus si l'oiseau est bien au milieu de l'ouverture
        closest = self.closest_pipe()
        if closest:
            gap_center = closest.top_height + (closest.opening / 2)
            dist_to_gap = abs(self.rect.centery - gap_center)
            
            # Plus il est proche du centre, plus il gagne de points
            proximity_reward = max(0, 1000 - dist_to_gap)
            self.fitness += proximity_reward
        
        self.fitness = max(0.0, self.fitness)

    def clone(self):
        """ Crée une copie de l'oiseau pour la génération suivante. """
        clone = Player(self.color)
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone
