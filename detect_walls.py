'''
    Generate wall data file for floorplan
    @Param img_path, path to input file
    @Param info, boolean if data should be printed
    @Return shape
    '''
import imutils as imutils

from utils.detect import *
from utils.transform import *
import cv2
import numpy as np


def detect_walls(img_path: str, kernel=3, opening_iter=3, dilate_iter=3):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # create wall image (filter out small objects from image)
    wall_img = wall_filter(gray, kernel, opening_iter, dilate_iter)
    # detect walls
    boxes, img = detectPreciseBoxes(wall_img, wall_img)
    cv2.imwrite('walls.jpg', imutils.resize(wall_img, width=1280))
    # create verts (points 3d), points to use in mesh creations
    verts = []

    # Scale pixel value to 3d pos
    scale = 100

    # Convert boxes to verts and faces
    wall_height = 1
    verts, faces, wall_amount = create_nx4_verts_and_faces(boxes, wall_height, scale)

    # Create top walls verts
    verts = []
    for box in boxes:
        verts.extend([scale_point_to_vector(box, scale, 0)])

    height, width = 720, 1280
    result_image = np.zeros((height, width, 3), np.uint8)
    walls_plan_for_xml_generator = []

    for room in verts:
        for i in range(len(room) - 1):
            line = (int(room[i][0] * width / 100), int(room[i][1] * height / 100)), \
                   (int(room[i + 1][0] * width / 100), int(room[i + 1][1] * height / 100))
            walls_plan_for_xml_generator.append(line)
            cv2.line(result_image, line[0], line[1], (255, 255, 0))

    cv2.imwrite('walls_from_vectors.jpg', result_image)
    # cv2.imwrite('walls_det.jpg', img)
    # print(walls_plan_for_xml_generator)
    return walls_plan_for_xml_generator


detect_walls('example.png', kernel=2, opening_iter=3, dilate_iter=2)
