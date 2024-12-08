import streamlit as st




st.set_page_config(page_title="Accueil", page_icon="🏠")




image_path = "Images/aliments-confinement.jpg"

st.image(image_path,width=1200,use_container_width=False)

st.title("Bienvenue sur l'application ")
st.write("Nos plus grands experts se sont réunis pour analyser VOS données, provenant de mangetamain !")
st.write("Quelles recettes ont marqué les tendances ? Quelle saison cuisine-t-on le plus ?")
st.write("tant de questions dont vous pourrez trouvez les réponses dans notre étude !")

st.write("nous nous somme notamment attardés sur une analyse des saisons. Nous avons trouvé cet axe assez pertinent")

st.write("notre site se décompose en 3 pages : une pour l'analyse des temps de cuisson, par rapport à la saison.")
st.write("une par rapport aux techniques de cuisine utilisées, en fonction de la saison")
st.write("et une dernière page, plus insolite, regroupant divers observations remarquables que nous pouvons faire sur le jeu de données")

st.write("Ci-dessous, vous retrouverez des explications sur la méthodologie employée lors de cette étude")

st.write("Nous avons commencé par un pré-traitement des données")

