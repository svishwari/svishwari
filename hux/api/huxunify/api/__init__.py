"""
Purpose of this sub-folder is to store any api modules
"""

import logging

# disable faker logs, unless error
logging.getLogger("faker").setLevel(logging.ERROR)
