import streamlit as st




st.set_page_config(page_title="Accueil", page_icon="🏠")




image_path = "./data/images/aliments-confinement.jpg"

st.image(image_path,width=1200,use_container_width=False)

# Texte multicolore
st.markdown(
    """
    <h1 style="font-size:60px; font-weight:bold; text-align:center;">
        <span style="color:red;">S</span>
        <span style="color:orange;">a</span>
        <span style="color:yellow;">v</span>
        <span style="color:green;">o</span>
        <span style="color:blue;">r</span>
        <span style="color:purple;">S</span>
        <span style="color:teal;">t</span>
        <span style="color:indigo;">a</span>
        <span style="color:violet;">t</span>
        <span style="color:pink;">s</span>
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="font-size:20px; font-style:italic; text-align:center;">
        Allie saveurs et statistiques
    </p>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
        .custom-container {
            background-color: #f9f9f9; 
            border-radius: 10px; 
            padding: 20px; 
            margin: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .custom-title {
            font-size: 24px; 
            font-weight: bold; 
            text-align: center; 
            color: #2c3e50;
        }
        .custom-text {
            font-size: 18px; 
            line-height: 1.6; 
            text-align: justify;
            font-family: 'Georgia', serif;
        }
        .custom-section-title {
            font-size: 20px; 
            font-weight: bold; 
            color: #16a085; 
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Conteneur principal
st.markdown('<div class="custom-container">', unsafe_allow_html=True)

# Titre principal
st.markdown('<div class="custom-title">Nos plus grands experts se sont réunis pour analyser VOS données, provenant de Mangetamain !</div>', unsafe_allow_html=True)

# Texte principal
st.write("\n")
st.markdown(
    """
    <div class="custom-text">
        <p>🌟 Quelles recettes ont marqué les tendances ? 
        <p>🌟 Quelle saison cuisine-t-on le plus ?</p>
        <p>Tant de questions dont vous pourrez trouver les réponses dans notre étude ! 📊✨</p>
        <p>Nous nous sommes notamment concentrés sur une analyse des saisons. Nous avons trouvé cet axe assez pertinent.</p>
        <p class="custom-section-title">Notre site se décompose en 3 pages :</p>
        <ul>
            <li>Une pour l'analyse des <strong>temps de cuisson</strong>, par rapport à la saison.</li>
            <li>Une par rapport aux <strong>techniques de cuisine</strong> utilisées, en fonction de la saison.</li>
            <li>Et une dernière page, plus insolite, regroupant diverses observations remarquables que nous pouvons faire sur le jeu de données.</li>
        </ul>
        <p>✏️Vous retrouverez des explications sur la méthodologie employée lors de cette étude dans la page commentaires.</p>
        <p>Nous avons commencé par un pré-traitement des données, expliqué à la page <strong>fun_facts</strong>.</p>
    </div>
    """,
    unsafe_allow_html=True
)

image_path_1 = "./data/images/image_accueil_1.jpg"
image_path_2 = "./data/images/image_accueil_2.jpg"
# Ajout d'images décoratives (exemple : des images alignées à gauche et à droite)
col1, col2 = st.columns(2)
with col1:
    st.image(image_path_1)
with col2:
    st.image(image_path_2)

# Fin du conteneur principal