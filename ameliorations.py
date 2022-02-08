from graphe import *
import os
import random
import argparse
import glob

# (a)
def charger_donnees (graphe, fichier) :
    # Nom du fichier
    f_nom = fichier.split('.')[0]
    with open(fichier, 'r') as f :
        for ligne in f :
            if ligne[0] == '#' :
                champ = ligne[2:-1]
            elif champ == 'stations' :
                # Si on est dans le champ du fichier qui contient l'id et le nom des stations
                station = ligne.split(':')
                station_id = int(station[0])
                station_nom = station[1][:-1]
                graphe.ajouter_sommet((station_id, station_nom))
            elif champ == 'connexions' :
                connexion = ligne.split('/')
                a = int(connexion[0])
                b = int(connexion[1])
                graphe.ajouter_arete(a, b, f_nom)
    
# (b)
def numerotation (graphe):
    debut = dict()
    parent = dict()
    ancetre = dict()
    instant = 0
    
    for sommet in graphe.sommets():
        parent[sommet] = None
        debut[sommet] = ancetre[sommet] = 0

    def numeroration_rec (sommet):
        nonlocal instant
        instant = instant + 1
        debut[sommet] = ancetre[sommet] = instant
        for t, _ in sorted(graphe.voisins(sommet)) :
            if debut[t] != 0:
                if parent[sommet] != t :
                    ancetre[sommet] = min(ancetre[sommet], debut[t])
            else:
                parent[t] = sommet
                numeroration_rec(t)
                ancetre[sommet] = min(ancetre[sommet], ancetre[t])
    
    for v in sorted(graphe.sommets()) :
        if debut[v] == 0 :
            numeroration_rec(v)

    return (debut, parent, ancetre)                
                
                
def points_articulation (reseau):
    debut, parent, ancetre = numerotation(reseau)
    articulations = set()
    racines = set()
    racines = {v for v in parent if parent[v] == None}
    
    for depart in racines:
        degre = reseau.degre(depart)
        for voisin, _ in reseau.voisins(depart):
            if parent[voisin] != depart:
                degre -= 1
        if degre >= 2:
            articulations.add(depart)
            
    racines.add(None)
    
    for sommet in reseau.sommets() :
        if not parent[sommet] in racines and ancetre[sommet] >= debut[parent[sommet]]:
            articulations.add(parent[sommet]) 
            
    return articulations


# (c)
def ponts (reseau):
    debut, parent, ancetre = numerotation(reseau)
    return [(parent[u], u) for u in parent if parent[u] != None and ancetre[u] > debut[parent[u]]]

# (d)
def amelioration_ponts (reseau):
    aretes = set()
    liste_feuilles = list()
    visite = dict()
    feuilles = set()
    pont = ponts(reseau)
    n = 0
    
    def est_traite (sommet):
        for u, v in pont:
            if u == sommet or v == sommet:
                return True
        return False

    def aux (depart, extremite) :
        visite[depart] = True
        feuille.add(depart)
        for voisin in reseau.voisins(depart) :
            if not visite[voisin[0]] and voisin[0] != extremite :
                if not est_traite(voisin[0]):
                    aux(voisin[0],extremite)
                else:
                    feuille.add(voisin[0])

    for u, v in pont:
        for i in range(2):
            feuille = set()
            for sommet in reseau.sommets():
                visite[sommet] = False
            aux(u,v)
            for sommet in feuille :
                if est_traite(sommet):
                    n += 1
            if n < 2:
                feuilles.add(tuple(feuille))
            n = 0
            a = u
            u = v
            v = a

    for element in feuilles:
        liste_feuilles.append(element)

    for i in range(len(liste_feuilles) - 1):
        a = random.choice(liste_feuilles[i])
        b = random.choice(liste_feuilles[i + 1])
        aretes.add((a, b))
    return aretes


# (e)
def amelioration_points_articulation (reseau):
    liste_points_articulations = list(points_articulation(reseau))
    liste_points_articulations_initial = liste_points_articulations.copy()
    debut, parent, ancetre = numerotation(reseau)
    visites = dict()
    voisins = list()
    aretes = set()
    racine = None

    def racine_sommet(sommet):
        def trouver_indice(sommet):
            i = 0
            for point, _ in reseau.voisins(sommet):
                if parent[point] == sommet and ancetre[point] >= debut[sommet] :
                    i += 1
            return i

        nonlocal racine
        if parent[sommet] is None:
            racine = sommet
        else:
            if sommet in liste_points_articulations and trouver_indice(sommet) < 2:
                visites[sommet] = True
                liste_points_articulations.remove(sommet)
            racine_sommet(parent[sommet])

    #############################################
    for point in liste_points_articulations:
        visites[point] = False
    
    #racines_articulations = [point for point in visites.values()]
    
    while not all(point for point in visites.values()):
        
        point = liste_points_articulations[0]
        for sommet in liste_points_articulations:
            if debut[sommet] > debut[point]:
                point = sommet
                
        if parent[point] is None:
            for voisin, _ in reseau.voisins(point):
                if  parent[voisin] == point:
                    voisins.append(voisin)
            for i in range(len(voisins) - 1):
                aretes.add((voisins[i],voisins[i + 1]))
            visites[point] = True
            liste_points_articulations.remove(point)
            
        else :
            racine_sommet(point)
            for voisin, _ in reseau.voisins(point):
                if not voisin in liste_points_articulations_initial and parent[voisin] == point and ancetre[voisin] >= debut[point]:
                    aretes.add((voisin, racine))
                if point in liste_points_articulations:
                    visites[point] = True
    return aretes

