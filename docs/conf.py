import os
import sys
from datetime import datetime

# Ensure the package can be imported for autodoc
sys.path.insert(0, os.path.abspath("../src"))

project = "pdf-unlocker"
author = "Abhisek-Ashirbad"

try:
    from pdf_unlocker._version import version as release
except Exception:
    release = "0.0.0"

copyright = f"{datetime.now().year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = ["_static"]
