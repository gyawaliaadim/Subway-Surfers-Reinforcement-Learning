import os
import cv2
from utilities.detect_coin_number import detect_coin_number


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.abspath(os.path.join(
BASE_DIR,
"..",
"game_regions",
"game_screen.jpg"
))
print(image_path)
# image_path = "C:\\Users\\gyawa\\GitHub\\Subway-Surfers-Reinforcement-Learning\\game_regions\\game_screen.jpg"  # Replace with your image path
img = cv2.imread(image_path)
print(detect_coin_number(img))