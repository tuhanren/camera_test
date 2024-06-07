import streamlit as st
import imageio
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np

st.title("条形码扫描应用")

st.write("使用摄像头扫描条形码")

# 启用摄像头并拍照
def capture_image():
    st.write("请允许摄像头权限，并按按钮拍照")
    cam = imageio.get_reader('<video0>')
    for i, image in enumerate(cam):
        st.image(image)
        if st.button("拍照"):
            img_name = "captured_image.png"
            imageio.imwrite(img_name, image)
            return img_name

def decode_barcode(image_path):
    image = Image.open(image_path)
    barcodes = decode(image)
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
        barcode_info = decode_barcode(img_path)
        if barcode_info:
            st.write("识别到的条形码信息：")
            for info in barcode_info:
                st.write(info)
        else:
            st.write("未能识别条形码。")
    else:
        st.write("拍照失败，请重试。")
