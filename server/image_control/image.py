import cupy as cp
import numpy as np
from PIL import Image
import os

def convert_to_png_algorithm_with_gpu(input_path, output_path):
    for root, dirs, files in os.walk(input_path):
        for filename in files:
            if filename.endswith('.jpg') or filename.endswith('.jpeg'):
                img_path = os.path.join(root, filename)
                img = Image.open(img_path)
                img_np = np.array(img)

                # 转换图像到GPU
                img_gpu = cp.asarray(img_np)

                # 假设在此处进行一些GPU加速的图像处理
                # 例如：对图像做一些简单的操作
                # img_gpu = cp.clip(img_gpu + 10, 0, 255)  # 举例：增加亮度

                # 转回CPU
                img_np_processed = cp.asnumpy(img_gpu)
                img_processed = Image.fromarray(img_np_processed)

                output_filename = os.path.join(output_path, os.path.relpath(img_path, input_path))
                output_dir = os.path.dirname(output_filename)

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # 转换并保存图像
                temp_output_filename = os.path.join(output_dir, "temp.png")
                img_processed.save(temp_output_filename, 'PNG')

                # 读取并保存为原始扩展名
                img_png = Image.open(temp_output_filename)
                img_png.save(output_filename, 'JPEG')

                # 删除临时文件
                os.remove(temp_output_filename)

                print(f"Converted {img_path} to PNG algorithm and saved as {output_filename}")

input_path = 'H:/web_project/image'
output_path = 'H:/web_project/image'
convert_to_png_algorithm_with_gpu(input_path, output_path)
