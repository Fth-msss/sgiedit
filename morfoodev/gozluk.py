import cv2
import numpy as np
#dudak boyama gibi shape predictor kullanilmali
#cascade kullaninca cogunda gozleri algilayamiyor
face_cascade = cv2.CascadeClassifier('C:\\Users\\fatih\\PycharmProjects\\morfoodev\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('C:\\Users\\fatih\\PycharmProjects\\morfoodev\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml')


glass_img = cv2.imread('masks/dgfadsga.png')


def gozlukekle(imag):
    image = cv2.imread(imag)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    centers = []
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            centers.append((x + int(ex + 0.5 * ew), y + int(ey + 0.5 * eh)))
    #center gozleri olmali ama cogunda gozleri bulamiyor
    if len(centers) == 2:
        glasses_width = 2.16 * abs(centers[1][0] - centers[0][0])
        overlay_img = np.ones(image.shape, np.uint8) * 255
        h, w = glass_img.shape[:2]
        scaling_factor = glasses_width / w

        overlay_glasses = cv2.resize(glass_img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        x = centers[0][0] if centers[0][0] < centers[1][0] else centers[1][0]

        x -= 0.26 * overlay_glasses.shape[1]
        y += 0.85 * overlay_glasses.shape[0]

        h, w = overlay_glasses.shape[:2]
        overlay_img[int(y):int(y + h), int(x):int(x + w)] = overlay_glasses

        # threshhold pek ayarli degil
        gray_glasses = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_glasses, 170, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        temp = cv2.bitwise_and(image, image, mask=mask)

        temp2 = cv2.bitwise_and(overlay_img, overlay_img, mask=mask_inv)
        final_img = cv2.add(temp, temp2)

        cv2.imshow('umarim gozluk gozundedir', final_img)
        cv2.waitKey()
        cv2.destroyAllWindows()
