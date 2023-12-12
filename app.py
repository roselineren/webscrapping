# %%
# ! pip install streamlit


# %%
import streamlit as st
import json

# Charger les données
with open('recettes.json', 'r', encoding='UTF-8') as f:
    recettes = json.load(f)

# Afficher les recettes
for recette in recettes:
    st.image(recette['url_image'], width=150)
    st.write(recette['titre'])

    st.markdown(f"[Voir la recette]({recette['lien']})")

# %%



