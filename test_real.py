import cv2
import numpy as np
import os
import time
import mediapipe as mp
# from imutils.video import VideoStream
# import random
import tensorflow as tf
from sklearn.model_selection import train_test_split
#allow to partition our dara into a training
from tensorflow.keras.utils import to_categorical
# from picamera2.array import PiRGBArray
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from landmark_detection import *
import threading
import random
mp_holistic = mp.solutions.holistic #holistic model
mp_drawing = mp.solutions.drawing_utils #Drawing utilities
DATA_PATH = os.path.join('/home/sam/Desktop/signlanguage/MP_Data')
# Initialize actions as an empty list
# actions = []
Actions = os.listdir(DATA_PATH) #action name..
Actions1 = np.array(Actions) #read data_path .npy
#Load tflite model
interpreter = tf.lite.Interpreter(model_path="/home/sam/Desktop/signlanguage/model.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
def generate_random_colors():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
colors = generate_random_colors()
def prob_viz(res, Actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        # colors = generate_random_colors()
        cv2.rectangle(output_frame,( 0,60 + num * 40),(int(prob*100),90 + num*40), colors,-1)
        cv2.putText(output_frame, Actions[num], (0,85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
    return output_frame
def test_real():

    sequence =[]
    sentence = []
    predictions= []
    threshold = 0.6
    picam2 =Picamera2()
    config =picam2.create_video_configuration(main={"format": "XRGB8888"})
    picam2.configure(config)
    picam2.start()
    with mp_holistic.Holistic(min_detection_confidence=0.4, min_tracking_confidence=0.5) as holistic:
        while True:
            frame = picam2.capture_array()
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            image, results = mediapipe_detection(frame, holistic)
            # print(results)
            # keypoint = extract_keypoints(results)

            draw_styled_landmarks(image, results)
            # Prediction logic
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]
            if len(sequence) == 30:
                input_data = np.expand_dims(sequence, axis=0).astype(np.float32)
                interpreter.set_tensor(input_details[0]['index'], input_data)
                interpreter.invoke()
                res = interpreter.get_tensor(output_details[0]['index'])[0]
                # print(Actions[np.argmax(res)])
                # print(res[np.argmax(res)] > threshold)
                predictions.append(np.argmax(res))
                # print(res[np.argmax(res)])
                # Viz logic
                if np.unique(predictions[-10:])[0] == np.argmax(res):
                    if res[np.argmax(res)] > threshold:
                        new_actions = Actions[np.argmax(res)]
                        if len(sentence) > 0:
                            if new_actions != sentence[-1]:
                                sentence.append(new_actions)
                                # Assuming `res[np.argmax(res)]` is the confidence score as a decimal
                        else:
                            sentence.append(new_actions)

                if len(sentence) > 5:
                    sentence = sentence[-5:]
                image = prob_viz(res, Actions, image, colors)   

            cv2.rectangle(image,(0,0), (1240,40), (200,107,178), -1)
            cv2.putText(image, ''.join(sentence), (3,30),cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.imshow("Test Real", image)

            if cv2.waitKey(10) & 0xFF ==ord('q'):
                break

    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()
def start_test():
    threading.Thread(target=test_real).start()