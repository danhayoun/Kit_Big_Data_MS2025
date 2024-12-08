# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'KIT_BIG_DATA_MS2025'
copyright = '2024, Cecile LI, Josephine BERNARD, Dan HAYOUN'
author = 'Cecile LI, Josephine BERNARD, Dan HAYOUN'
release = 'v1'

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.githubpages',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme', #pour traduire si on rédige la documentation dans une autre langue que l'anglais
] 

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'collapse_navigation': False,  # Permet de garder les menus étendus
    'sticky_navigation': True,     # La navigation reste visible en haut
    'navigation_depth': 4,         # Profondeur maximale du menu latéral
    'includehidden': True,         # Inclut les éléments cachés dans la navigation
    'titles_only': False,           # Affiche les titres et les sous-titres
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'version_selector': True,
    'language_selector': True,
}
