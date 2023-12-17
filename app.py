import streamlit as st
import json

# Configurer la page pour utiliser le mode large
st.set_page_config(page_title='Baby Recipe... YUMMY!', page_icon='logo.png', layout="wide",
                   menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     })

# Style personnalisé pour le titre principal et les titres des recettes
st.markdown("""
<style>

.big-font {
    font-size:60px !important;
    font-family: Akaya Telivigala;
    font-weight: bold;
    color: #c46e28;
    text-align: center;
}
.recipe {
    font-size:40px;
    font-weight: bold;
    font-family: Akaya Telivigala;
    color: #c46e28;
}
.recipe-title {
    font-size:20px;
    font-weight: bold;
    color: #cca995;
    text-align: center;
}
.img-container img {
    width: 100%;  /* Prend toute la largeur de la colonne */
    height: 300px; /* Hauteur fixe pour toutes les images */
    object-fit: cover; /* Couvre la zone de l'image tout en conservant ses proportions */
}
</style>
""", unsafe_allow_html=True)

# Créer trois colonnes pour le logo, le titre et un espace vide
col1, col2, col3 = st.columns([1, 2, 1])

# Placer le logo dans la première colonne
with col1:
    st.image('logo.png', width=150)  

# Placer le titre au centre
with col2:
    st.markdown('<h1 style="text-align: center;">Baby Recipe... YUMMY!</h1>', unsafe_allow_html=True)


# Titre de la page avec le style personnalisé
#st.markdown('<p class="big-font">Baby Recipe... YUMMY!</p>', unsafe_allow_html=True)

# Charger les données
with open('recettes.json', 'r', encoding='UTF-8') as f:
    recettes = json.load(f)

# Extraire les tags uniques
tags_uniques = set()

# Extraction et classification des tags
tags_age_bebe = set()
tags_allergenes_regime = set()
tags_autres = set()

for recette in recettes:
    for tag in recette.get('tags', []):
        if "mois" in tag in tag:
            tags_age_bebe.add(tag)
        elif "sans" in tag or "vegan" in tag or "végétarien" in tag or "avec poisson" in tag or "avec viande" in tag:
            tags_allergenes_regime.add(tag)
        else:
            if ('Recettes' in tag or 'Gâteaux' in tag or 'Fruits' in tag or 'Biscuits' in tag ):
                tags_autres.add(tag)
           


#region Filtrage bare menu

# Titre pour les filtres dans la barre latérale
st.sidebar.title("Filtres")

# Barre de recherche
mot_cle_recherche = st.sidebar.text_input("Rechercher une recette")

# Affichage des filtres de tags triés
selected_tags = []
st.sidebar.subheader("Âge de Bébé")
for tag in sorted(tags_age_bebe):
    if st.sidebar.checkbox(tag, key=tag):
        selected_tags.append(tag)

st.sidebar.subheader("Allergènes et Régime Spécifique")
for tag in sorted(tags_allergenes_regime):
    if st.sidebar.checkbox(tag, key=tag):
        selected_tags.append(tag)

st.sidebar.subheader("Autres")
for tag in sorted(tags_autres):
    if st.sidebar.checkbox(tag, key=tag):
        selected_tags.append(tag)

# Filtrage des recettes
recettes_filtrees = [recette for recette in recettes if all(tag in recette.get('tags', []) for tag in selected_tags)]


# Filtrer les recettes basées sur le mot-clé et les tags sélectionnés
if mot_cle_recherche:
    recettes_filtrees = [recette for recette in recettes_filtrees 
                         if mot_cle_recherche.lower() in recette['titre'].lower() or 
                            any(mot_cle_recherche.lower() in ingredient.lower() 
                                for ingredient in recette.get('ingredients', []))]
#endregion 

st.markdown('<p class="recipe">Recettes</p>', unsafe_allow_html=True)

#region onglets page 
# Fonction pour nettoyer le nom du produit (enlever l'article)
def nettoyer_nom_produit(nom):
    # Liste des articles à enlever
    articles = ["Le ", "La ", "Les ", "L’"]
    for article in articles:
        if nom.startswith(article):
            return nom[len(article):]
    return nom

