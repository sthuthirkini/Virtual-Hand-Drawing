# Virtual-Hand-Drawing

A simple project to explore **landmarks, coordinates, hand tracking, drawing, and gesture logic** using the OpenCV and MediaPipe modules of Python.

## Image Processing Fundamentals Learned Through Experimentation

A few fundamentals of image processing that I understood through experimenting with this project are:

- An image is represented by a computer as a **NumPy array of pixel values**. For a colour image, each pixel contains values corresponding to colour channels such as R, G, and B. Different libraries may use different channel conventions; for example, OpenCV commonly uses **BGR** instead of RGB.

- `np.zeros_like()` creates an array of zeros, which appears as a **black canvas `(0,0,0)`**. When this black canvas is added to the webcam frame, it does not change the original frame because adding zero changes nothing. Therefore, the coloured line drawn on the canvas becomes visible over the webcam frame.

- However, a **black line is indistinguishable from the black canvas**. Therefore, a different way of representing the drawing is required. This led to the use of a **mask**.

- The drawing is therefore stored in two separate ways:
  - The **canvas** stores *what colour* the drawing should have.
  - The **mask** stores *where* the drawing exists.

  Whenever a line is drawn on the canvas, a white line (`255`) is simultaneously drawn at the same location on the mask. The final output is then constructed by selecting pixels from the **canvas wherever the mask is white**, and pixels from the **original webcam frame everywhere else**.

- Apart from being used to detect objects of a certain colour using their **H, S, and V (HSV)** values, I discovered another use of masks: a mask can represent **where an object or drawing exists**, regardless of its colour.

- A more advanced way of understanding this concept would be to introduce an additional image channel: **R, G, B, and A**, where **A represents alpha/transparency**. Exploring alpha channels provides another way to understand how transparent drawing layers can be implemented.

## Experiments

### V1 — Black Canvas
A coloured marker could be drawn successfully, but a black marker was invisible because the canvas itself was black.

### V2 — White Canvas
A black marker became visible, but the white canvas covered the webcam background.

### V3 — Mask Solution
A separate canvas and mask were used. The canvas stores the drawing colour, while the mask identifies the pixels belonging to the drawing. This allows even a black marker to be drawn while preserving the original webcam background.