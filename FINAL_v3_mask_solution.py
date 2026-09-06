# Virtual Drawing Board using OpenCV + MediaPipe

import cv2
import mediapipe as mp
import numpy as np


# --------------------------------
# Choose marker colour
# --------------------------------

colour = input(
    "Enter marker colour (black/red/blue/green): "
).lower()

if colour == "black":
    marker_colour = (0, 0, 0)          # BGR → black

elif colour == "red":
    marker_colour = (0, 0, 255)        # BGR → red

elif colour == "blue":
    marker_colour = (255, 0, 0)        # BGR → blue

elif colour == "green":
    marker_colour = (0, 255, 0)        # BGR → green

else:
    print("Invalid colour. Using red.")
    marker_colour = (0, 0, 255)


# --------------------------------
# MediaPipe Hands
# --------------------------------

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# --------------------------------
# Capture webcam
# --------------------------------

cap = cv2.VideoCapture(0)

canvas = None#to draw we start with blank canvas
mask = None

prev_x = 0
prev_y = 0


# --------------------------------
# Main loop
# --------------------------------

while True:

    # Capture frame
    success, frame = cap.read()

    if not success:
        break

    # Flip frame horizontally
    frame = cv2.flip(frame, 1)


    # --------------------------------
    # Create canvas and mask
    # --------------------------------

    if canvas is None:#this is needed for retention of previous lines drawn
        #if not,for every frame captured, a new blank canvas would be created
        #previous one would be lost and only cuurent line is used

        # Black canvas to store the drawing
        canvas = np.zeros_like(frame)

        # Mask stores WHERE the drawing exists
        mask = np.zeros(#binary image, initially all black, where drawing exists, it will be white  
            frame.shape[:2],#take height and witdh,slice of the first 2 fields in frame.shape
            dtype=np.uint8#store each value as an 8 bit unsigned integer
            #0 to 255 is 2 power 8,thus store as 8 bit value
        )


    # --------------------------------
    # Convert BGR → RGB
    # --------------------------------

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # --------------------------------
    # Detect hand
    # --------------------------------

    results = hands.process(rgb_frame)


    # --------------------------------
    # If hand detected
    # --------------------------------

    if results.multi_hand_landmarks:

        # Take the first detected hand
        hand = results.multi_hand_landmarks[0]


        # Get index fingertip
        index_tip = hand.landmark[
            mp_hands.HandLandmark.INDEX_FINGER_TIP
        ]


        # Get frame dimensions
        h, w, _ = frame.shape


        # Convert MediaPipe coordinates
        # to pixel coordinates
        x = int(index_tip.x * w)
        y = int(index_tip.y * h)


        # Show fingertip
        cv2.circle(
            frame,
            (x, y),
            10,
            (0, 0, 255),
            -1
        )


        # --------------------------------
        # Draw line
        # --------------------------------

        if prev_x != 0 and prev_y != 0:#as long as previous exist

            # Draw the selected colour
            # on the canvas
            cv2.line(#draw on the canvas with the selected colour, from previous point to current point 
                canvas,
                (prev_x, prev_y),
                (x, y),
                marker_colour,
                5
            )

            #simultaneously, on the fully black canvas , if first time
            #tell the mask wheer the drawing is done, it must be drawn in white
            # Tell the mask WHERE
            # the drawing exists
            cv2.line(
                mask,
                (prev_x, prev_y),
                (x, y),
                255,
                5
            )


        # Store current position
        # for the next frame
        prev_x = x
        prev_y = y


    else:

        # No hand detected
        # Start a new stroke next time
        prev_x = 0
        prev_y = 0


    # --------------------------------
    # Combine drawing with webcam
    # --------------------------------

    # To use 1 channel mask and convolve with original frame
    # Convert 1-channel mask into 3-channel mask
    mask_3channel = cv2.cvtColor(
        mask,
        cv2.COLOR_GRAY2BGR
    )

    #FINAL SOLUTION
    # If mask = 255 → use canvas
    # If mask = 0   → use webcam frame
    output = np.where(#chooses 2 things based on the condition, if condition is true, choose first, else choose second 
        mask_3channel == 255,#if any mask pixel area is 255,
        canvas,#choose first option:canvas#which is the respective colour:R/G/B on black canas/black on black canvas
        frame#else choose the webcam frame
    )


    # --------------------------------
    # Display output
    # --------------------------------

    cv2.imshow(
        "Virtual Drawing Board",
        output
    )


    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------
# Cleanup
# --------------------------------

cap.release()
cv2.destroyAllWindows()