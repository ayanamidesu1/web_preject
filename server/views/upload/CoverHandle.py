import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import uuid
from .CoverConfig import cover_dict


class CoverHandle:

    cover='template_1'
    def create_uuid(self):
        return str(uuid.uuid4())

    cover_dict = cover_dict

    def handle(self, title, font_size=None, template_name=None):
        if template_name is None:
            template_name = self.cover
        template = self.cover_dict.get(template_name)
        if not template:
            raise ValueError(f"Template {template_name} not found")

        img_path = template['path']
        text = title
        initial_font_size = font_size if font_size else template['font-size']
        font_path = template['font']
        direction = template['direction']
        x_coords = template['x']
        y_coords = template['y']
        font_color = template['font-color']

        # 打开图像并转换为 RGBA 模式以处理透明度
        image = Image.open(img_path).convert('RGBA')
        draw = ImageDraw.Draw(image)

        # 获取文本区域的最大宽度和高度
        max_width = max(x_coords) - min(x_coords)
        max_height = max(y_coords) - min(y_coords)

        # 逐步尝试以获取合适文字大小
        def get_font_size(text, max_width, max_height, direction, min_font_size=26):
            text_len = len(text)

            if direction == 'vertical':
                # 初始搜索范围
                low, high = min_font_size, max_width // 1.5
            else:
                low, high = min_font_size, max_height // 1.5

            while low <= high:
                mid = (low + high) // 2
                if direction == 'vertical':
                    all_height = mid * 1.5 * text_len
                    if all_height <= max_height:
                        low = mid + 1
                    else:
                        high = mid - 1
                else:
                    all_width = mid * 1.5 * text_len
                    if all_width <= max_width:
                        low = mid + 1
                    else:
                        high = mid - 1

            return int(high)

        # 确定适合区域的最大字体大小
        max_font_size = get_font_size(text, max_width, max_height, direction)
        print(max_font_size)
        font = ImageFont.truetype(font_path, max_font_size)

        # 重新计算文本宽度和高度以便后续使用
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # 计算文本位置以确保竖直和横向居中
        if direction == 'vertical':
            # 计算竖直文本的起始位置
            text_x = min(x_coords) + (max(x_coords) - min(x_coords) - text_height) / 2
            text_y = min(y_coords) + (max(y_coords) - min(y_coords) - (text_height * 1.5 * len(text))) / 2

            # 绘制竖直方向的文本
            for i, char in enumerate(text):
                char_bbox = draw.textbbox((0, 0), char, font=font)
                char_width = char_bbox[2] - char_bbox[0]
                char_height = char_bbox[3] - char_bbox[1]
                char_x = text_x
                char_y = text_y + i * char_height * 1.5  # 设置行间距为1.5倍
                color = font_color if not isinstance(font_color, list) else self.convert_color(
                    font_color[i % len(font_color)])
                draw.text((char_x, char_y), char, font=font, fill=color)
        else:
            # 计算水平文本的起始位置
            text_x = min(x_coords) + (max(x_coords) - min(x_coords) - text_width) / 2
            text_y = min(y_coords) + (max(y_coords) - min(y_coords) - text_height) / 2

            # 绘制水平方向的文本
            lines = self.wrap_text(text, max_width, draw, font)
            for i, line in enumerate(lines):
                line_bbox = draw.textbbox((0, 0), line, font=font)
                line_width = line_bbox[2] - line_bbox[0]
                line_height = line_bbox[3] - line_bbox[1]
                line_x = min(x_coords) + (max(x_coords) - min(x_coords) - line_width) / 2
                line_y = text_y + i * line_height * 1.5  # 设置行间距为1.5倍
                color = font_color if not isinstance(font_color, list) else self.convert_color(
                    font_color[i % len(font_color)])
                draw.text((line_x, line_y), line, font=font, fill=color)

        # 创建临时文件夹路径
        temp_path = self.cover_dict['temp_path']
        os.makedirs(temp_path, exist_ok=True)
        temp_output_path = os.path.join(temp_path, f"{template_name}_{self.create_uuid()}_temp.png")

        # 保存中间PNG图像
        image.save(temp_output_path)
        filename=f'{template_name}_{self.create_uuid()}_output.jpg'
        # 转换PNG图像为JPG并保存
        output_path = os.path.join(temp_path, filename)
        with Image.open(temp_output_path) as img:
            img.convert('RGB').save(output_path, 'JPEG')

        # 删除临时PNG文件
        os.remove(temp_output_path)

        return filename

    def wrap_text(self, text, max_width, draw, font):
        """Wrap text to fit within the given width."""
        words = text.split(' ')
        lines = []
        line = ''
        for word in words:
            test_line = line + word + ' '
            test_width = draw.textbbox((0, 0), test_line, font=font)[2] - draw.textbbox((0, 0), test_line, font=font)[0]
            if test_width <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)
        return lines

    def convert_color(self, color):
        if isinstance(color, str):
            if color.startswith('#'):
                hex_color = color.lstrip('#')
                return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
        return color

    def create_gradient(self, colors, direction, model, font_size, text_length):
        gradient = []
        print(f"Colors received for gradient: {colors}")
        if model == 'line-random':
            for i in range(text_length):
                gradient.append(np.random.choice(colors))
        elif model == 'line':
            num_colors = len(colors)
            for i in range(text_length):
                ratio = i / (text_length - 1)
                idx = int(ratio * (num_colors - 1))
                next_idx = min(idx + 1, num_colors - 1)
                color1 = self.rgba_to_tuple(colors[idx])
                color2 = self.rgba_to_tuple(colors[next_idx])
                gradient.append(self.interpolate_colors(color1, color2, ratio))
        return gradient

    def rgba_to_tuple(self, rgba):
        try:
            rgba = rgba.strip('rgba()').split(',')
            return tuple(int(float(rgba[i]) * 255) if i < 3 else int(float(rgba[i]) * 255) for i in range(4))
        except ValueError:
            print(f"Invalid rgba value: {rgba}")
            return (0, 0, 0, 255)  # 返回黑色不透明作为默认值或根据需要处理错误

    def interpolate_colors(self, color1, color2, ratio):
        return tuple(int(color1[i] * (1 - ratio) + color2[i] * ratio) for i in range(3)) + (
        int(color1[3] * (1 - ratio) + color2[3] * ratio),)

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % tuple(map(int, rgb[:3]))

