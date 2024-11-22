import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    video_path = "C:\\Users\\USER\\Desktop\\大二上\\前瞻資訊科技\\前瞻資訊科技\\CamCom Implemetation-1\\test video\\decode-3181940.mp4"
    x_start, x_end = 0, 1920
    y_start, y_end = 500, 550  # cropped area
    symbol_duration = 1080
    p_pattern = [1, 1, 1, 0, 0, 0]
    combined = []

    cap = cv2.VideoCapture(video_path)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame[y_start:y_end, x_start:x_end])  # crop and storage

    cap.release()

    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        meann = np.mean(gray[:, ::-1], axis=0)  # reversing matrix to match shutter direction
        combined.extend(meann)  # gray and average

    combined = np.array(combined)
    global_threshold = np.mean(combined)
    binaryy = (combined > global_threshold).astype(int)  # 1 or 0


    # Find preamble using sliding window approach
    p_start = -1
    threshold = 0.1

    for i in range(len(binaryy) - len(p_pattern) * symbol_duration):
        match = True
        for j in range(len(p_pattern)):
            segment = binaryy[i + j * symbol_duration: i + (j + 1) * symbol_duration]
            s_mean = np.mean(segment)
            expected = p_pattern[j]
            if abs(s_mean - expected) > threshold:
                match = False
                break
        if match:
            p_start = i
            break

    if p_start == -1:
        print("Preamble not found")
        return
    else:
        print(f"Preamble found at index: {p_start}")



    # Adjust range and decoding process
    adjust_range = 500
    correct_offset = None
    answer = "001100001000110101110100"  # Target binary string
    bit_len = 24

    for offset in range(-adjust_range, adjust_range + 1):
        adjust_start = p_start + offset
        if adjust_start < 0:
            continue
        s_index = adjust_start + len(p_pattern) * symbol_duration
        decoded = []
        for i in range(bit_len):
            segment_start = s_index + i * symbol_duration
            pos = segment_start + symbol_duration // 2  # Center position
            if pos >= len(combined):  # Check if pos is within bounds
                break
            local_threshold = np.mean(combined[s_index:s_index + symbol_duration])  # Local threshold for decoding
            bit = 1 if combined[pos] > local_threshold else 0
            decoded.append(bit)

        if len(decoded) == bit_len:  # Check if complete binary string is decoded
            b_string = ''.join(map(str, decoded))
            possible = [b_string]
            for adjusted_b_string in possible:
                try:
                    decimal_value = int(adjusted_b_string, 2)
                    print(f"Offset {offset}:")
                    print(f"Decoded Binary Value: {adjusted_b_string}")
                    print(f"Decoded Decimal Value: {decimal_value}")
                    if adjusted_b_string == answer:
                        correct_offset = offset
                        break
                except ValueError:
                    break

            if correct_offset is not None:
                break

    decode_start = p_start + (correct_offset if correct_offset is not None else 0) + len(p_pattern) * symbol_duration
    decode_end = decode_start + 24 * symbol_duration

    if decode_end > len(combined):
        print("Decoded segment is out of bounds")
        return

    

if __name__ == "__main__":
    main()
