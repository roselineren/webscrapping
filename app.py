import streamlit as st
import json

# Configurer la page pour utiliser le mode large
st.set_page_config(layout="wide")

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
.recipe-title {
    font-size:26px;
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





# Titre de la page avec le style personnalisé
st.markdown('<p class="big-font">Baby Recipe... YUMMY!</p>', unsafe_allow_html=True)

# Charger les données
with open('recettes.json', 'r', encoding='UTF-8') as f:
    recettes = json.load(f)



# Extraire les tags uniques
tags_uniques = set()
for recette in recettes:
    for tag in recette.get('tags', []):
        tags_uniques.add(tag)

# Créer des cases à cocher pour les tags dans la barre latérale
selected_tags = []
for tag in tags_uniques:
    if st.sidebar.checkbox(tag, key=tag):
        selected_tags.append(tag)
    else: recettes_filtrees = recettes

# Filtrer les recettes basées sur les tags sélectionnés
recettes_filtrees = [recette for recette in recettes if all(tag in recette.get('tags', []) for tag in selected_tags)]


# Créer des lignes avec 4 recettes chacune
for i in range(0, len(recettes_filtrees), 4):
    cols = st.columns(4)  # Crée 4 colonnes
    for j in range(4):
        if i + j < len(recettes_filtrees):
            with cols[j]:
                recette = recettes_filtrees[i + j]
                # Utilisation de HTML pour l'image
                st.markdown(f"<div class='img-container'><img src='{recette['url_image']}' alt='{recette['titre']}'></div>", unsafe_allow_html=True)
                
                # Titre de la recette avec style personnalisé
                st.markdown(f"<p class='recipe-title'>{recette['titre']}</p>", unsafe_allow_html=True)

                st.markdown(f"[Voir la recette]({recette['lien']})", unsafe_allow_html=True)
