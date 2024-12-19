import cv2
import numpy as np
import matplotlib.pyplot as plt


def main():
    video_path = "C:\\Users\\USER\\Desktop\\大二上\\前瞻資訊科技\\前瞻資訊科技\\CamCom Implemetation-1\\test video\\decode-3181940.mp4"
    x_start, x_end = 0, 1920
    y_start, y_end = 500, 550
    symbol_duration = 1080
    p_pattern = [1, 1, 1, 0, 0, 0]

    cap = cv2.VideoCapture(video_path)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame[y_start:y_end, x_start:x_end])

    cap.release()

    combined = []
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        meann = np.mean(gray[:, ::-1], axis=0)
        combined.extend(meann)

    combined = np.array(combined)
    global_threshold = np.mean(combined)
    binaryy = (combined > global_threshold).astype(int)

    p_start = -1
    threshold = 0.1

    for i in range(len(binaryy) - len(p_pattern) * symbol_duration):
        match = True
        for j in range(len(p_pattern)):
            segment = binaryy[i + j * symbol_duration : i + (j + 1) * symbol_duration]
            s_mean = np.mean(segment)
            expected = p_pattern[j]
            if abs(s_mean - expected) > threshold:
                match = False
                break
        if match:
            p_start = i
            break

    if p_start == -1:
        return

    offset = 60
    s_index = p_start + len(p_pattern) * symbol_duration + offset
    if s_index < 0 or s_index + 24 * symbol_duration > len(combined):
        return

    decoded = []
    for _ in range(24):
        if s_index + symbol_duration > len(combined):
            break
        segment = combined[s_index : s_index + symbol_duration]
        pos = s_index + symbol_duration // 2
        local_threshold = np.mean(segment)
        bit = 1 if combined[pos] > local_threshold else 0
        decoded.append(bit)
        s_index += symbol_duration

    decoded_binary_string = "".join(map(str, decoded))
    print(decoded_binary_string)


if __name__ == "__main__":
    main()
