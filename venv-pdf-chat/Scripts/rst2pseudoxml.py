#!c:\Users\ashok\OneDrive\Ashok_personal\AAA_AWS_All_AI_ML_Projects_Ashok\1_AWS_Chat_PDF\Chat_with_pdf_Ashok_2\venv-pdf-chat\Scripts\python.exe

# $Id: rst2pseudoxml.py 8927 2022-01-03 23:50:05Z milde $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing pseudo-XML.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description


description = ('Generates pseudo-XML from standalone reStructuredText '
               'sources (for testing purposes).  ' + default_description)

publish_cmdline(description=description)
