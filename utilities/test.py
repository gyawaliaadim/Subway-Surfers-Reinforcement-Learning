import cv2
import os

# =========================
# INPUTS
# =========================

current_dir = os.path.dirname(os.path.abspath(__file__))

template_path = os.path.join(
    current_dir,
    "..",
    "game_regions",
    "cropped_police.jpg"
)

screenshot_path = os.path.join(
    current_dir,
    "..",
    "game_regions",
    "police.jpg"
)

REGION = {
    'top': 569,
    'left': 362,
    'width': 1173,
    'height': 454
}

GOOD_MATCH_THRESHOLD = 20

# =========================
# LOAD IMAGES
# =========================

template = cv2.imread(template_path)
screenshot = cv2.imread(screenshot_path)

if template is None:
    print("Failed to load template image")
    exit()

if screenshot is None:
    print("Failed to load screenshot")
    exit()

# =========================
# CROP SEARCH REGION
# =========================

x = REGION["left"]
y = REGION["top"]
w = REGION["width"]
h = REGION["height"]

search_region = screenshot[y:y+h, x:x+w]

# =========================
# CONVERT TO GRAYSCALE
# =========================

template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
search_gray = cv2.cvtColor(search_region, cv2.COLOR_BGR2GRAY)

# =========================
# ORB FEATURES
# =========================

orb = cv2.ORB_create(nfeatures=2000)

kp1, des1 = orb.detectAndCompute(template_gray, None)
kp2, des2 = orb.detectAndCompute(search_gray, None)

if des1 is None:
    print("No features found in template")
    exit()

if des2 is None:
    print("No features found in search region")
    exit()

# =========================
# FEATURE MATCHING
# =========================

bf = cv2.BFMatcher(cv2.NORM_HAMMING)

matches = bf.knnMatch(des1, des2, k=2)

good_matches = []

for pair in matches:
    if len(pair) != 2:
        continue

    m, n = pair

    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# =========================
# RESULTS
# =========================

print(f"Keypoints in template: {len(kp1)}")
print(f"Keypoints in region: {len(kp2)}")
print(f"Good matches: {len(good_matches)}")

found = len(good_matches) >= GOOD_MATCH_THRESHOLD

print("Found:", found)

# =========================
# VISUALIZE MATCHES
# =========================

match_img = cv2.drawMatches(
    template,
    kp1,
    search_region,
    kp2,
    good_matches[:50],
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

cv2.imshow("ORB Matches", match_img)
cv2.waitKey(0)
cv2.destroyAllWindows()