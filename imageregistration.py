import cv2
import numpy as np
import argparse

#Store the points selected by the user 
srcpoint =[]
destpoint=[]

#Argument Parser to allow user input before runtime 
parser = argparse.ArgumentParser()
parser.add_argument('-reg', '--imgreg', required=True, help="Image to Register ")
parser.add_argument('-ref', '--imgref', required=True, help="Reference Image")
args = vars(parser.parse_args())
img_path_reg = args['imgreg']
img_path_ref= args['imgref']


#Automatic Harris corner important feature detection 
def harris_register():

    img = cv2.imread(img_path_reg)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.03)
    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst > 0.01 * dst.max()] = [0, 0, 255]
    cv2.imshow('Harris Important Point Detected', img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

#Event handler for the source image
def click_event_srcimg(event, x, y, flags, params):
    global srccount

    if event == cv2.EVENT_LBUTTONDOWN:
        srcpoint.append((x,y))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                       str(y), (x, y), font,
                        1, (255, 0, 0), 2)
        cv2.imshow('Base Image', img)


#Event handler for the target image
def click_event_dstimg(event, x, y, flags, params):
    global destpoint
    if event == cv2.EVENT_LBUTTONDOWN:
        destpoint.append((x,y))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img1, str(x) + ',' +
                       str(y), (x, y), font,
                        1, (255, 0, 0), 2)
        cv2.imshow('Target Image', img1)

#using the points selected by the user transform the image and display it
def homography_manual():
    sourcepoint=np.array(srcpoint)
    targetpoint=np.array(destpoint)
    h,status=cv2.findHomography(sourcepoint,targetpoint)
    image_output=cv2.warpPerspective(img,h,(img1.shape[1],img1.shape[0]))
    final_img = cv2.hconcat((img, image_output))
    cv2.imshow("Transformed Image Selected Points",final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":

    img = cv2.imread(img_path_reg)
    img1= cv2.imread(img_path_ref)
    cv2.imshow('Base Image', img)
    cv2.setMouseCallback('Base Image', click_event_srcimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('Target Image', img1)
    cv2.setMouseCallback('Target Image', click_event_dstimg)
    cv2.waitKey(0)
    homography_manual()
    harris_register()
