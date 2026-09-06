# Virtual-Drawing-Board
A simple project to implement landmarks,coordinates , tracking , drawing and gesture logic using OpenCV and Mediapipe modules of Python.

A few fundamentals of Image Processing that were grasped through experimenting around are:
-an image is seen by the computer as a numpy array of values of R,G,B in different conventions across different libraries.
- np.zeros_like() creates a black canvas (0,0,0) that acts like a transparent layer when added to the webcam frame because adding black changes nothing, and the coloured line becomes visible.
-  but a black line is indistinguishable from that black "transparent" background, so we need a different way to represent the drawing layer, fo which we use a mask,that identifies only the line drawn ,with the colour and solely overlaps that with our original webcam frame to create the virtual drawing board
-  Apart from being used to detect object of a certain colour using its H,S,V values , a new usecase of masks was found:to detect where an object is drawn.

-  A more advanced solution would be to understand image processing with an extra parameter: R,G,B, and A,where A stands for alpha/transparency and then implement the mask.
