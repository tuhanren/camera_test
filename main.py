import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
# import cv2
# import numpy as np

def main():
    st.title("条形码扫描应用")
    st.write("使用摄像头扫描条形码")

    # 启用摄像头
    picture = st.camera_input("拍照")

    if picture:
        # 保存拍摄的图像
        # img = Image.open(picture)
        # img.save("captured_image.png")

        # 读取保存的图像并解码条形码
        # image_path = "captured_image.png"
        st.image(picture)
        img = Image.open(picture)
        st.write(img)
        barcodes = decode(img)
        st.write(barcodes)

        if barcodes:
            st.write("识别到的条形码信息：")
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                st.write(barcode_data)
        else:
            st.write("未能识别条形码。")

if __name__ == "__main__":
    main()
