from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
# import tensorflowjs as tfjs
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
import tensorflow as tf
import os
import numpy as np

DATA_PATH = os.path.join('MP_Data')
actions = os.listdir(DATA_PATH)
Actions = np.array(actions)
sequence_length = 30
no_sequences=30
label_map = {label:num for num, label in enumerate(actions)}
# print(label_map)
sequences, labels = [],[]
for action in actions:
    for sequence in np.array(os.listdir(os.path.join(DATA_PATH,action))).astype(int):
        window = []
        for frame_num in range(sequence_length):

            res = np.load(os.path.join(DATA_PATH,action,str(sequence),"{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])
# print(np.array(sequences).shape)
# print(np.array(labels).shape)
X = np.array(sequences)
y = to_categorical(labels).astype(int)
# print(X.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
# print(Actions.shape[0])
# # # print(y_train.shape)
# print("input shape:" , X_train.shape)
# print("output shaoe: " ,y_train.shape)

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir = log_dir)
es_callback = EarlyStopping(monitor='categorical_accuracy', mode='max', patience=200, min_delta=0.01, baseline=0.88)
mc_callback = ModelCheckpoint('model1.h5', monitor='val_categorical_accuracy', mode='max', save_best_only=True)

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(Actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy',metrics=['categorical_accuracy'])
model.fit(X_train, y_train, epochs = 200, batch_size=32, validation_split=0.2, callbacks=[tb_callback, mc_callback, es_callback])
# # # tfjs.converters.save_keras_model(model,'models')
model.save('action.h5')
# print("Starting to convert keras model to TensorflowLite.......")
# # model.summary()

# save_model = tf.keras.models.load_model("model1.h5")
# converter = tf.lite.TFLiteConverter.from_keras_model(save_model)
# converter.target_spec.supported_ops = [
#     tf.lite.OpsSet.TFLITE_BUILTINS,  # TensorFlow Lite ?? ops
#     tf.lite.OpsSet.SELECT_TF_OPS     # TensorFlow ops (?? Flex)
# ]

# # # Disable lowering tensor list operations
# converter._experimental_lower_tensor_list_ops = False
# tflite_model = converter.convert()
# name = 'model.tflite'
# with open(name,'wb')as f:
#     f.write(tflite_model)
# print(f'Successful created the model file {name}')
# # 
model.load_weights('model1.h5')
# model.load_weights('action.h5')
yhat = model.predict(X_train)
ytrue = np.argmax(y_train, axis=1).tolist()
yhat_indices = np.argmax(yhat, axis=1).tolist()

accuracy_score(ytrue,yhat_indices )
multilabel_confusion_matrix(ytrue, yhat_indices)
accuracy = accuracy_score(ytrue, yhat_indices)
confusion_matrix = multilabel_confusion_matrix(ytrue, yhat_indices)
print(confusion_matrix)
print(f"Tensorflow Keras Model :{accuracy}")
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
def run_tflite_model(X_test, y_test):
    correct_preictions = 0

    for i in range(len(X_test)):
        test_sample = X_test[i].reshape(input_details[0]['shape'])
        test_label = np.argmax(y_test[i])

        interpreter.set_tensor(input_details[0]['index'], test_sample.astype(np.float32))
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])
        predicted_label = np.argmax(output_data)

        if predicted_label ==test_label:
            correct_preictions += 1
    accuracy = correct_preictions / len(X_test)
    return accuracy
accuracy1 = run_tflite_model(X_test,y_test)
print(f"TensorflowLite Model Accuracy: {accuracy1*100:.2f}%")
