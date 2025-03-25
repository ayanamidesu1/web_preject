import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image, UnidentifiedImageError
from io import BytesIO

###########################################
# 定义CBAM模块和ResNet18_CBAM模型（与训练时保持一致）
###########################################
class ChannelAttention(nn.Module):
    def __init__(self, in_planes, reduction=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Sequential(
            nn.Conv2d(in_planes, in_planes // reduction, 1, bias=False),
            nn.ReLU(),
            nn.Conv2d(in_planes // reduction, in_planes, 1, bias=False)
        )
        self.sigmoid = nn.Sigmoid()
    def forward(self, x):
        avg_out = self.fc(self.avg_pool(x))
        max_out = self.fc(self.max_pool(x))
        out = avg_out + max_out
        return self.sigmoid(out)

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        padding = (kernel_size - 1) // 2
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()
    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x_cat = torch.cat([avg_out, max_out], dim=1)
        out = self.conv(x_cat)
        return self.sigmoid(out)

class CBAM(nn.Module):
    def __init__(self, in_planes, reduction=16, kernel_size=7):
        super(CBAM, self).__init__()
        self.channel_attention = ChannelAttention(in_planes, reduction)
        self.spatial_attention = SpatialAttention(kernel_size)
    def forward(self, x):
        out = x * self.channel_attention(x)
        out = out * self.spatial_attention(out)
        return out

class ResNet18_CBAM(nn.Module):
    def __init__(self, pretrained=True, num_classes=2):
        super(ResNet18_CBAM, self).__init__()
        self.resnet = models.resnet18(pretrained=pretrained)
        # 替换全连接层
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, num_classes)
        # 在layer4后加入CBAM模块，layer4输出通道为512
        self.cbam = CBAM(512)
    def forward(self, x):
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = self.resnet.relu(x)
        x = self.resnet.maxpool(x)
        x = self.resnet.layer1(x)
        x = self.resnet.layer2(x)
        x = self.resnet.layer3(x)
        x = self.resnet.layer4(x)
        x = self.cbam(x)  # 应用注意力机制
        x = self.resnet.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.resnet.fc(x)
        return x

###########################################
# 定义推理阶段的预处理流程（与验证时一致）
###########################################
inference_transform = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

###########################################
# 定义图像分类器调用类
###########################################
class ImageClassifier:
    def __init__(self, model_path='H:/web_project/ai_model/final_model.pth'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # 使用与训练时一致的模型架构
        self.model = ResNet18_CBAM(pretrained=False, num_classes=2)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()  # 设置为评估模式

    def process_image_from_bytes(self, image_bytes):
        try:
            image = Image.open(BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            input_tensor = inference_transform(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                output = self.model(input_tensor)
                # 使用softmax转换logits为概率分布，取索引1的概率作为R18的概率
                probabilities = F.softmax(output, dim=1)
                r18_probability = probabilities[0, 1].item()
                return r18_probability
        except UnidentifiedImageError:
            print("Error: Cannot identify image from bytes input")
            return None
        except Exception as e:
            print(f"Error processing image from bytes: {e}")
            return None

    def classify_r18(self, image_bytes):
        return self.process_image_from_bytes(image_bytes)*10



# 测试用法
if __name__ == '__main__':
    classifier = ImageClassifier()
    with open("G:/p站/壁纸/95472855_p0.png", "rb") as f:  # 将此处的"test_image.jpg"替换为你的文件路径
        image_bytes = f.read()  # 读取图像为比特流

    result = classifier.classify_r18(image_bytes)
    print(result)
    if result is not None:
        if result >=0.25:
            print("The image is classified as R18.")
        elif result <0.10:
            print("The image is not classified as R18.")
        else:
            print("不确定人工审核",result)
    else:
        print("Failed to classify the image.")

