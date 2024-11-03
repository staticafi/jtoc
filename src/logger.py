import logging
import sys

sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))

logger = logging.getLogger('jtoc')
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)
