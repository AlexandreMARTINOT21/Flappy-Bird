import operator
import random

class Species:
    """
    Regroupe les oiseaux qui ont des cerveaux similaires pour protéger l'innovation.
    Cela évite que de nouvelles structures prometteuses soient éliminées trop vite.
    """
    def __init__(self, player):
        self.players = []            # Liste des oiseaux appartenant à cette espèce
        self.average_fitness = 0     # Score moyen de l'espèce
        self.threshold = 0.5         # Seuil de similarité pour rester dans l'espèce
        self.players.append(player)
        self.benchmark_fitness = player.fitness
        self.benchmark_brain = player.brain.clone() # Cerveau de référence pour l'espèce
        self.champion = player.clone()             # Le meilleur oiseau de l'espèce
        self.staleness = 0           # Nombre de générations sans amélioration

    def similarity(self, brain):
        """
        Vérifie si un cerveau est assez proche de celui de l'espèce.
        """
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity

    @staticmethod
    def weight_difference(brain_1, brain_2):
        """
        Calcule la différence de 'poids' entre deux cerveaux.
        """
        total_weight_difference = 0
        count = min(len(brain_1.connections), len(brain_2.connections))
        
        for i in range(0, count):
            total_weight_difference += abs(brain_1.connections[i].weight -
                                           brain_2.connections[i].weight)
        
        return total_weight_difference

    def add_to_species(self, player):
        """
        Ajoute un oiseau à cette catégorie.
        """
        self.players.append(player)

    def sort_players_by_fitness(self):
        """
        Trie les membres par performance et met à jour le champion.
        """
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        # Si le meilleur oiseau bat ou égale le record de l'espèce
        if self.players[0].fitness >= self.benchmark_fitness:
            if self.players[0].fitness > self.benchmark_fitness:
                self.staleness = 0 # On remet à zéro car il y a du progrès
                self.benchmark_fitness = self.players[0].fitness
                self.champion = self.players[0].clone()
                self.benchmark_brain = self.champion.brain.clone()
            else:
                self.staleness = 0 # On ne punit pas si on stagne au sommet
        else:
            self.staleness += 1 # On s'approche de l'extinction si pas de progrès

    def calculate_average_fitness(self):
        """
        Calcule la moyenne des scores de tous les membres.
        """
        total_fitness = 0
        for p in self.players:
            total_fitness += p.fitness
        if self.players:
            self.average_fitness = int(total_fitness / len(self.players))
        else:
            self.average_fitness = 0

    def offspring(self):
        """
        Crée un 'bébé' oiseau à partir d'un membre aléatoire de l'espèce.
        """
        baby = self.players[random.randint(1, len(self.players)) - 1].clone()
        baby.brain.mutate() # Le bébé est une version légèrement modifiée (mutation)
        return baby
