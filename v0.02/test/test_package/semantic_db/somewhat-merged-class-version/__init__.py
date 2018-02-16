# import our classes:
from semantic_db.objects import *
from semantic_db.context import *
from semantic_db.sigmoids import *
from semantic_db.functions import *
#from semantic_db.processor import *
from semantic_db.processor import process_sw_file, extract_compound_sequence
from semantic_db.misc import *

# set up logging:
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger()