# Options

def option_liste_stations (reseau) :
    stations = [(reseau.nom_sommet(s), s) for s in reseau.sommets()]
    for station in sorted(stations):
        print(str(station[0]) + " (" + str(station[1]) + ")")

def option_articulations (reseau) :
    liste_points_articulations = list(points_articulation(reseau))

    print("Le reseau contient les " + str(len(liste_points_articulations)) + " points articulation suivants :")

    for i, sommet in enumerate(liste_points_articulations) : 
        liste_points_articulations[i] = reseau.nom_sommet(sommet)
    for i, station in enumerate(sorted(liste_points_articulations)) :
        print(str(i+1) + " : " + station)

def option_ponts (reseau):
    liste_ponts = list(ponts(reseau))
    
    print("Le reseau contient " + str(len(liste_ponts)) + " ponts suivants :")

    for i, sommets in enumerate(liste_ponts):
        sommets = sorted([reseau.nom_sommet(sommets[0]), reseau.nom_sommet(sommets[1])])
        liste_ponts[i] = str(sommets[0]) + " -- " + str(sommets[1])

    for pont in sorted(liste_ponts):
        print(pont)
        
def option_ameliorer_articulations(reseau):
    liste_points_articulations = list(amelioration_points_articulation(reseau))
    
    print("On peut rajouter les " + str(len(liste)) +  " arêtes suivantes afin de supprimer tout les points d'articulations :")

    for u, v in liste_points_articulations :  
        print(reseau.nom_sommet(u) + " -- " + reseau.nom_sommet(v))
        
def option_ameliorer_ponts(reseau):
    liste_ponts = list(amelioration_ponts(reseau))
    
    print("On peut rajouter les " + str(len(liste_ponts)) +  " arêtes suivantes afin de supprimer tout les ponts :")
    
    for u, v in liste_ponts:
        print(reseau.nom_sommet(u) + " -- " + reseau.nom_sommet(v))
        
def main () :
    import doctest
    """
    doctest.testfile('doctest_charger_donnees.txt')
    doctest.testfile('doctest_points_articulation.txt')
    doctest.testfile('doctest_ponts.txt')
    doctest.testfile('doctest_amelioration_ponts.txt')
    doctest.testfile('doctest_amelioration_points_articulation.txt')
    doctest.testfile('mes_tests.txt')
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--metro", help="La ligne de metro que l'on veut changer", nargs='*')
    parser.add_argument("--rer", help="La ligne de RER que l'on veut changer", nargs='*')
    parser.add_argument("--liste-stations", help="Afficher la liste des stations", action ='store_true')
    parser.add_argument("--articulations", help="Afficher la liste des articulations", action ='store_true')
    parser.add_argument("--ponts", help="Afficher la liste des ponts", action ='store_true')
    parser.add_argument("--ameliorer-articulations", help="Afficher les points d'articulations chargé et les arêtes à rajouter", action ='store_true')
    parser.add_argument("--ameliorer-ponts", help="Afficher les ponts chargé et les arêtes à rajouter", action ='store_true')
    args = parser.parse_args()
    
    reseau = Graphe()
    
    if args.metro or args.rer :
        if args.rer :
            print("Chargement des lignes {} de rer ... terminé.".format(args.metro))
            charger_donnees(reseau, "RER_{}.txt".format(args.metro[0]))
        
        if args.metro :
            print("Chargement des lignes {} de metro ... terminé.".format(args.metro))
            charger_donnees(reseau, "METRO_{}.txt".format(args.metro[0]))
            
    else :
        if args.rer is None :
            print("Chargement de toutes les lignes de rer ... terminé")
            for fichier in glob.iglob("RER*.txt") :
                charger_donnees(reseau, fichier)
        
        if args.metro is None :
            print("Chargement de toutes les lignes de rer ... terminé")
            for fichier in glob.iglob("METRO*.txt") :
                charger_donnees(reseau, fichier)

    sommets = reseau.nombre_sommets()
    aretes = reseau.nombre_aretes()
    
    print("Le réseau contient " + str(sommets) + " sommets et " + str(aretes) + " aretes")
    
    dict_fonctions = globals()

    for argument in vars(args):
        if getattr(args, argument):
            nom_fonction = 'option_' + argument
            if nom_fonction in dict_fonctions:
                dict_fonctions[nom_fonction](reseau)

if __name__ == "__main__":
    main()
