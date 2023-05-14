from django.shortcuts import render
import cv2
import dlib
import numpy as np

################## image preparation ####################
# loading the mpdel image
from numpy import empty


# Create your views here.
def tryon(request):
    # if u wanna use external USB webcam
    cap = cv2.VideoCapture(0)

    # declare the detector from the dlib
    detector = dlib.get_frontal_face_detector()

    while cap.isOpened():
        ret, img = cap.read()
        # resizing the frame for better view
        img = cv2.resize(img, (800, 600))
        cv2.imshow("RGB frame", img)
        # make copy from the original image
        finalimageOri = img.copy()
        # covert the image to gray
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Grey frame", gray_img)

        # start to detect the faces in the image
        faces = detector(gray_img)

        # Enter key 'q' to break the loop
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    # When all the process is done
    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

    return render(request, "shopping/category.html")
