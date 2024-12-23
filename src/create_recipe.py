import random

def probabilistic_node_selection(to_visit, k=5):
    """
    Sélectionne un nœud de manière probabiliste parmi les k meilleurs.

    :param to_visit: Liste des nœuds candidats [(pondération, nœud)]
    :param k: Nombre maximum de candidats à considérer
    :return: Nœud sélectionné
    """
    # Trier par pondération décroissante et prendre les k premiers
    top_candidates = sorted(to_visit, reverse=True, key=lambda x: x[0])[:k]

    # Extraire les pondérations et les nœuds
    weights = [candidate[0] for candidate in top_candidates]
    nodes = [candidate[1] for candidate in top_candidates]

    # Normaliser les pondérations pour en faire des probabilités
    total_weight = sum(weights)
    probabilities = [w / total_weight for w in weights]

    # Sélectionner un nœud de manière probabiliste
    chosen_node = random.choices(nodes, probabilities)[0]

    return chosen_node


def find_best_subgraph(G, start_ingredient, max_depth):
    """
    Parcourt le graphe pour trouver un sous-graphe maximisant la somme des pondérations des arêtes.

    :param G: Graphe NetworkX
    :param start_ingredient: Nom de l'ingrédient de départ
    :param max_depth: Nombre maximum d'ingrédients dans le sous-graphe
    :return: Liste des ingrédients et somme des pondérations
    """
    if start_ingredient not in G:
        raise ValueError(f"L'ingrédient '{start_ingredient}' n'existe pas dans le graphe.")

    visited = set()
    selected_edges = []
    total_weight = 0

    # Utilisation d'une liste pour trier les voisins par pondération
    to_visit = [(0, start_ingredient)]  # (weight, ingredient)

    while to_visit and len(visited) < max_depth:
        # Récupérer l'ingrédient avec la pondération maximale
        to_visit.sort(reverse=True, key=lambda x: x[0])
        weight, current = to_visit.pop(0)

        if current in visited:
            continue

        visited.add(current)
        total_weight += weight

        # Ajouter les voisins du nœud courant
        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                edge_weight = G[current][neighbor]["weight"]
                to_visit.append((edge_weight, neighbor))
                selected_edges.append((current, neighbor, edge_weight))

    return list(visited), total_weight


def find_best_subgraph_with_min_connections(G, start_ingredient, nb_ingredients=5, min_connections=1, min_weight=0.05, k=5):
    """
    Parcourt le graphe pour trouver un sous-graphe où chaque nœud est connecté à au moins n-1 nœuds existants.

    :param G: Graphe NetworkX
    :param start_ingredient: Nom de l'ingrédient de départ
    :param nb_ingredients: Nombre maximum d'ingrédients dans le sous-graphe
    :param min_connections: Nombre minimum de connexions nécessaires pour chaque nœud ajouté
    :param min_weight: Pondération minimale des arêtes
    :param k: Nombre maximum de voisins considérés pour le choix probabiliste
    :return: Liste des ingrédients et somme des pondérations
    """
    if start_ingredient not in G:
        raise ValueError(f"L'ingrédient '{start_ingredient}' n'existe pas dans le graphe.")

    visited = set()
    total_weight = 0
    to_visit = [(0, start_ingredient)]  # (poids, ingrédient)

    while to_visit and len(visited) < nb_ingredients:
        # Sélectionner un nœud de manière probabiliste parmi les k meilleurs
        
        if len(to_visit) == 1: # Si il reste un seul voisin, on le prend
            chosen_node = to_visit[0][1]
        else: 
            if len(to_visit) < k: # Si le nombre de voisins est inferieur a k, on prend le nombre de voisins
                k_bis = len(to_visit)
                chosen_node = probabilistic_node_selection(to_visit, k_bis)
            else: # Si le nombre de voisins est superieur ou egal a k, on prend k
                k_bis = k
                chosen_node = probabilistic_node_selection(to_visit, k_bis)
        to_visit = [(weight, node) for weight, node in to_visit if node != chosen_node]

        # Vérifier la contrainte de connexions
        connections = [neighbor for neighbor in visited if G.has_edge(chosen_node, neighbor) and G[chosen_node][neighbor]['weight'] >= min_weight]
        if len(connections) >= max(len(visited) - min_connections, 0):  # Au moins n-1 connexions si len(visited) >= 2
            visited.add(chosen_node)
            total_weight += sum(G[chosen_node][neighbor]['weight'] for neighbor in connections)

            # Ajouter les voisins du nœud courant à visiter
            for neighbor in G.neighbors(chosen_node):
                if neighbor not in visited:
                    edge_weight = G[chosen_node][neighbor]['weight']
                    to_visit.append((edge_weight, neighbor))

    return list(visited), total_weight
