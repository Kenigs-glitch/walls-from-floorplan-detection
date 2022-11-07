'''
    Generate wall data for floorplan
    @Param img_path, path to input file
    @Param kernel, size of square kernel for morphological operations, e.g. kernel = 3 means kernel is (3, 3)
    @Param opening_iter, number of iterations of opening operation for wall filter
    @Param dilate_iter, number of iterations of dilate operation for wall filter
    @Param approx_accuracy, maximum distance from contour to approximated contour
    @Return list of walls in format ((start_x, start_y), (end_x, end_y))
'''

from utils.detect import *
from utils.transform import *
import argparse
import imutils
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Optional app description')


def detect_walls(img_path: str, kernel=3, opening_iter=3, dilate_iter=3, approx_accuracy=0.001):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # create wall image (filter out small objects from image)
    wall_img = wall_filter(gray, kernel, opening_iter, dilate_iter)
    # detect walls
    boxes, img = detectPreciseBoxes(wall_img, wall_img, approx_accuracy)
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


parser.add_argument('img_path', type=str, help='Image path')
parser.add_argument('--kernel', type=int, help='size of square kernel for morphological operations')
parser.add_argument('--opening_iter', type=int, help='number of iterations of opening operation for wall filter')
parser.add_argument('--dilate_iter', type=int, help='number of iterations of dilate operation for wall filter')
parser.add_argument('--approx_accuracy', type=float, help='maximum distance from contour to approximated contour')

args = parser.parse_args()

detect_walls(args.img_path,
             kernel=args.kernel if args.kernel else 2,
             opening_iter=args.opening_iter if args.opening_iter else 3,
             dilate_iter=args.dilate_iter if args.dilate_iter else 3,
             approx_accuracy=args.approx_accuracy if args.approx_accuracy else 1)
