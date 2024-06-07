import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import cv2

st.title("条形码扫描应用")

# 用于存储拍摄的图像
captured_image = st.empty()

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.image = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.image = img
        return img

    def get_image(self):
        return self.image

# 实例化 VideoTransformer
video_transformer = VideoTransformer()

webrtc_ctx = webrtc_streamer(key="barcode-scanner", video_transformer_factory=lambda: video_transformer)

if st.button("拍照"):
    if webrtc_ctx.video_transformer:
        image = video_transformer.get_image()
        if image is not None:
            # 将图片显示出来
            st.image(image, channels="BGR")
            captured_image.image(image, channels="BGR")

            # 保存图片
            img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            img_pil.save("captured_image.png")

            # 读取保存的图片并解码条形码
            image_path = "captured_image.png"
            img_pil = Image.open(image_path)
            barcodes = decode(img_pil)
            if barcodes:
                st.write("识别到的条形码信息：")
                for barcode in barcodes:
                    barcode_data = barcode.data.decode("utf-8")
                    st.write(barcode_data)
            else:
                st.write("未能识别条形码。")
        else:
            st.write("无法获取图像，请重试。")
