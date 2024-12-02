# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import sys
import os

import sphinx_pdj_theme

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, pathlib.Path(__file__).parents[1].resolve().as_posix())
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../../src/compilation'))
sys.path.insert(0, os.path.abspath('../../src/compilation/amici_scripts'))
sys.path.insert(0, os.path.abspath('../../src/compilation/antimony_scripts'))
sys.path.insert(0, os.path.abspath('../../src/compilation/sbml_scripts'))
sys.path.insert(0, os.path.abspath('../../src/simulation'))
sys.path.insert(0, os.path.abspath('../../src/simulation/utils'))
sys.path.insert(0, os.path.abspath('../../src/utils'))
sys.path.insert(0, os.path.abspath('../../src/benchmarking'))
sys.path.insert(0, os.path.abspath('../../src/benchmarking/simulation'))
sys.path.insert(0, os.path.abspath('../../src/benchmarking/visualization'))
sys.path.insert(0, os.path.abspath('../../src/benchmarking/creation'))
sys.path.insert(0, os.path.abspath('../../src/benchmarking/sedml'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SPARCED'
copyright = '2024, The Birtwistle Lab'
author = 'The Birtwistle Lab'
release = '2.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',              # Use markdown in documentation
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]
autosummary_generate = True
source_suffix = {
    '.rst': 'restructuredtext',
    '.md' : 'markdown'
}

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_pdj_theme'
html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]
html_static_path = ['_static']
