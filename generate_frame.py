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

#generate_frames for flask server
def generate_frames(redis_client=None):
    picam2 = Picamera2()
    config =picam2.create_video_configuration(main={"format": "XRGB8888"})
    picam2.configure(config)
    picam2.start()
    time.sleep(2.0)
    sequence = []
    sentence = []
    predictions = []
    threshold = 0.8
    try:        
        with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while True:
                frame = picam2.capture_array()
                # Make detections
                frame, results = mediapipe_detection(frame, holistic)

                # Draw landmarks
                draw_styled_landmarks(frame, results)

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
                                    confidence_percentage = float(res[np.argmax(res)]) * 100
                                    redis_client.set("joinlatest_result", ' '.join(sentence))
                                    redis_client.set("latest_result", new_actions)
                                    redis_client.set("confidence", confidence_percentage)

                            else:
                                sentence.append(new_actions)
                                confidence_percentage = float(res[np.argmax(res)]) * 100
                                redis_client.set("joinlatest_result", ' '.join(sentence))
                                redis_client.set("latest_result", new_actions)
                                redis_client.set("confidence", confidence_percentage)

                    if len(sentence) > 5:
                        sentence = sentence[-5:]
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        picam2.stop()
        picam2.close()