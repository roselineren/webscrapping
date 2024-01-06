import requests
import re

def obtenir_empreinte_carbone_ingredient(ingredient):
    url = "https://data.ademe.fr/data-fair/api/v1/datasets/agribalyse-31-detail-par-ingredient/metric_agg"
    params = {
        'metric': 'avg',
        'field': 'Changement_climatique',
        'q': ingredient
    }
    try:
        reponse = requests.get(url, params=params)
        if reponse.status_code == 200 and reponse.json():
            data = reponse.json()
            if 'metric' in data:
                return data['metric']
    except requests.RequestException as e:
        print(f"Erreur lors de l'appel de l'API : {e}")
    return 0  # Retourne 0 si l'ingrédient n'est pas trouvé ou en cas d'erreur

def calculer_empreinte_recette(ingredients):
    empreinte_totale = 0
    for ingredient in ingredients:
        empreinte = obtenir_empreinte_carbone_ingredient(ingredient)
        empreinte_totale += empreinte
    return empreinte_totale

# Exemple d'utilisation
ingredients_recette = ['carotte', 'patate douce', 'oignon']  # Liste des ingrédients de la recette
empreinte_recette = calculer_empreinte_recette(ingredients_recette)
print(f"L'empreinte carbone totale de la recette est : {empreinte_recette} kgCO2e/kg")

def nettoyer_ingredients(ingredients):
    ingredients_nettoyes = []
    for ingredient in ingredients:
        # Supprimer les caractères non alphabétiques et les chiffres
        ingredient_nettoye = re.sub(r'[^A-Za-zéèàêâôûùïüçÔÄËÏÜÇÉÈÀÊÂÛÙ ]+', '', ingredient)
        # Supprimer les espaces supplémentaires
        ingredient_nettoye = re.sub(r'\s+', ' ', ingredient_nettoye).strip()
        ingredients_nettoyes.append(ingredient_nettoye)
    return ingredients_nettoyes

# Exemple d'utilisation
ingredients = [
    "▢ 2 banane(s) (bien mûres, environ 250g épluchées)",
    "▢ 125 g farine",
    "▢ 100 mL lait (vache, amande, riz, au choix)",
    "▢ 1 c. à café huile(s) végétale(s)"
]

ingredients_nettoyes = nettoyer_ingredients(ingredients)
print(ingredients_nettoyes)