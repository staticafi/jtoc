import logging
import sys

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

JBMC = ROOT / 'jbmc' / 'jbmc'
CAPTURE_DIR = ROOT / 'capture'
TEST_DIR = ROOT / 'tests'
SOURCE_DIR = ROOT / 'src'
COMPILE_DIR = ROOT / 'build'

INDENT_WIDTH = 4


sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))

logger = logging.getLogger('jtoc')
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)
