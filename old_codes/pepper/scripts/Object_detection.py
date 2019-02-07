#import numpy as np
#import cv2
#
#watch_cascade = cv2.CascadeClassifier("C:/Users/welcome/Desktop/RMI/data/cascade.xml")
#
#cap = cv2.VideoCapture(0)
#
#while 1:
#    ret, img = cap.read()
#    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    watches = watch_cascade.detectMultiScale(gray, 20, 20)
#    print watches
#    
#    # add this
#    for (x,y,w,h) in watches:
#        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
#
#    cv2.imshow('img',img)
#    k = cv2.waitKey(30) & 0xff
#    if k == 27:
#        break
#
#cap.release()
#cv2.destroyAllWindows()


import cv2
#import cv2.cv as cv
import getopt, sys
import time

def detect(img, cascade):
    for scale in [float(i)/10 for i in range(11, 15)]:
        for neighbors in range(2,5):
            rects = cascade.detectMultiScale(img, scaleFactor=scale, minNeighbors=neighbors,
                                             minSize=(250, 250))

            print 'scale: %s, neighbors: %s, len rects: %d' % (scale, neighbors, len(rects))
            
            for (x,y,w,h) in rects:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'Watch',(x-w,y-h), font, 10, (11,255,255), 2, cv2.LINE_AA)
    


def find_face_from_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    rects = detect(gray, cascade)


if __name__ == '__main__':

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "C:/Users/welcome/Desktop/RMI/data/cascade.xml")
    cascade = cv2.CascadeClassifier(cascade_fn)

    c=cv2.VideoCapture(0)
    while(1):
        ret, frame = c.read()
        print ret
        rects = find_face_from_img(frame)
        cv2.imshow('frame',frame)
        
        if 0xFF & cv2.waitKey(30) == 27:
                break
    c.release()
    cv2.destroyAllWindows()