
import pygame
import os

# Paramètres de redimensionnement des images
PIPE_WIDTH = 52 # Largeur des tuyaux
PIPE_HEIGHT = 800
BIRD_SCALE = 1.0

# Variables globales pour stocker les images et polices
BG_IMG = None
GROUND_IMG = None
BIRD_IMGS = []
PIPE_TOP_IMG = None
PIPE_BOTTOM_IMG = None
SCORE_FONT = None

def load_assets(win_width, win_height):
    """
    Charge et redimensionne toutes les images et polices du jeu.
    """
    global BG_IMG, GROUND_IMG, BIRD_IMGS, PIPE_TOP_IMG, PIPE_BOTTOM_IMG, SCORE_FONT

    # Chargement des images brutes depuis le dossier 'images'
    bg_raw = pygame.image.load(os.path.join("images", "bg.png"))
    ground_raw = pygame.image.load(os.path.join("images", "base.png"))
    bird1_raw = pygame.image.load(os.path.join("images", "bird1.png"))
    bird2_raw = pygame.image.load(os.path.join("images", "bird2.png"))
    bird3_raw = pygame.image.load(os.path.join("images", "bird3.png"))
    pipe_top_raw = pygame.image.load(os.path.join("images", "toppipe.png"))
    pipe_bottom_raw = pygame.image.load(os.path.join("images", "bottompipe.png"))

    # Chargement de la police de caractères pour le score
    SCORE_FONT = pygame.font.Font(os.path.join("images", "flappy-bird-font.ttf"), 50)

    # Redimensionnement du fond d'écran
    BG_IMG = pygame.transform.scale(bg_raw, (win_width, win_height))

    # Le sol (base)
    GROUND_IMG = ground_raw

    # Redimensionnement des oiseaux (animation)
    if BIRD_SCALE != 1.0:
        BIRD_IMGS = [
            pygame.transform.scale(bird1_raw, (int(bird1_raw.get_width() * BIRD_SCALE), int(bird1_raw.get_height() * BIRD_SCALE))),
            pygame.transform.scale(bird2_raw, (int(bird2_raw.get_width() * BIRD_SCALE), int(bird2_raw.get_height() * BIRD_SCALE))),
            pygame.transform.scale(bird3_raw, (int(bird3_raw.get_width() * BIRD_SCALE), int(bird3_raw.get_height() * BIRD_SCALE)))
        ]
    else:
        BIRD_IMGS = [bird1_raw, bird2_raw, bird3_raw]

    # Redimensionnement des tuyaux en gardant les proportions
    ratio = PIPE_WIDTH / pipe_top_raw.get_width()
    new_height = int(pipe_top_raw.get_height() * ratio)
    
    PIPE_TOP_IMG = pygame.transform.scale(pipe_top_raw, (PIPE_WIDTH, new_height))
    PIPE_BOTTOM_IMG = pygame.transform.scale(pipe_bottom_raw, (PIPE_WIDTH, new_height))
