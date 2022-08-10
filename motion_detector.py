# Motion detector to apture the motion from my computer camera

import cv2, time, pandas
from cv2 import threshold
from datetime import datetime

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

# Creat an instance of the video
video = cv2.VideoCapture(0)

# For capturing video
while True:
    # Create a frame from the video to read the face
    check, frame = video.read()

    # Set status to 0 and will change to 1 if camera detects a motion
    status = 0
    # print(check)
    # print(frame) # Print out the 2D array of the video that was captured

    # Convert to gray scale
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_scale = cv2.GaussianBlur(gray_scale, (21, 21), 0)

    # Check the condition of the first frame
    if first_frame is None:
      first_frame = gray_scale
      continue

    delta_frame = cv2.absdiff(first_frame, gray_scale)

    # For binary threshold - access the 2nd element
    threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Make the threshold frame smoother
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)

    # To find the contours
    (cnts,_) = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Only keep some of the contours, iterate and create a condition
    for contour in cnts:
      if cv2.contourArea(contour) < 10000:
        continue
      
      status = 1

      # Draw rectangle on contour that is > or = to 10000
      (x, y, w, h) = cv2.boundingRect(contour)
      cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    # Record the time of the status change
    status_list.append(status)

    # Only need the last 2 items in the list - just to avoid memory issue if this is run a long time
    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
      times.append(datetime.now())

    if status_list[-1] == 0 and status_list[-2] == 1:
      times.append(datetime.now())


    # To show the frame
    cv2.imshow("Gray Frame", gray_scale)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", threshold_frame)
    cv2.imshow("Color Frame", frame)

    # Wait time before the program continues
    key = cv2.waitKey(1)

    # Prints the coordinates of each frame
    # print(gray_scale)
    # print(delta_frame)
    # print(threshold_frame)

    if key == ord('q'):
      if status == 1:
        times.append(datetime.now())
      break

print(status_list)
print(times)

# Iterate in df
for i in range(0, len(times), 2):
  df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index = True)

# Exporting data to csv
df.to_csv("Times.csv")

# Release the video
video.release()
cv2.destroyAllWindows
