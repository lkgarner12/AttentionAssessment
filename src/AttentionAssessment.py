import sys
import cv2
import numpy as np
import pandas as pd
import pytesseract
import time
import ctypes

print(cv2.getBuildInformation())

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

input_name = "input.mp4"
output_name = "output.mp4"
data_output_name = "data_output.xlsx"
distraction_vid_name = "AttentionAssessment.mp4"

video_path = f'./input/{input_name}'
distraction_vid_path = f'./input/{distraction_vid_name}'
detected_letter = ""
started = False

contrast, brightness = [0, 0]
fps = 50
min_fps = 50
max_fps = 72

start_time, prev_time = [0, 0]

black_frame = np.zeros((screen_height, screen_width, 3), np.uint8)

participant_input, correct_input = [None, None]
letter_is_present = False
distraction_start = 150
distraction_end = 210

fields = ['time', 'contrast', 'brightness', 'fps', 'participant input', 'correct input']
values = [] # default value for values, if the program is successful (see the try block below), then it should give the test values, otherwise it will print an empty string: " "
data_collection = {}

def find_time():
    current_time = time.localtime(time.time())
    time_string = ":".join("0%s" % (current_time[i]) if current_time[i] < 10 else "%s" % (current_time[i]) for i in range (3, 6))
    return time_string

def letter_detection(frame):
    img = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(img, (5,5), 0)
    ret, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # kernel = np.ones((5, 5), np.uint8)
    # img_erosion = cv2.erode(img, kernel, iterations=1) 
    # img_dilation = cv2.dilate(img, kernel, iterations=1)

    # kernel_size = (15, 1)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    # bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
    print(data)
    return data
    # img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
    # contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # padding = 3
    
    
# def main():
#     print(sys.argv)

#     if len(sys.argv) == 4:
#         data_output_name = sys.argv[3]
#     if len(sys.argv) == 3:
#         output_name = sys.argv[2]
#     if len(sys.argv) <= 3:
#         input_name = sys.argv[1]


#     video_path = f'./input/{input_name}'
#     distraction_vid_path = f'./input/{distraction_vid_name}'

#     return video_path, distraction_vid_path, output_name, data_output_name

cap = cv2.VideoCapture(video_path)
distraction_cap = cv2.VideoCapture(distraction_vid_path)

    
while not cap.isOpened() and not distraction_cap.isOpened():
    cap = cv2.VideoCapture(video_path)
    distraction_cap = cv2.VideoCapture(distraction_vid_path)
    cv2.waitkey(1000)
    print("Wait for the header")

pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
pos_dis_frame = distraction_cap.get(cv2.CAP_PROP_POS_FRAMES)


while True:
    data_collection.update({'time' : find_time()})
    data_collection.update({'contrast' : contrast})
    data_collection.update({'brightness' : brightness})
    data_collection.update({'fps' : fps})
    
    flag, frame = cap.read()
    
    init_delta_time  = time.time() - start_time
    fps_delta_time = init_delta_time

    if init_delta_time <= 120:
        contrast = 1.25
        brightness = 75

    else:
        if cv2.waitKey(10) == ord('b'):
            # decrease brightness
            brightness = brightness - 0.1 if brightness > 0 else brightness
        elif cv2.waitKey(10) == ord('B'):
            # increase brightness   
            brightness = brightness + 0.1 if brightness < 100 else brightness
        elif cv2.waitKey(10) == ord('f'):
            # decrease fps of black frames   
            fps = fps - 0.1 if fps > min_fps else fps
        elif cv2.waitKey(10) == ord('F'):
            # increase fps of black frames  
            fps = fps + 0.1 if fps < max_fps else fps

        else:
            if (started) and (init_delta_time >= distraction_start and init_delta_time <= distraction_end):
                d_flag, d_frame = distraction_cap.read()
                if d_flag:
                    cv2.imshow('video 2', d_frame)
                    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    print(pos_frame)+" frames"
                    detected_letter = letter_detection(d_frame)
                if cv2.waitKey(10) == ord('space'):
                    ~participant_input 
                    data_collection.update({'participant input' : True})
                    data_collection.update({'correct input' : ('A' == detected_letter) and participant_input})
                    ~participant_input
                else:
                    # The next frame is not ready, so we try to read it again
                    distraction_cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
                    print("frame is not ready")
                    # It is better to wait for a while for the next frame to be ready
                    cv2.waitKey(1000)
            if fps_delta_time > 1./fps:
                prev = time.time()
                cv2.imshow('video 1', black_frame)

            else:   
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                frame[:,:,2] = np.clip(contrast * frame[:,:,2] + brightness, 0, 255)
                frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
                    
                if flag:
                    if ~started:
                        start_time = time.time()
                        ~started
                        print("-----------------")
                        print("video processing successful and started:")
                    # The frame is ready and already captured
                    cv2.imshow('video1 ', frame)
                    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    print(pos_frame)+" frames"
                else:
                    # The next frame is not ready, so we try to read it again
                    cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
                    print("frame is not ready")
                    # It is better to wait for a while for the next frame to be ready
                    cv2.waitKey(1000)
                    
            values.append(data_collection.copy())
                    

    if cv2.waitKey(10)& 0xFF == ord('q') or cv2.waitKey(10) & 0xFF == ord('x'):
        df = pd.DataFrame(values)
        df.to_excel(data_output_name)
        break
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames, we stop
        df = pd.DataFrame(values)
        df.to_excel(data_output_name)
        break

def test_run_success():
    with open(f'{data_output_name}.xlsx', encoding="utf-8") as f:
        assert(f.read)
        
