# CamCom Decoder
+ A Python program designed to decode CamCom signals modulated with OOK and Manchester coding. This project extracts binary data from a prerecorded video to achieve the specified task.
## Features
+ Decodes preamble and data bits from the provided video file.
+ Supports OOK and Manchester coding schemes.
+ Outputs the decoded 24-bit binary data and its decimal representation.
## How to use
+ Ensure required modules are installed : OpenCV, Numpy, Matplotlib
+ Output：
  + The decoded 24-bit binary data
## Decoding Process
1. Read Video Frames: Extract frames from the video using OpenCV.
2. Signal Processing: Convert frames to grayscale and detect brightness changes.
3. Preamble Detection: Use a sliding window to detect the predefined preamble [1, 1, 1, 0, 0, 0].
4. Data Decoding: Segment the signal based on symbol duration to extract 24-bit data.
