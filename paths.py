# Resolve o problema dos Path quando o peao é promovido a uma nova peça.
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

def get_asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)