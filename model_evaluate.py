# Download the data from : https://github.com/greatsharma/Thumb-Gestures-Detection/raw/master/data.zip

from tensorflow.keras.models import load_model
from CNN_model import DataBuilder
import os

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

databuilder_obj = DataBuilder("data/")

img_arr, img_label, label_to_text = databuilder_obj.build_from_directory()
img_arr = img_arr / 255.
print(label_to_text)

X_train, X_test, y_train, y_test = train_test_split(img_arr, img_label, shuffle=True, stratify=img_label,
                                                    train_size=0.8, random_state=42)

print(f"X_train: {X_train.shape}, X_test: {X_test.shape}, y_train: {y_train.shape}, y_test: {y_test.shape} \n")


model = load_model(os.path.join(".app/dumps/", "model.h5"))

model.evaluate(X_test, y_test, "outputs/confusion_matrix.png")

model.save_training_history("outputs/epoch_metrics.png")