import PIL.Image
import cv2
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        success, image = self.video.read()
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        j = 1
        for (x, y, w, h) in faces:
            mm=cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            print(faces)
            cv2.imwrite("myface.jpg", mm)
            image = cv2.imread("myface.jpg")
            cropped = image[y:y+h, x:x+w]
            gg="f"+str(j)+".jpg"
            cv2.imwrite("faces/"+gg, cropped)
            mm2 = PIL.Image.open('faces/'+gg)
            rz = mm2.resize((100,100), PIL.Image.LANCZOS)
            rz.save('faces/'+gg)
            j += 1
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
