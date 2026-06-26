import cv2
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

template_path = os.path.join(
    current_dir, "..", "game_regions", "cropped_police.jpg"
)

screenshot_path = os.path.join(
    current_dir, "..", "game_regions", "police.jpg"
)

REGION = {
    'top': 569,
    'left': 362,
    'width': 1173,
    'height': 454
}

THRESHOLD = 0.5

# Load images
template = cv2.imread(template_path)
screenshot = cv2.imread(screenshot_path)

if template is None or screenshot is None:
    print("Error loading images")
    exit()

# Crop search region from screenshot
x = REGION['left']
y = REGION['top']
w = REGION['width']
h = REGION['height']

search_region = screenshot[y:y+h, x:x+w]

# Template matching
result = cv2.matchTemplate(
    search_region,
    template,
    cv2.TM_CCOEFF_NORMED
)

_, max_val, _, max_loc = cv2.minMaxLoc(result)

print("Best similarity:", max_val)

found = max_val >= THRESHOLD
print(found)

if found:
    top_left = max_loc
    bottom_right = (
        top_left[0] + template.shape[1],
        top_left[1] + template.shape[0]
    )

    cv2.rectangle(
        search_region,
        top_left,
        bottom_right,
        (0, 255, 0),
        2
    )

    cv2.imshow("Match", search_region)
    cv2.waitKey(0)
    cv2.destroyAllWindows()