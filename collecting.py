import os 
import time 
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from testing import mp_holistic, mp_drawing
import time
import cv2
import mediapipe as mp
import threading
from testing import extract_keypoints, draw_styled_landmarks,mediapipe_detection,draw_landmarks,create_blanck_image
from collection import *
from preprocess_data import *
# print("Current working directory:", os.getcwd()) 
# def collect_data(action):
DATA_PATH = os.path.join('/home/sam/Desktop/signlanguage/MP_Data')
actions = []
no_sequences=30
sequence_length =30
start_folder = 0
action = input("Enter action :")
# action = entry_collect.get()
actions.append(action)
dirmax=0
try:
    action_dir =os.path.join(DATA_PATH,action)
    if os.path.exists(action_dir):
        dirmax = np.max(np.array(os.listdir(action_dir)).astype(int))
    for sequence in range(0, no_sequences):
        try:
            path = os.path.join(action_dir,str(dirmax + sequence))
            os.makedirs(path,exist_ok=True)
        except FileExistsError:
            pass
except Exception as e:
    print("Error:",e)
try:
    picam2 =Picamera2()
    config =picam2.create_video_configuration(main={"format": "XRGB8888"})
    picam2.configure(config)
    picam2.start()
    time.sleep(2)
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            for i in range(10,0,-1):
                frame = picam2.capture_array()
                image = create_blanck_image()
                cv2.putText(image,"You need Collect 30 Times",(490,240),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                cv2.putText(image,"Different Angles for ({})".format(action),(485,280),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                cv2.putText(image,"Starting in {} second".format(i),(508,320),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                cv2.imshow('Feed',image)
                cv2.waitKey(1000)
            sequence_counter = 0
            for sequence in range(start_folder, start_folder + no_sequences):
                for frame_num in range(sequence_length):

                    frame = picam2.capture_array()
                    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    image, results = mediapipe_detection(frame, holistic)
                    # print(results)
                    draw_styled_landmarks(image, results)
                    if frame_num == 0:
                        cv2.putText(image, 'STARTING COLLECTING', (500,280),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 4, cv2.LINE_AA)
                        cv2.putText(image, 'Collecting action for {} Video Number {}'.format(action,sequence), (400,50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                        cv2.waitKey(2000)
                    else:
                        cv2.putText(image,f'Collecting action for {action} Video Number {sequence}', (400,50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                    cv2.imshow("Collection", image)
                    keypoints = extract_keypoints(results)
                    npy_path = os.path.join(DATA_PATH,action,str(sequence),str(frame_num))
                    np.save(npy_path, keypoints)
                    if cv2.waitKey(10) & 0xFF ==ord('q'):
                        break
                sequence_counter += 1
            if sequence_counter >= 30:
                break
    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()
except Exception as e:
    print(f"Error occurred: {e}")
        # picam2.stop()
        # picam2.close()
        # cv2.destroyAllWindows()
        # if cv2.waitKey(10) & 0xFF ==ord('q'):
        #     break
finally:
    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()

def on_start(action_entry):
    action = action_entry.get()
    threading.Thread(target=collect_data, args=(action,)).start()
# def stop_camera(canvas):
#     # picam2 = Picamera2()
#     picam2.stop()
#     picam2.close()
# def on_start(canvas):
#     action = entry_collect.get()
#     hreading.Thread(target=collect_data, args=(action,)).start()
    # cv2.destroyAllWindows()