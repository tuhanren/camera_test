import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from pyzbar.pyzbar import decode
import cv2
import numpy as np


class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.barcode_info = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded_objects = decode(img)

        for obj in decoded_objects:
            # Draw rectangle around the barcode
            (x, y, w, h) = obj.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the barcode data
            barcode_data = obj.data.decode("utf-8")
            barcode_type = obj.type
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            self.barcode_info = text

        return img

    def get_barcode_info(self):
        return self.barcode_info


st.title("条形码扫描应用")
st.write("使用摄像头扫描条形码")

# 实例化 VideoTransformer
video_transformer = VideoTransformer()

webrtc_ctx = webrtc_streamer(key="barcode-scanner", video_transformer_factory=lambda: video_transformer)

if webrtc_ctx.video_transformer:
    barcode_info = video_transformer.get_barcode_info()
    if barcode_info:
        st.write("识别到的条形码信息：")
        st.write(barcode_info)
