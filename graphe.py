class Graphe(object):
    def __init__(self):
        """Initialise un graphe sans arêtes"""
        self.dictionnaire = dict()
        self.dictionnaire_sommets = dict()

    def ajouter_arete(self, u, v, ligne):
        """Ajoute une arête entre les sommmets u et v, en créant les sommets
        manquants le cas échéant.        
        """
        # vérification de l'existence de u et v, et création(s) sinon
        if u not in self.dictionnaire:
            self.dictionnaire[u] = set()
        if v not in self.dictionnaire:
            self.dictionnaire[v] = set()
        # ajout de u (resp. v) parmi les voisins de v (resp. u)
        if u == v :
                self.dictionnaire[u].add((v, ligne))
        else :
                self.dictionnaire[u].add((v, ligne))
                self.dictionnaire[v].add((u, ligne))

    def ajouter_aretes(self, iterable):
        """Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple).
        """
        for u, v, ligne in iterable:
            self.ajouter_arete(u, v, ligne)

    def ajouter_sommet(self, sommet):
        """Ajoute un sommet (de n'importe quel type hashable) au graphe."""
        temp = list(sommet)
        self.dictionnaire_sommets[temp[0]] = temp[1]

    def ajouter_sommets(self, iterable):
        """Ajoute tous les sommets de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des éléments hashables."""
        for sommet in iterable:
            self.ajouter_sommet(sommet)

    def aretes(self):
        """Renvoie l'ensemble des arêtes du graphe. Une arête est représentée
        par un tuple (a, b, ligne) avec a <= b afin de permettre le renvoi de boucles et p le poids de l'arête.
        """
        return {tuple((u, v, ligne)) for u in self.dictionnaire for v, ligne in self.dictionnaire[u] if u <= v}
                                                                
    def contient_arete(self, u, v):
        """Renvoie True si l'arête {u, v} existe, False sinon.
        """
        if self.contient_sommet(u) and self.contient_sommet(v):
            return u in self.voisins(v)  # ou v in self.dictionnaire[u]
        return False

    def contient_sommet(self, u):
        """Renvoie True si le sommet u existe, False sinon."""
        return u in self.dictionnaire

    def nom_sommet(self, sommet):
        return self.dictionnaire_sommets[sommet]
        
    def degre(self, sommet):
        """Renvoie le nombre de voisins du sommet; s'il n'existe pas, provoque
        une erreur."""
        return len(self.dictionnaire[sommet])

    def nombre_aretes(self):
        """Renvoie le nombre d'arêtes du graphe."""
        return len(self.aretes())

    def nombre_sommets(self):
        """Renvoie le nombre de sommets du graphe."""
        return len(self.dictionnaire_sommets)  
                  
    def sommets(self):
        """Renvoie l'ensemble des sommets du graphe."""
        return set(self.dictionnaire_sommets.keys())

    def voisins(self, sommet):
        """Renvoie l'ensemble des voisins du sommet donné.
        """
        return {u for u in self.dictionnaire[sommet]}
