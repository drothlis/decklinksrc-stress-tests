import glob
import sys

import cv2


while True:
    matches_heatmap = cv2.convertScaleAbs(
        cv2.matchTemplate(
            cv2.imread("source.png"),
            cv2.imread("template.png"),
            cv2.TM_SQDIFF_NORMED),
        alpha=255)
    correct = cv2.imread(
        "source_matchtemplate_CORRECT.png",
        cv2.CV_LOAD_IMAGE_GRAYSCALE)
    if not (matches_heatmap == correct).all():
        cv2.imwrite(
            "source_matchtemplate_INCORRECT.png",
            matches_heatmap)
        print "source.png INCORRECT"
        sys.exit(1)
    print "source.png CORRECT"
