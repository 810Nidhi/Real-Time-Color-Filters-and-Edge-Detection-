import cv2
import numpy as np
def apply_filter(image,ftype):
    img=image.copy()
    if ftype=="red":
        img[:,:,1]= img[:,:,2]=0
    elif ftype=="green":
        img[:,:,0] = img[:,:,2]=0
    elif ftype=="blue":
        img[:,:,0]=img[:,:,1]=0
    elif ftype=="sobel":
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        sx=cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
        sy=cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
        sob=cv2.bitwise_or(sx.astype(np.uint8),sy.astype(np.uint8))
        img=cv2.cvtColor(sob,cv2.COLOR_GRAY2BGR)
    elif ftype=="canny":
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        can=cv2.canny(gray,100,200)
        img=cv2.cvtColor(can,cv2.COLOR_GRAY2BGR)
    elif ftype=="cartoon":
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur=cv2.medianBlur(gray,5)
        edges=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
        color=cv2.bilateralFilter(image,9,300,300)
        img=cv2.bitwise_and(color,color,mask=edges)
    return img
def main():
    cap=cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error could not open camera")
        return
    ftype="original"
    print("keys: r-red, g-green, b-blue, s-sobel, c-canny, t-cartoon")
    while True:
        ret,frame=cap.read()
        if not ret:
            print("Error reading frame")
            break
        out=apply_filter(frame,ftype)
        cv2.imshow("Filter",out)
        key=cv2.waitKey(1) & 0xFF
        if key==ord("r"):
            ftype="red"
        elif key==ord("g"):
            ftype="green"
        elif key==ord("b"):
            ftype="blue"
        elif key==ord("s"):
            ftype="sobel"
        elif key==ord("c"):
            ftype="canny"
        elif key==ord("t"):
            ftype="cartoon"
        elif key==ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__=="__main__":
    main()
