import cv2 as cv
import numpy as np
import dlib
from PIL import Image as pill


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def createBox(img, points, scale=5, masked=False, cropped=True):
    if masked:
        mask = np.zeros_like(img)
        mask = cv.fillPoly(mask, [points], (255, 255, 255))
        img = cv.bitwise_and(img, mask)

    if cropped:
        bbox = cv.boundingRect(points)
        x, y, w, h = bbox
        imgCrop = img[y:y + h, x:x + w]
        imgCrop = cv.resize(imgCrop, (0, 0), None, scale, scale)
        return imgCrop
    else:
        return mask


def dudakboya(renk, imag):
    cv.namedWindow("BGR")
    cv.resizeWindow("BGR", 400, 400)
    img = pill.open(imag).resize((400, 400))
    img = np.array(img)
    img = img[:, :, ::-1].copy()
    imgoriginal = img.copy()

    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = detector(imgGray)

    for face in faces:
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        landmarks = predictor(imgGray, face)
        myPoints = []
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            myPoints.append([x, y])
    myPoints = np.array(myPoints)
    imgLips = createBox(img, myPoints[48:61], masked=True, cropped=False)

    imgColorLips = np.zeros_like(imgLips)
# r g b
# b g r
    if renk == 'yellow':
        imgColorLips[:] = 0, 255, 255
    elif renk == 'red':
        imgColorLips[:] = 0, 0, 255
    elif renk == 'purple':
        imgColorLips[:] = 255, 0, 255
    elif renk == 'green':
        imgColorLips[:] = 0, 255, 0
    else:
        imgColorLips[:] = 0, 0, 0

    imgColorLips = cv.bitwise_and(imgLips, imgColorLips)
    imgColorLips = cv.GaussianBlur(imgColorLips, (7, 7), 10)  # blur
    imgColorLips = cv.addWeighted(imgoriginal, 1, imgColorLips, 0.3, 0)  # 0.3 scale not enough for some colors/imgs

    cv.imshow('BGR', imgColorLips)
    # cv.imshow('lefteye',imgLeftEye)
    # cv.imshow('lips',imgLips)


