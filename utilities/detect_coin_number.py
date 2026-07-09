
import cv2
import os
from config import coin_region, game_regions_path, MATCH_THRESHOLD, MIN_DISTANCE




# ----------------------------
# Load image
    # ----------------------------
def detect_coin_number(img):

    if img is None:
        raise ValueError("Input image is None")

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

    # start_time = time.perf_counter()
    # ----------------------------
    # Template matching
    # ----------------------------
    matches_found = []

    for digit in range(10):

        template_path = os.path.join(game_regions_path, "numbers", f"{digit}.png")
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        if template is None:
            print(f"Missing template: {template_path}")
            continue

        _, template = cv2.threshold(template, 128, 255, cv2.THRESH_BINARY)

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)


        ys, xs = (result >= MATCH_THRESHOLD).nonzero()

        for x in xs:
            matches_found.append((x, str(digit)))

    # ----------------------------
    # Remove duplicate detections
    # ----------------------------
    matches_found.sort()

    filtered = []

   

    for x, digit in matches_found:
        if not filtered or x - filtered[-1][0] > MIN_DISTANCE:
            filtered.append((x, digit))

    number = "".join(d for _, d in filtered)

    # end_time = time.perf_counter()


    # Check if the pressed key is EXACTLY 'q'

    # execution_time = end_time - start_time

    # # print(f"Task completed in {} seconds")
    # print("Matches:", filtered)
    # print("Detected number:", number, f"Execution time: {execution_time:.6f}", "seconds")
    return number

if __name__ == "__main__":
    # Example usage
    image_path = os.path.abspath(os.path.join(
    game_regions_path,
    "game_screen.jpg"
))
    print(image_path)
    # image_path = "C:\\Users\\gyawa\\GitHub\\Subway-Surfers-Reinforcement-Learning\\game_regions\\game_screen.jpg"  # Replace with your image path
    img = cv2.imread(image_path)
    
    print(detect_coin_number(img))




