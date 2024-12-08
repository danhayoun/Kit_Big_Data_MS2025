.. KIT_BIG_DATA_MS2025 documentation master file, created by
   sphinx-quickstart on Tue Dec  3 19:44:55 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

KIT_BIG_DATA_MS 2025
====================

Voir la section :ref:`Présentation du Projet <presentation>` pour plus de détails.

Pour les instructions d'installation, consultez la section :ref:`Installation <installation>`.

La documentation de l'API est disponible dans la section :ref:`API Documentation <API_doc>`.

.. _presentation:

Présentation du Projet
----------------------
Bienvenue dans la documentation du projet KIT_BIG_DATA_MS2025. Ce projet est conçu pour faire une analyse du jeu de données provenant de Kaggle pour un projet de Telecom Paris visant à produire une Web App avec Streamlit.

.. _installation:

Installation
------------
Pour installer ce projet, suivez les étapes ci-dessous :

.. code-block:: bash
   curl -sSL https://install.python-poetry.org | python3 -
   export PATH=\"$HOME/.local/bin:$PATH\"
   poetry install

Utilisation
------------
Pour lancer l'application Streamlit :
Avec poetry :

.. code-block:: bash
   poetry run streamlit run Frontend/Accueil.py

Sinon :

.. code-block:: bash
   streamlit run Frontend/Accueil.py

.. Hidden TOCs

.. toctree::
   :maxdepth: 2
   :caption: Présentation 

   self

.. toctree::
   :maxdepth: 2
   :caption: Documentation 

   API_doc

.. toctree::
   :maxdepth: 2
   :caption: Index 

   genindex
   modindex