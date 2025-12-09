project = 'PUFFIN'
copyright = '2025, Luke Keyte'
author = 'Luke Keyte'
release = '1.0'
version = '1.0'

extensions = [
    'myst_parser',
    'sphinx.ext.mathjax'
]

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "colon_fence"
]

myst_update_mathjax = False

# Specify the master document
master_doc = 'index'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
    'logo_only': True,
    'display_version': False,
}

html_static_path = ['_static']
html_css_files = ['custom.css']
html_logo = '_static/puffin_logo_v2.png'

# Enable numbering for headers
myst_heading_anchors = 3