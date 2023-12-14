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
print (tags_uniques)

# Barre de recherche
mot_cle_recherche = st.sidebar.text_input("Rechercher une recette")

# Titre pour les filtres dans la barre latérale
st.sidebar.title("Filtres")

# Option pour afficher/masquer le titre "Menu"
afficher_menu = st.sidebar.checkbox("Afficher le titre Menu", value=True)

# Afficher le titre "Menu" sur la page principale si l'option est activée
if afficher_menu:
    st.title("Recette")

# Créer des cases à cocher pour les tags dans la barre latérale
selected_tags = []
for tag in tags_uniques:
    if st.sidebar.checkbox(tag, key=tag):
        selected_tags.append(tag)
    else: recettes_filtrees = recettes

# Filtrer les recettes basées sur les tags sélectionnés
recettes_filtrees = [recette for recette in recettes if all(tag in recette.get('tags', []) for tag in selected_tags)]


# Filtrer les recettes basées sur le mot-clé et les tags sélectionnés

if mot_cle_recherche:
    recettes_filtrees = [recette for recette in recettes_filtrees 
                         if mot_cle_recherche.lower() in recette['titre'].lower() or 
                            any(mot_cle_recherche.lower() in ingredient.lower() 
                                for ingredient in recette.get('ingredients', []))]




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