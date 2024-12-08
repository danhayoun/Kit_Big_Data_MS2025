# Kit_Big_Data_MS2025

## Description

Ce projet est une application d'analyse de données développée en Python avec Streamlit comme front-end. Il permet de visualiser, analyser et interpréter des données de manière interactive.

## Installation

1. **Cloner le dépôt :**
    ```bash
    git clone https://github.com/danhayoun/Kit_Big_Data_MS2025.git
    cd Kit_Big_Data_MS2025
    ```

2. **Télécharger poetry :**
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. **Installer les dépendances :**
    
    Si vous avez installé poetry :
    ```bash
    poetry install
    ```
    Sinon :
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

## Utilisation

Pour lancer l'application Streamlit :
Avec poetry :
```bash
poetry run streamlit run app/main.py
```
Sinon :
```bash
streamlit run app/main.py
```