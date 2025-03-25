import os
from PIL import Image, ImageOps
import io


class ReWriteImg:
    """格式化图像，初始参数width、、height、file、max_size"""
    def __init__(self, width=200, height=200,file=None,max_size=10 * 1024 * 1024):
        self.file = None
        self.width = width
        self.height = height
        self.max_size = max_size
        if file:
            self.set_file(file)

    # 设置文件并检查文件格式和大小
    def set_file(self, file):
        """设置文件"""
        self.file = file
        if not self.is_safe_image():
            #raise ValueError("Unsupported or invalid image format.")
            return False
        if not self.check_file_size():
            #raise ValueError(f"File size exceeds the limit of {self.max_size / (1024 * 1024)} MB.")
            return False
        return True

    # 检查文件格式是否为安全的图像格式
    def is_safe_image(self) -> bool:
        """检查是否为图像"""
        if not self.file:
            raise ValueError("No file provided.")

        # 检查扩展名是否合法
        ext = os.path.splitext(self.file.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.tiff']
        if ext not in allowed_extensions:
            return False

        # 检查是否为图像文件
        try:
            img = Image.open(self.file)
            img.verify()  # 检查文件是否损坏或非图像
            return True
        except (IOError, SyntaxError):
            return False

    # 检查文件大小是否小于最大允许大小
    def check_file_size(self) -> bool:
        if not self.file:
            raise ValueError("No file provided.")
        return self.file.size <= self.max_size

    # 执行裁剪和格式化处理
    def process_image(self) -> io.BytesIO:
        """剪裁为指定尺寸图像"""
        if not self.file:
            raise ValueError("No file provided.")

        # 打开图像文件并执行复制-粘贴操作
        with Image.open(self.file) as img:
            # 检查是否具有透明度（RGBA），否则转换为 RGB
            img = img.convert('RGBA' if img.mode == 'RGBA' else 'RGB')

            # 保持原比例的缩放，并优先缩放到指定宽高范围
            img.thumbnail((self.width, self.height), Image.Resampling.LANCZOS)

            # 如果图像尺寸不符，执行裁剪操作
            img = ImageOps.fit(img, (self.width, self.height), Image.Resampling.LANCZOS)

            # 创建一个新的图像对象，模拟"复制-粘贴"
            clean_img = Image.new(img.mode, img.size)
            clean_img.paste(img)

            # 将处理后的图像保存到内存中为 PNG 格式
            img_io = io.BytesIO()
            clean_img.save(img_io, format='PNG')  # 保存为PNG格式，保持透明度
            img_io.seek(0)

        return img_io  # 返回格式化后的图像字节流

    # 执行复制-粘贴操作并返回一个 BytesIO 对象
    def copy_paste(self) -> io.BytesIO:
        """重写图像，方式恶意代码嵌入"""
        if not self.file:
            raise ValueError("No file provided.")
        with Image.open(self.file) as img:
            # 检查图像模式并转换为支持透明度的模式
            img = img.convert('RGBA' if img.mode == 'RGBA' else 'RGB')

            clean_img = Image.new(img.mode, img.size)
            clean_img.paste(img)

            img_io = io.BytesIO()
            clean_img.save(img_io, format='PNG')  # 保存为PNG格式
            img_io.seek(0)
            return img_io
