"""
Web crawler module
"""

MONGO_DBNAME = 'webometrics'
MONGO_COLLECTION_LINKS = 'links'
MONGO_COLLECTION_OUTLINKS = 'outlinks'

RICH_FILES = {
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'pdf': 'application/pdf',
    'ps': 'application/postscript',
    'eps': 'application/postscript',
    'txt': 'text/plain'
}
