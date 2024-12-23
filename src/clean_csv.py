import csv

def normalize_and_trim(value):
    """
    Normalise une chaîne en supprimant les espaces avant et après, et en la mettant en minuscule.
    :param value: Chaîne à normaliser
    :return: Chaîne normalisée
    """
    if isinstance(value, str):
        return value.strip().lower()
    return value

def remove_columns_csv(input_file, output_file, columns_to_keep):
    """
    Supprime les colonnes inutiles d'un fichier CSV, normalise les valeurs et enregistre le résultat dans un nouveau fichier.

    :param input_file: Chemin du fichier CSV d'entrée.
    :param output_file: Chemin du fichier CSV de sortie.
    :param columns_to_keep: Liste des colonnes à conserver dans le fichier de sortie.
    """
    try:
        # Lire le fichier d'entrée
        with open(input_file, mode='r', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)

            # Filtrer les colonnes à conserver
            filtered_columns = [col for col in columns_to_keep if col in reader.fieldnames]

            # Vérifier que toutes les colonnes à conserver sont présentes
            missing_columns = set(columns_to_keep) - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(f"Colonnes manquantes dans le fichier d'entrée : {missing_columns}")

            # Ouvrir le fichier de sortie
            with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=filtered_columns)
                writer.writeheader()

                # Écrire uniquement les colonnes filtrées et normaliser les valeurs
                for row in reader:
                    filtered_row = {col: normalize_and_trim(row[col]) for col in filtered_columns}
                    writer.writerow(filtered_row)

        print(f"Fichier nettoyé enregistré avec succès sous : {output_file}")

    except Exception as e:
        print(f"Erreur lors du nettoyage du fichier CSV : {e}")

if __name__ == "__main__":
    # Exemple d'utilisation
    input_file = "data/mr-boston-flattened.csv"  # Remplace par le chemin de ton fichier
    output_file = "data/mr-boston-flattened_cleaned.csv"  # Chemin du fichier de sortie
    columns_to_keep = [
        "name", "category", "measurement-1", "ingredient-1", "measurement-2", "ingredient-2", 
        "measurement-3", "ingredient-3", "measurement-4", "ingredient-4", "measurement-5", 
        "ingredient-5", "measurement-6", "ingredient-6", "glass"
    ]

    remove_columns_csv(input_file, output_file, columns_to_keep)
