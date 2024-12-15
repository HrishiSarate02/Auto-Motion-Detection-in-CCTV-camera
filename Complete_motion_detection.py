import cv2
import sys
import datetime
import tkinter as tk
from tkinter import simpledialog


#i_v = simpledialog.askstring(title="Camera mode", prompt="For internal camera enter 0 and for webcam enter URL:")

#app_mode=1
#i_v=0
# Create the main window
window = tk.Tk()

# Create the panel with a custom size
panel = tk.Frame(window, width=500, height=200)
panel.pack(side="bottom", fill="both", expand=True)
label = tk.Label(window, text='Enter 0 for internal web-camera, 1 for another camera which may be \nconnected througth wire or ip address for wireless web-camera',
                 font=('Helvetica', 12, 'bold'))
label.pack()

# Create the single line text box and set its default text
text_box = tk.Entry(panel)
text_box.insert(0, "Enter text here")
text_box = tk.Text(window, width=40, height=1, font=("Arial", 20))
text_box.pack(side="top", fill="both", expand=True)


def b1():
    i_v = text_box.get("0.0", 'end')
    app_mode=1
    i_v = i_v.strip()
    if i_v =='0' or i_v =='1' or i_v =='2':
        i_v=int(i_v)
    else:
        i_v = str(i_v)
    window.quit()
    window.destroy()
    motion(i_v, app_mode)
    

def b2():
    i_v = text_box.get("0.0", 'end')
    app_mode=2
    i_v = i_v.strip()
    if i_v =='0' or i_v =='1' or i_v =='2':
        i_v=int(i_v)
    else:
        i_v = str(i_v)
    window.quit()
    window.destroy()
    motion(i_v, app_mode)

def b3():
    i_v = text_box.get("0.0", 'end')
    app_mode=3
    i_v = i_v.strip()
    if i_v =='0' or i_v =='1' or i_v =='2':
        i_v=int(i_v)
    else:
        i_v = str(i_v)
    window.quit()
    window.destroy()
    motion(i_v, app_mode)


# Create the four buttons
button1 = tk.Button(panel, text="Record All", width=10, height=3, command=b1)
button1.pack(side="left", fill="both", expand=True)

button2 = tk.Button(panel, text="Don't Record", width=10, height=3, command=b2)
button2.pack(side="left", fill="both", expand=True)

button3 = tk.Button(panel, text="Auto Record", width=10, height=3, command=b3)
button3.pack(side="left", fill="both", expand=True)



def close_button():
    window.quit()
    window.destroy()
    sys.exit()
button4 = tk.Button(panel, text="Close", width=10, height=3, command=close_button)
button4.pack(side="left", fill="both", expand=True)



#if i_v =='0' or i_v =='1' or i_v =='2':
#    i_v=int(i_v)




#Get camera from user
#cap= cv2.VideoCapture(i_v)

# Capture video from the webcam
#cap = cv2.VideoCapture(0)

#Capture video from ip camera
#cap = cv2.VideoCapture("http://192.168.3.100:8080/video")

# Set the width and height of the capture
#cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#cap.get( cv2.CAP_PROP_FRAME_HEIGHT)

def motion(i_v, app_mode):

    cap= cv2.VideoCapture(i_v)
    
    frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))


    # Define the codec and create VideoWriter object
    #fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

    if app_mode==3 or app_mode==1:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        out = cv2.VideoWriter(f'video_{timestamp}.avi', fourcc, 20.0, (frame_width,frame_height))

    # Read the first frame
    ret, frame = cap.read()

    # Set the background model to the first frame
    bg_model = cv2.createBackgroundSubtractorMOG2(0, 50)

    # Define the region of interest (ROI)
    roi = (0, 0, 640, 480)

    # Initialize variables
    font = cv2.FONT_HERSHEY_SIMPLEX
    recording = False

    while True:
        # Read the next frame
        ret, frame = cap.read()

        # Update the background model
        fgmask = bg_model.apply(frame, learningRate=0.001)

        # Count the number of foreground pixels
        count = cv2.countNonZero(fgmask)

        # Display the current time and date
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        
        # Check if motion is detected
        if app_mode == 2 or app_mode==3:
            if count > 1000:
                # Draw a rectangle around the ROI
                #cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 0, 255), 3)

                

                cv2.putText(frame, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                # Check if we are already recording
                if not recording:
                    # Start recording
                    recording = True

                if app_mode==3 or app_mode==1:
                    # Write the frame to the output video file
                    out.write(frame)

            else:
                # Draw a rectangle around the ROI
                cv2.putText(frame, "Status: {}".format('No Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                #cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 0), 3)

                # Check if we are currently recording
                if recording:
                    # Stop recording
                    recording = False
        else:
            if count > 1000:
                cv2.putText(frame, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Status: {}".format('No Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            out.write(frame)


        # Display the frame
        cv2.imshow('Motion Detection', frame)

        # Check if the user pressed 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy the windows
    cap.release()
    if app_mode==3 or app_mode==1:
        out.release()
    cv2.destroyAllWindows()
window.mainloop()
