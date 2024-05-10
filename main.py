# 工程：test
# 创建时间：2024/5/10 22:28
# encoding:utf-8

from PIL import Image, ImageDraw, ImageFont
import os
import configparser

# 指定INI文件的路径
ini_file_path = 'user.ini'

# 读取INI文件
config = configparser.ConfigParser()
config.read(ini_file_path)

# 从INI文件中获取配置值
font_path = config['diy']['path']
font_size = int(config['diy']['size'])
text = config['diy']['text']
font_color = tuple(map(int, config['diy']['color'].split(',')))

input_dir = config['directories']['input']
output_dir = config['directories']['out']

x = int(config['xy']['x'])
y = int(config['xy']['y'])

# 设置字体
font = ImageFont.truetype(font_path, size=font_size)

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历输入目录下的所有文件
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.webp', '.gif')):
        # 打开图像文件
        image_path = os.path.join(input_dir, filename)
        image = Image.open(image_path)
        width, height = image.size

        # 计算文本的位置
        text_bbox = ImageDraw.Draw(image).textbbox((0, 0), text, font=font)
        text_x = width - text_bbox[2] - x
        text_y = height - text_bbox[3] - y

        # 在图像上绘制文本
        draw = ImageDraw.Draw(image)
        draw.text((text_x, text_y), text, font=font, fill=font_color)

        # 保存处理后的图像到输出目录
        output_path = os.path.join(output_dir, filename)
        image = image.convert('RGB')
        image.save(output_path)

        print(f"{output_path}")

print('批量处理完成！')
