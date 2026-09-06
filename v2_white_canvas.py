#to build a virtual drawimg board

#NOTE-to be run with python 3.11 as mediapipe is not compatible with python 3.14 yet
#python3.11 "/Users/sthuthirkini/Python Projects/Project1-Virtual-Hand-Drawing/v3_mask_solution.py"

#capture frame
#capture movement
#focus on movement
#trace movement
import cv2#to open webcam,capture frames,draw on frames
import mediapipe as mp #to track hand and get coordinates of fingertips 
import numpy as np#as an image is just a giant numpy array

# --------------------------------------------------
# 1. SET UP MEDIAPIPE
# --------------------------------------------------

mp_hands = mp.solutions.hands#hands model of mediapipe
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7#before moving onto next frame to 
    #understand how line progresses, it needs to be confident that it is tracking the hand correctly right now      
)

mp_draw = mp.solutions.drawing_utils


# --------------------------------------------------
# 2. OPEN WEBCAM
# --------------------------------------------------

cap = cv2.VideoCapture(0)

#ASKING FOR USER CHOICE OF MARKER COLOUR  BEFORE CREATING CANVAS    
colour = input("Enter marker colour (black/red/blue/green): ").lower()
if colour == "black":
    marker_colour = (0, 0, 0)
elif colour == "red":
    marker_colour = (0, 0, 255)
elif colour == "blue":
    marker_colour = (255, 0, 0)
elif colour == "green":
    marker_colour = (0, 255, 0)

# --------------------------------------------------
# 3. CREATE A BLANK CANVAS
# --------------------------------------------------

canvas = None#to draw we start with blank canvas


# Previous fingertip position
prev_x = 0
prev_y = 0


while True:

    # --------------------------------------------------
    # 4. GET FRAME FROM CAMERA
    # --------------------------------------------------

    success, frame = cap.read()

    if not success:
        break

    # Flip so movement feels natural
    frame = cv2.flip(frame, 1)

    # Create canvas after knowing frame size
    if canvas is None:
        if colour != "black":#if canvas is not created yet and colour is not black
            canvas = np.zeros_like(frame)#adjust canvas to frame size
        else:
            canvas = np.ones_like(frame) * 255#white canvas for black marker    

    # --------------------------------------------------
    # 5. SEND FRAME TO MEDIAPIPE
    # --------------------------------------------------

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#opencv to mediapipe convention variation in oreder of RGb

    results = hands.process(rgb_frame)


    # --------------------------------------------------
    # 6. CHECK IF A HAND WAS DETECTED
    # --------------------------------------------------

    #results is an object containing the information MediaPipe found.
    #if it found your hand, results contains information about the hand(s).
    
    #multi_hand_landmarks means:
    #the collection/list of landmarks for all the hands MediaPipe detected.

    #take the first hand detected, if any, and store its landmarks in the variable hand
    #bc we specified limit as only 1 hand


    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        # Draw hand skeleton
        mp_draw.draw_landmarks(#draws the hand skeleton on the frame  using points and connections  
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )
        #

        # --------------------------------------------------
        # 7. GET INDEX FINGERTIP
        # --------------------------------------------------
        #mediapipe gives us 21 points on the hand, we are interested in the tip of the index finger 
        index_tip = hand.landmark[
            mp_hands.HandLandmark.INDEX_FINGER_TIP
        ]
        #hand has 21 landmarks corresponding to different parts of the hand, 
        # we are interested in the tip of the index finger, which is landmark number 8
        # We access it using mp_hands.HandLandmark.INDEX_FINGER_TIP
        #and store it in index
        # MediaPipe gives coordinates between 0 and 1
        # Convert them into actual pixel coordinates

        h, w, _ = frame.shape#we get frame shape

        #mediapipe normalises the coordinates of the hand landmarks to be between 0 and 1, so we multiply by the width and height of the frame to get the actual pixel coordinates  
        #but to draw on the frame using opencv we must have actual pixel data
        #so we multiply the normalised coordinates by the width and height of the frame to get the actual pixel coordinates 
        x = int(index_tip.x * w)
        y = int(index_tip.y * h)


        # --------------------------------------------------
        # 8. DRAW A CIRCLE AT FINGERTIP
        # --------------------------------------------------

        cv2.circle(
            frame,
            (x, y),
            10,
            (0, 0, 0),
            -1
        )


        # --------------------------------------------------
        # 9. DRAW LINE FROM PREVIOUS POSITION
        # --------------------------------------------------

        if prev_x != 0 and prev_y != 0:

            cv2.line(
                canvas,
                (prev_x, prev_y),
                (x, y),
                marker_colour,
                5
            )


        # Current position becomes previous position
        prev_x = x
        prev_y = y


    else:

        # No hand → stop drawing
        prev_x = 0
        prev_y = 0


    # --------------------------------------------------
    # 10. COMBINE CAMERA + DRAWING
    # --------------------------------------------------

    output = cv2.add(frame, canvas)


    # --------------------------------------------------
    # 11. SHOW RESULT
    # --------------------------------------------------

    cv2.imshow("Virtual Drawing Board", output)


    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# --------------------------------------------------
# 12. CLEAN UP
# --------------------------------------------------

cap.release()
cv2.destroyAllWindows()