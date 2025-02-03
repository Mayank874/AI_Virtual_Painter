import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
brushThickness = 25
eraserThickness = 100

# Path to header images
folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)  # Use 0 for the default camera
cap.set(3, 1280)  # Set the width of the frame
cap.set(4, 720)  # Set the height of the frame

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
while True:
    #1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        #print(lmList)
        #tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
        # 4. If Selection Mode (Two fingers up)
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            print("Selection Mode")
            #Checking for the click
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)

                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. Drawing Mode (Index finger up)
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):  # Eraser
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp,yp), (x1,y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp,yp), (x1,y1), drawColor, brushThickness)

            xp, yp = x1, y1

#Merge canvas with the original frame
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:125, 0:1280] = header

    if not success:
        print("Failed to capture frame. Exiting...")
        break

    cv2.imshow("Image", img)
    #cv2.imshow("Image", imgCanvas)

    # Wait for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# drawColor = (255, 0, 255)  # Default color (pink)
#
# # Video capture
# cap = cv2.VideoCapture(0)  # Use primary camera
# if not cap.isOpened():
#     print("Error: Could not open the camera.")
#     exit()
#
# cap.set(3, 1280)  # Set width
# cap.set(4, 720)  # Set height
#
# # Hand Detector
# detector = htm.handDetector(detectionCon=0.75, maxHands=1)
# xp, yp = 0, 0  # Previous points
# imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Canvas for drawing
#
# while True:
#     # 1. Import and flip the image
#     success, img = cap.read()
#     if not success:
#         print("Failed to capture frame.")
#         break
#     img = cv2.flip(img, 1)
#
#     # 2. Detect hand landmarks
#     img = detector.findHands(img)
#     lmList = detector.findPosition(img, draw=False)
#
#     if lmList and len(lmList) >= 9:  # Check for minimum landmarks
#         # Tip of index and middle fingers
#         x1, y1 = lmList[8][1:]  # Index finger
#         x2, y2 = lmList[12][1:]  # Middle finger
#
#         # 3. Check which fingers are up
#         fingers = detector.fingersUp()
#
#         # 4. Selection Mode (Two fingers up)
#         if fingers[1] and fingers[2]:
#             xp, yp = 0, 0
#             print("Selection Mode")
#             if y1 < 125:  # If in header region
#                 if 250 < x1 < 450:
#                     header = overlayList[0]
#                     drawColor = (255, 0, 255)  # Pink
#                 elif 550 < x1 < 750:
#                     header = overlayList[1]
#                     drawColor = (255, 0, 0)  # Blue
#                 elif 800 < x1 < 950:
#                     header = overlayList[2]
#                     drawColor = (0, 255, 0)  # Green
#                 elif 1050 < x1 < 1200:
#                     header = overlayList[3]
#                     drawColor = (0, 0, 0)  # Eraser
#             cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
#
#         # 5. Drawing Mode (Index finger up)
#         if fingers[1] and not fingers[2]:
#             cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
#             print("Drawing Mode")
#             if xp == 0 and yp == 0:
#                 xp, yp = x1, y1
#
#             # Eraser or Brush
#             if drawColor == (0, 0, 0):  # Eraser
#                 cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
#                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
#             else:
#                 cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
#                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
#
#             xp, yp = x1, y1
#
#     # Merge canvas with the original frame
#     imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
#     _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
#     imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
#     img = cv2.bitwise_and(img, imgInv)
#     img = cv2.bitwise_or(img, imgCanvas)
#
#     # Add header image
#     img[0:125, 0:1280] = header
#
#     # Display images
#     cv2.imshow("Image", img)
#     cv2.imshow("Canvas", imgCanvas)
#
#     # Exit with 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