def charger_fruits_du_mois(mois):
    with open(f'{mois}_fruits.json', 'r', encoding='UTF-8') as f:
        return json.load(f)
    
# Vérifier si un aliment est dans la liste des ingrédients (méthode 'contains')
def contient_aliment(ingredients, aliment):
    return any(aliment.lower() in ingredient.lower() for ingredient in ingredients)

# Filtrer les recettes par produits de saison
def filtrer_recettes_par_produits(recettes, produits_de_saison):
    recettes_filtrees = []
    for recette in recettes:
        if any(contient_aliment(recette['ingredients'], nettoyer_nom_produit(produit)) for produit in produits_de_saison):
            recettes_filtrees.append(recette)
    return recettes_filtrees

#main, janvier, fevrier, mars, avril, mai, juin, juillet, aout, septembre, octobre, novembre, decembre = st.tabs(['Accueil', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'])

# Création des onglets pour chaque mois
onglets_mois = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
main, *onglets = st.tabs(['Accueil'] + onglets_mois)

with main :
    # Créer des lignes avec 4 recettes chacune
    for i in range(0, len(recettes_filtrees), 4):
        cols = st.columns(4)  # Crée 4 colonnes
        for j in range(4):
            if i + j < len(recettes_filtrees):
                with cols[j]:
                    recette = recettes_filtrees[i + j]
                    
                    # Créer un conteneur pour chaque recette
                    with st.container():
                        # Utilisation de HTML pour l'image avec une hauteur maximale
                        st.markdown(f"<div class='img-container' style='max-height: 200px; overflow:hidden'><img src='{recette['url_image']}' alt='{recette['titre']}'></div>", unsafe_allow_html=True)


                        # Conteneur pour le titre avec une hauteur fixe
                        st.markdown(f"<div style='height: 100px;'><p class='recipe-title'>{recette['titre']}</p></div>", unsafe_allow_html=True)
                    

                        # Expanders pour les détails de la recette
                        with st.expander("Voir plus"):
                            st.subheader("Ingrédients")
                            for ingredient in recette['ingredients']:
                                st.write(ingredient)
                            
                            st.subheader("Matériels")
                            for materiel in recette['materiel']:
                                st.write(materiel)
                            
                            st.subheader("Indications de Préparation")
                            st.write(recette['indication'])
                        
                        st.markdown(f"[Voir la recette]({recette['lien']})", unsafe_allow_html=True)

for mois, onglet in zip(onglets_mois, onglets):
    with onglet:
        # Charger les fruits de saison pour le mois
        fruits_de_saison = charger_fruits_du_mois(mois.lower())
        # Filtrer les recettes par ces fruits
        recettes_filtrees = filtrer_recettes_par_produits(recettes_filtrees, fruits_de_saison)
        
        # Afficher les recettes filtrées
        for i in range(0, len(recettes_filtrees), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(recettes_filtrees):
                    with cols[j]:
                        recette = recettes_filtrees[i + j]
                        # Créer un conteneur pour chaque recette
                        with st.container():
                            # Utilisation de HTML pour l'image avec une hauteur maximale
                            st.markdown(f"<div class='img-container' style='max-height: 200px; overflow:hidden'><img src='{recette['url_image']}' alt='{recette['titre']}'></div>", unsafe_allow_html=True)


                            # Conteneur pour le titre avec une hauteur fixe
                            st.markdown(f"<div style='height: 100px;'><p class='recipe-title'>{recette['titre']}</p></div>", unsafe_allow_html=True)
                        

                            # Expanders pour les détails de la recette
                            with st.expander("Voir plus"):
                                st.subheader("Ingrédients")
                                for ingredient in recette['ingredients']:
                                    st.write(ingredient)
                                
                                st.subheader("Matériels")
                                for materiel in recette['materiel']:
                                    st.write(materiel)
                                
                                st.subheader("Indications de Préparation")
                                st.write(recette['indication'])
                            
                            st.markdown(f"[Voir la recette]({recette['lien']})", unsafe_allow_html=True)

#endregion
