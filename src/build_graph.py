import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Charger le dataset
def load_data(file_path):
    """
    Charge le dataset CSV contenant les recettes.

    :param file_path: Chemin vers le fichier CSV contenant les recettes
    :return: DataFrame pandas
    """
    return pd.read_csv(file_path)

# Construire le graphe
def build_graph(data):
    """
    Construit un graphe non orienté pondéré à partir des ingrédients des recettes.

    :param data: DataFrame contenant les colonnes des ingrédients
    :return: Graphe NetworkX
    """
    G = nx.Graph()

    for _, row in data.iterrows():
        # Extraire les colonnes des ingrédients
        ingredients = [
            row[f"ingredient-{i}"] for i in range(1, 7)
            if pd.notna(row[f"ingredient-{i}"])
        ]

        # Ajouter des arêtes entre tous les ingrédients de la recette
        for i in range(len(ingredients)):
            for j in range(i + 1, len(ingredients)):
                ingredient_a, ingredient_b = ingredients[i], ingredients[j]

                # Si l'arête existe déjà, augmenter son poids
                if G.has_edge(ingredient_a, ingredient_b):
                    G[ingredient_a][ingredient_b]["weight"] += 1
                else:
                    G.add_edge(ingredient_a, ingredient_b, weight=1)

    return G
def adjust_weights_relative(G):
    """
    Ajuste les pondérations du graphe en fonction de la somme des connexions des nœuds.

    :param G: Graphe NetworkX
    """
    for u, v, data in G.edges(data=True):
        total_weight_u = sum(d['weight'] for _, _, d in G.edges(u, data=True))
        total_weight_v = sum(d['weight'] for _, _, d in G.edges(v, data=True))
        data['weight'] /= (total_weight_u + total_weight_v)
    print("Pondérations ajustées en fonction des connexions relatives.")

def adjust_weights_with_centrality(G):
    """
    Ajuste les pondérations du graphe en fonction de la centralité des nœuds.

    :param G: Graphe NetworkX
    """
    centrality = nx.degree_centrality(G)
    for u, v, data in G.edges(data=True):
        centrality_u = centrality[u]
        centrality_v = centrality[v]
        data['weight'] /= (1 + centrality_u + centrality_v)
    print("Pondérations ajustées avec centralité.")

def adjust_weights_with_rarity(G):
    """
    Ajuste les pondérations du graphe en favorisant les arêtes rares.

    :param G: Graphe NetworkX
    """
    for u, v, data in G.edges(data=True):
        rarity_factor = 1 / (len(list(G.edges(u))) + len(list(G.edges(v))))
        data['weight'] *= rarity_factor
    print("Pondérations ajustées pour favoriser les arêtes rares.")


# Visualiser le graphe
def visualize_graph(G):
    """
    Visualise le graphe avec les poids des arêtes.

    :param G: Graphe NetworkX
    """
    pos = nx.spring_layout(G)  # Disposition des nœuds
    
    # Dessiner les nœuds
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

    # Dessiner les arêtes avec leurs poids
    edges = G.edges(data=True) # Liste des arêtes avec les attributs
    nx.draw_networkx_edges( 
        G, pos,
        edgelist=[(u, v) for u, v, d in edges], # Liste des arêtes
        width=[d['weight'] for _, _, d in edges], # Largeur des arêtes
        alpha=0.999 # Transparence
    )

    # Ajouter des étiquettes
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

    # Poids des arêtes (2 chiffres après la virgule)
    edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Graphe des Ingrédients pour Cocktails")
    plt.show()


