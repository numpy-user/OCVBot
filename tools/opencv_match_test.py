# coding=UTF-8
"""
Script to test OpenCV's Template Matching using different confidence
levels.

Displays the needle matched against the haystack in 0.05 confidence
intervals from 1.0 to 0.05.

"""
import cv2
import numpy as np

# The base path to use for haystacks and templates.
path = '../tests/haystacks/user-interface/maps/'
# The path to each image.
haystack = path + 'chunks/varrock-east-mine.png'
needle = path + 'minimap/image_001.png'

# Specify a confidence threshold that each match must exceed to qualify.
confidence = 1.0

# ----------------------------------------------------------------------

# Show the match at each confidence interval, from 0.9 to 0.1.
while confidence >= 0.01:
    haystack_color = cv2.imread(haystack)
    needle_color = cv2.imread(needle)

    # Store width and height of template in w and h.
    rgb, w, h = needle_color.shape[::-1]

    # Perform template match.
    match_color = cv2.matchTemplate(haystack_color, needle_color, cv2.TM_CCOEFF_NORMED)

    # Store the coordinates of matched area in a numpy array.
    match_array = np.where(match_color >= confidence)

    # Draw a rectangle around the matched region.
    for pt in zip(*match_array[::-1]):
        cv2.rectangle(haystack_color, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 1)

    # Show the final image with the matched area.
    cv2.imshow(str(round(confidence, 2)), haystack_color)
    cv2.waitKey(0)

    # Lower the confidence rating for the next loop.
    confidence = confidence - 0.05

