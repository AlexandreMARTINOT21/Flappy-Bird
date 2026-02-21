import pygame
from sys import exit
import config
import components
import assets
import population

# Initialisation de Pygame
pygame.init()
clock = pygame.time.Clock()

# Chargement initial des ressources (images, sons, polices)
assets.load_assets(config.win_width, config.win_height)

# Ajustement de la position du sol en fonction de l'image chargée
if assets.GROUND_IMG:
    g_height = assets.GROUND_IMG.get_height()
    # On place le sol tout en bas de la fenêtre
    components.Ground.ground_level = config.win_height - g_height
    config.ground.y = components.Ground.ground_level
    config.ground.rect = pygame.Rect(0, config.ground.y, config.win_width, g_height)

# Création de la population d'oiseaux (ici 1000 individus au départ)
population_obj = population.Population(1000)

def generate_pipes(pipe_type='normal'):
    """ Crée de nouveaux tuyaux dans la liste globale. """
    config.pipes.append(components.Pipes(config.win_width, pipe_type))

def quit_game():
    """ Gère la fermeture propre du jeu. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Sauvegarder le meilleur cerveau avant de quitter
            population_obj.save_best_player()
            pygame.quit()
            exit()

def main():
    """ Boucle principale du jeu. """
    # On pourrait charger ici un ancien champion pour gagner du temps
    loaded_best = population_obj.load_best_player()

    pipes_spawn_time = 10 # Compteur pour l'apparition des tuyaux
    
    # Position et vitesse du décor (parallaxe)
    bg_x = 0
    bg_speed = 0.5 

    score = 0
    
    # Gestion des cycles d'obstacles spéciaux
    special_section_remaining = 0
    current_pipe_type = 'normal'
    transition_delay = 0

    while True:
        quit_game()

        # Dessin du fond d'écran avec effet de boucle (parallax)
        rel_x = bg_x % assets.BG_IMG.get_width()
        config.window.blit(assets.BG_IMG, (rel_x - assets.BG_IMG.get_width(), 0))
        if rel_x < config.win_width:
            config.window.blit(assets.BG_IMG, (rel_x, 0))
            
        bg_x -= bg_speed
        
        # Logique d'apparition des tuyaux
        if pipes_spawn_time <= 0 and transition_delay <= 0:
            if special_section_remaining > 0:
                # On génère des tuyaux spéciaux (ex: mobiles)
                generate_pipes(current_pipe_type)
                special_section_remaining -= 1
                pipes_spawn_time = 200
                if special_section_remaining == 0:
                    current_pipe_type = 'normal'
            else:
                # Déclenchement périodique de zones de difficulté
                if (score >= 8 and (score - 8) % 20 == 0) and current_pipe_type == 'normal':
                    current_pipe_type = 'moving'
                    special_section_remaining = 10
                    transition_delay = 200 
                
                if transition_delay <= 0:
                    generate_pipes(current_pipe_type)
                    pipes_spawn_time = 200
        
        if transition_delay > 0:
            transition_delay -= 1
            
        pipes_spawn_time -= 1

        # Mise à jour et affichage des tuyaux
        for p in config.pipes:
            p.draw(config.window)
            old_passed = p.passed
            p.update()
            # Si le tuyau est dépassé, on augmente le score
            if not old_passed and p.passed:
                score += 1
                
            # On retire les tuyaux sortis de l'écran
            if p.off_screen:
                config.pipes.remove(p)

        # Mise à jour et affichage du sol
        config.ground.update()
        config.ground.draw(config.window)

        # Affichage du score au centre
        score_surface = assets.SCORE_FONT.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(config.win_width // 2, 100))
        config.window.blit(score_surface, score_rect)
        
        # Affichage des statistiques de l'IA (Génération, oiseaux en vie)
        alive_count = sum(1 for p in population_obj.players if p.alive)
        species_count = len(population_obj.species)
        stats_text = f"Gen: {population_obj.generation}  Vivants: {alive_count}  Especes: {species_count}"
        stats_surface = pygame.font.SysFont("Arial", 20).render(stats_text, True, (255, 255, 255))
        config.window.blit(stats_surface, (10, 10))

        # Si certains oiseaux sont encore en vie : on les met à jour
        if not population_obj.extinct():
            population_obj.update_live_players()
        else:
            # Si tout le monde est mort : on lance l'évolution
            config.pipes.clear()
            score = 0
            special_section_remaining = 0
            current_pipe_type = 'normal'
            transition_delay = 0
            population_obj.natural_selection() # Création de la génération suivante

        # On limite à 50 images par seconde
        clock.tick(50)
        pygame.display.flip()

if __name__ == "__main__":
    main()
