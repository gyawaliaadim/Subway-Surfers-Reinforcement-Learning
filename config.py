import os
BASE_DIR = os.getcwd()

coin_region = {
    'top': 268,
    'left': 1672,
    'width': 178,
    'height': 34
}
game_regions_path = os.path.abspath(os.path.join(
    BASE_DIR,
    "game_regions"
))

'''
Detecting Coins
'''
MATCH_THRESHOLD = 0.8
MIN_DISTANCE = 5
