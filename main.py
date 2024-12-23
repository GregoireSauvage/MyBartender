from src.build_graph import load_data, build_graph, visualize_graph, adjust_weights_relative
from src.create_recipe import find_best_subgraph_with_min_connections



if __name__ == "__main__":
    # Chemin vers le fichier CSV
    file_path = "data/mr-boston-flattened_cleaned.csv"  # Remplace par ton fichier

    # Charger les données
    data = load_data(file_path)

    # On garde que les 200 premières lignes du dataset pour des raisons de performance
    #data = data[:200]
    
    # Construire le graphe
    G = build_graph(data)

    # Normaliser les pondérations du graphe
    adjust_weights_relative(G)

    # Visualiser le graphe
    #visualize_graph(G)

    # Trouver un sous-graphe optimisé à partir d'un ingrédient
    start_ingredient = "vodka"  # Ingrédient de départ pour le sous-graphe
    nb_ingredients = 5          # Limite du nombre d'ingrédients
    min_connections = 2         # Le nom est trompeur : permet de calculer le nombre de connexions minimales avec k > n - min_connections
    min_weight = 0.02           # Pondération minimale des arêtes
    k = 5                        # Nombre maximum de voisins considérés pour le choix probabiliste des ingrédients (k = 1 pour le choix déterministe, k > 1 pour le choix probabiliste)
    
    best_subgraph, total_weight = find_best_subgraph_with_min_connections(G, start_ingredient, nb_ingredients, min_connections, min_weight)    
    print(f"Recette trouvée à partir de '{start_ingredient}' : {best_subgraph}")
    print(f"Somme des pondérations : {total_weight}")

    # Visualiser le sous-graphe
    subgraph = G.subgraph(best_subgraph)
    visualize_graph(subgraph)