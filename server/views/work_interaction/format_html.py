import base64
import os
import re
import uuid

from bs4 import BeautifulSoup

from djangoProject.model.format_img import ReWriteImg
from djangoProject.log.log import Logger
from djangoProject.settings import BASE_DIR


class FormatHtml:
    """格式化HTML，并且移除危险的元素"""
    def __init__(self):
        self.logger = Logger()
        self.re_write_img = ReWriteImg()
        self.web_server_ip = 'http://localhost:8000/static/img/'
        self.save_path = os.path.join(BASE_DIR,'static','img')

    def format_html(self, temp_html):
        """格式化传入的HTML内容，返回格式化后的HTML内容"""
        try:
            temp_html=self.format_emoji(temp_html)
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(temp_html, 'html.parser')

            # 递归处理HTML中的所有节点，逐一处理img标签
            self.process_elements(soup)

            # 返回格式化后的HTML
            return str(soup)

        except Exception as e:
            self.logger.error(f"格式化HTML时发生错误: {str(e)}")
            return False  # 如果发生异常，返回False

    def process_elements(self, soup):
        """递归处理所有节点"""
        # 遍历所有元素，处理img标签以及span标签
        for element in soup.descendants:
            if isinstance(element, str):
                continue  # 如果是字符串，则跳过（防止处理文本节点）

            if element.name == 'img':
                # 处理图片标签：替换表情包或普通图片
                new_img_tag = self.format_img(str(element))
                if new_img_tag:
                    # 替换整个img标签
                    element.replace_with(BeautifulSoup(new_img_tag, 'html.parser'))
                else:
                    return False

            elif element.name == 'span':  # 处理span标签
                if not hasattr(element, 'class') and not hasattr(element, 'style'):
                    element.unwrap()  # 去掉<span>标签，只保留内容

    def format_emoji(self, html_text):
        """格式化表情包"""
        try:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html_text, 'html.parser')

            # 找到所有class为emoji的img标签
            img_tags = soup.find_all('img', class_='emoji')

            # 输出调试信息，查看找到的标签
            self.logger.info(f"找到的表情包标签数量：{len(img_tags)}")

            # 遍历所有img标签，替换为占位符
            for img in img_tags:
                emoji_name = img.get('alt', '')  # 获取alt属性作为表情包名称
                if emoji_name:
                    # 生成占位符，例如 $$大笑$$
                    placeholder = f"$$ {emoji_name} $$"
                    # 用占位符替换img标签
                    img.replace_with(placeholder)
                    self.logger.info(f"表情包替换完成，表情包名称：{emoji_name}，占位符：{placeholder}")

            # 输出替换后的HTML内容
            updated_html = str(soup)
            # 返回替换后的HTML文本
            return updated_html

        except Exception as e:
            self.logger.error(f"格式化emoji时发生错误: {str(e)}")
            return False  # 如果发生异常，返回False

    def format_img(self, img_tag):
        """格式化img标签中的src的原始file，返回格式化后的file名称，并保存文件"""
        try:
            # 提取图片的src、alt和class属性
            src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)

            if src_match:
                src = src_match.group(1)
                return self.replace_normal_img_tag(img_tag, src)
            return False  # 如果没有匹配到src，返回False

        except Exception as e:
            self.logger.error(f"处理img标签时发生错误: {str(e)}")
            return False  # 如果发生异常，返回False

    def replace_normal_img_tag(self, img_tag, src):
        """格式化普通图片的src，保存文件并修改src为服务器IP地址"""
        try:
            # 如果src是base64编码的图片
            if src.startswith('data:image'):
                file_name = self.generate_file_name(self.save_path)
                if self.save_base64_image(src, os.path.join(self.save_path, file_name)):
                    new_img_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{self.web_server_ip}{file_name}"', img_tag)
                    self.logger.info(f"Base64图片替换完成，新的src：{self.web_server_ip}{file_name}")
                    return new_img_tag
                else:
                    raise Exception("Base64文件保存失败")
            else:
                # 处理普通图片
                file_name = self.generate_file_name(self.save_path)
                if self.save_file(src, os.path.join(self.save_path, file_name)):
                    new_img_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{self.web_server_ip}{file_name}"', img_tag)
                    self.logger.info(f"普通图片替换完成，新的src：{self.web_server_ip}{file_name}")
                    return new_img_tag
                else:
                    raise Exception("文件保存失败")
        except Exception as e:
            self.logger.error(f"替换图片时发生错误: {str(e)}")
            return False  # 如果发生异常，返回False

    def save_base64_image(self, base64_str, file_path):
        """保存base64编码的图片"""
        try:
            # 提取base64编码部分
            base64_data = base64_str.split('base64,')[-1]
            img_data = base64.b64decode(base64_data)

            with open(file_path, 'wb') as f:
                f.write(img_data)
                self.logger.info(f"Base64图片保存成功，路径为：{file_path}")
            return True
        except Exception as e:
            self.logger.error(f"保存Base64图片时发生错误: {str(e)}")
            return False  # 如果发生异常，返回False

    def generate_file_name(self, save_path):
        """生成唯一的文件名"""
        try:
            file_name = str(uuid.uuid4()) + '.jpg'  # 假设是jpg格式的图片
            # 检查文件是否存在
            while os.path.exists(os.path.join(save_path, file_name)):
                file_name = str(uuid.uuid4()) + '.jpg'
                self.logger.info('文件已存在，重新生成文件名')
            return file_name
        except Exception as e:
            self.logger.error(f"生成文件名时发生错误: {str(e)}")
            return False  # 如果发生异常，返回False

    def save_file(self, file, path):
        """保存文件"""
        try:
            if self.re_write_img.set_file(file):
                # 获取格式化之后的图片文件
                file_data = self.re_write_img.copy_paste()
                with open(path, 'wb') as f:
                    f.write(file_data.getvalue())
                    self.logger.info(f'文件保存成功：{path}')
                return True
            else:
                self.logger.error("文件处理失败")
                return False
        except Exception as e:
            self.logger.error(f"保存文件时发生错误: {str(e)}")
            return False  # 如果发生异常，返回False
