import cv2
import os

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.getcwd()

image_path = os.path.abspath(os.path.join(
    BASE_DIR,
    "..",
    "game_regions",
    "game_screen.jpg"
))

numbers_path = os.path.abspath(os.path.join(
    BASE_DIR,
    "..",
    "game_regions",
    "numbers"
))

# ----------------------------
# Coin region
# ----------------------------
coin_region = {
    "top": 268,
    "left": 1672,
    "width": 178,
    "height": 34
}

# ----------------------------
# Load image
# ----------------------------
img = cv2.imread(image_path)

if img is None:
    raise FileNotFoundError(image_path)

# Crop
x = coin_region["left"]
y = coin_region["top"]
w = coin_region["width"]
h = coin_region["height"]

cropped = img[y:y+h, x:x+w]

# Convert to grayscale
gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

# Threshold
_, gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Uncomment to see what is being matched
cv2.imshow("Coin Region", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ----------------------------
# Template matching
# ----------------------------
matches_found = []

for digit in range(10):

    template_path = os.path.join(numbers_path, f"{digit}.png")
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if template is None:
        print(f"Missing template: {template_path}")
        continue

    _, template = cv2.threshold(template, 128, 255, cv2.THRESH_BINARY)

    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.95

    ys, xs = (result >= threshold).nonzero()

    for x in xs:
        matches_found.append((x, str(digit)))

# ----------------------------
# Remove duplicate detections
# ----------------------------
matches_found.sort()

filtered = []

min_distance = 5

for x, digit in matches_found:
    if not filtered or x - filtered[-1][0] > min_distance:
        filtered.append((x, digit))

number = "".join(d for _, d in filtered)

print("Matches:", filtered)
print("Detected number:", number)