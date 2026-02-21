import node
import connection
import random


class Brain:
    """
    Le 'cerveau' de l'oiseau, représenté par un réseau de neurones.
    """
    def __init__(self, inputs, clone=False):
        self.connections = [] # Liste des liens entre neurones
        self.nodes = []       # Liste des neurones
        self.inputs = inputs  # Nombre d'entrées (ce que l'oiseau voit)
        self.net = []         # Structure du réseau ordonnée pour le calcul
        self.layers = 2       # Nombre de couches (entrée et sortie par défaut)

        if not clone:
            # 1. Création des neurones d'entrée (Couche 0)
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
            
            # 2. Création du neurone de biais (toujours actif pour aider l'apprentissage)
            bias_id = self.inputs
            self.nodes.append(node.Node(bias_id))
            self.nodes[bias_id].layer = 0
            
            # 3. Création du neurone de sortie (Couche 1 : l'oiseau saute ou non)
            output_id = bias_id + 1
            self.nodes.append(node.Node(output_id))
            self.nodes[output_id].layer = 1

            # 4. Création des connexions initiales
            # On connecte chaque entrée et le biais au neurone de sortie avec un poids aléatoire
            for i in range(0, bias_id + 1):
                self.connections.append(connection.Connection(self.nodes[i],
                                                              self.nodes[output_id],
                                                              random.uniform(-1, 1)))

    def connect_nodes(self):
        """
        Établit les liens physiques entre les objets Node et Connection.
        """
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        for i in range(0, len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])

    def generate_net(self):
        """
        Organise les neurones par couche pour permettre le calcul du signal.
        """
        self.connect_nodes()
        self.net = []
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])

    def feed_forward(self, vision):
        """
        Calcule la décision de l'oiseau en fonction de ce qu'il voit.
        """
        # On donne les informations (vision) aux neurones d'entrée
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        # Le neurone de biais est toujours à 1
        self.nodes[self.inputs].output_value = 1

        # On active chaque neurone l'un après l'autre
        for i in range(0, len(self.net)):
            self.net[i].activate()

        # On récupère la valeur du dernier neurone (le neurone de sortie)
        output_node = self.nodes[-1]
        output_value = output_node.output_value

        # On réinitialise les entrées des neurones pour le prochain calcul
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0

        return output_value

    def clone(self):
        """
        Crée une copie identique du cerveau.
        """
        clone = Brain(self.inputs, True)

        # Copie des neurones
        for n in self.nodes:
            clone.nodes.append(n.clone())

        # Copie des connexions en les reliant aux nouveaux neurones correspondants
        for c in self.connections:
            clone.connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))

        clone.layers = self.layers
        clone.connect_nodes()
        return clone

    def getNode(self, id):
        """
        Trouve un neurone par son identifiant.
        """
        for n in self.nodes:
            if n.id == id:
                return n

    def mutate(self):
        """
        Apporte des modifications aléatoires pour explorer de nouvelles solutions.
        """
        # 80 % de chance qu'une mutation se produise
        if random.uniform(0, 1) < 0.8:
            for i in range(0, len(self.connections)):
                # 10% de chance pour chaque connexion d'être modifiée
                if random.uniform(0, 1) < 0.1:
                    self.connections[i].mutate_weight()
