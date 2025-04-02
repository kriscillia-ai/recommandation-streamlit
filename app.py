import streamlit as st
import requests
import numpy as np

# Configuration
st.set_page_config(page_title="Recommandation", layout="wide")
st.title("📚 Système de Recommandation")

# URL Azure (à adapter)
AZURE_FUNCTION_URL = "https://recommandationappv1.azurewebsites.net"

# Entrée utilisateur
user_input = st.text_input(
    "Entrez un ID utilisateur (ex: 5, 8, 10, etc.)",
    placeholder="Exemple : 5",
    key="user_input"
)

if st.button("Générer les recommandations"):
    if user_input:
        try:
            # Conversion en int natif uniquement
            user_id = int(user_input.strip())  # Pas de np.int64 ici
            
            # Appel Azure avec payload en int standard
            response = requests.post(
                AZURE_FUNCTION_URL,
                json={"user_id": user_id}  # Envoi en int natif
            )
            
            # Gestion des réponses
            if response.status_code == 200:
                data = response.json()
                st.success(f"Recommandations pour {data['user_id']}:")
                for idx, rec in enumerate(data['recommendations'], 1):
                    st.markdown(f"**#{idx}** : Article `{rec['article_id']}` (score: {rec['score']:.2f})")
            
            elif response.status_code == 404:
                st.error(f"ID {user_input} non trouvé. Essayer : 5, 8, 10, etc.")
            
            else:
                st.error(f"Erreur serveur : {response.text}")
        
        except ValueError:
            st.error("Format invalide : entrez uniquement des chiffres (ex: 5)")
        except Exception as e:
            st.error(f"Erreur de connexion : {str(e)}")
    else:
        st.warning("Veuillez saisir un identifiant")
