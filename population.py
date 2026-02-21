import config
import player
import math
import species
import operator
import pickle
import os


class Population:
    """
    Gère l'ensemble des oiseaux (la population) et leur évolution.
    """
    def __init__(self, size):
        self.players = []       # Tous les oiseaux de la génération actuelle
        self.generation = 1     # Numéro de la génération actuelle
        self.species = []       # Liste des espèces identifiées
        self.size = size        # Taille maximale de la population
        self.best_player = None # Le meilleur oiseau de tous les temps
        self.best_fitness = 0   # Le meilleur score de tous les temps
        
        # On remplit la première génération avec des oiseaux aléatoires
        for i in range(0, self.size):
            self.players.append(player.Player())

    def update_live_players(self):
        """
        Fait vivre, réfléchir et dessine chaque oiseau encore en vie.
        """
        for p in self.players:
            if p.alive:
                p.look()   # L'oiseau regarde les obstacles
                p.think()  # L'oiseau décide (grâce à son cerveau)
                p.draw(config.window)
                p.update(config.ground) # L'oiseau se déplace
                
                # Mise à jour du record absolu
                if p.fitness > self.best_fitness:
                    self.best_fitness = p.fitness
                    self.best_player = p.clone()
                    self.save_best_player()

    def natural_selection(self):
        """
        Lance le processus de sélection naturelle pour créer la prochaine génération.
        """
        self.speciate()                # 1. On regroupe par espèces
        self.calculate_fitness()       # 2. On évalue les performances
        self.kill_extinct_species()    # 3. On supprime les espèces vides
        self.kill_stale_species()      # 4. On supprime les espèces qui ne progressent plus
        self.sort_species_by_fitness() # 5. On trie par excellence
        self.next_gen()                # 6. On crée les bébés pour la suite

    def speciate(self):
        """
        Répartit les oiseaux dans les différentes espèces existantes ou en crée de nouvelles.
        """
        for s in self.species:
            s.players = [] # On vide les espèces avant de les remplir

        for p in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(p.brain):
                    s.add_to_species(p)
                    add_to_species = True
                    break
            if not add_to_species:
                # Si l'oiseau est trop différent, il fonde une nouvelle espèce
                self.species.append(species.Species(p))

    def calculate_fitness(self):
        """
        Demande à chaque oiseau et espèce de calculer sa performance.
        """
        for p in self.players:
            p.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        """
        Supprime les espèces qui n'ont plus de membres.
        """
        species_bin = []
        for s in self.species:
            if len(s.players) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def kill_stale_species(self):
        """
        Élimine les espèces qui n'ont pas progressé depuis longtemps (staleness).
        """
        player_bin = []
        species_bin = []
        for i, s in enumerate(self.species):
            # On ne tue jamais les 2 meilleures espèces pour garder les meilleurs gènes
            if s.staleness >= 15:
                if len(self.species) > len(species_bin) + 1 and i > 1:
                    species_bin.append(s)
                    for p in s.players:
                        player_bin.append(p)
                else:
                    s.staleness = 0 # Réinitialisation si c'est une espèce élite
        
        for p in player_bin:
            self.players.remove(p)
        for s in species_bin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        """
        Trie les espèces de la meilleure à la moins bonne.
        """
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)
        
        # On limite le nombre d'espèces pour optimiser les performances
        if len(self.species) > 20:
            self.species = self.species[:20]

    def next_gen(self):
        """
        Régénère la population en mélangeant les meilleurs éléments.
        """
        children = []

        # 1. Élitisme : On garde toujours une copie du champion de chaque espèce
        for s in self.species:
            children.append(s.champion.clone())

        # 2. Reproduction : On remplit le reste avec des bébés
        if len(self.species) > 0:
            slots_remaining = self.size - len(children)
            # On favorise les espèces qui ont les meilleurs champions (mathématique)
            total_champ_fitness_sq = sum((s.benchmark_fitness ** 4) for s in self.species)
            
            if slots_remaining > 0:
                if total_champ_fitness_sq > 0:
                    # Distribution proportionnelle au mérite
                    for s in self.species:
                        num_offspring = math.floor(((s.benchmark_fitness ** 4) / total_champ_fitness_sq) * slots_remaining)
                        for i in range(0, num_offspring):
                            children.append(s.offspring())
                else:
                    # Si personne n'a de point, on distribue équitablement
                    children_per_species = math.floor(slots_remaining / len(self.species))
                    for s in self.species:
                        for i in range(0, children_per_species):
                            children.append(s.offspring())

        # 3. On finit de remplir les places vides avec des bébés du meilleur champion
        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []
        for child in children:
            self.players.append(child)
        self.generation += 1

    def extinct(self):
        """
        Vérifie si tous les oiseaux sont morts.
        """
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct

    def save_best_player(self):
        """
        Sauvegarde le meilleur oiseau de l'histoire dans un fichier.
        """
        if self.best_player:
            with open('best_bird_brain.pkl', 'wb') as f:
                pickle.dump(self.best_player, f)

    def load_best_player(self):
        """
        Charge le meilleur oiseau sauvegardé.
        """
        if os.path.exists('best_bird_brain.pkl'):
            try:
                with open('best_bird_brain.pkl', 'rb') as f:
                    return pickle.load(f)
            except:
                return None

    def seed_population(self, best_bird):
        """
        Remplace la population actuelle par des versions mutées du champion chargé.
        """
        self.best_player = best_bird.clone()
        self.best_fitness = best_bird.fitness
        
        self.players = []
        # On garde un clone exact
        self.players.append(best_bird.clone())
        
        # On crée le reste par mutation pour explorer autour de cette bonne base
        for i in range(1, self.size):
            p = best_bird.clone()
            p.brain.mutate()
            self.players.append(p)
        return None
