import logging
import sys

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

SOURCE_DIR = ROOT / 'src'
TEST_DIR = ROOT / 'tests'
JBMC = SOURCE_DIR / 'jbmc' / 'jbmc'
CAPTURE_DIR = SOURCE_DIR / 'capture'
COMPILE_DIR = SOURCE_DIR / 'build'

INDENT_WIDTH = 4

CAPTURE_DIR.mkdir(exist_ok=True)
COMPILE_DIR.mkdir(exist_ok=True)


sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))

logger = logging.getLogger('jtoc')
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)
