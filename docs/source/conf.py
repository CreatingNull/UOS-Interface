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
from re import match
from unittest import mock

sys.path.insert(0, os.path.abspath("../../src"))
from uosinterface import __version__  # noqa: E402

# Mock Scrypt because of its OpenSSL OS dependency.
MOCKED_MODULES = ["hashlib.scrypt"]
for module_name in MOCKED_MODULES:
    sys.modules[module_name] = mock.Mock()


# -- Project information -----------------------------------------------------

project = "UOS Interface"
copyright = "2021, Steve Richardson"
author = "Steve Richardson"

# The short MAJOR.MINOR version.
version = match(r"^[\d].[\d]", __version__).group(0)
# The full version, including alpha/beta/rc tags.
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc"]
master_doc = "index"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = "../../resources/UOSLogoSmall.png"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
