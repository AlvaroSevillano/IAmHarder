import sys

from iamharder import IAmHarder
import logging

logging.basicConfig(filemode='w', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

name = sys.argv[1]
is_dev = int(sys.argv[2])

from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
if not is_dev:
    display.start()

IAmHarder(name, is_dev)