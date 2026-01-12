# camera.py


import PIL.Image
import cv2
from PIL import Image


class VideoCamera1(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        frame=image

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        j = 1
        face_counts=len(faces)
        if 1==0:
            dd=0
        elif 1>1:
            dd=0
        else:
            side=0
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in eyes:
                i = (len(eyes))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if x<100 or x>100:
                    # print(side)
                    side=side+1

            # for (x, y, w, h) in faces:
            #     mm = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #     cv2.imwrite("myface.jpg", mm)
            #     image = cv2.imread("myface.jpg")
            #     cropped = image[y:y + h, x:x + w]
            #     gg = "f" + str(j) + ".jpg"
            #     cv2.imwrite("faces/" + gg, cropped)
            #     mm2 = PIL.Image.open('faces/' + gg)
            #     rz = mm2.resize((10, 10), PIL.Image.ANTIALIAS)
            #     rz.save('faces/' + gg)
            #     j += 1

            #########################################
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
