# coding=UTF-8
"""
Compares OpenCV Template Matching speed of color image vs grayscale
image.
"""
import cv2

# Set to 1 to display the matched region of the haystack.
show_match = 1
# The number of iterations from which to determine the average speed.
runs = 5
# The base path to use for haystacks and templates.
path = '../tests/haystacks/user-interface/maps/'
# The path to each image.
haystack = path + 'chunks/varrock-east-mine.png'
needle = path + 'minimap/image_001.png'

# ----------------------------------------------------------------------

haystack_color = cv2.imread(haystack)
needle_color = cv2.imread(needle)
haystack_gray = cv2.imread(haystack, cv2.IMREAD_GRAYSCALE)
needle_gray = cv2.imread(needle, cv2.IMREAD_GRAYSCALE)

durations = []
match_color = None
match_gray = None
cw = None
ch = None
gw = None
gh = None

# Run the template match five times.
for _ in range(runs):
    start_time = cv2.getTickCount()
    rgb, cw, ch = needle_color.shape[::-1]
    result_color = cv2.matchTemplate(haystack_color, needle_color,
                                     cv2.TM_CCOEFF_NORMED)
    loc = cv2.minMaxLoc(result_color)
    match_color = loc[3]
    stop_time = cv2.getTickCount()
    duration = (stop_time - start_time) / cv2.getTickFrequency()
    durations.append(duration)

# Get average duration for each run.
color_avg = round((sum(durations) / runs), 3)
# Convert to miliseconds
color_avg = int(color_avg * 1000)
print('Color Avg =', color_avg, 'miliseconds')

durations = []
# Do the same thing for grayscale versions of the images.
for _ in range(runs):
    start_time = cv2.getTickCount()
    gw, gh = needle_gray.shape[::-1]
    result_gray = cv2.matchTemplate(haystack_gray, needle_gray,
                                    cv2.TM_CCOEFF_NORMED)
    loc = cv2.minMaxLoc(result_gray)
    match_gray = loc[3]
    stop_time = cv2.getTickCount()
    duration = (stop_time - start_time) / cv2.getTickFrequency()
    durations.append(duration)

gray_avg = round((sum(durations) / runs), 3)
gray_avg = int(gray_avg * 1000)
print('Grayscale Avg =', gray_avg, 'miliseconds')
print('\nGrayscale avg / Color avg =', round((gray_avg / color_avg), 2))

if show_match == 1:
    cv2.rectangle(haystack_color, match_color,
                  (match_color[0] + cw, match_color[1] + ch),
                  (0, 255, 0), 2)
    cv2.imshow("haystack", haystack_color)
    cv2.waitKey(0)

    cv2.rectangle(haystack_gray, match_gray,
                  (match_gray[0] + gw, match_gray[1] + gh),
                  (0, 255, 0), 2)
    cv2.imshow("haystack", haystack_gray)
    cv2.waitKey(0)
