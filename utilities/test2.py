import cv2
import os

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(
    BASE_DIR,
    "..",
    "dataset",
    "noop",
    # "fd1fb289-0f58-4b2b-bb63-3604906de803.jpg"
    # "f76f5d55-3ee7-4f77-bcdd-a2c898113b87.jpg"
    "fe3b1b81-098f-4373-88dd-b06adc9af899.jpg"
)

image_path = os.path.abspath(image_path)
# img = cv2.imread(image_path)
# cv2.imshow("Zoom", img)
# cv2.waitKey(0)

print(image_path)
coin_region = {
    "top": 268,
    "left": 1672,
    "width": 178,
    "height": 34
}

SAVE_FOLDER = os.path.abspath(os.path.join(
    BASE_DIR,
    "..",
    "game_regions",
    "numbers_new"
))

os.makedirs(SAVE_FOLDER, exist_ok=True)

ZOOM = 8           # How much to enlarge the second window
BOX_W = 18+6-2             # Width of selection box
BOX_H = 24+8       # Height of selection box

# -----------------------------
# Load image
# -----------------------------
img = cv2.imread(image_path)

if img is None:
    raise FileNotFoundError(image_path)

x = coin_region["left"]
y = coin_region["top"]
w = coin_region["width"]
h = coin_region["height"]

coin = img[y:y+h, x:x+w]
# cv2.imshow("Coin Region", coin)
cv2.waitKey(0)
# Starting position of box
box_x = 0
box_y = 0

print("""
Controls
--------
W A S D : Move box
P       : Save current box
Q       : Quit
""")

while True:

    # Small view
    small = coin.copy()

    cv2.rectangle(
        small,
        (box_x, box_y),
        (box_x + BOX_W, box_y + BOX_H),
        (0, 255, 0),
        1
    )

    # Zoomed view
    big = cv2.resize(
        small,
        None,
        fx=ZOOM,
        fy=ZOOM,
        interpolation=cv2.INTER_NEAREST
    )

    cv2.imshow("Coin Region", small)
    cv2.imshow("Zoom", big)

    key = cv2.waitKey(0) & 0xFF
    print(key)
    if key == ord('a'):
        box_x = max(0, box_x - 1)

    elif key == ord('d'):
        box_x = min(w - BOX_W, box_x + 1)

    elif key == ord('w'):
        box_y = max(0, box_y - 1)

    elif key == ord('s'):
        box_y = min(h - BOX_H, box_y + 1)
    elif key == ord('j'):
            
            BOX_W -= 1
    # RIGHT ARROW -> grow width
    elif key == ord('l'):
        if box_x + BOX_W < w:
            BOX_W += 1

    elif key == ord('p'):
        crop = coin[box_y:box_y+BOX_H, box_x:box_x+BOX_W]



        name = input("Save as (0-9): ").strip()

        if name:
            filename = os.path.join(SAVE_FOLDER, f"{name}.png")
            cv2.imwrite(filename, crop)
            print(f"Saved {filename}")

    elif key == ord('q'):
        break

cv2.destroyAllWindows()

