import cv2
import time
import joblib
import argparse
import numpy as np
from tensorflow.keras.models import load_model

import os
# os.environ['QT_QPA_PLATFORM'] = 'offscreen'
# os.environ['QT_STYLE_OVERRIDE'] = 'gtk2'
print(cv2.__version__)

import utils

ap = argparse.ArgumentParser()
ap.add_argument('-mo', '--mode', required=False,
                help='either `debug` or `prod` (production), default is prod')

ap.add_argument('-ip', '--ip', required=False,
                help='if you connect to external IP camera')

ap.add_argument('-cam', '--camera', required=False,
                help='if you connect to external IP camera')
args = vars(ap.parse_args())

print(args)
# Debug or Production Mode
if args["mode"] is None:
    args["mode"] = "prod"

# IP camera 
if args["ip"] is not None:
    try:
        # address = "http://10.0.0.101:8080/video" # Your address might be different
        address = args['ip']
        vidcap = cv2.VideoCapture(address)
    except Exception as e:
        print('ERROR: ', e)
        print('Try again with something like: http://10.0.0.101:8080/video')

# Main or secondary camera
elif args["camera"] is None:
    print('Standard Camera: 0')
    vidcap = cv2.VideoCapture(0)
else:
    try:
        vidcap = cv2.VideoCapture(args["camera"])
    except Exception as e:
        print('ERROR: ', e)
    
    finally:
        print('Trying main camera...')
        vidcap = cv2.VideoCapture(0)
    
   
# Load model
model = load_model(os.path.join("./dumps/", "model.h5"))
label2text = joblib.load(os.path.join("./dumps/", "label2text.pkl"))

# Aux Variables
first_frame = None
tt = 0
frame_count = 0

#Loop
while True:
    status, frame = vidcap.read()
    if not status:
        break

    frame = cv2.flip(frame, 1, 0)

    frame_count += 1
    tik = time.time()

    # draw box
    frame_h, frame_w = frame.shape[:2]
    start_coords = (int(frame_w * 0.5), int(frame_h * 0.05))
    end_coords = (int(frame_w * 0.95), int(frame_h * 0.6))
    cv2.rectangle(frame, start_coords, end_coords, (0,255,0), 3)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (7,7), 0)

    if frame_count > 240:
        bb = gray_frame[start_coords[1]:end_coords[1], start_coords[0]: end_coords[0]]

        if first_frame is None:
            first_frame = bb
            continue

        frame_delta = cv2.absdiff(first_frame, bb)
        thresh = cv2.threshold(frame_delta, 50, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        try:
            cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
            (x, y, w, h) = cv2.boundingRect(max_cnt[0])

            area_occupied = (w * h) / (bb.shape[0] * bb.shape[1])
            if area_occupied < 0.1:
                raise Exception

            if args["mode"] == "debug":
                bb = cv2.resize(bb, (640, 480), interpolation = cv2.INTER_AREA)
                thresh = cv2.resize(thresh, (640, 480), interpolation = cv2.INTER_AREA)
                combined = np.hstack((bb, thresh))
                cv2.imshow("bb v/s thresh", combined)

            img = cv2.resize(thresh, (120, 120), fx=0.5, fy=0.5)
            img = np.expand_dims(img, axis=2)
            img = np.expand_dims(img, axis=0)
            img = img / 255.

            predicted_proba = model.predict(img)
            predicted_label = np.argmax(predicted_proba[0])
            bb_text = label2text[predicted_label]
        except Exception as e:
            bb_text = "no hand"
        
        utils.draw_text_with_backgroud(frame, bb_text, x=start_coords[0], y=start_coords[1], font_scale=1.2)
        tt += time.time() - tik
        fps = round(frame_count / tt, 2)
        main_text = "Running..." + f"   fps: {fps}"

        utils.draw_text_with_backgroud(frame, main_text, x=15, y=25, font_scale=1., thickness=2)
        utils.draw_text_with_backgroud(frame, "Instructions for better results:", x=15, y=65, font_scale=1., thickness=2)
        utils.draw_text_with_backgroud(frame, "- Place your hand completely inside the window", x=15, y=115, font_scale=1., thickness=2)
        utils.draw_text_with_backgroud(frame, "- Place your hand close to window", x=15, y=165, font_scale=1., thickness=2)
        utils.draw_text_with_backgroud(frame, "- Press Q to exit", x=15, y=215, font_scale=1., thickness=2)
    else:
        main_text = "Wait 10 seconds and ensure that the background behind the window doesn't change"
        utils.draw_text_with_backgroud(frame, main_text, x=15, y=30, font_scale=0.9, thickness=2)
    
    # cv2.namedWindow('Thumb Recognition', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Thumb Recognition", 1200, 800)
    fresized = cv2.resize(frame, (1200, 800), interpolation = cv2.INTER_AREA)
    cv2.imshow("Thumb Recognition", fresized)
    if cv2.waitKey(10) == ord("q"):
        break

vidcap.release()
cv2.destroyAllWindows()