# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..','..' ,'..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..','..' ,'QuadScan')))
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..','..', 'SimFrame_fork', 'SimFrame')))
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..','..', 'VELA_CLARA_repository', 'Software', 'Utils',
                                  'MachineState')))
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..','..', 'VELA_CLARA_repository', 'catapillar-build',
                                  'PythonInterface', 'Release')))
sys.path.insert(0, os.path.abspath('.'))
from QuadScan.QuadScanclass import GeneralQuadScan
from QuadScan.virtualclarabeamsizes import BeamSizeDetermination
import machine_state
import CATAP.HardwareFactory


# -- Project information -----------------------------------------------------

project = 'Emittance_GUI'
copyright = '2020, H.M. Castaneda Cortes, D.J. Scott, A. Wolski, A. Brynes, M. King'
author = 'H.M. Castaneda Cortes, D.J. Scott, A. Wolski, A. Brynes, M. King'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram',
	'sphinx.ext.graphviz',
    'sphinx.ext.viewcode',
              'sphinx.ext.autosummary']


autodoc_docstring_signature = True
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'
inheritance_graph_attrs = dict(size='"40.0,20.0"',
                               fontsize=40, ratio='auto')
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = 'Emittance Measurement'
html_theme = 'agogo'
#html_logo = 'stfc_logo.png'
html_theme_options = {'bodyfont': "#6495ED", "headerfont": "#00008B", "bgcolor":"#483D8B"}
#html_theme_options = {"full_logo": "true", 'headingcolor': "#6495ED", "textcolor": "#00008B", "linkcolor":"#483D8B"}
#
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'EmittanceMeasurementsDocs '

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'SphinxTest.tex', u'SphinxTest Documentation',
     u'Hector', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'sphinxtest', u'SphinxTest Documentation',
     [author], 1)
]
autoclass_content = "both"
# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'SphinxTest', u'SphinxTest Documentation',
     author, 'SphinxTest', 'One line description of project.',
     'Miscellaneous'),
]

# -- Extension configuration -------------------------------------------------