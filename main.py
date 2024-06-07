import streamlit as st
import cv2
from pyzbar import pyzbar
import numpy as np
from PIL import Image

st.title("条形码扫描应用")

st.write("使用摄像头扫描条形码")


# 启用摄像头
def capture_image():
    # 使用 OpenCV 启用摄像头
    cap = cv2.VideoCapture(0)
    st.write("请按空格键拍照")
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame)

        # 按空格键拍照
        if cv2.waitKey(1) & 0xFF == ord(' '):
            img_name = "captured_image.png"
            cv2.imwrite(img_name, frame)
            cap.release()
            cv2.destroyAllWindows()
            return img_name


def decode_barcode(image):
    # 使用 pyzbar 解码条形码
    barcodes = pyzbar.decode(image)
    barcode_info = []
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_info.append(barcode_data)
    return barcode_info


# Streamlit 主逻辑
if st.button("启用摄像头并拍照"):
    img_path = capture_image()
    if img_path:
        st.write("拍照成功！")
        st.image(img_path)
        image = Image.open(img_path)
        image_np = np.array(image)
        barcode_info = decode_barcode(image_np)
        if barcode_info:
            st.write("识别到的条形码信息：")
            for info in barcode_info:
                st.write(info)
        else:
            st.write("未能识别条形码。")

