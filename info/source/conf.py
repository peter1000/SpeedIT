#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Documentation build configuration file..
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this file.
#

# -- General configuration ------------------------------------------------


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'peter1000 Projects General Info'
copyright = '2014, `peter1000` https://github.com/peter1000'


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '_templates']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
   "bodyfont": "Arial, sans-serif",
   "headfont": "Arial, sans-serif"
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = 'img/peter1000.png'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr'
html_search_language = 'en'

# Output file base name for HTML help builder.
htmlhelp_basename = 'SpeedITdoc'
