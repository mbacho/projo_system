"""
Web crawler module
"""

MONGO_DBNAME = 'webometrics'
MONGO_COLLECTION_LINKS = 'links'
MONGO_COLLECTION_OUTLINKS = 'outlinks'

RICH_FILES = {
    'doc': 'application/msword',
    'docx': '',
    'odt': 'application/vnd.oasis.opendocument.text	',
    'pdf': 'application/pdf',
    'ps': 'application/postscript',
    'eps': 'application/postscript',
    'txt': 'text/plain'
}
